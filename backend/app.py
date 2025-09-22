import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, upgrade, stamp, init, migrate as alembic_migrate

from api.models import db, User, UserRole
from api.routes.auth import Register, Login, Logout, Refresh, GetCurrentUser
from api.routes.issues import (
    ReportIssue,
    MyIssues,
    AllIssues,
    GetIssue,
    GetIssueUpdates,
    GeocodeAddress,
    ReverseGeocode,
)
from api.routes.admin import (
    GetAllUsers,
    DeleteUser,
    GetAllIssues,
    UpdateIssueStatus,
    ListDepartments,
    AssignDepartment,
    CreateIssueUpdate,
)

from config import Config

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    CORS(app)

    print("------ [ INFO ] ------ Initializing Database")

    db.init_app(app)
    migrate.init_app(app, db)

    print("------ [ INFO ] ------ Initializing JWT Manager")
    jwt = JWTManager(app)

    print("------ [ INFO ] ------ Initializing Flask-RESTful API")
    api = Api(app)

    print("------ [ INFO ] ------ Registering Resources")
    api.add_resource(Register, "/api/auth/register")
    api.add_resource(Refresh, "/api/auth/refresh")
    api.add_resource(Logout, "/api/auth/logout")
    api.add_resource(Login, "/api/auth/login")

    api.add_resource(GetCurrentUser, "/api/auth/me")

    api.add_resource(ReportIssue, "/api/issues/report")
    api.add_resource(AllIssues, "/api/issues")
    api.add_resource(GetIssue, "/api/issues/<int:issue_id>")
    api.add_resource(GetIssueUpdates, "/api/issues/<int:issue_id>/updates")
    api.add_resource(GeocodeAddress, "/api/geocode")
    api.add_resource(ReverseGeocode, "/api/reverse-geocode")

    api.add_resource(MyIssues, "/api/issues/my-issues")

    api.add_resource(GetAllUsers, "/api/admin/users")
    api.add_resource(DeleteUser, "/api/admin/users/<int:user_id>")

    api.add_resource(GetAllIssues, "/api/admin/issues")
    api.add_resource(UpdateIssueStatus, "/api/admin/issues/<int:issue_id>/status")
    api.add_resource(ListDepartments, "/api/admin/departments")
    api.add_resource(AssignDepartment, "/api/admin/issues/<int:issue_id>/department")
    api.add_resource(CreateIssueUpdate, "/api/admin/issues/<int:issue_id>/updates")

    @app.route("/ping", methods=["GET", "POST"])
    def ping():
        return "Pong!", 200

    return app


def create_db():
    try:
        User.query.first()
        print("------ [ INFO ] ------ Database Already Exists")
        return
    except:
        print("------ [ INFO ] ------ Creating Database")
        db.create_all()

    print("------ [ INFO ] ------ Creating Default Admin User")

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
