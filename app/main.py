
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .core.db import create_db_and_tables

from .routers.masters import router as masters_router
from .routers.auth import router as auth_router
from .routers.users import router as users_router
from .routers.lessons import router as lessons_router
from .routers.reservations import router as reservations_router


def _get_allowed_origins() -> list[str]:
    # Comma separated origins from env, e.g. "https://foo.azurestaticapps.net,https://bar.example.com"
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]

    if "http://localhost:5173" not in origins:
        origins.append("http://localhost:5173")

    return origins


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    # Azure Static Web Apps のプレビューURLや再作成時のURL変更に追従する
    allow_origin_regex=r"https://.*\.azurestaticapps\.net",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def printout(request: Request, call_next):
    # リクエストの内容をログに出力
    print(f"Request: {request.method} {request.url}")
    print(f"Headers: {request.headers}")
    print(f"Body: {await request.body()}")
    return await call_next(request)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(masters_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(lessons_router)
app.include_router(reservations_router)