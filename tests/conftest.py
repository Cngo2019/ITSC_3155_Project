import pytest
from app import app

@pytest.fixture()
def client():
    return app.test_client()

@pytest.fixture(scope='module')
def test_app():
    return app.test_client()

@pytest.fixture()
def runner():
    return app.test_cli_runner()

