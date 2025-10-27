from typing import Optional
from dataclasses import dataclass
@dataclass
class SpaceConnectionOptions:
    url: str
    api_key: str
    timeout: Optional[int] = None

    def __repr__(self):
        return f"SpaceConnectionOptions(url={self.url}, api_key={self.api_key}, timeout={self.timeout})"
        