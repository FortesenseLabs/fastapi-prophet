import os

# import asyncio
import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.db import mk_engine, setup_db
from app.main import create_application

# import nest_asyncio


# nest_asyncio.apply()


def get_settings_override():
    return Settings(testing=1, database_url=os.getenv("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    settings = get_settings()
    if settings.database_url is None:
        settings.testing = True
        settings.environment = "test"
        settings.database_url = os.getenv("DATABASE_TEST_URL")
    app = create_application()
    with TestClient(app) as test_client:
        yield test_client


# @pytest.fixture(scope="session")
# def event_loop():
#     yield asyncio.get_event_loop()


@pytest.fixture(scope="module")
def db(test_app):
    mk_engine()
    db = setup_db()
    try:
        yield db
    finally:
        db.disconnect()
