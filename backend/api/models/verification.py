import enum
from . import db


class VerificationStatus(enum.Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"


class VerificationStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"), nullable=False)
    status = db.Column(
        db.Enum(VerificationStatus), default=VerificationStatus.pending, nullable=False
    )

    verified_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)

    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Verification Issue ID: {self.issue_id} - Status: {self.status.value}>"

    def to_dict(self):
        return {
            "id": self.id,
            "issue_id": self.issue_id,
            "status": self.status.value,
            "verified_by": self.verified_by,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
        }
