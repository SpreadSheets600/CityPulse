import os
from flask import request, redirect, current_app
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from authlib.integrations.flask_client import OAuth

from api.models import db, User, UserRole

oauth = OAuth()

_oauth_enabled = os.getenv("OAUTH_ENABLED", "false").lower() in ("true", "1", "yes")

if _oauth_enabled:
    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID", ""),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET", ""),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    oauth.register(
        name="github",
        client_id=os.getenv("GITHUB_CLIENT_ID", ""),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET", ""),
        access_token_url="https://github.com/login/oauth/access_token",
        access_token_params=None,
        authorize_url="https://github.com/login/oauth/authorize",
        authorize_params=None,
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "user:email"},
    )


class GoogleLogin(Resource):
    def get(self):
        if not _oauth_enabled:
            return {"error": "OAuth is disabled"}, 501
        redirect_uri = current_app.config.get(
            "OAUTH_REDIRECT_URI", "http://localhost:5000/api/auth/oauth/callback"
        )
        return oauth.google.authorize_redirect(redirect_uri)


class GitHubLogin(Resource):
    def get(self):
        if not _oauth_enabled:
            return {"error": "OAuth is disabled"}, 501
        redirect_uri = current_app.config.get(
            "OAUTH_REDIRECT_URI", "http://localhost:5000/api/auth/oauth/callback"
        )
        return oauth.github.authorize_redirect(redirect_uri)


class OAuthCallback(Resource):
    def get(self):
        if not _oauth_enabled:
            return {"error": "OAuth is disabled"}, 501

        provider = request.args.get("provider", "google")

        if provider == "google":
            token = oauth.google.authorize_access_token()
            user_info = token.get("userinfo")
            email = user_info.get("email")
            firstname = user_info.get("given_name", "")
            lastname = user_info.get("family_name", "")
        elif provider == "github":
            token = oauth.github.authorize_access_token()
            resp = oauth.github.get("user", token=token)
            user_info = resp.json()
            email = user_info.get("email")
            if not email:
                emails_resp = oauth.github.get("user/emails", token=token)
                for e in emails_resp.json():
                    if e.get("primary"):
                        email = e["email"]
                        break
            firstname = user_info.get("name", "").split(" ")[0] if user_info.get("name") else ""
            lastname = " ".join(user_info.get("name", "").split(" ")[1:]) if user_info.get("name") else ""
        else:
            return {"error": "Unknown provider"}, 400

        if not email:
            return {"error": "Could not retrieve email from provider"}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                role=UserRole.citizen,
                phone="",
                firstname=firstname or "User",
                lastname=lastname or "",
                address="",
            )
            db.session.add(user)
            db.session.commit()

        access_token = create_access_token(identity=str(user.id))
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        return redirect(f"{frontend_url}/auth/callback?token={access_token}")


def init_oauth(app):
    if _oauth_enabled:
        oauth.init_app(app)
    else:
        print("------ [ INFO ] ------ OAuth disabled (OAUTH_ENABLED=false)")
