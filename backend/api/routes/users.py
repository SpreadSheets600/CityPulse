from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api.models import db, User, UserRole
from ..utils.reputation import get_user_reputation


class GetUserReputation(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get reputation for a user."""
        reputation = get_user_reputation(user_id)
        return {"reputation": reputation}, 200


class GetMyReputation(Resource):
    @jwt_required()
    def get(self):
        """Get current user's reputation."""
        user_id = get_jwt_identity()
        reputation = get_user_reputation(user_id)
        return {"reputation": reputation}, 200
