import logging

from fastapi import FastAPI

from app.api import ping, predictions, train
from app.db import engine, database
from app.models.sqlalchemy import metadata

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(
        predictions.router, prefix="/predict", tags=["predict"]
    )
    application.include_router(train.router, prefix="/train", tags=["train"])
    return application


app = create_application()
metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    log.info("Starting up...")
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    log.info("Shutting down...")
    await database.disconnect()
