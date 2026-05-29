
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .core.db import create_db_and_tables

from .routers.masters import router as masters_router
from .routers.auth import router as auth_router
from .routers.users import router as users_router
from .routers.lessons import router as lessons_router
from .routers.reservations import router as reservations_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", # vueのデフォルト,
        "https://orange-glacier-0f64ab200.7.azurestaticapps.net"
    ],
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
    # create_db_and_tables()
    pass


app.include_router(masters_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(lessons_router)
app.include_router(reservations_router)