from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from .user import User
from .issue import Issue
from .department import Department
from .verification import VerificationStatus

print("------ [ INFO ] ------ Models Imported Successfully")
