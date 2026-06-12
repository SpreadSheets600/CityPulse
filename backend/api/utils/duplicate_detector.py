"""
Duplicate Detection for issues using text similarity.
Identifies similar/reported issues to prevent duplicate reporting.
"""

import re
from typing import List, Tuple, Optional
from sqlalchemy import or_


def preprocess_text(text: str) -> set:
    """
    Preprocess text for similarity comparison.
    Returns a set of significant words.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'shall', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'what', 'which', 'who', 'whom', 'where', 'when', 'why', 'how',
        'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
        'some', 'such', 'no', 'not', 'only', 'same', 'so', 'than', 'too',
        'very', 'just', 'about', 'above', 'after', 'again', 'against',
        'as', 'before', 'below', 'between', 'into', 'through', 'during',
        'out', 'off', 'over', 'under', 'further', 'then', 'once', 'here',
        'there', 'when', 'where', 'why', 'how', 'any', 'if', 'nor', 'own'
    }
    
    return {w for w in words if w not in stop_words and len(w) > 2}


def jaccard_similarity(set1: set, set2: set) -> float:
    """Calculate Jaccard similarity between two sets."""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0


def cosine_similarity(set1: set, set2: set) -> float:
    """Calculate simplified cosine similarity using set overlap."""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    magnitude = (len(set1) * len(set2)) ** 0.5
    return intersection / magnitude if magnitude > 0 else 0.0


def find_duplicate_candidates(
    db_session,
    issue_model,
    title: str,
    description: str,
    latitude: float = None,
    longitude: float = None,
    exclude_id: int = None,
    threshold: float = 0.3,
    max_results: int = 5
) -> List[dict]:
    """
    Find potential duplicate issues based on text similarity and location.
    
    Args:
        db_session: SQLAlchemy session
        issue_model: Issue model class
        title: New issue title
        description: New issue description
        latitude: New issue latitude (optional, for location-based matching)
        longitude: New issue longitude (optional)
        exclude_id: Issue ID to exclude from results (for updates)
        threshold: Minimum similarity threshold (0-1)
        max_results: Maximum number of results to return
    
    Returns:
        List of dicts with issue details and similarity scores
    """
    new_text = preprocess_text(f"{title} {description}")
    
    # Query recent issues (last 30 days)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    query = issue_model.query.filter(
        issue_model.created_at >= thirty_days_ago
    )
    
    if exclude_id:
        query = query.filter(issue_model.id != exclude_id)
    
    issues = query.all()
    
    candidates = []
    
    for issue in issues:
        issue_text = preprocess_text(f"{issue.title} {issue.description}")
        
        # Calculate text similarity
        text_sim = max(
            jaccard_similarity(new_text, issue_text),
            cosine_similarity(new_text, issue_text)
        )
        
        # Location proximity bonus (if both have coordinates)
        location_bonus = 0.0
        if all([latitude, longitude, issue.latitude, issue.longitude]):
            lat_diff = abs(latitude - issue.latitude)
            lng_diff = abs(longitude - issue.longitude)
            # Rough approximation: ~111km per degree
            distance_km = ((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111
            
            if distance_km < 0.5:  # Within 500m
                location_bonus = 0.3
            elif distance_km < 1.0:  # Within 1km
                location_bonus = 0.2
            elif distance_km < 2.0:  # Within 2km
                location_bonus = 0.1
        
        total_similarity = min(text_sim + location_bonus, 1.0)
        
        if total_similarity >= threshold:
            candidates.append({
                "id": issue.id,
                "title": issue.title,
                "description": issue.description,
                "status": issue.status.value if hasattr(issue.status, 'value') else issue.status,
                "created_at": issue.created_at.isoformat() if issue.created_at else None,
                "latitude": issue.latitude,
                "longitude": issue.longitude,
                "similarity": round(total_similarity, 3),
                "text_similarity": round(text_sim, 3),
                "location_bonus": round(location_bonus, 3),
                "upvotes": len(issue.upvotes) if issue.upvotes else 0
            })
    
    # Sort by similarity (highest first)
    candidates.sort(key=lambda x: x["similarity"], reverse=True)
    
    return candidates[:max_results]


def is_likely_duplicate(
    db_session,
    issue_model,
    title: str,
    description: str,
    latitude: float = None,
    longitude: float = None,
    threshold: float = 0.6
) -> Tuple[bool, Optional[dict]]:
    """
    Quick check if an issue is likely a duplicate.
    
    Returns:
        Tuple of (is_duplicate, best_match)
    """
    candidates = find_duplicate_candidates(
        db_session,
        issue_model,
        title,
        description,
        latitude,
        longitude,
        threshold=threshold,
        max_results=1
    )
    
    if candidates and candidates[0]["similarity"] >= threshold:
        return True, candidates[0]
    
    return False, None
