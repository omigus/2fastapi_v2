from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.db.events import init_db ,close_db
from app.api.routes.api import run_router

def get_application() -> FastAPI:
    application = FastAPI(title="PROJECT_NAME", debug="DEBUG", version="1")

    application.add_middleware(
        CORSMiddleware,
        allow_origins="ALLOWED_HOSTS" or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application

app = get_application()
run_router(app)


@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()