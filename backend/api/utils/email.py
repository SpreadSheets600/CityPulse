import os
from flask_mail import Mail, Message

mail = Mail()


def init_mail(app):
    if not os.getenv("EMAIL_ENABLED", "false").lower() in ("true", "1", "yes"):
        print("------ [ INFO ] ------ Email disabled (EMAIL_ENABLED=false)")
        return
    mail.init_app(app)


def send_status_notification(user, issue, new_status):
    if not mail.app:
        return
    if not os.getenv("EMAIL_ENABLED", "false").lower() in ("true", "1", "yes"):
        return

    status_labels = {
        "pending": "Pending",
        "in_progress": "In Progress",
        "resolved": "Resolved",
        "rejected": "Rejected",
        "verified": "Verified",
    }

    subject = f"Issue #{issue.id} Status Update: {status_labels.get(new_status, new_status)}"
    body = (
        f"Hello {user.firstname},\n\n"
        f"Your issue \"{issue.title}\" (#{issue.id}) has been updated.\n\n"
        f"New Status: {status_labels.get(new_status, new_status)}\n\n"
        f"Thank you,\nCityPulse Team"
    )

    try:
        msg = Message(subject=subject, recipients=[user.email], body=body)
        mail.send(msg)
    except Exception as e:
        print(f"------ [ WARN ] ------ Failed to send email: {e}")


def send_flag_notification(user, reputation, reason, db):
    """Notify admin when a user is auto-suspended after 3 flags."""
    if not mail.app:
        return
    if not os.getenv("EMAIL_ENABLED", "false").lower() in ("true", "1", "yes"):
        return

    from ..models.user import User, UserRole
    admins = User.query.filter_by(role=UserRole.admin).all()
    admin_emails = [a.email for a in admins]

    if not admin_emails:
        return

    subject = f"User Suspended: {user.firstname} {user.lastname} (Flag #{reputation.flag_count})"
    body = (
        f"Hello Admin,\n\n"
        f"User {user.firstname} {user.lastname} ({user.email}) has been automatically suspended.\n\n"
        f"Reason: {reason}\n"
        f"Total Flags: {reputation.flag_count}\n"
        f"Total Points: {reputation.total_points}\n\n"
        f"Please review this user's account.\n\n"
        f"Thank you,\nCityPulse System"
    )

    try:
        msg = Message(subject=subject, recipients=admin_emails, body=body)
        mail.send(msg)
    except Exception as e:
        print(f"------ [ WARN ] ------ Failed to send flag notification: {e}")
