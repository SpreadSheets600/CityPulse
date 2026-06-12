import secrets
from datetime import datetime, timedelta
from . import db


class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship("User", backref="reset_tokens")

    @staticmethod
    def create_for_user(user_id):
        token = secrets.token_urlsafe(48)
        reset_token = PasswordResetToken(
            user_id=user_id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(hours=1),
        )
        db.session.add(reset_token)
        db.session.commit()
        return token

    def is_valid(self):
        return not self.used and datetime.utcnow() < self.expires_at
