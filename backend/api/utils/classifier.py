"""
AI Issue Classification using keyword-based rules.
Auto-categorizes issues based on title and description text.
"""

import re
from typing import Tuple

# Category definitions with keywords and weights
CATEGORIES = {
    "Road Maintenance": {
        "keywords": [
            "pothole",
            "road",
            "crack",
            "asphalt",
            "pavement",
            "sidewalk",
            "street",
            "highway",
            "bridge",
            "traffic light",
            "sign",
            "cone",
            "roadkill",
            "debris",
            "road damage",
            "road repair",
            "road work",
            "manhole",
            "drain",
            "gutter",
            "curb",
            "intersection",
        ],
        "weight": 1.0,
        "department": "Road Maintenance",
    },
    "Electricity": {
        "keywords": [
            "power",
            "electric",
            "electricity",
            "outage",
            "blackout",
            "wire",
            "cable",
            "transformer",
            "pole",
            "street light",
            "lamp",
            "light out",
            "voltage",
            "short circuit",
            "spark",
            "electrical",
            "power line",
            "substation",
            "meter",
            "breaker",
            "fuse",
        ],
        "weight": 1.0,
        "department": "Electricity",
    },
    "Water Supply": {
        "keywords": [
            "water",
            "pipe",
            "leak",
            "leakage",
            "burst",
            "flood",
            "drainage",
            "sewage",
            "toilet",
            "faucet",
            "tap",
            "hydrant",
            "water tank",
            "water supply",
            "water pressure",
            "contaminated",
            "dirty water",
            "waterlogging",
            "storm drain",
            "septic",
        ],
        "weight": 1.0,
        "department": "Water Supply",
    },
    "Waste Management": {
        "keywords": [
            "garbage",
            "trash",
            "waste",
            "rubbish",
            "litter",
            "dump",
            "recycling",
            "bin",
            "container",
            "collection",
            "pickup",
            "landfill",
            "compost",
            "organic",
            "plastic",
            "debris",
            "illegal dumping",
            "overflow",
            "smell",
            "odor",
            "vermin",
            "rats",
            "flies",
            "mosquito",
        ],
        "weight": 1.0,
        "department": "Waste Management",
    },
    "Public Transportation": {
        "keywords": [
            "bus",
            "train",
            "metro",
            "transit",
            "public transport",
            "stop",
            "station",
            "route",
            "schedule",
            "delay",
            "overcrowded",
            "broken",
            "vehicle",
            "driver",
            "fare",
            "ticket",
            "card",
            "accessibility",
            "wheelchair",
            "ramp",
            "bus stop",
            "shelter",
        ],
        "weight": 1.0,
        "department": "Public Transportation",
    },
}

# Priority keywords that escalate severity
URGENCY_KEYWORDS = {
    "critical": [
        "danger",
        "dangerous",
        "hazard",
        "hazardous",
        "emergency",
        "urgent",
        "immediate",
        "life threatening",
        "risk",
        "severe",
        "extreme",
        "collapse",
        "fire",
        "flood",
        "explosion",
        "gas leak",
        "electrocution",
    ],
    "high": [
        "broken",
        "damaged",
        "failure",
        "outage",
        "blocked",
        "clogged",
        "overflow",
        "leaking",
        "sparking",
        "down",
        "not working",
        "failed",
    ],
    "medium": [
        "issue",
        "problem",
        "concern",
        "repair",
        "fix",
        "maintenance",
        "needed",
        "required",
        "reported",
        "complaint",
    ],
}


def classify_issue(title: str, description: str) -> Tuple[str, float, str]:
    """
    Classify an issue based on its title and description.

    Returns:
        Tuple of (category, confidence, suggested_department)
    """
    text = f"{title} {description}".lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    scores = {}

    for category, config in CATEGORIES.items():
        score = 0
        matched_keywords = []

        for keyword in config["keywords"]:
            if keyword in text:
                # Weight by keyword specificity (longer = more specific)
                weight = len(keyword.split()) * 0.5 + 0.5
                score += weight
                matched_keywords.append(keyword)

        if score > 0:
            # Normalize by number of keywords in category
            scores[category] = {
                "score": score,
                "matched": matched_keywords,
                "department": config["department"],
            }

    if not scores:
        return "Unspecified", 0.0, None

    # Get best match
    best_category = max(scores.keys(), key=lambda k: scores[k]["score"])
    best_score = scores[best_category]["score"]

    # Calculate confidence (0-1 scale)
    confidence = min(best_score * 2, 1.0)

    return best_category, confidence, scores[best_category]["department"]


def get_priority_level(
    title: str, description: str, upvote_count: int = 0
) -> Tuple[str, float]:
    """
    Determine priority level based on text urgency signals and community upvotes.

    Returns:
        Tuple of (priority_level, priority_score)
        priority_level: "critical", "high", "medium", "low"
        priority_score: 0-100 numeric score
    """
    text = f"{title} {description}".lower()
    text = re.sub(r"[^\w\s]", " ", text)

    score = 0.0

    # Text-based urgency scoring
    for level, keywords in URGENCY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                if level == "critical":
                    score += 50
                elif level == "high":
                    score += 30
                elif level == "medium":
                    score += 15
                break

    # Upvote-based scoring (logarithmic scale)
    import math

    if upvote_count > 0:
        upvote_score = min(math.log2(upvote_count + 1) * 10, 30)
        score += upvote_score

    # Cap at 100
    score = min(score, 100)

    # Determine level
    if score >= 60:
        level = "critical"
    elif score >= 40:
        level = "high"
    elif score >= 20:
        level = "medium"
    else:
        level = "low"

    return level, score


def suggest_department(category: str, confidence: float) -> str:
    """
    Suggest a department based on issue category.

    Returns:
        Department name or None if confidence is too low
    """
    if confidence < 0.3:
        return None

    if category in CATEGORIES:
        return CATEGORIES[category]["department"]

    return None
