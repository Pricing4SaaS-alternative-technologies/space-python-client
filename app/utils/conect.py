from app.utils.__init__ import SpaceConnectionOptions
from config import SpaceClient

def connect(options: SpaceConnectionOptions) -> SpaceClient:
    """
    Conecta usando SpaceConnectionOptions. Los valores de `url`, `api_key` y `timeout` son obligatorios.
    """
    # Validar los parámetros de conexión
    options.validate()

    # Si los valores son correctos, creamos el SpaceClient
    return SpaceClient(url=options.url, api_key=options.api_key, timeout=options.timeout)