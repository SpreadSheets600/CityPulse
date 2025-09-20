from flask import request
from flask_restful import Resource
from string import ascii_letters, digits

from flask_jwt_extended import (
    create_refresh_token,
    create_access_token,
    unset_jwt_cookies,
    get_jwt_identity,
    jwt_required,
)

from api.models import db, User
from sqlalchemy.exc import IntegrityError


class Register(Resource):
    def post(self):
        data = request.get_json()
        required = ["phone", "email", "password", "firstname", "lastname"]

        if not all(k in data for k in required):
            return {"error": "Missing Required Fields"}, 400

        if (
            data.get("password")
            and len(data["password"]) < 8
            and ascii_letters not in data["password"]
            and digits not in data["password"]
        ):
            return {"error": "Password Must Be 8 Characters Long"}, 400

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
            return {"message": "User Registered Successfully"}, 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "User With This Phone / Email Already Exists"}, 400


class Login(Resource):
    def post(self):
        data = request.get_json()

        password = data.get("password")
        user = None

        if data.get("email"):
            user = User.query.filter_by(email=data["email"]).first()

        elif data.get("phone"):
            user = User.query.filter_by(phone=data["phone"]).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            return (
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user.to_dict(),
                },
                200,
            )

        return {"msg": "Invalid Credentials"}, 401


class Logout(Resource):
    @jwt_required()
    def post(self):
        response = {"msg": "Logout Successful"}

        unset_jwt_cookies(response)
        return response, 200


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {"access_token": new_access_token}, 200
