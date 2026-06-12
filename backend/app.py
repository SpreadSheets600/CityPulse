import json
import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate, upgrade, stamp, init

from api.models import db, User, UserRole, Department
from api.routes.auth import (
    Register,
    Login,
    Logout,
    Refresh,
    GetCurrentUser,
    UpdateProfile,
    ForgotPassword,
    ResetPassword,
)
from api.routes.issues import (
    ReportIssue,
    MyIssues,
    AllIssues,
    PublicIssues,
    GetIssue,
    GetIssueUpdates,
    GeocodeAddress,
    ReverseGeocode,
    UpvoteIssue,
    IssueComments,
    VerifyIssueImages,
)
from api.routes.admin import (
    GetAllUsers,
    DeleteUser,
    GetAllIssues,
    UpdateIssueStatus,
    ListDepartments,
    CreateDepartment,
    AssignDepartment,
    CreateIssueUpdate,
    GetAuditLog,
    GetAnalytics,
    ExportIssues,
    GetSLAReport,
    ListGeofences,
    CreateGeofence,
    DeleteGeofence,
    AutoAssignByGeofence,
    VerifyIssue,
    GetFlaggedUsers,
    UnflagUser,
)
from api.routes.users import GetUserReputation, GetMyReputation
from api.routes.oauth import GoogleLogin, GitHubLogin, OAuthCallback, init_oauth
from api.routes.chatbot import Chatbot

from config import Config
from api.utils.email import init_mail

migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")
    CORS(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
        supports_credentials=True,
    )

    limiter.init_app(app)

    print("------ [ INFO ] ------ Initializing Database")

    db.init_app(app)
    migrate.init_app(app, db)

    print("------ [ INFO ] ------ Initializing JWT Manager")
    JWTManager(app)

    print("------ [ INFO ] ------ Initializing Mail")
    init_mail(app)

    print("------ [ INFO ] ------ Initializing OAuth")
    init_oauth(app)

    # Log feature status
    features = {
        "Email": app.config.get("EMAIL_ENABLED", False),
        "SMS": app.config.get("SMS_ENABLED", False),
        "OAuth": app.config.get("OAUTH_ENABLED", False),
        "S3": app.config.get("S3_ENABLED", True),
        "Image Classification (LocateAnything)": app.config.get("IMAGE_CLASSIFICATION_ENABLED", False),
        "AI Text (Ollama)": app.config.get("AI_TEXT_ENABLED", False),
        "Geocoding": app.config.get("GEOCODING_ENABLED", True),
    }
    print("------ [ INFO ] ------ Feature Toggles:")
    for name, enabled in features.items():
        status = "ON" if enabled else "OFF"
        print(f"      {name}: {status}")

    print("------ [ INFO ] ------ Initializing Flask-RESTful API")
    api = Api(app)

    print("------ [ INFO ] ------ Registering Resources")
    api.add_resource(Register, "/api/auth/register")
    api.add_resource(Refresh, "/api/auth/refresh")
    api.add_resource(Logout, "/api/auth/logout")
    api.add_resource(Login, "/api/auth/login")

    api.add_resource(GetCurrentUser, "/api/auth/me")
    api.add_resource(UpdateProfile, "/api/auth/profile")
    api.add_resource(ForgotPassword, "/api/auth/forgot-password")
    api.add_resource(ResetPassword, "/api/auth/reset-password")

    api.add_resource(ReportIssue, "/api/issues/report")
    api.add_resource(AllIssues, "/api/issues")
    api.add_resource(PublicIssues, "/api/issues/public")
    api.add_resource(GetIssue, "/api/issues/<int:issue_id>")
    api.add_resource(GetIssueUpdates, "/api/issues/<int:issue_id>/updates")
    api.add_resource(IssueComments, "/api/issues/<int:issue_id>/comments")
    api.add_resource(VerifyIssueImages, "/api/issues/<int:issue_id>/verify")
    api.add_resource(GeocodeAddress, "/api/geocode")
    api.add_resource(ReverseGeocode, "/api/reverse-geocode")

    api.add_resource(MyIssues, "/api/issues/my-issues")
    api.add_resource(UpvoteIssue, "/api/issues/<int:issue_id>/upvote")

    api.add_resource(GetAllUsers, "/api/admin/users")
    api.add_resource(DeleteUser, "/api/admin/users/<int:user_id>")

    api.add_resource(GetAllIssues, "/api/admin/issues")
    api.add_resource(UpdateIssueStatus, "/api/admin/issues/<int:issue_id>/status")
    api.add_resource(ListDepartments, "/api/admin/departments")
    api.add_resource(CreateDepartment, "/api/admin/departments")
    api.add_resource(AssignDepartment, "/api/admin/issues/<int:issue_id>/department")
    api.add_resource(CreateIssueUpdate, "/api/admin/issues/<int:issue_id>/updates")
    api.add_resource(GetAuditLog, "/api/admin/audit-log")
    api.add_resource(GetAnalytics, "/api/admin/analytics")
    api.add_resource(ExportIssues, "/api/admin/export")
    api.add_resource(GetSLAReport, "/api/admin/sla")
    api.add_resource(ListGeofences, "/api/admin/geofences")
    api.add_resource(CreateGeofence, "/api/admin/geofences")
    api.add_resource(DeleteGeofence, "/api/admin/geofences/<int:fence_id>")
    api.add_resource(
        AutoAssignByGeofence, "/api/admin/issues/<int:issue_id>/auto-assign"
    )

    api.add_resource(VerifyIssue, "/api/admin/issues/<int:issue_id>/verify")

    api.add_resource(GetFlaggedUsers, "/api/admin/flagged-users")
    api.add_resource(UnflagUser, "/api/admin/users/<int:user_id>/unflag")

    api.add_resource(GetUserReputation, "/api/users/<int:user_id>/reputation")
    api.add_resource(GetMyReputation, "/api/users/me/reputation")

    api.add_resource(GoogleLogin, "/api/auth/oauth/google")
    api.add_resource(GitHubLogin, "/api/auth/oauth/github")
    api.add_resource(OAuthCallback, "/api/auth/oauth/callback")

    api.add_resource(Chatbot, "/api/chatbot")

    @app.route("/ping", methods=["GET", "POST"])
    def ping():
        return "Pong!", 200

    @app.route("/api/v1/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    def api_v1_redirect(path):
        from flask import redirect as flask_redirect

        return flask_redirect(f"/api/{path}", code=301)

    return app


def create_db():
    try:
        User.query.first()
        print("------ [ INFO ] ------ Database Already Exists")
        return
    except Exception as e:
        print(f"------ [ INFO ] ------ Error Occurred With Database : {e}")
        print("------ [ INFO ] ------ Creating Database")
        db.session.rollback()
        db.create_all()

    print("------ [ INFO ] ------ Creating Default Admin User")
    db.session.rollback()

    existing_admin = User.query.filter_by(email="admin@citypulse.com").first()

    if existing_admin:
        print("------ [ INFO ] ------ Admin Already Exists")

    else:
        admin_user = User(
            email="admin@citypulse.com",
            role=UserRole.admin,
            phone="1234567890",
            firstname="Admin",
            lastname="User",
            address="Admin Office",
        )
        admin_user.set_password("admin123")

        try:
            db.session.add(admin_user)
            db.session.commit()
            print("------ [ INFO ] ------ Default Admin User Created")
            print()
            print("------ [ INFO ] ------ Email : admin@citypulse.com")
            print("------ [ INFO ] ------ Password : admin123")

        except Exception as e:
            db.session.rollback()
            print(f"------ [ ERROR ] ------ Failed to create admin user: {e}")

    # Load departments from JSON
    departments_path = os.path.join(
        os.path.dirname(__file__), "api", "data", "departments.json"
    )
    try:
        with open(departments_path) as f:
            departments_data = json.load(f)
    except Exception as e:
        print(f"------ [ ERROR ] ------ Failed to load departments.json: {e}")
        departments_data = {"departments": []}

    created_count = 0
    for dept in departments_data.get("departments", []):
        existing = Department.query.filter_by(name=dept["name"]).first()
        if not existing:
            new_dept = Department(
                name=dept["name"],
                description=dept["description"],
                contact_email=dept["contact"]["email"],
                contact_phone=dept["contact"]["phone"],
            )
            db.session.add(new_dept)
            created_count += 1

    try:
        db.session.commit()
        print(f"------ [ INFO ] ------ Created {created_count} new departments")
    except Exception as e:
        db.session.rollback()
        print(f"------ [ ERROR ] ------ Failed to create departments: {e}")


def run_migrations(app):
    with app.app_context():
        if not os.path.exists("migrations"):
            init()

        stamp()
        upgrade()


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        create_db()

    app.run(host="0.0.0.0", port=5000, debug=True)
