from . import db


class UserReputation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    user = db.relationship("User", backref="reputation")

    issues_reported = db.Column(db.Integer, default=0)
    issues_verified = db.Column(db.Integer, default=0)
    issues_resolved = db.Column(db.Integer, default=0)
    upvotes_received = db.Column(db.Integer, default=0)
    penalties = db.Column(db.Integer, default=0)

    total_points = db.Column(db.Integer, default=0)

    trust_level = db.Column(db.String(20), default="newcomer")

    is_flagged = db.Column(db.Boolean, default=False)
    flag_reason = db.Column(db.String(200), nullable=True)
    flag_count = db.Column(db.Integer, default=0)
    is_suspended = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<UserReputation User ID: {self.user_id} - Points: {self.total_points}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "issues_reported": self.issues_reported,
            "issues_verified": self.issues_verified,
            "issues_resolved": self.issues_resolved,
            "upvotes_received": self.upvotes_received,
            "penalties": self.penalties,
            "total_points": self.total_points,
            "trust_level": self.trust_level,
            "is_flagged": self.is_flagged,
            "flag_reason": self.flag_reason,
            "flag_count": self.flag_count,
            "is_suspended": self.is_suspended,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def calculate_trust_level(self):
        if self.total_points >= 501:
            self.trust_level = "expert"
        elif self.total_points >= 201:
            self.trust_level = "trusted"
        elif self.total_points >= 51:
            self.trust_level = "contributor"
        else:
            self.trust_level = "newcomer"
