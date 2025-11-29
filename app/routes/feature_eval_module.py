from __future__ import annotations
import aiohttp
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from .config import SpaceClient
import aiohttp
from typing import Dict, Union
from app.models.feature_eval_result import FeatureEvaluationResult

class FeatureEvalModule:
    def __init__(self, space_client: SpaceClient):
        self.space_client = space_client
        self.url = "http://localhost:8080/features"

    async def evaluate(self, 
                       user_id: str, 
                       feature_id: str, 
                       expected_consumption: Dict[str, Union[int, float]] = {}, 
                       options: Dict[str, bool] = {}):
        """Evalúa una característica para un usuario específico."""
        session = await self.space_client._get_session()
        try:
            query_params = []
            if options.get('details'):
                query_params.append("details=true")
            if options.get('server'):
                query_params.append("server=true")
                
            query_string = f"?{'&'.join(query_params)}" if query_params else ""
            response = await session.post(f"{self.url}/{user_id}/{feature_id}{query_string}", json=expected_consumption)
            response.raise_for_status()

            result = await response.json()
            feature_evaluation_result = FeatureEvaluationResult(**result)

            return feature_evaluation_result

        except aiohttp.ClientResponseError as e:
            print(f"Error evaluating feature: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    async def revert_evaluation(self, 
                                user_id: str, 
                                feature_id: str, 
                                revert_to_latest: bool = True):
        """Revierte la evaluación optimista de una característica."""
        session = await self.space_client._get_session()
        try:
            params = {"revert": "true", "latest": revert_to_latest}
            response = await session.post(f"{self.url}/{user_id}", params=params)
            response.raise_for_status()
            return True

        except aiohttp.ClientResponseError as e:
            print(f"Error reverting evaluation for feature {feature_id}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    async def generate_user_pricing_token(self, 
                                          user_id: str):
        """Genera un token de precios para un usuario."""
        session = await self.space_client._get_session()
        try:
            response = await session.post(f"{self.url}/{user_id}/pricing-token")
            response.raise_for_status()
            result = await response.json()
            return result.get("pricingToken", "")

        except aiohttp.ClientResponseError as e:
            print(f"Error generating pricing token: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise