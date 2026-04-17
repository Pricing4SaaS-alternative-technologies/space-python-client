from __future__ import annotations
import aiohttp
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .config import SpaceClient
from app_SpacePyCl.models.contracts import ContractToCreate, Subscription, UsageLevelUpdate, UsageLevel
 
class ContractModule:
    def __init__(self, space_client: "SpaceClient"):
        self.space_client = space_client
        
    async def get_user_id_contract(self, user_id: str):
        session = await self.space_client._get_session()
        try:
            async with session.get(
            f"{self.space_client.http_url}/contracts/{user_id}",
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            print(f"Error fetching contracts: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        
    async def add_contract(self, contract_to_create: ContractToCreate):
        session = await self.space_client._get_session()
        try:
            async with session.post(f"{self.space_client.http_url}/contracts", json=contract_to_create,
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            print(f"Error adding contract: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        
    async def update_contract_subscription(self, user_id: str, newSubscription: Subscription):
        session = await self.space_client._get_session()
        try:
            async with session.put(f"{self.space_client.http_url}/contracts/{user_id}", json=newSubscription,
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            print(f"Error updating contract subscription: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        
    async def update_usage_levels(self, user_id: str, usageLevels: dict[str, dict[str, int]]):
        # El backend espera valores numéricos directos, no objetos UsageLevel
        transformed_levels = {}
        
        for service_name, metrics in usageLevels.items():
            transformed_metrics = {}
            for metric_name, value in metrics.items():
                # Si el valor ya es un dict (con 'consumed'), extraer el valor
                if isinstance(value, dict) and 'consumed' in value:
                    transformed_metrics[metric_name] = value['consumed']
                else:
                    transformed_metrics[metric_name] = value
            
            transformed_levels[service_name.lower()] = transformed_metrics
            
        session = await self.space_client._get_session()
        url = f"{self.space_client.http_url}/contracts/{user_id}/usageLevels"
        
        try:
            async with session.put(url, json=transformed_levels) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            print(f"Error updating usage levels: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        
    async def update_user_contact(self, user_id: str, contact_data: dict):
        """
        Updates the user contact information of a contract in SPACE.
        """
        session = await self.space_client._get_session()
        url = f"{self.space_client.http_url}/contracts/{user_id}/userContact"
        
        try:
            async with session.put(url, json=contact_data) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            print(f"Error updating user contact in contract: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error updating user contact: {e}")
            raise