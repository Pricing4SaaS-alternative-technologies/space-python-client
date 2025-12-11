from __future__ import annotations
import aiohttp
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .config import SpaceClient
from datetime import datetime
import os
from typing import Optional
from app.models.contracts import FallbackSubscription
from app.models.service_context import *

class ServiceContextModule:
    def __init__(self, space_client: SpaceClient):
        self.space_client = space_client
        
    async def get_service(self,service_name: str)->Service:
        session = await self.space_client._get_session()
        try:
            response = await session.get(f"{self.space_client.http_url}/services/{service_name}")
            response.raise_for_status()
            service_data = await response.json()
            #print(f"SERVICIO: {service_data}")
            return service_data
        
            
        except aiohttp.ClientResponseError as e:
            print(f"Error fetching service {service_name}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    async def get_pricing(self,service_name: str, pricing_version:str)-> Pricing:
        session = await self.space_client._get_session()
        try:
            response = await session.get(f"{self.space_client.http_url}/services/{service_name}/pricings/{pricing_version}")
            response.raise_for_status()
            pricing_data = await response.json()
            return pricing_data
        except aiohttp.ClientResponseError as e:
            print(f"Error fetching pricing for service {service_name}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    async def _post_with_file_path(self, endpoint: str, file_path: str)-> Service:
        form = aiohttp.FormData()
        file_name= os.path.basename(file_path)
        
        with open(file_path, 'rb') as file_stream:
            form.add_field("pricing", file_stream, file_name )
        
        session = await self.space_client._get_session()
        try:
            response = await session.post(endpoint, data=form)
            response.raise_for_status()
            data = await response.json()
            return data
        except aiohttp.ClientResponseError as e:
            print(f"Error posting file to {endpoint}: {e}")
            return e
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    async def _post_with_file(self, endpoint: str, file_bytes: bytes)-> Service:
        form = aiohttp.FormData()
        form.add_field("file", file_bytes, filename=f"{datetime.now().timestamp()}.yaml" )
        
        session = await self.space_client._get_session()
        try:
            response = await session.post(endpoint, data=form)
            response.raise_for_status()
            data = await response.json()
            return data
        except aiohttp.ClientResponseError as e:
            print(f"Error posting file to {endpoint}: {e}")
            return e
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    async def _post_with_url(self, endpoint: str, url: str)-> Service:
        payload = {"pricing": url}
        
        session = await self.space_client._get_session()
        try:
            response = await session.post(endpoint, json=payload)
            response.raise_for_status()
            data = await response.json()
            return data
        except aiohttp.ClientResponseError as e:
            print(f"Error posting URL to {endpoint}: {e}")
            return e
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

 
    async def add_pricing(self, service_name:str, url:Optional[str]=None, service_file:Optional[bytes]= None):
        
        if( not url and not service_file):
            raise ValueError("Se requiere url o service_file")
        if(url and service_file):
            raise ValueError("Solo se permite url o service_file, no ambos")
        if(url):
            remote_url = url.startswith(('http://', 'https://'))
            endpoint = f"/services/{service_name}/pricings"
            if(remote_url):
                return await self._post_with_url(endpoint,url)
            else:
                resolved_path = os.path.abspath(url) 
                return await self._post_with_file_path(endpoint,resolved_path)
        if(service_file):
            return await self._post_with_file(f"/services/{service_name}/pricings",service_file)
        

    async def change_pricing_availability(self, service_name: str, pricing_version: str, availability: availability_type, fallback_subscription: Optional[FallbackSubscription]=None)-> Service:
        if(availability not in [availability_type.ACTIVE, availability_type.ARCHIVED]):
            raise ValueError("Invalid availability type")
        if(availability == availability_type.ARCHIVED and not fallback_subscription):
            raise ValueError("Fallback subscription is required when archiving a pricing version")
        session = await self.space_client._get_session()
        try:
            url = f"{self.space_client.http_url}/services/{service_name}/pricings/{pricing_version}?availability={availability}"
            if fallback_subscription:
                response = await session.patch(url, json=fallback_subscription)
            else:
                response = await session.patch(url)
            response.raise_for_status()
            service_data = await response.json()
            return service_data
        except aiohttp.ClientResponseError as e:
            print(f"Error changing availability for service {service_name}, pricing version {pricing_version}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    async def add_service(self, file_path: str):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
            
            with open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field(
                    'pricing', 
                    f.read(),
                    filename=os.path.basename(file_path),
                    content_type='application/yaml'
                )                
                
                session = await self.space_client._get_session()
                timeout = aiohttp.ClientTimeout(total=30) 
                
                async with session.post(
                    f"{self.space_client.http_url}/services",
                    data=data,
                    timeout=timeout
                ) as response:
                    
                    response.raise_for_status()
                    service_data = await response.json()
                    #print(f"Servicio creado exitosamente: {service_data}")
                    return service_data
                    
        except aiohttp.ClientResponseError as e:
            print(f"Error del servidor al añadir servicio {file_path}: {e.status} - {e.message}")
            raise
        except aiohttp.ClientConnectionError as e:
            print(f"Error de conexión al añadir servicio {file_path}: {e}")
            raise
        except FileNotFoundError as e:
            print(f"Archivo no encontrado: {e}")
            raise
        except Exception as e:
            print(f"Error inesperado al añadir servicio {file_path}: {e}")
            raise
        
        
