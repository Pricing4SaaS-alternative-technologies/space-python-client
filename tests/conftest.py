import os
import pytest
from app.routes.config import SpaceClient

TEST_SPACE_URL = "http://localhost:5403"
TEST_API_KEY = "76494fc1a6db95d175412b130c64ffa8f73b0adc8480c9891df98507c7e4bb78"
TEST_SERVICE_PATH = "tests/resources/pricings/TomatoMeter.yml"

@pytest.fixture
def space_client():
    """
    Fixture síncrono simple que devuelve un SpaceClient.
    La conexión real se hará en cada test que lo necesite.
    """
    return SpaceClient(TEST_SPACE_URL, TEST_API_KEY)
