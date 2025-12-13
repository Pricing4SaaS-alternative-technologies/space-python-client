import os
import pytest
import pytest_asyncio
import tempfile
import uuid
from app.routes.config import SpaceClient

TEST_SPACE_URL = "http://localhost:5403"
TEST_API_KEY_PABLO = "57ab59b541bafc971b7588a192661ed01e3e354a9f1464f868e28a4b66931b01"
TEST_API_KEY_DANIEL = "f7e0316af74ea3602e16081a9c38b18e1b1a63f4f1ba66088d35a9c91b71f87f"



@pytest_asyncio.fixture
async def space_client():
    client = SpaceClient(TEST_SPACE_URL, TEST_API_KEY_DANIEL)
    
    yield client

#-------------------------------------------------------------------------------------------------------------
# LIMPIEZA: COMENTAR PARA MANTENER SERVICIO TRAS TEST
#-------------------------------------------------------------------------------------------------------------

    try:
        session = await client._get_session()
        delete_url = f"{f"{client.http_url}/services"}"
        await session.delete(delete_url)
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