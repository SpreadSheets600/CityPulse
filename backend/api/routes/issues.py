from flask import Blueprint, request, jsonify, current_app as app

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from uuid import uuid4
from api.models import db, User, Issue
from ..utils.s3 import upload_file_to_s3, compress_image

issue_bp = Blueprint("issues", __name__)


@issue_bp.route("/report", methods=["POST"])
def report_issue():
    print("DEBUG: Entered /report route")
    user_id = get_jwt_identity()

    print("DEBUG: Headers:", dict(request.headers))
    print("DEBUG: Content-Type:", request.content_type)
    print("DEBUG: request.form:", dict(request.form))
    print("DEBUG: request.files:", request.files)
    print("DEBUG: files.getlist('images'):", request.files.getlist("images"))

    data = request.form
    files = request.files.getlist("images")

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    issue_type = data.get("issue_type", "Unspecified")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    address = data.get("address", "").strip()

    voice_note = request.files.get("voice_note")
    video_note = request.files.get("video_note")

    # Debug file details
    if files:
        for idx, f in enumerate(files):
            print(
                f"DEBUG: Image[{idx}] - filename: {f.filename}, mimetype: {f.mimetype}, size: {f.content_length}"
            )

    if not title:
        print("ERROR: Title missing")
        return jsonify({"error": "Title is required"}), 400
    if not description:
        print("ERROR: Description missing")
        return jsonify({"error": "Description is required"}), 400
    if not files or any(f.mimetype.split("/")[0] != "image" for f in files):
        print("ERROR: Image(s) missing or wrong mimetype")
        return jsonify({"error": "At least one image is required"}), 400
    if any(f.content_length > 15 * 1024 * 1024 for f in files):
        print("ERROR: Image too large")
        return jsonify({"error": "Each image must be less than 15MB"}), 400

    if not latitude or not longitude:
        if not address:
            print("ERROR: Location missing")
            return jsonify({"error": "Either coordinates or address is required"}), 400
    else:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                print("ERROR: Invalid coordinates range")
                return jsonify({"error": "Invalid coordinates"}), 400
        except ValueError:
            print("ERROR: Invalid coordinate format")
            return jsonify({"error": "Invalid coordinate format"}), 400

    image_urls = []
    for file in files:
        try:
            print(f"DEBUG: Uploading image {file.filename}")
            img = compress_image(file)
            url = upload_file_to_s3(
                img,
                f"issues/images/{user_id}_{uuid4()}_{file.filename}",
                config=app.config["S3_CONFIG"],
            )
            print(f"DEBUG: Image uploaded to {url}")
            image_urls.append(url)
        except Exception as e:
            print("ERROR: Failed to upload image", e)
            return jsonify({"error": f"Failed to upload image: {str(e)}"}), 500

    voice_url = None
    if voice_note:
        try:
            print(f"DEBUG: Uploading voice note {voice_note.filename}")
            voice_url = upload_file_to_s3(
                voice_note,
                f"issues/voice_notes/{user_id}_{uuid4()}_{voice_note.filename}",
                config=app.config["S3_CONFIG"],
                content_type=voice_note.mimetype,
            )
            print(f"DEBUG: Voice note uploaded to {voice_url}")
        except Exception as e:
            print("ERROR: Failed to upload voice note", e)
            return jsonify({"error": f"Failed to upload voice note: {str(e)}"}), 500

    video_url = None
    if video_note:
        try:
            print(f"DEBUG: Uploading video note {video_note.filename}")
            video_url = upload_file_to_s3(
                video_note,
                f"issues/video_notes/{user_id}_{uuid4()}_{video_note.filename}",
                config=app.config["S3_CONFIG"],
                content_type=video_note.mimetype,
            )
            print(f"DEBUG: Video note uploaded to {video_url}")
        except Exception as e:
            print("ERROR: Failed to upload video note", e)
            return jsonify({"error": f"Failed to upload video note: {str(e)}"}), 500

    issue = Issue(
        citizen_id=user_id,
        title=title,
        description=description,
        issue_type=issue_type,
        image_urls=image_urls,
        voice_note_url=voice_url,
        video_note_url=video_url,
        latitude=latitude,
        longitude=longitude,
        address=address,
    )
    db.session.add(issue)
    db.session.commit()

    print("DEBUG: Issue created successfully:", issue.to_dict())

    return (
        jsonify({"message": "Issue Reported Successfully", "issue": issue.to_dict()}),
        201,
    )


@issue_bp.route("/my-issues", methods=["GET"])
@jwt_required()
def get_my_issues():
    user_id = get_jwt_identity()

    issues = (
        Issue.query.filter_by(citizen_id=user_id)
        .order_by(Issue.created_at.desc())
        .all()
    )

    return jsonify({"issues": [issue.to_dict() for issue in issues]}), 200


@issue_bp.route("/<int:issue_id>", methods=["GET"])
@jwt_required()
def get_issue(issue_id):
    user_id = get_jwt_identity()

    issue = Issue.query.filter_by(id=issue_id, citizen_id=user_id).first()

    if not issue:
        return jsonify({"error": "Issue not found"}), 404

    return jsonify({"issue": issue.to_dict()}), 200
