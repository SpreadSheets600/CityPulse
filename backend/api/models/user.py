import enum
from . import db
from passlib.hash import bcrypt


class UseRole(enum.Enum):
    citizen = "citizen"
    admin = "admin"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(80), unique=True, nullable=False)

    address = db.Column(db.String(200), nullable=False)

    role = db.Column(db.Enum(UseRole), default=UseRole.citizen, nullable=False)

    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(120), nullable=False)

    profile_picture = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    isuues = db.relationship("Issue", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "address": self.address,
            "role": self.role.value,
            "phone": self.phone,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def profile_picture_url(self, firstname, lastname):
        if self.profile_picture:
            return self.profile_picture
        else:
            self.profile_picture = f"https://api.dicebear.com/9.x/notionists-neutral/svg?seed={firstname}{lastname}"
            return self.profile_picture
