from typing import Optional

class SpaceConnectionOptions:
    def __init__(self, url: str, api_key: str, timeout: Optional[int] = 5000):
        self.url = url
        self.api_key = api_key
        self.timeout = timeout

    def validate(self):
        """Método para validar los parámetros de la conexión."""
        if not self.url or not self.api_key:
            raise ValueError("Both 'url' and 'apiKey' are required to connect to Space.")
        
        if self.timeout is not None and self.timeout <= 0:
            raise ValueError("Invalid 'timeout' value. It must be a positive number.")
        
        if not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("Invalid 'url'. It must start with 'http://' or 'https://'.")
        
        if not isinstance(self.api_key, str) or not self.api_key.strip():
            raise ValueError("Invalid 'apiKey'. It must be a non-empty string.")

    def __repr__(self):
        return f"SpaceConnectionOptions(url={self.url}, api_key={self.api_key}, timeout={self.timeout})"
