
from typing import Optional
import aiohttp


class SpaceClient:
    
    def __init__(self, url: str, api_key: str, timeout: int = 5000):
        # Validación de parámetros
        if not url or not api_key:
            raise ValueError("Se requieren url y api_key")
        
        # Configuración básica
        self.http_url = f"{url.rstrip('/')}/api/v1"
        self.api_key = api_key
        self.timeout = aiohttp.ClientTimeout(total=timeout/1000)  # ms a segundos
        
        # Inicialización de módulos
        self.contracts = None  # necesitamos construirlos
        self.featureEvaluators = None # Tenemos que cosntruirlo aun FeatureModule(self)
        
        # Sesión HTTP (se crea bajo demanda)
        self._session: Optional[aiohttp.ClientSession] = None

        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Crea o reutiliza una sesión HTTP."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={'x-api-key': self.api_key},
                timeout=self.timeout
            )
        return self._session

    async def is_connected_to_space(self) -> bool:
        """Verifica la conexión con el servidor."""
        try:
            session = await self._get_session()
            async with session.get(
                f"{self.http_url}/healthcheck",
                skip_auto_headers=['x-api-key']  # Healthcheck no necesita autenticación
            ) as response:
                data = await response.json()
                return response.status == 200 and bool(data.get("message"))
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False

    async def close(self) -> None:
        """Cierra la sesión HTTP."""
        if self._session and not self._session.closed:
            await self._session.close()

    # Soporte para 'async with'
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
