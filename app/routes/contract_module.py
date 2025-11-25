import aiohttp
from config import SpaceClient
from app.models.contracts import ContractToCreate, Subscription
 
class ContractModule:
    def __init__(self, space_client: SpaceClient):
        self.space_client = space_client
        
    async def get_contracts(self, user_id: str):
        session = await self.space_client._get_session()
        try:
            async with session.get(
            f"{self.space_client.http_url}/contracts/{user_id}",
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            error_detail = await response.text()
            print(f"Error fetching contracts: {e} - {error_detail}")
            return None
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
            error_detail = await response.text()
            print(f"Error adding contract: {e} - {error_detail}")
            return None
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
            error_detail = await response.text()
            print(f"Error updating contract subscription: {e} - {error_detail}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise