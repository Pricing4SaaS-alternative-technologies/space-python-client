from pydantic import BaseModel
from typing import Dict, Union, Optional

class FeatureError(BaseModel):
    code: str
    message: str

class FeatureEvaluationResult(BaseModel):
    eval: bool

    # Union type allows for introducing either int or bool values in the dict
    used: Optional[Dict[str, Union[int, bool]]] = None
    limit: Optional[Dict[str, Union[int, bool]]] = None
    error: Optional[FeatureError] = None