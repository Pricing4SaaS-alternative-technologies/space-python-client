import os
import pytest
from app.routes.config import SpaceClient

TEST_SPACE_URL =  "http://localhost:5403"
TEST_API_KEY = "76494fc1a6db95d175412b130c64ffa8f73b0adc8480c9891df98507c7e4bb78"
TEST_SERVICE_PATH = "tests/resources/pricings/TomatoMeter.yml"

@pytest.fixture(scope="session")
async def space_client():
    """
    Crea y devuelve un SpaceClient listo para tests.
    - crea la session (lazy) dentro del loop de pytest-asyncio
    - comprueba healthcheck (skip si no disponible)
    - intenta subir un pricing de prueba (adaptar endpoint si hace falta)
    - cierra el cliente al finalizar la sesión de tests
    """
    client = SpaceClient(TEST_SPACE_URL, TEST_API_KEY)
    await client._get_session()

    ok = False
    try:
        ok = await client.is_connected_to_space()
    except Exception:
        ok = False

    if not ok:
        await client.close()
        pytest.skip("SPACE no disponible para tests (healthcheck falló)")

    # intentar añadir el pricing de prueba (adaptar endpoint /pricings según API)
    try:
        if os.path.exists(TEST_SERVICE_PATH):
           await client.service_context.add_service(TEST_SERVICE_PATH)
    except Exception:
        # no bloquear tests si la carga falla; puedes hacer fail/log según prefieras
        pass

    yield client

    # teardown
    await client.close()