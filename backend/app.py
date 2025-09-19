import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, upgrade, stamp, init, migrate as alembic_migrate

from api.models import db

from api.routes.auth import auth_bp
from api.routes.users import users_bp
from api.routes.issues import issue_bp

from config import Config

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    print("------ [ INFO ] ------ Initializing Database")

    db.init_app(app)
    migrate.init_app(app, db)

    print("------ [ INFO ] ------ Initializing JWT Manager")
    jwt = JWTManager(app)

    print("------ [ INFO ] ------ Registering Blueprints")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(issue_bp, url_prefix="/api/issues")

    @app.route("/ping", methods=["GET", "POST"])
    def ping():
        return "Pong!", 200

    return app


def run_migrations(app):
    with app.app_context():
        if not os.path.exists("migrations"):
            init()

        stamp()
        upgrade()


if __name__ == "__main__":
    app = create_app()
    run_migrations(app)

    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
