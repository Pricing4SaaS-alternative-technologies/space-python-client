from app_SpacePyCl.utils import SpaceConnectionOptions
from app_SpacePyCl.routes.config import SpaceClient

def connect(options: SpaceConnectionOptions) -> SpaceClient:
    """
    Conecta usando SpaceConnectionOptions. Los valores de `url`, `api_key` y `timeout` son obligatorios.
    """
    options.validate()

    return SpaceClient(url=options.url, api_key=options.api_key, timeout=options.timeout)