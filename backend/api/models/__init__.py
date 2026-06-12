from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from .user import User, UserRole
from .department import Department
from .issue import Issue, IssueStatus
from .issue_update import IssueUpdate
from .verification import VerificationStatus, VerificationState
from .password_reset import PasswordResetToken
from .upvote import Upvote
from .comment import Comment
from .audit_log import AuditLog
from .geofence import Geofence
from .user_reputation import UserReputation

print("------ [ INFO ] ------ Models Imported Successfully")
