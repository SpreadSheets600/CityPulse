# CityPulse - Implementation Plan

## Confirmed Requirements

| Requirement | Decision |
|-------------|----------|
| Image verification threshold | 70% AI confidence triggers user flag |
| Reputation points | +10 report, +25 verified, +15 resolved, +2 upvote, -50 mismatch |
| Account suspension | Auto-suspend at 3 flags + admin notification + revert capability |
| Ollama model | `gemma4:31b-cloud` for ALL AI (chatbot, classification, verification) |
| Geocoding | No caching, use browser geolocation coordinates directly |

---

## PHASE 1: Critical Bug Fixes

### 1.1 Fix Password Validation (`backend/api/routes/auth.py`)

**Current (Broken):**
```python
if (
    data.get("password")
    and len(data["password"]) < 8
    and ascii_letters not in data["password"]
    and digits not in data["password"]
):
```

**Fixed:**
```python
if (
    data.get("password")
    and (len(data["password"]) < 8
    or ascii_letters not in data["password"]
    or digits not in data["password"])
):
```

### 1.2 Fix Registration Response (`backend/api/routes/auth.py`)

**Current:**
```python
return {"message": "User Registered Successfully"}, 201
```

**Fixed:**
```python
access_token = create_access_token(identity=str(user.id))
refresh_token = create_refresh_token(identity=str(user.id))
return {
    "message": "User Registered Successfully",
    "access_token": access_token,
    "refresh_token": refresh_token,
    "user": user.to_dict(),
}, 201
```

### 1.3 Remove Hardcoded Secrets (`backend/config.py`)

**Current:**
```python
SECRET_KEY = os.getenv("SECRET_KEY", "SuperSuperDuperSecretKey")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "AnotherSuperDuperSecretKey")
```

**Fixed:**
```python
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY or not JWT_SECRET_KEY:
    raise ValueError("SECRET_KEY and JWT_SECRET_KEY must be set in environment variables")
```

### 1.4 Fix Frontend Axios BaseURL (`frontend/src/api/client.js`)

**Current:**
```javascript
baseURL: 'http://localhost:5000'
```

**Fixed:**
```javascript
baseURL: '/api'
```

---

## PHASE 2: Image Verification System

### 2.1 New Model: Enhanced VerificationStatus

**File: `backend/api/models/verification.py`**

```python
import enum
from . import db


class VerificationState(enum.Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"


class VerificationStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"), nullable=False)
    status = db.Column(
        db.Enum(VerificationState), default=VerificationState.pending, nullable=False
    )
    
    verified_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    
    notes = db.Column(db.Text, nullable=True)
    
    # NEW FIELDS
    ai_confidence = db.Column(db.Float, nullable=True)  # 0.0 - 1.0
    ai_reasoning = db.Column(db.Text, nullable=True)
    is_consistent = db.Column(db.Boolean, nullable=True)  # Image matches issue
    detected_objects = db.Column(db.JSON, nullable=True)  # What AI saw in image
    mismatch_flags = db.Column(db.JSON, nullable=True)  # Specific mismatches

    def __repr__(self):
        return f"<Verification Issue ID: {self.issue_id} - Status: {self.status.value}>"

    def to_dict(self):
        return {
            "id": self.id,
            "issue_id": self.issue_id,
            "status": self.status.value,
            "verified_by": self.verified_by,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "notes": self.notes,
            "ai_confidence": self.ai_confidence,
            "ai_reasoning": self.ai_reasoning,
            "is_consistent": self.is_consistent,
            "detected_objects": self.detected_objects,
            "mismatch_flags": self.mismatch_flags,
        }
```

### 2.2 New Utility: Image Verifier

**File: `backend/api/utils/image_verifier.py`**

```python
"""
Image verification using Ollama Gemma 4 Cloud model.

Verifies that uploaded images actually match the described civic issue.
Detects fake/misleading images and flags users accordingly.
"""

import base64
import os
import tempfile
from typing import Dict, List, Optional


_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client

    try:
        import ollama
        base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        _client = ollama.Client(host=base_url)
        return _client
    except Exception as e:
        print(f"------ [ ERROR ] ------ Failed to init Ollama client: {e}")
        return None


def _get_model() -> str:
    return os.getenv("OLLAMA_VISION_MODEL", "gemma4:31b-cloud")


def _image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def verify_image_matches_issue(
    image_path: str,
    issue_title: str,
    issue_description: str,
    issue_type: str,
) -> Dict:
    """
    Verify that an image actually shows the described civic issue.
    
    Uses Gemma 4 Cloud to analyze the image and compare it against
    the issue details provided by the user.
    
    Returns:
        Dict with keys:
            - is_valid (bool): Whether image matches issue
            - confidence (float): 0.0 - 1.0 confidence score
            - reasoning (str): AI explanation
            - detected_objects (list): What AI sees in image
            - mismatch_flags (list): Specific issues found
    """
    client = _get_client()
    if client is None:
        return {
            "is_valid": True,  # Fail open if AI unavailable
            "confidence": 0.0,
            "reasoning": "AI verification unavailable",
            "detected_objects": [],
            "mismatch_flags": [],
        }

    model = _get_model()
    img_b64 = _image_to_base64(image_path)

    prompt = f"""You are a civic issue verification expert. Analyze this image and determine if it actually shows the reported issue.

REPORTED ISSUE:
- Type: {issue_type}
- Title: {issue_title}
- Description: {issue_description}

TASK:
1. What do you actually see in this image? List all visible objects/scenes.
2. Does this image show a {issue_type} issue?
3. Is the image consistent with the title and description?
4. Are there any red flags (e.g., stock photo, unrelated image, manipulated image)?

RESPOND WITH ONLY A JSON OBJECT (no markdown, no explanation):
{{
    "is_valid": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "one line explanation",
    "detected_objects": ["object1", "object2", ...],
    "mismatch_flags": ["flag1", "flag2", ...] or []
}}

EXAMPLES OF MISMATCH FLAGS:
- "Image shows indoor scene, not outdoor infrastructure"
- "No visible road/pavement damage detected"
- "Image appears to be a stock photo"
- "Image quality too low to verify"
- "Image shows different location type than described"
- "No evidence of water leak or damage"
- "Image appears manipulated or edited"
"""

    try:
        response = client.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [img_b64],
                }
            ],
            options={"temperature": 0.1},
        )
        text = response["message"]["content"].strip()

        # Parse JSON response
        import json
        
        # Handle markdown code blocks
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        result = json.loads(text)
        
        return {
            "is_valid": bool(result.get("is_valid", True)),
            "confidence": float(result.get("confidence", 0.5)),
            "reasoning": str(result.get("reasoning", "")),
            "detected_objects": list(result.get("detected_objects", [])),
            "mismatch_flags": list(result.get("mismatch_flags", [])),
        }

    except Exception as e:
        print(f"------ [ WARN ] ------ Image verification failed: {e}")
        return {
            "is_valid": True,  # Fail open
            "confidence": 0.0,
            "reasoning": f"Verification error: {str(e)}",
            "detected_objects": [],
            "mismatch_flags": [],
        }


def verify_image_from_bytes(
    image_bytes: bytes,
    filename: str = "image.jpg",
    issue_title: str = "",
    issue_description: str = "",
    issue_type: str = "",
) -> Dict:
    """Verify an image from raw bytes."""
    suffix = os.path.splitext(filename)[1] or ".jpg"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    try:
        return verify_image_matches_issue(
            tmp_path, issue_title, issue_description, issue_type
        )
    finally:
        os.unlink(tmp_path)


def should_flag_user(verification_result: Dict) -> bool:
    """
    Determine if a user should be flagged based on verification result.
    
    Flags user if:
    - AI confidence > 0.7 that image doesn't match
    - Multiple mismatch flags detected
    """
    if verification_result["is_valid"]:
        return False
    
    confidence = verification_result["confidence"]
    mismatch_count = len(verification_result["mismatch_flags"])
    
    # Flag if high confidence mismatch or multiple flags
    return confidence >= 0.7 or mismatch_count >= 2
```

### 2.3 Enhanced Admin Verification Endpoint

**File: `backend/api/routes/admin.py` - Modify `VerifyIssue` class**

```python
class VerifyIssue(Resource):
    @jwt_required()
    def post(self, issue_id):
        """Run AI image verification on an issue's images."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        issue = Issue.query.get(issue_id)
        if not issue:
            return {"error": "Issue Not Found"}, 404

        if not issue.image_urls:
            return {"error": "No images to verify"}, 400

        import os
        img_cls_enabled = os.getenv("IMAGE_CLASSIFICATION_ENABLED", "false").lower() in ("true", "1", "yes")
        if not img_cls_enabled:
            return {"error": "Image classification is disabled"}, 501

        try:
            from ..utils.image_verifier import verify_image_from_bytes, should_flag_user
            import requests as http_requests
            from datetime import datetime

            all_verifications = []
            overall_valid = True
            overall_confidence = 0.0
            all_mismatch_flags = []
            user_should_be_flagged = False

            for idx, url in enumerate(issue.image_urls):
                try:
                    resp = http_requests.get(url, timeout=30)
                    resp.raise_for_status()
                    
                    result = verify_image_from_bytes(
                        image_bytes=resp.content,
                        filename=f"image_{idx}.jpg",
                        issue_title=issue.title,
                        issue_description=issue.description,
                        issue_type=issue.issue_type,
                    )
                    
                    all_verifications.append({
                        "image_index": idx,
                        "url": url,
                        "is_valid": result["is_valid"],
                        "confidence": result["confidence"],
                        "reasoning": result["reasoning"],
                        "detected_objects": result["detected_objects"],
                        "mismatch_flags": result["mismatch_flags"],
                    })
                    
                    if not result["is_valid"]:
                        overall_valid = False
                    overall_confidence = max(overall_confidence, result["confidence"])
                    all_mismatch_flags.extend(result["mismatch_flags"])
                    
                    if should_flag_user(result):
                        user_should_be_flagged = True

                except Exception as e:
                    all_verifications.append({
                        "image_index": idx,
                        "url": url,
                        "is_valid": True,
                        "confidence": 0.0,
                        "reasoning": f"Error: {str(e)}",
                        "detected_objects": [],
                        "mismatch_flags": [],
                    })

            # Determine verification status
            if overall_valid and overall_confidence > 0.3:
                state = VerificationState.verified
                verification_message = "AI verification passed. Images match the reported issue."
            elif not overall_valid and overall_confidence > 0.7:
                state = VerificationState.rejected
                verification_message = "AI verification failed. Images do not match the reported issue."
            else:
                state = VerificationState.pending
                verification_message = "AI verification inconclusive. Manual review recommended."

            # Upsert verification record
            existing_v = VerificationStatus.query.filter_by(issue_id=issue_id).first()
            if existing_v:
                existing_v.status = state
                existing_v.verified_by = user_id
                existing_v.verified_at = datetime.utcnow()
                existing_v.ai_confidence = overall_confidence
                existing_v.ai_reasoning = verification_message
                existing_v.is_consistent = overall_valid
                existing_v.detected_objects = all_verifications[0].get("detected_objects", []) if all_verifications else []
                existing_v.mismatch_flags = all_mismatch_flags
            else:
                v = VerificationStatus(
                    issue_id=issue_id,
                    status=state,
                    verified_by=user_id,
                    verified_at=datetime.utcnow(),
                    ai_confidence=overall_confidence,
                    ai_reasoning=verification_message,
                    is_consistent=overall_valid,
                    detected_objects=all_verifications[0].get("detected_objects", []) if all_verifications else [],
                    mismatch_flags=all_mismatch_flags,
                )
                db.session.add(v)
            
            db.session.commit()

            # Flag user if needed
            user_flagged = False
            if user_should_be_flagged:
                from ..utils.reputation import flag_user
                citizen = User.query.get(issue.citizen_id)
                if citizen:
                    user_flagged = flag_user(citizen, "AI detected image mismatch", db)

            return {
                "verification": {
                    "status": state.value,
                    "message": verification_message,
                    "ai_confidence": overall_confidence,
                    "is_consistent": overall_valid,
                    "mismatch_flags": all_mismatch_flags,
                },
                "detections": all_verifications,
                "user_flagged": user_flagged,
            }, 200

        except Exception as e:
            return {"error": f"Verification failed: {str(e)}"}, 500
```

---

## PHASE 3: User Reputation System

### 3.1 New Model: UserReputation

**File: `backend/api/models/user_reputation.py`**

```python
from . import db


class UserReputation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    user = db.relationship("User", backref="reputation")
    
    # Points breakdown
    issues_reported = db.Column(db.Integer, default=0)
    issues_verified = db.Column(db.Integer, default=0)  # Issue confirmed real
    issues_resolved = db.Column(db.Integer, default=0)  # Issue fixed
    upvotes_received = db.Column(db.Integer, default=0)
    penalties = db.Column(db.Integer, default=0)  # Negative points
    
    # Total score
    total_points = db.Column(db.Integer, default=0)
    
    # Trust level
    trust_level = db.Column(db.String(20), default="newcomer")
    # Levels: newcomer(0-50), contributor(51-200), trusted(201-500), expert(501+)
    
    # Flags
    is_flagged = db.Column(db.Boolean, default=False)
    flag_reason = db.Column(db.String(200), nullable=True)
    flag_count = db.Column(db.Integer, default=0)
    is_suspended = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<UserReputation User ID: {self.user_id} - Points: {self.total_points}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "issues_reported": self.issues_reported,
            "issues_verified": self.issues_verified,
            "issues_resolved": self.issues_resolved,
            "upvotes_received": self.upvotes_received,
            "penalties": self.penalties,
            "total_points": self.total_points,
            "trust_level": self.trust_level,
            "is_flagged": self.is_flagged,
            "flag_reason": self.flag_reason,
            "flag_count": self.flag_count,
            "is_suspended": self.is_suspended,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def calculate_trust_level(self):
        """Update trust level based on total points."""
        if self.total_points >= 501:
            self.trust_level = "expert"
        elif self.total_points >= 201:
            self.trust_level = "trusted"
        elif self.total_points >= 51:
            self.trust_level = "contributor"
        else:
            self.trust_level = "newcomer"
```

### 3.2 Update User Model

**File: `backend/api/models/user.py` - Add relationship**

```python
# Add after line 29
reputation = db.relationship("UserReputation", backref="user", uselist=False, lazy=True)
```

### 3.3 New Utility: Reputation Manager

**File: `backend/api/utils/reputation.py`**

```python
"""
User reputation management system.

Tracks user contributions, awards points, and manages trust levels.
"""

from datetime import datetime
from typing import Optional


# Points configuration
POINTS = {
    "issue_reported": 10,
    "issue_verified": 25,
    "issue_resolved": 15,
    "upvote_received": 2,
    "image_mismatch_penalty": -50,
}

# Suspension threshold
FLAG_THRESHOLD = 3


def get_or_create_reputation(user_id, db):
    """Get or create reputation record for a user."""
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
    
    # Update breakdown
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
        points = abs(points) * -1  # Ensure negative
    
    # Update total
    rep.total_points = max(0, rep.total_points + points)  # Never go below 0
    
    # Recalculate trust level
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
    Returns True if user was flagged.
    """
    from ..models.user_reputation import UserReputation
    from ..utils.email import send_flag_notification
    
    rep = get_or_create_reputation(user.id, db)
    
    rep.flag_count += 1
    rep.is_flagged = True
    rep.flag_reason = reason
    
    # Award penalty points
    award_points(user.id, "penalty_image_mismatch", db, POINTS["image_mismatch_penalty"])
    
    # Auto-suspend at threshold
    if rep.flag_count >= FLAG_THRESHOLD:
        rep.is_suspended = True
        # Notify admin
        send_flag_notification(user, rep, reason, db)
    
    db.session.commit()
    return True


def unreputation_user(user_id: int, admin_id: int, reason: str, db) -> dict:
    """
    Revert a user flag/suspension (admin action).
    
    Returns:
        dict with success status
    """
    from ..models.user_reputation import UserReputation
    from ..models.audit_log import AuditLog
    
    rep = get_or_create_reputation(user_id, db)
    
    # Remove suspension if applicable
    was_suspended = rep.is_suspended
    rep.is_suspended = False
    rep.is_flagged = rep.flag_count > 1  # Still flagged if multiple flags
    rep.flag_reason = None if rep.flag_count <= 1 else rep.flag_reason
    
    # Log admin action
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
```

### 3.4 New Endpoint: User Reputation

**File: `backend/api/routes/users.py` (NEW FILE)**

```python
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api.models import db, User, UserRole
from ..utils.reputation import get_user_reputation


class GetUserReputation(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get reputation for a user."""
        reputation = get_user_reputation(user_id)
        return {"reputation": reputation}, 200


class GetMyReputation(Resource):
    @jwt_required()
    def get(self):
        """Get current user's reputation."""
        user_id = get_jwt_identity()
        reputation = get_user_reputation(user_id)
        return {"reputation": reputation}, 200
```

### 3.5 Update Issues Route for Reputation

**File: `backend/api/routes/issues.py` - Modify `ReportIssue.post()`**

Add after issue is created (around line 216):

```python
# Award points for reporting
from ..utils.reputation import award_points
award_points(user_id, "issue_reported", db)
```

### 3.6 Update Admin Route for Reputation

**File: `backend/api/routes/admin.py` - Modify `UpdateIssueStatus.put()`**

Add after status is updated to 'resolved' or 'verified':

```python
# Award points based on status change
from ..utils.reputation import award_points

if new_status == "verified":
    award_points(issue.citizen_id, "issue_verified", db)
elif new_status == "resolved":
    award_points(issue.citizen_id, "issue_resolved", db)
```

### 3.7 New Admin Endpoint: Flagged Users

**File: `backend/api/routes/admin.py` - Add new class**

```python
class GetFlaggedUsers(Resource):
    @jwt_required()
    def get(self):
        """List all flagged users."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        from ..models.user_reputation import UserReputation
        
        flagged = UserReputation.query.filter(
            UserReputation.is_flagged == True
        ).all()
        
        users_data = []
        for rep in flagged:
            u = User.query.get(rep.user_id)
            if u:
                users_data.append({
                    "user": {
                        "id": u.id,
                        "firstname": u.firstname,
                        "lastname": u.lastname,
                        "email": u.email,
                    },
                    "reputation": rep.to_dict(),
                })
        
        return {"flagged_users": users_data}, 200


class UnflagUser(Resource):
    @jwt_required()
    def post(self, user_id):
        """Remove flag/suspension from a user."""
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)
        if not admin or admin.role != UserRole.admin:
            return {"error": "Admin Access Required"}, 403

        from ..utils.reputation import unreputation_user
        
        data = request.get_json() or {}
        reason = data.get("reason", "Admin review cleared")
        
        result = unreputation_user(user_id, admin_id, reason, db)
        return result, 200
```

---

## PHASE 4: Register New Routes

### 4.1 Update Backend App Registration

**File: `backend/app.py` - Add new routes**

```python
# Add imports
from api.routes.users import GetUserReputation, GetMyReputation

# Add after existing route registrations
api.add_resource(GetUserReputation, "/api/users/<int:user_id>/reputation")
api.add_resource(GetMyReputation, "/api/users/me/reputation")

# Add to admin routes
api.add_resource(GetFlaggedUsers, "/api/admin/flagged-users")
api.add_resource(UnflagUser, "/api/admin/users/<int:user_id>/unflag")
```

### 4.2 Update Models Init

**File: `backend/api/models/__init__.py` - Add new model**

```python
from .user_reputation import UserReputation
```

---

## PHASE 5: Frontend Updates (Optional but Recommended)

### 5.1 Add Reputation Badge Component

**File: `frontend/src/components/ReputationBadge.vue`**

```vue
<template>
  <div class="badge gap-1" :class="badgeClass">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
      <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
    </svg>
    {{ trustLevel }}
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  trustLevel: { type: String, default: 'newcomer' },
  totalPoints: { type: Number, default: 0 }
})

const badgeClass = computed(() => {
  switch (props.trustLevel) {
    case 'expert': return 'badge-primary'
    case 'trusted': return 'badge-secondary'
    case 'contributor': return 'badge-accent'
    default: return 'badge-ghost'
  }
})
</script>
```

### 5.2 Update User Dashboard

Add reputation display to `User-Dashboard.vue`:

```vue
<!-- Add to template -->
<div class="stat">
  <div class="stat-title">Reputation</div>
  <div class="stat-value">{{ reputation.total_points }}</div>
  <div class="stat-desc">
    <ReputationBadge :trust-level="reputation.trust_level" :total-points="reputation.total_points" />
  </div>
</div>

<!-- Add script -->
<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api/client'
import ReputationBadge from '@/components/ReputationBadge.vue'

const reputation = ref({})

onMounted(async () => {
  try {
    const { data } = await api.get('/users/me/reputation')
    reputation.value = data.reputation
  } catch (e) {
    console.error('Failed to load reputation:', e)
  }
})
</script>
```

---

## Implementation Order

| Step | Task | Files Modified | Estimated Time |
|------|------|----------------|----------------|
| 1 | Fix password validation bug | `auth.py` | 5 min |
| 2 | Fix registration response | `auth.py` | 10 min |
| 3 | Remove hardcoded secrets | `config.py` | 5 min |
| 4 | Fix Axios baseURL | `client.js` | 5 min |
| 5 | Create enhanced VerificationStatus model | `verification.py` | 15 min |
| 6 | Create image_verifier.py | NEW FILE | 45 min |
| 7 | Update admin verification endpoint | `admin.py` | 30 min |
| 8 | Create UserReputation model | NEW FILE | 20 min |
| 9 | Update User model | `user.py` | 5 min |
| 10 | Create reputation.py utility | NEW FILE | 40 min |
| 11 | Create users.py routes | NEW FILE | 15 min |
| 12 | Update issues.py for reputation | `issues.py` | 10 min |
| 13 | Update admin.py for reputation | `admin.py` | 20 min |
| 14 | Register new routes | `app.py` | 10 min |
| 15 | Update models init | `__init__.py` | 5 min |
| 16 | Create ReputationBadge component | NEW FILE | 15 min |
| 17 | Update User Dashboard | `User-Dashboard.vue` | 20 min |
| 18 | Run database migrations | - | 10 min |
| 19 | Test all endpoints | - | 30 min |

**Total Estimated Time: ~5 hours**

---

## Database Migration

```sql
-- Run after implementation
flask db migrate -m "Add user_reputation and enhanced verification"
flask db upgrade
```

---

## New API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/:id/reputation` | Get user reputation |
| GET | `/api/users/me/reputation` | Get current user's reputation |
| GET | `/api/admin/flagged-users` | List all flagged users |
| POST | `/api/admin/users/:id/unflag` | Remove flag/suspension |

---

## Points System Summary

| Action | Points | Condition |
|--------|--------|-----------|
| Issue reported | +10 | Always |
| Issue verified (AI + manual) | +25 | Issue confirmed real |
| Issue resolved | +15 | Admin marks resolved |
| Upvote received | +2 | Per upvote |
| Image mismatch flagged | -50 | AI detects fake image |
| 3 flags | Account suspended | Auto-suspend + admin notification |

---

## Trust Levels Summary

| Level | Points Required | Benefits |
|-------|-----------------|----------|
| Newcomer | 0-50 | Basic access |
| Contributor | 51-200 | Can add comments |
| Trusted | 201-500 | Can upvote, priority display |
| Expert | 501+ | Can verify issues, badge |
