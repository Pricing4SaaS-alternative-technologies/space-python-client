from typing import Optional
from .contract_module import ContractModule
from .feature_eval_module import FeatureEvalModule
from .service_context_module import ServiceContextModule
import aiohttp
import asyncio


class SpaceClient:
    
    def __init__(self, url: str, api_key: str, timeout: int = 5000, api_prefix: str = "api/v1"):
        if not url or not api_key:
            raise ValueError("Se requieren url y api_key")

        self.api_prefix = api_prefix
        if api_prefix:
            self.http_url = f"{url.rstrip('/')}/{api_prefix.strip('/')}"
        else:
            self.http_url = url.rstrip('/')

        self.api_key = api_key
        self.timeout_ms = timeout
        
        self.contracts = ContractModule(self)
        self.featureEvaluators = FeatureEvalModule(self)
        self.service_context = ServiceContextModule(self)
        
        self._session: Optional[aiohttp.ClientSession] = None

        
    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout_ms/1000)
            self._session = aiohttp.ClientSession(
                headers={'x-api-key': self.api_key},
                timeout=timeout
            )
        return self._session

    async def is_connected_to_space(self) -> bool:
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            
            async with aiohttp.ClientSession(timeout=timeout) as temp_session:
                async with temp_session.get(
                    f"{self.http_url}/healthcheck",
                    headers={'x-api-key': self.api_key}
                ) as response:
                    data = await response.json()
                return response.status == 200 and bool(data.get("message"))
                    
        except asyncio.TimeoutError:
            print("Timeout: SPACE no responde después de 5 segundos")
            return False
        except aiohttp.ClientConnectorError:
            print("Error: No se puede conectar al servidor SPACE")
            return False
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    # Soporte para 'async with'
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()