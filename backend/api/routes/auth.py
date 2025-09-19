from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    create_access_token,
    unset_jwt_cookies,
    jwt_required,
)

from api.models import db, User
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    required = ["phone", "email", "password", "firstname", "lastname"]

    if not all(k in data for k in required):
        return jsonify({"error": "Missing Required Fields"}), 400

    user = User(
        email=data["email"],
        role=data["role"],
        phone=data["phone"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        address=data["address"],
    )
    user.set_password(data["password"])

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User Registered Successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User With This Phone / Email Already Exists"}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    password = data.get("password")
    user = None

    if data.get("email"):
        user = User.query.filter_by(email=data["email"]).first()

    elif data.get("phone"):
        user = User.query.filter_by(phone=data["phone"]).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, user=user.to_dict()), 200

    return jsonify({"msg": "Invalid Credentials"}), 401


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "Logout Successful"})
    unset_jwt_cookies(response)
    return response, 200
