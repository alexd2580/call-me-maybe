from datetime import datetime
from typing import Optional

import fastapi
from fastapi import Depends, Request, Form
from sqlalchemy.orm import Session

from app.models import get_db
from app.models.link import Link

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = fastapi.APIRouter(prefix="/links")
templates = Jinja2Templates(directory="templates")


base_url = "www.example.com"


@router.get("", response_class=HTMLResponse)
def get_links(request: Request, session: Session = Depends(get_db)):
    links = session.query(Link).all()
    return templates.TemplateResponse(
        "links.html", {"request": request, "links": links}
    )


@router.post("", response_class=RedirectResponse, status_code=302)
def post_link(
    request: Request,
    description: str = Form(...),
    session: Session = Depends(get_db),
):
    link = Link(description=description)
    session.add(link)
    session.commit()
    return "/links"


@router.post("/{id}/delete", response_class=RedirectResponse, status_code=302)
def delete_link(request: Request, id: str, session: Session = Depends(get_db)):
    link = session.query(Link).get(id)
    if link is None:
        return "/links"

    session.delete(link)
    session.commit()
    return "/links"


@router.get("/{id}")
def track_visit(id: str, session: Session = Depends(get_db)):
    link = session.query(Link).get(id)
    link.date_opened = datetime.utcnow()
    session.add(link)
    session.commit()
    return ""
