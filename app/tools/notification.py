import requests
from langchain_core.tools import tool

from app.config import settings


@tool
def send_booking_notification(
    email: str,
    date: str,
    time: str,
) -> dict:
    """
    Send a mock booking confirmation webhook.
    """

    payload = {
        "email": email,
        "date": date,
        "time": time,
        "status": "confirmed",
        "message": "Your appointment has been booked successfully."
    }

    try:
        response = requests.post(
            settings.WEBHOOK_URL,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        return {
            "success": True,
            "message": "Notification sent successfully.",
            "status_code": response.status_code,
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Notification failed: {str(e)}",
        }