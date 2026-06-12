import os


def send_sms(phone_number, message):
    if not os.getenv("SMS_ENABLED", "false").lower() in ("true", "1", "yes"):
        print(f"------ [ INFO ] ------ SMS skipped (SMS_ENABLED=false): {message[:80]}...")
        return False

    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_from = os.getenv("TWILIO_PHONE_NUMBER")

    if not all([twilio_sid, twilio_token, twilio_from]):
        print(
            f"------ [ INFO ] ------ SMS skipped (Twilio not configured): {message[:80]}..."
        )
        return False

    try:
        from twilio.rest import Client

        client = Client(twilio_sid, twilio_token)
        client.messages.create(body=message, from_=twilio_from, to=phone_number)
        return True
    except Exception as e:
        print(f"------ [ WARN ] ------ Failed to send SMS: {e}")
        return False


def send_status_sms(user, issue, new_status):
    if not user.phone:
        return

    status_labels = {
        "pending": "Pending",
        "in_progress": "In Progress",
        "resolved": "Resolved",
        "rejected": "Rejected",
        "verified": "Verified",
    }

    message = (
        f'CityPulse: Your issue "{issue.title}" (#{issue.id}) '
        f"is now {status_labels.get(new_status, new_status)}."
    )

    send_sms(user.phone, message)
