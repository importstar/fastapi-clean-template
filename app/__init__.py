import time

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from contextlib import asynccontextmanager

from fastapi_pagination.api import _add_pagination

from loguru import logger

from app.api import init_router
from app.models import init_mongoengine, disconnect_mongoengine
from app.core.app import get_app_settings, AppSettings

from app.utils.http_error import http_error_handler
from app.utils.validation_error import http422_error_handler


def create_app() -> FastAPI:
    settings: AppSettings = get_app_settings()
    settings.configure_logging()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # on app start up
        await init_router(app, settings)
        await init_mongoengine(settings)
        _add_pagination(app)
        yield
        # on app shutdown
        await disconnect_mongoengine()

    app = FastAPI(**settings.fastapi_kwargs)
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.add_middleware(GZipMiddleware, minimum_size=1000)  # Allow accept gzip encoding
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_origins=settings.ALLOW_HOSTS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )
    app.router.lifespan_context = lifespan

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        user_agent = request.headers.get("user-agent", "")
        logger.debug(f"user-agent ==> {user_agent}")
        for agent in settings.DISALLOW_AGENTS:
            if agent in user_agent.lower():
                logger.warning({"detail": "Client is not allow to uses."})

                return JSONResponse(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    content={"detail": "Client is not allow to uses."},
                )

        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = "{:0.6f}".format(process_time)
        return response

    @app.get("/", tags=["Root"])
    async def root():
        return {"message": "service is working"}

    return app


app = create_app()
