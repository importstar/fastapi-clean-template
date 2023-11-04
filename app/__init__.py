from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination.api import _add_pagination
from app.api import init_router
from app.core.app import get_app_settings, AppSettings
from app.models import init_mongoengine, disconnect_mongoengine


class App:
    def create_app(self) -> FastAPI:
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
            # await disconnect_mongoengine()

        self.app = FastAPI(**settings.fastapi_kwargs)
        self.app.router.lifespan_context = lifespan
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOWED_HOSTS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.app.get("/")
        async def root():
            return {"message": "api is working"}

        return self.app


app = App()
