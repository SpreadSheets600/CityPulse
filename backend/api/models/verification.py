import enum
from . import db


class VerificationState(enum.Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"


class VerificationStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"), nullable=False)
    status = db.Column(
        db.Enum(VerificationState), default=VerificationState.pending, nullable=False
    )

    verified_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)

    notes = db.Column(db.Text, nullable=True)

    ai_confidence = db.Column(db.Float, nullable=True)
    ai_reasoning = db.Column(db.Text, nullable=True)
    is_consistent = db.Column(db.Boolean, nullable=True)
    detected_objects = db.Column(db.JSON, nullable=True)
    mismatch_flags = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f"<Verification Issue ID: {self.issue_id} - Status: {self.status.value}>"

    def to_dict(self):
        return {
            "id": self.id,
            "issue_id": self.issue_id,
            "status": self.status.value,
            "verified_by": self.verified_by,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "notes": self.notes,
            "ai_confidence": self.ai_confidence,
            "ai_reasoning": self.ai_reasoning,
            "is_consistent": self.is_consistent,
            "detected_objects": self.detected_objects,
            "mismatch_flags": self.mismatch_flags,
        }
