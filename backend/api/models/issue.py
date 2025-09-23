import enum
from . import db
from geoalchemy2 import Geometry, alembic_helpers


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

    def __repr__(self):
        return f"<Issue {self.title} - {self.status.value}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "issue_type": self.issue_type,
            "status": self.status.value,
            "image_urls": self.image_urls,
            "voice_note_url": self.voice_note_url,
            "video_note_url": self.video_note_url,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "department_id": self.department_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "citizen_id": self.citizen_id,
            "user": self.user.to_dict() if self.user else None,
        }

    def to_public_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "issue_type": self.issue_type,
            "status": self.status.value,
            "image_urls": self.image_urls,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
