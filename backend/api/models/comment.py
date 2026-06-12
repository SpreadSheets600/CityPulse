from . import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    issue = db.relationship("Issue", backref=db.backref("comments", lazy=True, cascade="all, delete-orphan"))
    author = db.relationship("User", backref="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "body": self.body,
            "issue_id": self.issue_id,
            "author_id": self.author_id,
            "author": self.author.to_dict() if self.author else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
