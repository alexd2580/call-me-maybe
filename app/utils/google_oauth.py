import logging
import os
from typing import Optional

from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from app.models.user import User

logger = logging.getLogger(__name__)


def authenticate_via_google_oauth(
    access_token: str, session: Session
) -> Optional[User]:
    """Given a google auth token, get an internal `User`.

    If this user signs in for the first time, a new `User` is created.
    """
    try:
        id_info = id_token.verify_oauth2_token(
            access_token, requests.Request(), os.environ["GOOGLE_CLIENT_ID"]
        )
    except ValueError as e:
        logger.debug(str(e))
        return None

    # TODO invalid token.

    email = id_info["email"]

    user = session.query(User).filter_by(email=email).first()
    if not user:
        user = User(email=email)
        session.add(user)
        session.commit()

    return user
