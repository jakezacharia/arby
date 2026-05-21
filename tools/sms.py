from twilio.rest import Client
from config import settings

def send_sms_alert(message: str) -> None:
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    client.messages.create(
        body=message,
        from_=settings.twilio_from_number,
        to=settings.twilio_to_number,
    )
    print(f"[sms] Sent: {message}")