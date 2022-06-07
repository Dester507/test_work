from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import router


def get_application() -> FastAPI:
    # Create application
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION
    )
    # Middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    # Include main router
    application.include_router(router)

    return application


app = get_application()
