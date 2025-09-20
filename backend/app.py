import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, upgrade, stamp, init, migrate as alembic_migrate

from api.models import db
from api.routes.auth import Register, Login, Logout, Refresh
from api.routes.issues import ReportIssue, MyIssues, GetIssue

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

    api.add_resource(ReportIssue, "/api/issues/report")
    api.add_resource(GetIssue, "/api/issues/<int:issue_id>")

    api.add_resource(MyIssues, "/api/issues/my-issues")

    @app.route("/ping", methods=["GET", "POST"])
    def ping():
        return "Pong!", 200

    return app


def create_db():
    if not os.path.exists("citypulse.db"):
        print("------ [ INFO ] ------ Creating Database")
        db.create_all()
    else:
        print("------ [ INFO ] ------ Database Already Exists")


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
