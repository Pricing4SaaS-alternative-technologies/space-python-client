import aiohttp
from config import SpaceClient

class ContractModule:
    def __init__(self, space_client: SpaceClient):
        self.space_client = space_client
        
    async def get_contracts(self, user_id: str):
        session = await self.space_client._get_session()
        try:
            async with session.get(f"{self.space_client.http_url}/contracts/{user_id}") as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            print(f"Error fetching contracts: {e}")
            return None
        except Exception as e:
            raise