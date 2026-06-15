import enum
from . import db


class IssueStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    resolved = "resolved"
    rejected = "rejected"
    verified = "verified"


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    image_urls = db.Column(db.JSON, nullable=False)

    voice_note_url = db.Column(db.String())
    video_note_url = db.Column(db.String())

    issue_type = db.Column(db.String(50), default="Unspecified")

    status = db.Column(
        db.Enum(IssueStatus), default=IssueStatus.pending, nullable=False
    )

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200))

    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=True)

    ai_analysis = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    citizen_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    verification = db.relationship("VerificationStatus", backref="issue", uselist=False)

    updates = db.relationship(
        "IssueUpdate", backref="issue", lazy=True, cascade="all, delete-orphan"
    )

    department = db.relationship("Department", backref="issues")

    def __repr__(self):
        return f"<Issue {self.title} - {self.status.value}>"

    def to_dict(self):
        from flask_jwt_extended import get_jwt_identity
        try:
            current_user_id = get_jwt_identity()
        except Exception:
            current_user_id = None

        user_upvoted = False
        if current_user_id:
            user_upvoted = any(str(u.user_id) == str(current_user_id) for u in self.upvotes)

        from flask import current_app
        from ..utils.s3 import resolve_media_urls, resolve_media_url

        s3_config = current_app.config.get("S3_CONFIG", {})
        image_urls = resolve_media_urls(self.image_urls, s3_config) if s3_config.get("endpoint_url") else self.image_urls
        voice_url = resolve_media_url(self.voice_note_url, s3_config) if s3_config.get("endpoint_url") and self.voice_note_url else self.voice_note_url
        video_url = resolve_media_url(self.video_note_url, s3_config) if s3_config.get("endpoint_url") and self.video_note_url else self.video_note_url

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "issue_type": self.issue_type,
            "status": self.status.value,
            "image_urls": image_urls,
            "voice_note_url": voice_url,
            "video_note_url": video_url,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "department_id": self.department_id,
            "department": self.department.to_dict() if self.department else None,
            "ai_analysis": self.ai_analysis,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "citizen_id": self.citizen_id,
            "user": self.user.to_dict() if self.user else None,
            "upvote_count": len(self.upvotes),
            "user_upvoted": user_upvoted,
        }

    def to_public_dict(self):
        from flask import current_app
        from ..utils.s3 import resolve_media_urls

        s3_config = current_app.config.get("S3_CONFIG", {})
        image_urls = resolve_media_urls(self.image_urls, s3_config) if s3_config.get("endpoint_url") else self.image_urls

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "issue_type": self.issue_type,
            "status": self.status.value,
            "image_urls": image_urls,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "department": self.department.name if self.department else None,
            "ai_analysis": self.ai_analysis,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "upvote_count": len(self.upvotes),
        }
