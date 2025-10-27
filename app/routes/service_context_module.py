from typing import Optional
import aiohttp
from app.routes.config import SpaceClient


class serviceContextModule:
    def __init__(self, space_client: SpaceClient):
        self.space_client = space_client
        
    async def get_service(self,service_name: str):
        session = await self.space_client._get_session()
        try:
            response = await session.get(f"{self.space_client.http_url}/services/{service_name}")
            response.raise_for_status()
            service_data = await response.json()
            return service_data
        except aiohttp.ClientResponseError as e:
            print(f"Error fetching service {service_name}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    async def get_pricing(self,service_name: str, usage_metrics: dict):
        session = await self.space_client._get_session()
        try:
            response = await session.post(f"{self.space_client.http_url}/services/{service_name}/pricing", json=usage_metrics)
            response.raise_for_status()
            pricing_data = await response.json()
            return pricing_data
        except aiohttp.ClientResponseError as e:
            print(f"Error fetching pricing for service {service_name}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    async def add_pricing(self, service_name:str, url:Optional[str]=None, service_file:Optional[bytes]= None):
        session = await self.space_client.get_session()
        
        if( not url and not service_file):
            raise ValueError("Se requiere url o service_file")
        if(url and service_file):
            raise ValueError("Solo se permite url o service_file, no ambos")
        if(url):
            remote_url = "" #verificar si la url es remota 
            endpoint = f"/services/{service_name}/pricings"
            if(remote_url):
                return await session.post_with_url(endpoint,url)
            else:
                resolved_path = "" #extraer la ruta real 
                return await session.post_with_file_path(endpoint,resolved_path)
        if(service_file):
            return await session.post_with_file(f"/services/{service_name}/pricings",service_file)
        
    #Introducir resto de operaciones necesarias (postwith..)