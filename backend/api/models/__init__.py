from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from .user import User, UserRole
from .department import Department
from .issue import Issue, IssueStatus
from .issue_update import IssueUpdate
from .verification import VerificationStatus

print("------ [ INFO ] ------ Models Imported Successfully")
