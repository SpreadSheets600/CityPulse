"""
Unified AI Pipeline for CityPulse.

Orchestrates all AI subsystems in a single pipeline:
1. Image classification (vision LLM)
2. Text classification (text LLM)
3. Keyword classification (fallback)
4. Priority scoring
5. Duplicate detection
6. Image verification (vision LLM)
7. Department auto-routing

Results are stored as a single ai_analysis JSON blob on the Issue model,
providing a consistent view for both citizens and admins.
"""

import os
from datetime import datetime


def _is_enabled(flag_name: str) -> bool:
    return os.getenv(flag_name, "false").lower() in ("true", "1", "yes")


def run_pipeline(issue, image_files=None, db_session=None):
    """Run the full AI pipeline on an issue.

    Args:
        issue: Issue model instance (must have title, description, image_urls, latitude, longitude)
        image_files: List of uploaded file objects (for initial classification/verification).
                     If None, images are fetched from S3 (for re-runs).
        db_session: SQLAlchemy session for duplicate detection.

    Returns:
        dict: Complete ai_analysis result stored on issue.ai_analysis.
    """
    classification = _run_classification(issue, image_files)
    priority = _run_priority(issue)
    duplicates = _run_duplicates(issue, db_session)
    verification = _run_verification(issue, image_files)

    department = _resolve_department(issue, classification)

    result = {
        "classification": classification,
        "priority": priority,
        "verification": verification,
        "department": department,
        "duplicates": duplicates,
        "processed_at": datetime.utcnow().isoformat(),
    }

    issue.ai_analysis = result
    issue.issue_type = classification.get("category", issue.issue_type)

    if department.get("department_id") and not issue.department_id:
        issue.department_id = department["department_id"]

    return result


def _run_classification(issue, image_files=None):
    """Run the 3-tier classification cascade.

    Priority: Image classifier > Text LLM > Keyword fallback.
    """
    img_cls_enabled = _is_enabled("IMAGE_CLASSIFICATION_ENABLED")
    ai_text_enabled = _is_enabled("AI_TEXT_ENABLED")

    # Tier 1: Image classification
    if img_cls_enabled and image_files:
        try:
            from .image_classifier import classify_image_from_bytes
            files_with_content = []
            for f in image_files:
                f.seek(0)
                content = f.read()
                f.seek(0)
                files_with_content.append((content, f.filename or "image.jpg"))

            best = {"category": "Unspecified", "confidence": 0.0}
            all_detections = []

            for content, filename in files_with_content:
                result = classify_image_from_bytes(content, filename)
                all_detections.extend(result.get("detections", []))
                if result["confidence"] > best["confidence"]:
                    best = result

            if best["confidence"] > 0.3 and best["category"] != "Unspecified":
                return {
                    "source": "image",
                    "category": best["category"],
                    "confidence": best["confidence"],
                    "reasoning": f"Vision model detected {best['category']} with {best['confidence']:.0%} confidence",
                    "detections": all_detections,
                }
        except Exception as e:
            print(f"------ [ WARN ] ------ Image classification failed: {e}")

    # Tier 2: Text LLM classification
    if ai_text_enabled:
        try:
            from .ai_client import classify_issue_text
            result = classify_issue_text(issue.title, issue.description)
            if result["confidence"] > 0.3 and result["category"]:
                return {
                    "source": "text",
                    "category": result["category"],
                    "confidence": result["confidence"],
                    "reasoning": result.get("reasoning", ""),
                    "detections": [],
                }
        except Exception as e:
            print(f"------ [ WARN ] ------ Text classification failed: {e}")

    # Tier 3: Keyword fallback
    try:
        from .classifier import classify_issue
        category, confidence, dept = classify_issue(issue.title, issue.description)
        if confidence > 0.3:
            return {
                "source": "keyword",
                "category": category,
                "confidence": confidence,
                "reasoning": f"Keyword-based classification (confidence: {confidence:.0%})",
                "detections": [],
            }
    except Exception as e:
        print(f"------ [ WARN ] ------ Keyword classification failed: {e}")

    return {
        "source": "none",
        "category": "Unspecified",
        "confidence": 0.0,
        "reasoning": "All classification methods unavailable",
        "detections": [],
    }


def _run_priority(issue):
    """Run priority scoring with AI fallback to heuristic."""
    ai_text_enabled = _is_enabled("AI_TEXT_ENABLED")

    upvote_count = len(issue.upvotes) if issue.upvotes else 0

    # Try AI priority first
    if ai_text_enabled:
        try:
            from .ai_client import assess_priority
            result = assess_priority(
                issue.title, issue.description, issue.issue_type, upvote_count
            )
            if result["level"] and result["score"]:
                return {
                    "level": result["level"],
                    "score": result["score"],
                    "reasoning": result.get("reasoning", ""),
                    "source": "ai",
                }
        except Exception as e:
            print(f"------ [ WARN ] ------ AI priority failed: {e}")

    # Heuristic fallback
    try:
        from .priority_scorer import calculate_priority_score
        level, score, breakdown = calculate_priority_score(
            issue_type=issue.issue_type,
            title=issue.title,
            description=issue.description,
            upvote_count=upvote_count,
            comment_count=0,
            created_at=issue.created_at,
            status=issue.status.value if issue.status else "pending",
            has_images=bool(issue.image_urls),
        )
        return {
            "level": level,
            "score": score,
            "reasoning": f"Heuristic scoring: {breakdown}",
            "source": "heuristic",
            "breakdown": breakdown,
        }
    except Exception as e:
        print(f"------ [ WARN ] ------ Heuristic priority failed: {e}")
        return {"level": "medium", "score": 50, "reasoning": "Priority scoring unavailable", "source": "fallback"}


def _run_duplicates(issue, db_session):
    """Run duplicate detection."""
    if not db_session:
        return []

    try:
        from .duplicate_detector import find_duplicate_candidates
        from ..models import Issue
        return find_duplicate_candidates(
            db_session,
            Issue,
            issue.title,
            issue.description,
            issue.latitude,
            issue.longitude,
            threshold=0.4,
            max_results=3,
        )
    except Exception as e:
        print(f"------ [ WARN ] ------ Duplicate detection failed: {e}")
        return []


def _run_verification(issue, image_files=None):
    """Run image verification.

    If image_files are provided (initial upload), verify from bytes.
    Otherwise, download from S3 and verify.
    """
    img_cls_enabled = _is_enabled("IMAGE_CLASSIFICATION_ENABLED")
    if not img_cls_enabled:
        return {"status": "skipped", "reasoning": "Image verification disabled"}

    try:
        from .image_verifier import verify_image_from_bytes, should_flag_user
        import requests as http_requests

        all_results = []
        overall_valid = True
        overall_confidence = 0.0
        all_mismatch_flags = []

        if image_files:
            for idx, f in enumerate(image_files):
                try:
                    f.seek(0)
                    img_bytes = f.read()
                    result = verify_image_from_bytes(
                        image_bytes=img_bytes,
                        filename=f.filename or f"image_{idx}.jpg",
                        issue_title=issue.title,
                        issue_description=issue.description,
                        issue_type=issue.issue_type,
                    )
                    all_results.append(result)
                    if not result["is_valid"]:
                        overall_valid = False
                    overall_confidence = max(overall_confidence, result["confidence"])
                    all_mismatch_flags.extend(result["mismatch_flags"])
                except Exception as e:
                    print(f"------ [ WARN ] ------ Verify image {idx} failed: {e}")
        elif issue.image_urls:
            from flask import current_app
            from .s3 import resolve_media_urls
            s3_config = current_app.config.get("S3_CONFIG", {})
            fresh_urls = resolve_media_urls(issue.image_urls, s3_config) if s3_config.get("endpoint_url") else issue.image_urls

            for idx, url in enumerate(fresh_urls):
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
                    all_results.append(result)
                    if not result["is_valid"]:
                        overall_valid = False
                    overall_confidence = max(overall_confidence, result["confidence"])
                    all_mismatch_flags.extend(result["mismatch_flags"])
                except Exception as e:
                    print(f"------ [ WARN ] ------ Verify image {idx} failed: {e}")

        if not all_results:
            return {"status": "no_images", "reasoning": "No images to verify"}

        if overall_valid and overall_confidence > 0.3:
            status = "verified"
            reasoning = "AI verification passed. Images match the reported issue."
        elif not overall_valid and overall_confidence > 0.7:
            status = "rejected"
            reasoning = "AI verification failed. Images do not match the reported issue."
        else:
            status = "pending"
            reasoning = "AI verification inconclusive. Manual review recommended."

        user_should_flag = any(should_flag_user(r) for r in all_results)

        return {
            "status": status,
            "confidence": overall_confidence,
            "reasoning": reasoning,
            "is_consistent": overall_valid,
            "mismatch_flags": all_mismatch_flags,
            "image_count": len(all_results),
            "user_should_flag": user_should_flag,
        }
    except Exception as e:
        print(f"------ [ WARN ] ------ Image verification failed: {e}")
        return {"status": "error", "reasoning": f"Verification error: {str(e)}"}


def _resolve_department(issue, classification):
    """Auto-route to department based on classification."""
    category = classification.get("category", "Unspecified")
    confidence = classification.get("confidence", 0.0)

    if confidence < 0.3 or category == "Unspecified":
        return {"auto_assigned": False, "department_id": None, "department_name": None}

    try:
        from ..models import Department
        dept = Department.query.filter_by(name=category).first()
        if dept:
            return {
                "auto_assigned": True,
                "department_id": dept.id,
                "department_name": dept.name,
            }
    except Exception as e:
        print(f"------ [ WARN ] ------ Department routing failed: {e}")

    return {"auto_assigned": False, "department_id": None, "department_name": None}
