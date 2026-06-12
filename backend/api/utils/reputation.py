"""
User reputation management system.

Tracks user contributions, awards points, and manages trust levels.
"""

from datetime import datetime
from typing import Optional


POINTS = {
    "issue_reported": 10,
    "issue_verified": 25,
    "issue_resolved": 15,
    "upvote_received": 2,
    "image_mismatch_penalty": -50,
}

FLAG_THRESHOLD = 3


def get_or_create_reputation(user_id, db):
    from ..models.user_reputation import UserReputation

    rep = UserReputation.query.filter_by(user_id=user_id).first()
    if not rep:
        rep = UserReputation(user_id=user_id)
        db.session.add(rep)
        db.session.commit()
    return rep


def award_points(user_id, action: str, db, points: Optional[int] = None) -> dict:
    """
    Award points to a user for a specific action.

    Returns:
        dict with keys: success, points_awarded, new_total, trust_level
    """
    rep = get_or_create_reputation(user_id, db)

    if points is None:
        points = POINTS.get(action, 0)

    if points == 0:
        return {"success": False, "points_awarded": 0, "new_total": rep.total_points, "trust_level": rep.trust_level}

    if action == "issue_reported":
        rep.issues_reported += 1
    elif action == "issue_verified":
        rep.issues_verified += 1
    elif action == "issue_resolved":
        rep.issues_resolved += 1
    elif action == "upvote_received":
        rep.upvotes_received += 1
    elif action.startswith("penalty"):
        rep.penalties += abs(points)
        points = abs(points) * -1

    rep.total_points = max(0, rep.total_points + points)
    rep.calculate_trust_level()
    rep.updated_at = datetime.utcnow()

    db.session.commit()

    return {
        "success": True,
        "points_awarded": points,
        "new_total": rep.total_points,
        "trust_level": rep.trust_level,
    }


def flag_user(user, reason: str, db) -> bool:
    """
    Flag a user for suspicious activity.

    Auto-suspends at 3 flags and notifies admin.
    """
    from ..utils.email import send_flag_notification

    rep = get_or_create_reputation(user.id, db)

    rep.flag_count += 1
    rep.is_flagged = True
    rep.flag_reason = reason

    award_points(user.id, "penalty_image_mismatch", db, POINTS["image_mismatch_penalty"])

    if rep.flag_count >= FLAG_THRESHOLD:
        rep.is_suspended = True
        send_flag_notification(user, rep, reason, db)

    db.session.commit()
    return True


def unreputation_user(user_id: int, admin_id: int, reason: str, db) -> dict:
    """
    Revert a user flag/suspension (admin action).
    """
    from ..models.audit_log import AuditLog

    rep = get_or_create_reputation(user_id, db)

    was_suspended = rep.is_suspended
    rep.is_suspended = False
    rep.is_flagged = rep.flag_count > 1
    rep.flag_reason = None if rep.flag_count <= 1 else rep.flag_reason

    log = AuditLog(
        admin_id=admin_id,
        action="unflag_user",
        target_type="user",
        target_id=user_id,
        details=f"Reason: {reason}. Was suspended: {was_suspended}",
    )
    db.session.add(log)
    db.session.commit()

    return {
        "success": True,
        "was_suspended": was_suspended,
        "flag_count": rep.flag_count,
        "is_suspended": rep.is_suspended,
    }


def get_user_reputation(user_id: int) -> dict:
    """Get reputation for a user."""
    from ..models.user_reputation import UserReputation

    rep = UserReputation.query.filter_by(user_id=user_id).first()
    if not rep:
        return {
            "total_points": 0,
            "trust_level": "newcomer",
            "issues_reported": 0,
            "issues_verified": 0,
            "issues_resolved": 0,
            "upvotes_received": 0,
            "is_flagged": False,
            "is_suspended": False,
        }
    return rep.to_dict()
