from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api import init_router
from app.core.app import get_app_settings
from app.models import init_mongoengine, disconnect_mongoengine


class App:
    def create_app(self) -> FastAPI:
        settings = get_app_settings()
        settings.configure_logging()

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await init_router(app, settings)
            await init_mongoengine(settings)
            yield
            # await disconnect_mongoengine()

        self.app = FastAPI(lifespan=lifespan, **settings.fastapi_kwargs)
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
