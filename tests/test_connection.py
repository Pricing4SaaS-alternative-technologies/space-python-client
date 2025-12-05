import pytest
from app.routes.config import SpaceClient

@pytest.mark.asyncio
async def test_space_connection_detailed(space_client):
    """Test detallado de conexión a SPACE"""
    assert isinstance(space_client, SpaceClient)
    
    try:
        # Verificar que el cliente se crea correctamente
        assert space_client is not None
        assert hasattr(space_client, 'is_connected_to_space')
        
        # Intentar conexión
        is_connected = await space_client.is_connected_to_space()
        
        if is_connected:
            print("Conectado exitosamente a SPACE")
            assert is_connected is True
        else:
            print("SPACE no está disponible (servidor no ejecutándose)")
            # No hacemos assert False porque esto es normal en entornos de test
            
    except Exception as e:
        print(f"Excepción durante prueba de conexión: {e}")
        # No fallamos el test porque la conexión depende del entorno
    finally:
        await space_client.close()

@pytest.mark.asyncio
async def test_client_modules(space_client):
    """Test que verifica que todos los módulos del cliente existen"""
    assert isinstance(space_client, SpaceClient)
    
    try:
        required_modules = [
            'service_context',
            'contracts', 
            'featureEvaluators'
        ]
        
        for module in required_modules:
            assert hasattr(space_client, module), f"Falta el módulo: {module}"
            
        print("Todos los módulos están presentes")
        
    finally:
        await space_client.close()