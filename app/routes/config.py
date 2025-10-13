
import aiohttp


class SpaceClient:
    
    VALID_EVENTS = [
        'synchronized',
        'pricing_created',
        'pricing_archived',
        'pricing_actived',
        'service_disabled',
        'error',
    ]
    
    def __init__(self, url: str, api_key: str, timeout: int = 5000):
        
        if not url or not api_key:
            raise ValueError("url and api_key are required")
        
        raw_url = url
        clean = raw_url.rstrip('/') 
        self.http_url = f"{clean}/api/v1"
        self.api_key = api_key
        self.timeout = timeout
        
        self.valid_events = list(self.VALID_EVENTS)
        self.call_back_functions = {}
        
        self.contracts = None #ContractModule(self) por ahora no estan hechos 
        self.features = None #FeatureModule(self) 
        
        # the webSocket part is not implemented yet
      
        
    async def is_conected_to_space(self) -> bool:
        """
        Check if the client is connected to Space.
        """
        try:
            # the healthccheck endpoint doesnt need apikey
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.http_url}/healthcheck") as response:
                    if response.status != 200:
                        return False
                    data = await response.json()
                    return bool(data.get("message"))
                
        except Exception as e:
            print(f"Connection error: {e}")
            return False
        
    # the methods related to webSockets will be implemented later in the development, these are form better performance and control of the events