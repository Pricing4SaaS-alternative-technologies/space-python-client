import os
import pytest
import pytest_asyncio
import tempfile
import uuid
from app_SpacePyCl.routes.config import SpaceClient
from dotenv import load_dotenv

load_dotenv(encoding='utf-8-sig')

TEST_SPACE_URL = "http://localhost:5403"
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    print("API_KEY no encontrada en las variables de entorno.")
    print("-------------------------------------------------------------------------------------------------------------")

print(f"API_KEY cargada: {API_KEY}")
print("-------------------------------------------------------------------------------------------------------------")



@pytest_asyncio.fixture
async def space_client():
    client = SpaceClient(TEST_SPACE_URL, API_KEY)
    
    yield client
    print("-------------------------------------------------------------------------------------------------------------")

#-------------------------------------------------------------------------------------------------------------
# LIMPIEZA: COMENTAR PARA MANTENER SERVICIO TRAS TEST
#-------------------------------------------------------------------------------------------------------------

    try:
        session = await client._get_session()
        delete_url = f"{f"{client.http_url}/services"}"
        delete_url2 = f"{f"{client.http_url}/contracts"}"
        await session.delete(delete_url)
        await session.delete(delete_url2)
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
    yield
    
    print("LIMPIANDO TODOS LOS SERVICIOS (sesión finalizada)")
    
    client = SpaceClient(TEST_SPACE_URL, TEST_API_KEY)
    
    try:
        session = await client._get_session()
        
        delete_response = await session.delete(f"{client.http_url}/services")
        if delete_response.status in [200, 204]:
            print(f"Todos los servicios borrados exitosamente")
        else:
            error_text = await delete_response.text()
            print(f"No se pudieron borrar los servicios: {delete_response.status} - {error_text}")
    except Exception as e:
        print(f"Error en limpieza final: {e}")
    finally:
        await client.close()
        
'''