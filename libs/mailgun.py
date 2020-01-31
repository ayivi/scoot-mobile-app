import os
from typing import List
from requests import Response, post

FAILED_LOAD_API_KEY = "Failed to load MailGun API key."
FALIED_LOAD_DOMAIN = "Failed to load MailGun domain."
ERROR_SENDING_EMAIL = "Error occurred in sending confirmation email, user registration was unsuccessful."


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

    
class Mailgun:
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", None)
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", None)

    FROM_TTILE = "Scoot"
    FROM_EMAIL = f"do-not-reply@{MAILGUN_DOMAIN}"

    @classmethod
    def send_email(
        cls, email: List[str], subject, text: str, html: str
    ) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(FAILED_LOAD_API_KEY)

        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(FALIED_LOAD_DOMAIN)

        respose = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

        if response.status_code != 200:
            raise MailGunException(ERROR_SENDING_EMAIL)

        return response