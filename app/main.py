from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.views import link
from app.models import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(link.router)
