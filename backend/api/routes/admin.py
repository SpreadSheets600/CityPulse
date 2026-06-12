from flask import request, current_app as app, Response
from flask_restful import Resource
from sqlalchemy import func, extract
import csv
import io

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from uuid import uuid4
from api.models import db, User, UserRole, Issue, IssueStatus, Department, IssueUpdate, AuditLog, Geofence, VerificationStatus, VerificationState
from ..utils.s3 import upload_file_to_s3, compress_image
from ..utils.email import send_status_notification
from ..utils.sms import send_status_sms
from ..utils.reputation import award_points, unreputation_user


def log_admin_action(admin_id, action, target_type, target_id=None, details=None):
    entry = AuditLog(
        admin_id=admin_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        details=details,
    )
    db.session.add(entry)


class GetAllUsers(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        query = User.query.order_by(User.created_at.desc())
        total = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()

        users_data = [
            {
                "id": u.id,
                "firstname": u.firstname,
                "lastname": u.lastname,
                "email": u.email,
                "role": u.role.value,
                "phone": u.phone,
                "created_at": u.created_at.isoformat(),
            }
            for u in users
        ]

        return {
            "users": users_data,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }, 200


class DeleteUser(Resource):
    @jwt_required()
    def delete(self, user_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or admin.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        user = User.query.get(user_id)
        if not user:
            return {"error": "User Not Found"}, 404

        db.session.delete(user)
        log_admin_action(admin_id, "delete_user", "user", user_id, f"Deleted user {user.email}")
        db.session.commit()

        return {"message": "User Deleted Successfully"}, 200


class GetAllIssues(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        query = Issue.query.order_by(Issue.created_at.desc())
        total = query.count()
        issues = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            "issues": [issue.to_dict() for issue in issues],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }, 200


class UpdateIssueStatus(Resource):
    @jwt_required()
    def put(self, issue_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue Not Found"}, 404

        data = request.get_json()
        new_status = data.get("status")

        if new_status not in [status.value for status in IssueStatus]:
            return {"error": "Invalid Status"}, 400

        issue.status = IssueStatus(new_status)
        log_admin_action(user_id, "update_status", "issue", issue_id, f"Status changed to {new_status}")
        db.session.commit()

        if new_status == "verified":
            award_points(issue.citizen_id, "issue_verified", db)
        elif new_status == "resolved":
            award_points(issue.citizen_id, "issue_resolved", db)

        citizen = User.query.get(issue.citizen_id)
        if citizen:
            send_status_notification(citizen, issue, new_status)
            send_status_sms(citizen, issue, new_status)

        return {
            "message": "Issue Status Updated Successfully",
            "issue": issue.to_dict(),
        }, 200


class ListDepartments(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403
        departments = Department.query.order_by(Department.name.asc()).all()
        return {"departments": [d.to_dict() for d in departments]}, 200


class CreateDepartment(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        description = (data.get("description") or "").strip()
        contact_email = (data.get("contact_email") or "").strip()
        contact_phone = (data.get("contact_phone") or "").strip()

        if not name:
            return {"error": "name required"}, 400
        if not contact_email:
            return {"error": "contact_email required"}, 400
        if not contact_phone:
            return {"error": "contact_phone required"}, 400

        # Check if department already exists
        existing = Department.query.filter_by(name=name).first()
        if existing:
            return {"error": "Department with this name already exists"}, 400

        dept = Department(
            name=name,
            description=description,
            contact_email=contact_email,
            contact_phone=contact_phone,
            sla_hours=data.get("sla_hours", 72),
        )
        db.session.add(dept)
        log_admin_action(user_id, "create_department", "department", None, f"Created department {name}")
        db.session.commit()
        return {"message": "Department created", "department": dept.to_dict()}, 201


class AssignDepartment(Resource):
    @jwt_required()
    def put(self, issue_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        data = request.get_json() or {}
        department_id = data.get("department_id")
        if not department_id:
            return {"error": "department_id required"}, 400

        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue Not Found"}, 404

        dept = Department.query.get(department_id)
        if not dept:
            return {"error": "Department Not Found"}, 404

        issue.department_id = dept.id
        log_admin_action(user_id, "assign_department", "issue", issue_id, f"Assigned to {dept.name}")
        db.session.commit()
        return {"message": "Department assigned", "issue": issue.to_dict()}, 200


class CreateIssueUpdate(Resource):
    @jwt_required()
    def post(self, issue_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        data = request.form
        files = request.files.getlist("images")

        title = (data.get("title") or "").strip()
        body = (data.get("body") or "").strip()
        progress = data.get("progress", "0")

        if not title:
            return {"error": "title required"}, 400
        try:
            progress = int(progress)
            if progress < 0 or progress > 100:
                raise ValueError()
        except Exception:
            return {"error": "progress must be 0-100"}, 400

        if files and any(f.content_length > 15 * 1024 * 1024 for f in files):
            return {"error": "Each image must be less than 15 MB"}, 400

        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue Not Found"}, 404

        image_urls = []
        for file in files:
            try:
                img = compress_image(file)
                url = upload_file_to_s3(
                    img,
                    f"issues/updates/{user_id}_{uuid4()}_{file.filename}",
                    config=app.config["S3_CONFIG"],
                    content_type="image/webp",
                )
                image_urls.append(url)
            except Exception as e:
                return {"error": f"Failed to upload image: {str(e)}"}, 500

        update = IssueUpdate(
            issue_id=issue.id,
            author_id=user.id,
            title=title,
            body=body,
            progress=progress,
            image_urls=image_urls,
        )
        db.session.add(update)
        db.session.commit()
        return {"message": "Update posted", "update": update.to_dict()}, 201


class GetAuditLog(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        query = AuditLog.query.order_by(AuditLog.created_at.desc())
        total = query.count()
        logs = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            "logs": [log.to_dict() for log in logs],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }, 200


class GetAnalytics(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        # Status breakdown
        status_counts = (
            db.session.query(Issue.status, func.count(Issue.id))
            .group_by(Issue.status)
            .all()
        )
        status_breakdown = {s.value: c for s, c in status_counts}

        # Issue type breakdown
        type_counts = (
            db.session.query(Issue.issue_type, func.count(Issue.id))
            .group_by(Issue.issue_type)
            .all()
        )
        type_breakdown = {t: c for t, c in type_counts}

        # Issues per department
        dept_counts = (
            db.session.query(Department.name, func.count(Issue.id))
            .join(Issue, Issue.department_id == Department.id)
            .group_by(Department.name)
            .all()
        )
        department_breakdown = {d: c for d, c in dept_counts}

        # Monthly issue trend (last 12 months)
        monthly = (
            db.session.query(
                extract("year", Issue.created_at),
                extract("month", Issue.created_at),
                func.count(Issue.id),
            )
            .group_by(
                extract("year", Issue.created_at),
                extract("month", Issue.created_at),
            )
            .order_by(
                extract("year", Issue.created_at).desc(),
                extract("month", Issue.created_at).desc(),
            )
            .limit(12)
            .all()
        )
        monthly_trend = [
            {"year": int(y), "month": int(m), "count": c}
            for y, m, c in monthly
        ]
        monthly_trend.reverse()

        # Average resolution time (for resolved/verified issues)
        resolved_issues = (
            Issue.query.filter(Issue.status.in_([IssueStatus.resolved, IssueStatus.verified]))
            .filter(Issue.updated_at.isnot(None))
            .all()
        )
        if resolved_issues:
            total_seconds = sum(
                (i.updated_at - i.created_at).total_seconds() for i in resolved_issues
            )
            avg_resolution_hours = round(total_seconds / len(resolved_issues) / 3600, 1)
        else:
            avg_resolution_hours = 0

        # Total counts
        total_issues = Issue.query.count()
        total_users = User.query.filter(User.role == UserRole.citizen).count()
        total_departments = Department.query.count()

        # Unassigned issues (no department)
        unassigned = Issue.query.filter(Issue.department_id.is_(None)).count()

        return {
            "summary": {
                "total_issues": total_issues,
                "total_users": total_users,
                "total_departments": total_departments,
                "unassigned": unassigned,
                "avg_resolution_hours": avg_resolution_hours,
            },
            "status_breakdown": status_breakdown,
            "type_breakdown": type_breakdown,
            "department_breakdown": department_breakdown,
            "monthly_trend": monthly_trend,
        }, 200


class ExportIssues(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        # Optional filters
        status = request.args.get("status")
        issue_type = request.args.get("issue_type")
        department_id = request.args.get("department_id", type=int)

        query = Issue.query
        if status:
            query = query.filter(Issue.status == status)
        if issue_type:
            query = query.filter(Issue.issue_type == issue_type)
        if department_id:
            query = query.filter(Issue.department_id == department_id)

        issues = query.order_by(Issue.created_at.desc()).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "ID", "Title", "Description", "Type", "Status", "Address",
            "Latitude", "Longitude", "Department", "Reported By",
            "Created At", "Updated At",
        ])

        for issue in issues:
            dept = Department.query.get(issue.department_id) if issue.department_id else None
            reporter = User.query.get(issue.citizen_id)
            writer.writerow([
                issue.id,
                issue.title,
                issue.description,
                issue.issue_type,
                issue.status.value,
                issue.address,
                issue.latitude,
                issue.longitude,
                dept.name if dept else "",
                f"{reporter.firstname} {reporter.lastname}" if reporter else "",
                issue.created_at.isoformat() if issue.created_at else "",
                issue.updated_at.isoformat() if issue.updated_at else "",
            ])

        csv_content = output.getvalue()
        output.close()

        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=citypulse_issues.csv"},
        )


class GetSLAReport(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        departments = Department.query.all()
        report = []

        for dept in departments:
            issues = Issue.query.filter_by(department_id=dept.id).filter(
                Issue.status.in_([IssueStatus.resolved, IssueStatus.verified])
            ).all()

            total = len(issues)
            if total == 0:
                report.append({
                    "department": dept.name,
                    "sla_hours": dept.sla_hours,
                    "total_resolved": 0,
                    "met_sla": 0,
                    "breached_sla": 0,
                    "compliance_rate": 0,
                    "avg_resolution_hours": 0,
                })
                continue

            met = 0
            total_hours = 0
            for issue in issues:
                hours = (issue.updated_at - issue.created_at).total_seconds() / 3600
                total_hours += hours
                if hours <= dept.sla_hours:
                    met += 1

            report.append({
                "department": dept.name,
                "sla_hours": dept.sla_hours,
                "total_resolved": total,
                "met_sla": met,
                "breached_sla": total - met,
                "compliance_rate": round(met / total * 100, 1),
                "avg_resolution_hours": round(total_hours / total, 1),
            })

        # Overall stats
        all_resolved = Issue.query.filter(
            Issue.status.in_([IssueStatus.resolved, IssueStatus.verified])
        ).all()
        overall_total = len(all_resolved)
        overall_met = 0
        overall_hours = 0
        for issue in all_resolved:
            hours = (issue.updated_at - issue.created_at).total_seconds() / 3600
            overall_hours += hours
            if issue.department_id:
                dept = Department.query.get(issue.department_id)
                if dept and hours <= dept.sla_hours:
                    overall_met += 1

        return {
            "departments": report,
            "overall": {
                "total_resolved": overall_total,
                "met_sla": overall_met,
                "breached_sla": overall_total - overall_met,
                "compliance_rate": round(overall_met / overall_total * 100, 1) if overall_total else 0,
                "avg_resolution_hours": round(overall_hours / overall_total, 1) if overall_total else 0,
            },
        }, 200


class ListGeofences(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        fences = Geofence.query.all()
        return {"geofences": [f.to_dict() for f in fences]}, 200


class CreateGeofence(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        department_id = data.get("department_id")

        if not name or not department_id:
            return {"error": "name and department_id required"}, 400

        dept = Department.query.get(department_id)
        if not dept:
            return {"error": "Department not found"}, 404

        try:
            min_lat = float(data.get("min_lat"))
            max_lat = float(data.get("max_lat"))
            min_lng = float(data.get("min_lng"))
            max_lng = float(data.get("max_lng"))
        except (TypeError, ValueError):
            return {"error": "min_lat, max_lat, min_lng, max_lng must be numbers"}, 400

        if min_lat > max_lat or min_lng > max_lng:
            return {"error": "Invalid bounding box coordinates"}, 400

        fence = Geofence(
            name=name,
            department_id=department_id,
            min_lat=min_lat,
            max_lat=max_lat,
            min_lng=min_lng,
            max_lng=max_lng,
        )
        db.session.add(fence)
        log_admin_action(user_id, "create_geofence", "geofence", None, f"Created geofence {name} for {dept.name}")
        db.session.commit()
        return {"message": "Geofence created", "geofence": fence.to_dict()}, 201


class DeleteGeofence(Resource):
    @jwt_required()
    def delete(self, fence_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        fence = Geofence.query.get(fence_id)
        if not fence:
            return {"error": "Geofence not found"}, 404

        db.session.delete(fence)
        log_admin_action(user_id, "delete_geofence", "geofence", fence_id, f"Deleted geofence {fence.name}")
        db.session.commit()
        return {"message": "Geofence deleted"}, 200


class AutoAssignByGeofence(Resource):
    @jwt_required()
    def post(self, issue_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue not found"}, 404

        if issue.latitude is None or issue.longitude is None:
            return {"error": "Issue has no location data"}, 400

        fence = Geofence.query.filter(
            Geofence.min_lat <= issue.latitude,
            Geofence.max_lat >= issue.latitude,
            Geofence.min_lng <= issue.longitude,
            Geofence.max_lng >= issue.longitude,
        ).first()

        if not fence:
            return {"error": "No matching geofence found for this location"}, 404

        issue.department_id = fence.department_id
        log_admin_action(user_id, "auto_assign_geofence", "issue", issue_id, f"Auto-assigned to {fence.department.name} via geofence {fence.name}")
        db.session.commit()
        return {"message": f"Assigned to {fence.department.name}", "issue": issue.to_dict()}, 200


class VerifyIssue(Resource):
    @jwt_required()
    def post(self, issue_id):
        """Run AI image verification on an issue's images."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue Not Found"}, 404

        if not issue.image_urls:
            return {"error": "No images to verify"}, 400

        import os
        img_cls_enabled = os.getenv("IMAGE_CLASSIFICATION_ENABLED", "false").lower() in ("true", "1", "yes")
        if not img_cls_enabled:
            return {"error": "Image classification is disabled"}, 501

        try:
            from ..utils.image_verifier import verify_image_from_bytes, should_flag_user
            import requests as http_requests
            from datetime import datetime

            all_verifications = []
            overall_valid = True
            overall_confidence = 0.0
            all_mismatch_flags = []
            user_should_be_flagged = False

            for idx, url in enumerate(issue.image_urls):
                try:
                    resp = http_requests.get(url, timeout=30)
                    resp.raise_for_status()

                    result = verify_image_from_bytes(
                        image_bytes=resp.content,
                        filename=f"image_{idx}.jpg",
                        issue_title=issue.title,
                        issue_description=issue.description,
                        issue_type=issue.issue_type,
                    )

                    all_verifications.append({
                        "image_index": idx,
                        "url": url,
                        "is_valid": result["is_valid"],
                        "confidence": result["confidence"],
                        "reasoning": result["reasoning"],
                        "detected_objects": result["detected_objects"],
                        "mismatch_flags": result["mismatch_flags"],
                    })

                    if not result["is_valid"]:
                        overall_valid = False
                    overall_confidence = max(overall_confidence, result["confidence"])
                    all_mismatch_flags.extend(result["mismatch_flags"])

                    if should_flag_user(result):
                        user_should_be_flagged = True

                except Exception as e:
                    all_verifications.append({
                        "image_index": idx,
                        "url": url,
                        "is_valid": True,
                        "confidence": 0.0,
                        "reasoning": f"Error: {str(e)}",
                        "detected_objects": [],
                        "mismatch_flags": [],
                    })

            if overall_valid and overall_confidence > 0.3:
                state = VerificationState.verified
                verification_message = "AI verification passed. Images match the reported issue."
            elif not overall_valid and overall_confidence > 0.7:
                state = VerificationState.rejected
                verification_message = "AI verification failed. Images do not match the reported issue."
            else:
                state = VerificationState.pending
                verification_message = "AI verification inconclusive. Manual review recommended."

            existing_v = VerificationStatus.query.filter_by(issue_id=issue_id).first()
            if existing_v:
                existing_v.status = state
                existing_v.verified_by = user_id
                existing_v.verified_at = datetime.utcnow()
                existing_v.ai_confidence = overall_confidence
                existing_v.ai_reasoning = verification_message
                existing_v.is_consistent = overall_valid
                existing_v.detected_objects = all_verifications[0].get("detected_objects", []) if all_verifications else []
                existing_v.mismatch_flags = all_mismatch_flags
            else:
                v = VerificationStatus(
                    issue_id=issue_id,
                    status=state,
                    verified_by=user_id,
                    verified_at=datetime.utcnow(),
                    ai_confidence=overall_confidence,
                    ai_reasoning=verification_message,
                    is_consistent=overall_valid,
                    detected_objects=all_verifications[0].get("detected_objects", []) if all_verifications else [],
                    mismatch_flags=all_mismatch_flags,
                )
                db.session.add(v)

            db.session.commit()

            user_flagged = False
            if user_should_be_flagged:
                from ..utils.reputation import flag_user
                citizen = User.query.get(issue.citizen_id)
                if citizen:
                    user_flagged = flag_user(citizen, "AI detected image mismatch", db)

            return {
                "verification": {
                    "status": state.value,
                    "message": verification_message,
                    "ai_confidence": overall_confidence,
                    "is_consistent": overall_valid,
                    "mismatch_flags": all_mismatch_flags,
                },
                "detections": all_verifications,
                "user_flagged": user_flagged,
            }, 200

        except Exception as e:
            return {"error": f"Verification failed: {str(e)}"}, 500


class GetFlaggedUsers(Resource):
    @jwt_required()
    def get(self):
        """List all flagged users."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        from ..models.user_reputation import UserReputation

        flagged = UserReputation.query.filter(
            UserReputation.is_flagged == True
        ).all()

        users_data = []
        for rep in flagged:
            u = User.query.get(rep.user_id)
            if u:
                users_data.append({
                    "user": {
                        "id": u.id,
                        "firstname": u.firstname,
                        "lastname": u.lastname,
                        "email": u.email,
                    },
                    "reputation": rep.to_dict(),
                })

        return {"flagged_users": users_data}, 200


class UnflagUser(Resource):
    @jwt_required()
    def post(self, user_id):
        """Remove flag/suspension from a user."""
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)
        if not admin or admin.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        data = request.get_json() or {}
        reason = data.get("reason", "Admin review cleared")

        result = unreputation_user(user_id, admin_id, reason, db)
        return result, 200
