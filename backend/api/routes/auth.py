from flask import request
from flask_restful import Resource
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["200/day", "50/hour"])

from flask_jwt_extended import (
    create_refresh_token,
    create_access_token,
    unset_jwt_cookies,
    get_jwt_identity,
    jwt_required,
)

from api.models import db, User, PasswordResetToken
from sqlalchemy.exc import IntegrityError


class Register(Resource):
    method_decorators = [limiter.limit("5/minute")]

    def post(self):
        data = request.get_json()
        required = ["phone", "email", "password", "firstname", "lastname"]

        if not all(k in data for k in required):
            return {"error": "Missing Required Fields"}, 400

        password = data.get("password", "")
        if len(password) < 8 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            return {"error": "Password Must Be At Least 8 Characters And Include Letters And Numbers"}, 400

        user = User(
            email=data["email"],
            role=data.get("role", "citizen"),
            phone=data["phone"],
            firstname=data["firstname"],
            lastname=data["lastname"],
            address=data.get("address", ""),
        )
        user.set_password(data["password"])

        try:
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            return {
                "message": "User Registered Successfully",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.to_dict(),
            }, 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "User With This Phone / Email Already Exists"}, 400


class Login(Resource):
    method_decorators = [limiter.limit("10/minute")]

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
        from flask import make_response

        response = make_response({"msg": "Logout Successful"})
        unset_jwt_cookies(response)
        return response


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {"access_token": new_access_token}, 200


class GetCurrentUser(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return {"error": "User not found"}, 404
        return {"user": user.to_dict()}, 200


class UpdateProfile(Resource):
    @jwt_required()
    def put(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400

        updatable = ["firstname", "lastname", "phone", "address", "profile_picture"]
        for field in updatable:
            if field in data:
                setattr(user, field, data[field])

        try:
            db.session.commit()
            return {"message": "Profile Updated Successfully", "user": user.to_dict()}, 200
        except IntegrityError:
            db.session.rollback()
            return {"error": "Phone or email already in use"}, 400


class ForgotPassword(Resource):
    method_decorators = [limiter.limit("3/minute")]

    def post(self):
        data = request.get_json()
        email = data.get("email", "").strip()
        if not email:
            return {"error": "Email is required"}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "If an account exists, a reset link has been sent."}, 200

        token = PasswordResetToken.create_for_user(user.id)
        print(f"------ [ INFO ] ------ Password Reset Token for {email}: {token}")
        return {"message": "If an account exists, a reset link has been sent."}, 200


class ResetPassword(Resource):
    def post(self):
        data = request.get_json()
        token = data.get("token", "").strip()
        new_password = data.get("password", "")

        if not token or not new_password:
            return {"error": "Token and password are required"}, 400

        if len(new_password) < 8:
            return {"error": "Password must be at least 8 characters"}, 400

        reset_token = PasswordResetToken.query.filter_by(token=token).first()
        if not reset_token or not reset_token.is_valid():
            return {"error": "Invalid or expired token"}, 400

        user = User.query.get(reset_token.user_id)
        if not user:
            return {"error": "User not found"}, 404

        user.set_password(new_password)
        reset_token.used = True
        db.session.commit()

        return {"message": "Password Reset Successfully"}, 200
