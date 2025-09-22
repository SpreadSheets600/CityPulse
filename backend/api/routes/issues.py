from flask import request, current_app as app
from flask_restful import Resource

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from uuid import uuid4
from api.models import db, User, Issue, IssueUpdate, UserRole
from ..utils.s3 import upload_file_to_s3, compress_image


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

        return (
            {"message": "Issue Reported Successfully", "issue": issue.to_dict()},
            201,
        )


class MyIssues(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        issues = (
            Issue.query.filter_by(citizen_id=user_id)
            .order_by(Issue.created_at.desc())
            .all()
        )

        return {"issues": [issue.to_dict() for issue in issues]}, 200


class AllIssues(Resource):
    @jwt_required()
    def get(self):
        # Allow all authenticated users to view all issues
        issues = Issue.query.order_by(Issue.created_at.desc()).all()

        return {"issues": [issue.to_dict() for issue in issues]}, 200


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
