from flask import request, current_app as app
from flask_restful import Resource

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from uuid import uuid4
import os
import urllib.request
import urllib.parse
import json
from api.models import db, User, Issue, IssueUpdate, UserRole, Upvote, Comment
from sqlalchemy import or_
from ..utils.s3 import upload_file_to_s3, compress_image
from ..utils.classifier import classify_issue, get_priority_level
from ..utils.duplicate_detector import find_duplicate_candidates, is_likely_duplicate
from ..utils.priority_scorer import calculate_priority_score


def apply_issue_filters(query):
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()
    issue_type = request.args.get("issue_type", "").strip()
    date_from = request.args.get("date_from", "").strip()
    date_to = request.args.get("date_to", "").strip()

    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(
            Issue.title.ilike(pattern),
            Issue.description.ilike(pattern),
            Issue.address.ilike(pattern),
        ))

    if status:
        query = query.filter(Issue.status == status)

    if issue_type:
        query = query.filter(Issue.issue_type == issue_type)

    if date_from:
        query = query.filter(Issue.created_at >= date_from)

    if date_to:
        query = query.filter(Issue.created_at <= date_to + " 23:59:59")

    return query


class ReportIssue(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.form
        files = request.files.getlist("images")

        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        issue_type = data.get("issue_type", "Unspecified")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        address = data.get("address", "").strip()

        voice_note = request.files.get("voice_note")
        video_note = request.files.get("video_note")

        if not title:
            return {"error": "Title Is Required"}, 400
        if not description:
            return {"error": "Description Is Required"}, 400
        if not files or any(f.mimetype.split("/")[0] != "image" for f in files):
            return {"error": "At Least One Image Is Required!"}, 400
        if any(f.content_length > 15 * 1024 * 1024 for f in files):
            return {"error": "Each Image Must Be Less Than 15 MB"}, 400
        if not latitude or not longitude:
            if not address:
                return {"error": "Either Coordinates Or Address Is Required"}, 400
        else:
            try:
                latitude = float(latitude)
                longitude = float(longitude)

                if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                    return {"error": "Invalid Coordinates"}, 400

            except ValueError:
                return {"error": "Invalid Coordinate Format"}, 400

        image_urls = []
        for file in files:
            try:
                img = compress_image(file)

                url = upload_file_to_s3(
                    img,
                    f"issues/images/{user_id}_{uuid4()}_{file.filename}",
                    config=app.config["S3_CONFIG"],
                    content_type="image/webp",
                )
                image_urls.append(url)
            except Exception as e:
                return {"error": f"Failed To Upload Image : {str(e)}"}, 500

        voice_url = None
        if voice_note:
            try:
                voice_url = upload_file_to_s3(
                    voice_note,
                    f"issues/voice_notes/{user_id}_{uuid4()}_{voice_note.filename}",
                    config=app.config["S3_CONFIG"],
                    content_type=voice_note.mimetype,
                )
            except Exception as e:
                return {"error": f"Failed To Upload Voice Note : {str(e)}"}, 500

        video_url = None
        if video_note:
            try:
                video_url = upload_file_to_s3(
                    video_note,
                    f"issues/video_notes/{user_id}_{uuid4()}_{video_note.filename}",
                    config=app.config["S3_CONFIG"],
                    content_type=video_note.mimetype,
                )
            except Exception as e:
                return {"error": f"Failed To Upload Video Note : {str(e)}"}, 500

        # ── AI Image Classification (LocateAnything-3B) ─────────────
        image_classification = None
        img_cls_enabled = os.getenv("IMAGE_CLASSIFICATION_ENABLED", "false").lower() in ("true", "1", "yes")
        if img_cls_enabled and files:
            try:
                from ..utils.image_classifier import classify_image_from_bytes
                # Classify the first image
                files[0].seek(0)
                image_classification = classify_image_from_bytes(
                    files[0].read(), files[0].filename
                )
                # Use image classification to enhance issue_type if still unspecified
                if (issue_type == "Unspecified" or not issue_type) and image_classification["confidence"] > 0.3:
                    issue_type = image_classification["category"]
            except Exception as e:
                print(f"------ [ WARN ] ------ Image classification failed: {e}")

        # ── AI Text Classification (Ollama) ─────────────────────────
        ai_text_enabled = os.getenv("AI_TEXT_ENABLED", "false").lower() in ("true", "1", "yes")
        if ai_text_enabled and (issue_type == "Unspecified" or not issue_type):
            try:
                from ..utils.ai_client import classify_issue_text
                ai_result = classify_issue_text(title, description)
                if ai_result["confidence"] > 0.3 and ai_result["category"]:
                    issue_type = ai_result["category"]
            except Exception as e:
                print(f"------ [ WARN ] ------ Ollama classification failed: {e}")

        # Fallback: keyword-based classification
        if issue_type == "Unspecified" or not issue_type:
            category, confidence, suggested_dept = classify_issue(title, description)
            if confidence > 0.3:
                issue_type = category

        # Duplicate Detection
        duplicates = find_duplicate_candidates(
            db.session,
            Issue,
            title,
            description,
            latitude,
            longitude,
            threshold=0.4,
            max_results=3
        )

        # ── Priority Scoring ────────────────────────────────────────
        priority_level = "medium"
        priority_score = 50
        priority_breakdown = {}

        if ai_text_enabled:
            try:
                from ..utils.ai_client import assess_priority
                ai_priority = assess_priority(title, description, issue_type, upvote_count=0)
                priority_level = ai_priority["level"]
                priority_score = ai_priority["score"]
                priority_breakdown = {"ai_reasoning": ai_priority["reasoning"]}
            except Exception as e:
                print(f"------ [ WARN ] ------ Ollama priority failed, using heuristic: {e}")

        if not priority_breakdown:
            priority_level, priority_score, priority_breakdown = calculate_priority_score(
                issue_type=issue_type,
                title=title,
                description=description,
                upvote_count=0,
                comment_count=0,
                created_at=None,
                status="pending",
                has_images=len(image_urls) > 0
            )

        issue = Issue(
            citizen_id=user_id,
            title=title,
            description=description,
            issue_type=issue_type,
            image_urls=image_urls,
            voice_note_url=voice_url,
            video_note_url=video_url,
            latitude=latitude,
            longitude=longitude,
            address=address,
        )
        db.session.add(issue)
        db.session.commit()

        from ..utils.reputation import award_points
        award_points(user_id, "issue_reported", db)

        # AI Image Verification on Upload
        if img_cls_enabled and files:
            try:
                from ..utils.image_verifier import verify_image_from_bytes, should_flag_user
                from api.models import VerificationStatus, VerificationState
                from datetime import datetime

                all_verifications = []
                overall_valid = True
                overall_confidence = 0.0
                all_mismatch_flags = []
                user_should_be_flagged = False

                for idx, file in enumerate(files):
                    try:
                        file.seek(0)
                        img_bytes = file.read()
                        
                        result = verify_image_from_bytes(
                            image_bytes=img_bytes,
                            filename=file.filename or f"image_{idx}.jpg",
                            issue_title=issue.title,
                            issue_description=issue.description,
                            issue_type=issue.issue_type,
                        )
                        
                        all_verifications.append(result)
                        if not result["is_valid"]:
                            overall_valid = False
                        overall_confidence = max(overall_confidence, result["confidence"])
                        all_mismatch_flags.extend(result["mismatch_flags"])
                        if should_flag_user(result):
                            user_should_be_flagged = True
                    except Exception as ex:
                        print(f"------ [ WARN ] ------ Verification for image {idx} failed: {ex}")

                if overall_valid and overall_confidence > 0.3:
                    state = VerificationState.verified
                    verification_message = "AI verification passed. Images match the reported issue."
                elif not overall_valid and overall_confidence > 0.7:
                    state = VerificationState.rejected
                    verification_message = "AI verification failed. Images do not match the reported issue."
                else:
                    state = VerificationState.pending
                    verification_message = "AI verification inconclusive. Manual review recommended."

                v = VerificationStatus(
                    issue_id=issue.id,
                    status=state,
                    verified_by=None,
                    verified_at=datetime.utcnow(),
                    ai_confidence=overall_confidence,
                    ai_reasoning=verification_message,
                    notes=verification_message,
                    is_consistent=overall_valid,
                    detected_objects=all_verifications[0].get("detected_objects", []) if all_verifications else [],
                    mismatch_flags=all_mismatch_flags,
                )
                db.session.add(v)
                db.session.commit()

                if user_should_be_flagged:
                    from ..utils.reputation import flag_user
                    citizen = User.query.get(user_id)
                    if citizen:
                        flag_user(citizen, "AI detected image mismatch", db)
            except Exception as e:
                print(f"------ [ WARN ] ------ Overall image verification during upload failed: {e}")

        response = {
            "message": "Issue Reported Successfully",
            "issue": issue.to_dict(),
            "classification": {
                "issue_type": issue_type,
                "confidence": confidence if 'confidence' in locals() else 0.0
            },
            "priority": {
                "level": priority_level,
                "score": priority_score,
                "breakdown": priority_breakdown
            }
        }

        if image_classification:
            response["image_analysis"] = {
                "category": image_classification["category"],
                "confidence": image_classification["confidence"],
                "detections": image_classification["detections"],
            }

        if 'state' in locals():
            from datetime import datetime
            response["verification"] = {
                "status": state.value,
                "notes": verification_message,
                "verified_at": datetime.utcnow().isoformat()
            }

        if duplicates:
            response["potential_duplicates"] = duplicates

        return response, 201


class MyIssues(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        query = Issue.query.filter_by(citizen_id=user_id).order_by(Issue.created_at.desc())
        total = query.count()
        issues = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            "issues": [issue.to_dict() for issue in issues],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }, 200


class AllIssues(Resource):
    @jwt_required()
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        query = Issue.query.order_by(Issue.created_at.desc())
        query = apply_issue_filters(query)
        total = query.count()
        issues = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            "issues": [issue.to_dict() for issue in issues],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }, 200


class PublicIssues(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        query = Issue.query.filter(Issue.status.in_(['pending', 'in_progress', 'verified'])).order_by(Issue.created_at.desc())
        total = query.count()
        issues = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            "issues": [issue.to_public_dict() for issue in issues],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }, 200


class GetIssue(Resource):
    @jwt_required()
    def get(self, issue_id):
        issue = Issue.query.filter_by(id=issue_id).first()

        if not issue:
            return {"error": "Issue not found"}, 404

        return {"issue": issue.to_dict()}, 200

    @jwt_required()
    def put(self, issue_id):
        user_id = get_jwt_identity()
        issue = Issue.query.filter_by(id=issue_id).first()

        if not issue:
            return {"error": "Issue not found"}, 404

        # Check permissions: admin or owner
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        if str(issue.citizen_id) != str(user_id) and user.role != UserRole.admin:
            return {"error": "Forbidden"}, 403

        files = request.files.getlist("images")

        if not files or any(f.mimetype.split("/")[0] != "image" for f in files):
            return {"error": "At least one image is required"}, 400

        if any(f.content_length > 15 * 1024 * 1024 for f in files):
            return {"error": "Each image must be less than 15 MB"}, 400

        image_urls = []
        for file in files:
            try:
                img = compress_image(file)
                url = upload_file_to_s3(
                    img,
                    f"issues/images/{user_id}_{uuid4()}_{file.filename}",
                    config=app.config["S3_CONFIG"],
                    content_type="image/webp",
                )
                image_urls.append(url)
            except Exception as e:
                return {"error": f"Failed to upload image: {str(e)}"}, 500

        # Append new images to existing
        issue.image_urls.extend(image_urls)
        db.session.commit()

        return {
            "message": "Images uploaded successfully",
            "issue": issue.to_dict(),
        }, 200


class GetIssueUpdates(Resource):
    @jwt_required()
    def get(self, issue_id):
        user_id = get_jwt_identity()

        # User can view updates if they own the issue or are admin
        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue not found"}, 404

        if str(issue.citizen_id) != str(user_id):
            # Check admin
            from api.models import UserRole

            user = User.query.get(user_id)
            if not user or user.role != UserRole.admin:
                return {"error": "Forbidden"}, 403

        updates = (
            IssueUpdate.query.filter_by(issue_id=issue_id)
            .order_by(IssueUpdate.created_at.desc())
            .all()
        )
        return {"updates": [u.to_dict() for u in updates]}, 200


class GeocodeAddress(Resource):
    @jwt_required()
    def get(self):
        query = request.args.get("q", "").strip()

        if not query or len(query) < 3:
            return {"suggestions": []}, 200

        try:
            # Use Nominatim API for geocoding
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={urllib.parse.quote(query)}&limit=5&countrycodes=IN"

            # Set a user agent as required by Nominatim
            req = urllib.request.Request(url, headers={"User-Agent": "CityPulse/1.0"})

            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

            suggestions = []
            for result in data:
                suggestions.append(
                    {
                        "place_id": result.get("place_id"),
                        "display_name": result.get("display_name"),
                        "lat": float(result.get("lat", 0)),
                        "lon": float(result.get("lon", 0)),
                    }
                )

            return {"suggestions": suggestions}, 200

        except Exception as e:
            print(f"Geocoding error: {e}")
            return {"error": "Geocoding service unavailable"}, 500


class ReverseGeocode(Resource):
    @jwt_required()
    def get(self):
        lat = request.args.get("lat")
        lon = request.args.get("lon")

        if not lat or not lon:
            return {"error": "Latitude and longitude are required"}, 400

        try:
            lat = float(lat)
            lon = float(lon)

            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                return {"error": "Invalid coordinates"}, 400

            # Use Nominatim API for reverse geocoding
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"

            # Set a user agent as required by Nominatim
            req = urllib.request.Request(url, headers={"User-Agent": "CityPulse/1.0"})

            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

            if data and data.get("display_name"):
                return {"address": data.get("display_name"), "details": data}, 200
            else:
                return {"error": "Address not found"}, 404

        except Exception as e:
            print(f"Reverse geocoding error: {e}")
            return {"error": "Reverse geocoding service unavailable"}, 500


class UpvoteIssue(Resource):
    @jwt_required()
    def post(self, issue_id):
        user_id = get_jwt_identity()
        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue not found"}, 404

        existing = Upvote.query.filter_by(user_id=user_id, issue_id=issue_id).first()
        if existing:
            return {"message": "Already upvoted"}, 200

        upvote = Upvote(user_id=user_id, issue_id=issue_id)
        db.session.add(upvote)
        db.session.commit()

        return {"message": "Upvoted", "upvote_count": len(issue.upvotes)}, 201

    @jwt_required()
    def delete(self, issue_id):
        user_id = get_jwt_identity()
        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue not found"}, 404

        upvote = Upvote.query.filter_by(user_id=user_id, issue_id=issue_id).first()
        if not upvote:
            return {"error": "Not upvoted"}, 404

        db.session.delete(upvote)
        db.session.commit()

        return {"message": "Upvote removed", "upvote_count": len(issue.upvotes)}, 200


class IssueComments(Resource):
    @jwt_required()
    def get(self, issue_id):
        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue not found"}, 404

        comments = Comment.query.filter_by(issue_id=issue_id).order_by(Comment.created_at.asc()).all()
        return {"comments": [c.to_dict() for c in comments]}, 200

    @jwt_required()
    def post(self, issue_id):
        user_id = get_jwt_identity()
        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue not found"}, 404

        data = request.get_json()
        body = (data.get("body") or "").strip()
        if not body:
            return {"error": "Comment body is required"}, 400

        comment = Comment(issue_id=issue_id, author_id=user_id, body=body)
        db.session.add(comment)
        db.session.commit()

        return {"message": "Comment added", "comment": comment.to_dict()}, 201


class VerifyIssueImages(Resource):
    @jwt_required()
    def get(self, issue_id):
        """Get AI verification status for an issue (if available)."""
        from ..models import VerificationStatus

        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue not found"}, 404

        verification = VerificationStatus.query.filter_by(issue_id=issue_id).first()
        if not verification:
            return {"verification": None}, 200

        return {
            "verification": {
                "status": verification.status.value,
                "notes": verification.notes,
                "verified_at": verification.verified_at.isoformat() if verification.verified_at else None,
            }
        }, 200
