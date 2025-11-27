import pytest
from app.routes.config import SpaceClient


@pytest.mark.asyncio
async def test_space_client_setup(space_client):
    # El fixture debe devolver una instancia válida
    assert isinstance(space_client, SpaceClient)

    # Comprobación simple de conectividad (healthcheck)
    ok = await space_client.is_connected_to_space()
    assert ok is True

    # El módulo de service_context debe existir en el cliente
    assert hasattr(space_client, "service_context")