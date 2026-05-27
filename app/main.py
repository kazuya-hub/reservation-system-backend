
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.db import create_db_and_tables

from .routers.auth import router as auth_router
from .routers.users import router as users_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", # vueのデフォルト
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.middleware("http")
# async def printout(request: Request, call_next):
#     print(dict(request))
#     return await call_next(request)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth_router)
app.include_router(users_router)
