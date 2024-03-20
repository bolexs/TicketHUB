from ..model import Base
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from ..conf.settings import settings as app_settings

from ..main import app, get_db
from ..database import get_db_engine
import pytest

engine = get_db_engine(test_mode=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def settings():
    # Allow overriding for tests
    yield app_settings.model_copy(deep=True)


@pytest.fixture(scope="function")
def session():
    """ Return a session after test tear down"""
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def override_db(session):
    def _get_db():
        try:
            yield session
        finally:
            pass
    return _get_db


@pytest.fixture(scope="function")
def client(override_db):
    app.dependency_overrides[get_db] = override_db
    return TestClient(app)