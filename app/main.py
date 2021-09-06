from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from app.models import Base, SessionLocal, engine
from app.utils.google_oauth import authenticate_via_google_oauth
from app.views import login, setup, visit

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://alexd2580.skytaxi.jp", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def redirect_auth(request: Request, call_next):
    if request.url.path == "visit":
        return await call_next(request)

    try:
        session = SessionLocal()

        on_login_page = request.url.path == "/login"

        access_token = request.cookies.get("access_token", "invalid")
        request.state.user = authenticate_via_google_oauth(access_token, session)
        is_logged_in = request.state.user is not None

        if on_login_page and is_logged_in:
            return RedirectResponse("/", status_code=302)

        if not on_login_page and not is_logged_in:
            return RedirectResponse("/login", status_code=302)

    finally:
        session.close()

    return await call_next(request)


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def get_links(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})


app.include_router(login.router)
app.include_router(setup.router)
app.include_router(visit.router)
