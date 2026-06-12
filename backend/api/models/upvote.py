from . import db


class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    __table_args__ = (db.UniqueConstraint("user_id", "issue_id", name="uq_user_issue_upvote"),)

    user = db.relationship("User", backref="upvotes")
    issue = db.relationship("Issue", backref="upvotes")
