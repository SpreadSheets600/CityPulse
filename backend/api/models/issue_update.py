from . import db


class IssueUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=True)
    progress = db.Column(db.Integer, default=0)  # 0-100 percent
    image_urls = db.Column(db.JSON, default=list)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        from flask import current_app
        from ..utils.s3 import resolve_media_urls

        s3_config = current_app.config.get("S3_CONFIG", {})
        image_urls = resolve_media_urls(self.image_urls, s3_config) if s3_config.get("endpoint_url") and self.image_urls else self.image_urls or []

        return {
            "id": self.id,
            "issue_id": self.issue_id,
            "author_id": self.author_id,
            "title": self.title,
            "body": self.body,
            "progress": self.progress,
            "image_urls": image_urls,
            "created_at": self.created_at.isoformat(),
        }
