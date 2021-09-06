"""Authorize for use of Google Sheets."""
from itertools import zip_longest
from typing import Optional

import fastapi
import google.oauth2.credentials
import google_auth_oauthlib.flow
from fastapi import Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from googleapiclient.discovery import build
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.models import get_db

router = fastapi.APIRouter(prefix="/setup")
templates = Jinja2Templates(directory="templates")


def build_oauth2_flow(state: Optional[str] = None) -> google_auth_oauthlib.flow.Flow:
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
        state=state,
    )

    flow.redirect_uri = "https://alexd2580.skytaxi.jp/setup/oauth2-callback"
    return flow


@router.post("/oauth2", response_class=RedirectResponse, status_code=302)
def oauth2_request(request: Request, session: Session = Depends(get_db)):
    current_user = request.state.user

    flow = build_oauth2_flow()
    authorization_url, state = flow.authorization_url(
        login_hint=current_user.email,
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        prompt="consent",
    )

    current_user.oauth2_state = state
    session.add(current_user)
    session.commit()

    return authorization_url


@router.get("/oauth2-callback", response_class=RedirectResponse, status_code=302)
def oauth2_callback(
    request: Request,
    response: Response,
    # *,
    # state: str,
    # code: str,
    session: Session = Depends(get_db),
):
    flow = build_oauth2_flow(state=request.state.user.oauth2_state)
    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials

    current_user = request.state.user
    current_user.oauth2_credentials = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    current_user.oauth2_token = flow.credentials.token
    current_user.oauth2_refresh_token = flow.credentials.token
    session.add(current_user)
    session.commit()
    return "/setup"


@router.post("/spreadsheet", response_class=RedirectResponse, status_code=302)
def spreadsheet(
    request: Request,
    source_domain: Optional[str] = Form(None),
    spreadsheet_id: Optional[str] = Form(None),
    sheet_name: Optional[str] = Form(None),
    match_column: Optional[str] = Form(None),
    date_column: Optional[str] = Form(None),
    session: Session = Depends(get_db),
):
    current_user = request.state.user

    current_user.source_domain = source_domain
    current_user.spreadsheet_id = spreadsheet_id
    current_user.sheet_name = sheet_name
    current_user.match_column = match_column
    current_user.date_column = date_column

    session.add(current_user)
    session.commit()

    return "/setup"


@router.get("", response_class=HTMLResponse)
def setup(request: Request, session: Session = Depends(get_db)):
    user = request.state.user

    area_preview: Optional[list[list[str]]] = None
    if (
        user.oauth2_credentials
        and user.spreadsheet_id
        and user.sheet_name
        and user.match_column
        and user.date_column
    ):
        credentials = google.oauth2.credentials.Credentials(**user.oauth2_credentials)

        ranges = [
            f"{user.sheet_name}!{user.match_column}:{user.match_column}",
            f"{user.sheet_name}!{user.date_column}:{user.date_column}",
        ]

        service = build("sheets", "v4", credentials=credentials)
        resource = service.spreadsheets().values()
        req = resource.batchGet(spreadsheetId=user.spreadsheet_id, ranges=ranges)
        res = req.execute()

        value_ranges = res["valueRanges"]
        match_data = value_ranges[0]["values"]
        date_data = value_ranges[1]["values"]
        area_preview = [
            [(match or [None])[0], (data or [None])[0]]
            for match, data in zip_longest(match_data, date_data)
        ]

    template_values = {
        "request": request,
        "oauth_setup": user.oauth2_credentials is not None,
        "source_domain": user.source_domain,
        "spreadsheet_id": user.spreadsheet_id,
        "sheet_name": user.sheet_name,
        "match_column": user.match_column,
        "date_column": user.date_column,
        "area_preview": area_preview,
    }

    return templates.TemplateResponse("setup.html", template_values)
