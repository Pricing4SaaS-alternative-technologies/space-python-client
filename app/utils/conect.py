# connect.py
from dataclasses import dataclass
from typing import Optional, Union, Dict, Any
from config import SpaceClient 
from app.utils.__init__ import SpaceConnectionOptions

def connect(
    options: Optional[Union[SpaceConnectionOptions, Dict[str, Any]]] = None,
    url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: Optional[int] = None
) -> SpaceClient:

    if options is not None:
        if isinstance(options, dict):
            url = options.get("url", url)
            api_key = options.get("apiKey", options.get("api_key", api_key))
            timeout = options.get("timeout", timeout)
        elif isinstance(options, SpaceConnectionOptions):
            url = options.url if url is None else url
            api_key = options.api_key if api_key is None else api_key
            timeout = options.timeout if timeout is None else timeout
        else:
            raise TypeError("`options` debe ser dict o SpaceConnectionOptions.")

    if not url or not api_key:
        raise ValueError("Both 'url' and 'apiKey' are required to connect to Space.")

    if timeout is not None and (not isinstance(timeout, (int, float)) or timeout <= 0):
        raise ValueError("Invalid 'timeout' value. It must be a positive number.")

    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("Invalid 'url'. It must start with 'http://' or 'https://'.")

    if not isinstance(api_key, str) or api_key.strip() == "":
        raise ValueError("Invalid 'apiKey'. It must be a non-empty string.")

    eff_timeout = int(timeout) if timeout is not None else 5000

    return SpaceClient(url=url, api_key=api_key, timeout=eff_timeout)