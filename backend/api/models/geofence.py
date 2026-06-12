from . import db


class Geofence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=False)
    min_lat = db.Column(db.Float, nullable=False)
    max_lat = db.Column(db.Float, nullable=False)
    min_lng = db.Column(db.Float, nullable=False)
    max_lng = db.Column(db.Float, nullable=False)

    department = db.relationship("Department", backref=db.backref("geofences", lazy=True))

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Geofence {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department_id": self.department_id,
            "department_name": self.department.name if self.department else None,
            "min_lat": self.min_lat,
            "max_lat": self.max_lat,
            "min_lng": self.min_lng,
            "max_lng": self.max_lng,
            "created_at": self.created_at.isoformat(),
        }

    def contains(self, lat, lng):
        return self.min_lat <= lat <= self.max_lat and self.min_lng <= lng <= self.max_lng
