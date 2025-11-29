import pytest
from app.routes.config import SpaceClient

def test_imports():
    """Test mínimo para verificar que los imports funcionan"""
    assert SpaceClient is not None

@pytest.mark.asyncio
async def test_simple_client_creation():
    """Test simple de creación de cliente"""
    client = SpaceClient(
        "http://localhost:5403",
        "76494fc1a6db95d175412b130c64ffa8f73b0adc8480c9891df98507c7e4bb78"
    )
    assert client is not None
    assert hasattr(client, 'service_context')
    
    # Verificar que tiene el método close (esto fallará si no lo has añadido)
    assert hasattr(client, 'close')
    
    # Cerrar el cliente
    await client.close()
    
    
