"""
Priority Scoring for issues.
Combines AI classification, community signals, and temporal factors.
"""

import math
from datetime import datetime, timedelta
from typing import Tuple


def calculate_priority_score(
    issue_type: str,
    title: str,
    description: str,
    upvote_count: int = 0,
    comment_count: int = 0,
    created_at: datetime = None,
    status: str = "pending",
    has_images: bool = False
) -> Tuple[str, float, dict]:
    """
    Calculate comprehensive priority score for an issue.
    
    Args:
        issue_type: Issue category
        title: Issue title
        description: Issue description
        upvote_count: Number of upvotes
        comment_count: Number of comments
        created_at: When the issue was created
        status: Current issue status
        has_images: Whether issue has images attached
    
    Returns:
        Tuple of (priority_level, priority_score, breakdown)
        priority_level: "critical", "high", "medium", "low"
        priority_score: 0-100 numeric score
        breakdown: Dict explaining score components
    """
    breakdown = {
        "text_urgency": 0.0,
        "community_engagement": 0.0,
        "age_factor": 0.0,
        "type_severity": 0.0,
        "evidence_bonus": 0.0,
        "total": 0.0
    }
    
    # 1. Text urgency analysis (0-30 points)
    text_urgency = _analyze_text_urgency(title, description)
    breakdown["text_urgency"] = text_urgency
    
    # 2. Community engagement (0-25 points)
    community_score = _calculate_community_score(upvote_count, comment_count)
    breakdown["community_engagement"] = community_score
    
    # 3. Age factor (0-20 points) - older unresolved issues get priority
    age_score = _calculate_age_score(created_at, status)
    breakdown["age_factor"] = age_score
    
    # 4. Issue type severity (0-15 points)
    type_score = _calculate_type_severity(issue_type)
    breakdown["type_severity"] = type_score
    
    # 5. Evidence bonus (0-10 points)
    evidence_score = 10.0 if has_images else 0.0
    breakdown["evidence_bonus"] = evidence_score
    
    # Total score
    total = text_urgency + community_score + age_score + type_score + evidence_score
    total = min(total, 100.0)
    breakdown["total"] = round(total, 2)
    
    # Determine level
    if total >= 70:
        level = "critical"
    elif total >= 50:
        level = "high"
    elif total >= 30:
        level = "medium"
    else:
        level = "low"
    
    return level, round(total, 2), breakdown


def _analyze_text_urgency(title: str, description: str) -> float:
    """Analyze text for urgency signals."""
    text = f"{title} {description}".lower()
    
    critical_keywords = [
        "danger", "dangerous", "hazard", "hazardous", "emergency", "urgent",
        "immediate", "life threatening", "risk", "severe", "extreme",
        "collapse", "fire", "flood", "explosion", "gas leak", "electrocution",
        "critical", "catastrophic", "fatal", "injury", "accident",
        "leak", "broken", "damaged", "failure", "outage", "blocked", "clogged"
    ]
    
    high_keywords = [
        "overflow", "leaking", "sparking", "down", "not working", "failed",
        "severe", "major", "significant", "extensive"
    ]
    
    medium_keywords = [
        "issue", "problem", "concern", "repair", "fix", "maintenance",
        "needed", "required", "reported", "complaint", "request"
    ]
    
    score = 0.0
    
    for keyword in critical_keywords:
        if keyword in text:
            score = 30.0
            break
    
    if score == 0:
        for keyword in high_keywords:
            if keyword in text:
                score = 20.0
                break
    
    if score == 0:
        for keyword in medium_keywords:
            if keyword in text:
                score = 10.0
                break
    
    return score


def _calculate_community_score(upvote_count: int, comment_count: int) -> float:
    """Calculate score based on community engagement."""
    # Upvotes: logarithmic scale, max 15 points
    upvote_score = 0.0
    if upvote_count > 0:
        upvote_score = min(math.log2(upvote_count + 1) * 3, 15.0)
    
    # Comments: linear scale, max 10 points
    comment_score = min(comment_count * 2, 10.0)
    
    return upvote_score + comment_score


def _calculate_age_score(created_at: datetime, status: str) -> float:
    """Calculate score based on issue age (older = higher priority)."""
    if not created_at:
        return 0.0
    
    # Already resolved issues don't need priority
    if status in ["resolved", "verified", "rejected"]:
        return 0.0
    
    age_hours = (datetime.utcnow() - created_at).total_seconds() / 3600
    
    # Exponential decay: issues older than 7 days get max score
    if age_hours >= 168:  # 7 days
        return 20.0
    elif age_hours >= 72:  # 3 days
        return 15.0
    elif age_hours >= 24:  # 1 day
        return 10.0
    elif age_hours >= 6:  # 6 hours
        return 5.0
    
    return 0.0


def _calculate_type_severity(issue_type: str) -> float:
    """Calculate score based on issue type severity."""
    type_scores = {
        "Road Maintenance": 12.0,
        "Electricity": 15.0,
        "Water Supply": 13.0,
        "Waste Management": 8.0,
        "Public Transportation": 7.0,
        "Unspecified": 5.0
    }
    
    return type_scores.get(issue_type, 5.0)


def update_priority_on_upvote(
    current_score: float,
    current_level: str,
    new_upvote_count: int
) -> Tuple[str, float]:
    """
    Update priority when an issue receives a new upvote.
    
    Returns:
        Tuple of (new_level, new_score)
    """
    # Simple recalculation based on new upvote count
    community_boost = min(math.log2(new_upvote_count + 1) * 2, 10.0)
    new_score = min(current_score + community_boost, 100.0)
    
    if new_score >= 70:
        level = "critical"
    elif new_score >= 50:
        level = "high"
    elif new_score >= 30:
        level = "medium"
    else:
        level = "low"
    
    return level, round(new_score, 2)


def get_priority_color(level: str) -> str:
    """Get UI color for priority level."""
    colors = {
        "critical": "#dc2626",  # Red
        "high": "#ea580c",      # Orange
        "medium": "#ca8a04",    # Yellow
        "low": "#16a34a"        # Green
    }
    return colors.get(level, "#6b7280")  # Gray default


def get_priority_label(level: str) -> str:
    """Get human-readable priority label."""
    labels = {
        "critical": "Critical",
        "high": "High",
        "medium": "Medium",
        "low": "Low"
    }
    return labels.get(level, "Unknown")
