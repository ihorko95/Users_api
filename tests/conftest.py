import pytest
import os
from alembic import command
from alembic.config import Config
from starlette.testclient import TestClient
from pg_database import DATABASE_URL
from sqlalchemy_utils import create_database, drop_database
from main import app
os.environ['TESTING'] = 'True'


@pytest.fixture(scope="module")
def temp_db():
    """ Create new DB for tests """
    TEST_SQLALCHEMY_DATABASE_URL=DATABASE_URL+'_tester2'
    create_database(TEST_SQLALCHEMY_DATABASE_URL)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

    try:
        yield TEST_SQLALCHEMY_DATABASE_URL
    finally:
        drop_database(TEST_SQLALCHEMY_DATABASE_URL)