import os
import pytest
import pytest_asyncio
from unittest.mock import Mock, AsyncMock
from app.routes.config import SpaceClient

TEST_SPACE_URL = "http://localhost:5403"
TEST_API_KEY = "2faefe1f4d37b20ce24bad0da40f1fc3617b56fe6304c7b6479ae8e3710b8238"
TEST_SERVICE_PATH = "tests/resources/pricings/TomatoMeter.yml"


@pytest_asyncio.fixture
async def space_client():
    """
    Fixture síncrono simple que devuelve un SpaceClient.
    La conexión real se hará en cada test que lo necesite.
    """
    client = SpaceClient(TEST_SPACE_URL, TEST_API_KEY)
    
        # intentar añadir el pricing de prueba (adaptar endpoint /pricings según API)
    try:
        if os.path.exists(TEST_SERVICE_PATH):
            result = await client.service_context.add_service(TEST_SERVICE_PATH) # TODO: esto funciona pero como se ejecuta para todos los tests y la bbdd no se renueva, a paritr del primer test da error porque se repiten los servicios.
            if result:
               print("OK: Test service pricing uploaded to SPACE for tests.")
            else:
               print("WARNING: Test service pricing upload failed.")
           
    except Exception as e:
        print("WARNING: Exception during test service pricing upload: ",e)
        pass
    
    yield client
    await client.close()