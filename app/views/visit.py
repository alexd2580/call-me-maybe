from typing import Optional

import fastapi
from fastapi import Depends, Header, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import literal

from app.models import get_db
from app.models.user import User
from app.utils.spreadsheet import get_visits_table, log_visit

router = fastapi.APIRouter(prefix="/visit")


@router.get("", response_class=HTMLResponse)
def track_visit(
    request: Request,
    referer: Optional[str] = Header(None),
    session: Session = Depends(get_db),
):
    # Doesn't work without referer header.
    if not referer:
        return ""

    # Find user which matches by referrer url.
    wildcard = literal("%")
    wildcard_domain = wildcard.op("||")(User.source_domain.op("||")(wildcard))
    condition = literal(referer).ilike(wildcard_domain)
    user = session.query(User).filter(condition).first()

    if not user:
        return ""

    # Download spreadsheet and find matching row.
    table = get_visits_table(user)
    if not table:
        return ""

    for index, row in enumerate(table, 1):
        if row[0] is not None and row[0] in referer:
            log_visit(user, index)
            break

    return ""
