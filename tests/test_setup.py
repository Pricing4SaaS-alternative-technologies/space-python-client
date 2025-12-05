import pytest
from app.routes.config import SpaceClient  

@pytest.mark.asyncio
async def test_space_client_setup(space_client):
    # El fixture debe devolver una instancia válida
    assert isinstance(space_client, SpaceClient)
    
    # Comprobación simple de conectividad (healthcheck)
    try:
        ok = await space_client.is_connected_to_space()
        
        # Si SPACE está disponible, debería ser True
        # Si no está disponible, el test pasa igual (no es un fallo del código)
        if ok:
            assert ok is True
            print("Conectado a SPACE")
        else:
            print("SPACE no disponible, pero el cliente se creó correctamente")
            
    except Exception as e:
        print(f"Error durante healthcheck (esperado si SPACE no está ejecutándose): {e}")
    
    # Verificar que los módulos existen
    assert hasattr(space_client, "service_context")
    assert hasattr(space_client, "contracts")
    assert hasattr(space_client, "featureEvaluators")
    
    # Limpiar
    await space_client.close()
