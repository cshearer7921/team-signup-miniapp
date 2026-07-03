from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.admin_pages import router as admin_pages_router
from app.bootstrap import seed_initial_data
from app.database import Base, SessionLocal, engine
from app.routers import admin, auth, join_requests, matches, me


def create_app() -> FastAPI:
    app = FastAPI(title="Team Signup Miniapp API")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            seed_initial_data(db)

    @app.get("/health")
    def health() -> dict:
        return {"ok": True}

    app.include_router(auth.router, prefix="/api")
    app.include_router(me.router, prefix="/api")
    app.include_router(join_requests.router, prefix="/api")
    app.include_router(matches.router, prefix="/api")
    app.include_router(admin.router, prefix="/api")
    app.include_router(admin_pages_router)
    return app


app = create_app()
