from flask import request, current_app as app
from flask_restful import Resource

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from uuid import uuid4
from api.models import db, User, UserRole, Issue, IssueStatus, Department, IssueUpdate
from ..utils.s3 import upload_file_to_s3, compress_image


class GetAllUsers(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        users = User.query.all()
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

        return {"users": users_data}, 200


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
        db.session.commit()

        return {"message": "User Deleted Successfully"}, 200


class GetAllIssues(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        issues = Issue.query.order_by(Issue.created_at.desc()).all()
        issues_data = [issue.to_dict() for issue in issues]

        return {"issues": issues_data}, 200


class DeleteIssue(Resource):
    @jwt_required()
    def delete(self, issue_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue Not Found"}, 404

        db.session.delete(issue)
        db.session.commit()

        return {"message": "Issue Deleted Successfully"}, 200


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
        db.session.commit()

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
