"""Login with google."""
import os

import fastapi
from fastapi import Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.models import get_db
from app.utils.google_oauth import authenticate_via_google_oauth

router = fastapi.APIRouter(prefix="/login")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
def login_page(request: Request):
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    parameters = {
        "request": request,
        "google_client_id": client_id,
        "login_redirect_url": "https://alexd2580.skytaxi.jp/login",
    }
    return templates.TemplateResponse("login.html", parameters)


@router.post("", response_class=RedirectResponse, status_code=302)
def login_redirect(
    request: Request,
    response: Response,
    credential: str = Form(...),
    session: Session = Depends(get_db),
):
    authenticate_via_google_oauth(credential, session)
    response.headers["Set-Cookie"] = f"access_token={credential}"
    return "/setup"
