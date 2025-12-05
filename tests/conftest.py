import os
import pytest
import pytest_asyncio
import tempfile
import uuid
from app.routes.config import SpaceClient

TEST_SPACE_URL = "http://localhost:5403"
TEST_API_KEY = "57ab59b541bafc971b7588a192661ed01e3e354a9f1464f868e28a4b66931b01"


@pytest_asyncio.fixture
async def space_client():
    client = SpaceClient(TEST_SPACE_URL, TEST_API_KEY)
    
    service_name = None
    unique_id = uuid.uuid4().hex[:8]
    saas_name = f"TomatoMeter_{unique_id}"
    
    yaml_content = f"""saasName: {saas_name}
syntaxVersion: "3.0"
version: "1.0.0"
createdAt: "2025-01-01"
currency: USD
features:
  basicFeature:
    description: Basic test feature
    valueType: BOOLEAN
    defaultValue: true
    type: DOMAIN"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False, encoding='utf-8') as f:
        f.write(yaml_content)
        temp_yaml_path = f.name
    
    try:
        result = await client.service_context.add_service(temp_yaml_path)
        if result:
            service_name = saas_name
    except Exception as e:
        print(f"Error: {e}")
    
    try:
        os.unlink(temp_yaml_path) # Eliminar el archivo temporal
    except Exception as e:
        print(f"Error deleting temporary file: {e}")
    
    yield client

#-------------------------------------------------------------------------------------------------------------
# LIMPIEZA: COMENTAR PARA MANTENER SERVICIO TRAS TEST
#-------------------------------------------------------------------------------------------------------------

    if service_name:
        try:
            session = await client._get_session()
            delete_url = f"{f"{client.http_url}/services"}"
            async with session.delete(delete_url) as response:
                if response.status in [200, 204]:
                    print(f"✅ Servicio '{service_name}' borrado")
        except Exception as e:
            print(f"Error borrando: {e}")

    await client.close()

#-------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------
# FIXTURE DE SESIÓN: LIMPIEZA FINAL DE TODOS LOS SERVICIOS (POR SI FUERA NECESARIO)
#-------------------------------------------------------------------------------------------------------------

'''

@pytest_asyncio.fixture(scope="session", autouse=True)
async def cleanup_all_services_after_tests():
    """
    Fixture de sesión que borra todos los servicios después de ejecutar todos los tests.
    """
    yield  # Aquí se ejecutan todos los tests
    
    # Después de todos los tests, borrar todos los servicios
    print(f"\n{'='*60}")
    print("🧹 LIMPIANDO TODOS LOS SERVICIOS (sesión finalizada)")
    print(f"{'='*60}")
    
    client = SpaceClient(TEST_SPACE_URL, TEST_API_KEY)
    
    try:
        session = await client._get_session()
        
        # Borrar TODOS los servicios
        delete_response = await session.delete(f"{client.http_url}/services")
        if delete_response.status in [200, 204]:
            print(f"✅ Todos los servicios borrados exitosamente")
        else:
            error_text = await delete_response.text()
            print(f"⚠ No se pudieron borrar los servicios: {delete_response.status} - {error_text}")
    except Exception as e:
        print(f"⚠ Error en limpieza final: {e}")
    finally:
        await client.close()
        
'''