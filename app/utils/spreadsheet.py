"""Download data from google sheets."""
from datetime import datetime
from itertools import zip_longest
from typing import Optional

import google.oauth2.credentials
from googleapiclient.discovery import build

from app.models.user import User


def _is_set_up(user: User) -> bool:
    return bool(
        user.oauth2_credentials
        and user.spreadsheet_id
        and user.sheet_name
        and user.match_column
        and user.date_column
    )


def initialize_resource(user: User):
    credentials = google.oauth2.credentials.Credentials(**user.oauth2_credentials)
    service = build("sheets", "v4", credentials=credentials)
    return service.spreadsheets().values()


def get_visits_table(user: User) -> Optional[list[list[str]]]:
    if not _is_set_up(user):
        return None

    ranges = [
        f"{user.sheet_name}!{user.match_column}:{user.match_column}",
        f"{user.sheet_name}!{user.date_column}:{user.date_column}",
    ]

    resource = initialize_resource(user)
    req = resource.batchGet(spreadsheetId=user.spreadsheet_id, ranges=ranges)
    res = req.execute()

    value_ranges = res["valueRanges"]
    match_data = value_ranges[0]["values"]
    date_data = value_ranges[1]["values"]
    return [
        [(match or [None])[0], (data or [None])[0]]
        for match, data in zip_longest(match_data, date_data)
    ]


def log_visit(user: User, index: int) -> None:
    if not _is_set_up(user):
        return

    resource = initialize_resource(user)
    range = f"{user.sheet_name}!{user.date_column}{index}:{user.date_column}{index}"
    body = {"values": [[datetime.utcnow().isoformat()]]}
    req = resource.update(
        spreadsheetId=user.spreadsheet_id,
        range=range,
        body=body,
        valueInputOption="USER_ENTERED",
    )
    req.execute()
