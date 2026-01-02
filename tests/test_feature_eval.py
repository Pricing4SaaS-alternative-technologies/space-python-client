import aiohttp
import pytest
import uuid
import tempfile
import os

class TestFeatureEvalModule:
    
    @pytest.mark.asyncio
    async def test_evaluate_existing_feature_success(self, space_client):
        """Test de evaluación exitosa con feature que existe en el servicio"""
        service_name = f"Service_{uuid.uuid4().hex[:8]}"
        feature_name = "basicFeature"
        
        yaml = f"""saasName: {service_name}
syntaxVersion: "3.0"
version: "1.0.0"
createdAt: "2025-01-01"
currency: USD
features:
  {feature_name}:
    description: Basic test feature
    valueType: BOOLEAN
    defaultValue: true
    type: DOMAIN
    expression: pricingContext['features']['basicFeature']
plans:
  BASIC:
    description: Basic plan
    price: 0.0
    unit: user/month
    features:
      {feature_name}: true
    usageLimits: null"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml)
            temp_path = f.name
        
        try:
            await space_client.service_context.add_service(temp_path)
            print(f" Service created: {service_name}")
            
            user_id = uuid.uuid4().hex[:8]
            user_name = f"user_{user_id}"
            contract_to_create = {
                "userContact": {
                    "userId": user_id,
                    "username": user_name
                },
                "billingPeriod": {
                    "autoRenew": True,
                    "renewalDays": 30
                },
                "contractedServices": {
                    service_name: "1.0.0"
                },
                "subscriptionPlans": {	
                    service_name: "BASIC"
                },
                "subscriptionAddOns": {}
            }
            
            contract_response = await space_client.contracts.add_contract(contract_to_create)
            print(f" Contract created for user {user_id}")
            
            result = await space_client.featureEvaluators.evaluate(
                user_id=user_id,
                feature_id=f"{service_name.lower()}-{feature_name}"
            )
            
            assert result is not None
            assert hasattr(result, 'eval')
            
            print(f" Feature evaluation completed. eval={result.eval}")
            
            if result.error:
                print(f"Error: {result.error.code}: {result.error.message}")
            else:
                print(f"Feature is {'enabled' if result.eval else 'disabled'}")
                
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
    
    @pytest.mark.asyncio
    async def test_generate_pricing_token_success(self, space_client):
        """Test de generación de token exitosa"""
        service_name = f"Service_{uuid.uuid4().hex[:8]}"
        
        yaml = f"""saasName: {service_name}
syntaxVersion: "3.0"
version: "1.0.0"
createdAt: "2025-01-01"
currency: USD
features:
  basicFeature:
    description: Basic test feature
    valueType: BOOLEAN
    defaultValue: true
    type: DOMAIN
plans:
  BASIC:
    description: Basic plan
    price: 0.0
    unit: user/month
    features: null
    usageLimits: null"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml)
            temp_path = f.name
        
        try:
            await space_client.service_context.add_service(temp_path)
            
            user_id = uuid.uuid4().hex[:8]
            contract_to_create = {
                "userContact": {
                    "userId": user_id,
                    "username": f"user_{user_id}"
                },
                "billingPeriod": {
                    "autoRenew": True,
                    "renewalDays": 30
                },
                "contractedServices": {
                    service_name: "1.0.0"
                },
                "subscriptionPlans": {	
                    service_name: "BASIC"
                },
                "subscriptionAddOns": {}
            }
            
            await space_client.contracts.add_contract(contract_to_create)
            print(f" Contract created for user {user_id}")
            
            token = await space_client.featureEvaluators.generate_user_pricing_token(user_id)
            
            assert token is not None
            assert isinstance(token, str)
            assert len(token) > 0
            print(f" Aqui está el token: {token}")
                
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
    
    @pytest.mark.asyncio
    async def test_evaluate_nonexistent_feature(self, space_client):
        """Test de evaluación con feature que no existe"""
        service_name = f"Service_{uuid.uuid4().hex[:8]}"
        
        yaml = f"""saasName: {service_name}
syntaxVersion: "3.0"
version: "1.0.0"
createdAt: "2025-01-01"
currency: USD
features:
  existing_feature:
    description: Existing feature
    valueType: BOOLEAN
    defaultValue: true
    type: DOMAIN
plans:
  BASIC:
    description: Basic plan
    price: 0.0
    unit: user/month
    features: null
    usageLimits: null"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml)
            temp_path = f.name
        
        try:
            await space_client.service_context.add_service(temp_path)
            
            user_id = uuid.uuid4().hex[:8]
            contract_to_create = {
                "userContact": {
                    "userId": user_id,
                    "username": f"user_{user_id}"
                },
                "billingPeriod": {
                    "autoRenew": True,
                    "renewalDays": 30
                },
                "contractedServices": {
                    service_name: "1.0.0"
                },
                "subscriptionPlans": {	
                    service_name: "BASIC"
                },
                "subscriptionAddOns": {}
            }
            
            await space_client.contracts.add_contract(contract_to_create)
            print(f" Contract created for user {user_id}")
            
            result = await space_client.featureEvaluators.evaluate(
                user_id=user_id,
                feature_id="nonexistent_feature_123"
            )
            
            assert result is not None
            assert hasattr(result, 'eval')
            assert result.eval is False
            assert result.error is not None
            assert result.error.code == "FLAG_NOT_FOUND"
            print(f" Nonexistent feature correctly returns {result.error.code} error")
                
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass

#-------------------------------------------------------------------------------------------------------------
# ESTE TEST NO FUNCIONA, PENDIEDNTE DE REVISAR CON ALEJANDRO
#-------------------------------------------------------------------------------------------------------------
#     @pytest.mark.asyncio
#     async def test_revert_evaluation(self, space_client):
#         """Test de reversión de evaluación"""
#         service_name = f"Service_{uuid.uuid4().hex[:8]}"
#         feature_name = "basicFeature"
        
#         yaml = f"""saasName: {service_name}
# syntaxVersion: "3.0"
# version: "1.0.0"
# createdAt: "2025-01-01"
# currency: USD
# features:
#   {feature_name}:
#     description: Basic test feature
#     valueType: BOOLEAN
#     defaultValue: true
#     type: DOMAIN
#     expression: pricingContext['features']['basicFeature']
# plans:
#   BASIC:
#     description: Basic plan
#     price: 0.0
#     unit: user/month
#     features:
#       {feature_name}: true
#     usageLimits: null"""
        
#         with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
#             f.write(yaml)
#             temp_path = f.name
        
#         try:
#             await space_client.service_context.add_service(temp_path)
            
#             user_id = uuid.uuid4().hex[:8]
#             contract_to_create = {
#                 "userContact": {
#                     "userId": user_id,
#                     "username": f"user_{user_id}"
#                 },
#                 "billingPeriod": {
#                     "autoRenew": True,
#                     "renewalDays": 30
#                 },
#                 "contractedServices": {
#                     service_name: "1.0.0"
#                 },
#                 "subscriptionPlans": {	
#                     service_name: "BASIC"
#                 },
#                 "subscriptionAddOns": {}
#             }
            
#             await space_client.contracts.add_contract(contract_to_create)
#             print(f" Contract created for user {user_id}")
            
#             eval_result = await space_client.featureEvaluators.evaluate(
#                 user_id=user_id,
#                 feature_id=f"{service_name.lower()}-{feature_name}"
#             )
            
#             assert eval_result is not None
#             print(f" Feature evaluated successfully")
            
#             revert_result = await space_client.featureEvaluators.revert_evaluation(
#                 user_id=user_id,
#                 feature_id=f"{service_name.lower()}-{feature_name}"
#             )
            
#             """La reversión podría fallar (retorna False) si no hay evaluación previa para revertir"""
#             assert isinstance(revert_result, bool)
#             print(f" Revert operation completed. Result: {revert_result}")
                
#         finally:
#             try:
#                 os.unlink(temp_path)
#             except:
#                 pass



    @pytest.mark.asyncio
    async def test_evaluate_with_options(self, space_client):
        """Test de evaluación con diferentes opciones"""
        service_name = f"Service_{uuid.uuid4().hex[:8]}"
        
        yaml = f"""saasName: {service_name}
syntaxVersion: "3.0"
version: "1.0.0"
createdAt: "2025-01-01"
currency: USD
features:
  api_access:
    description: API Access
    valueType: BOOLEAN
    defaultValue: true
    type: DOMAIN
    expression: pricingContext['features']['api_access'] && subscriptionContext['api_calls'] <= pricingContext['usageLimits']['api_calls']
usageLimits:
    api_calls:
        description: 'api_calls'
        valueType: NUMERIC
        defaultValue: 10
        unit: timer
        type: RENEWABLE
        period:
          unit: DAY
          value: 30
        linkedFeatures:
          - api_access
plans:
  BASIC:
    description: Basic plan
    price: 0.0
    unit: user/month
    features: 
        api_access:
          value: true
    usageLimits:
        api_calls:
          value: 10

        
    """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml)
            temp_path = f.name
        
        try:
            await space_client.service_context.add_service(temp_path)
            
            user_id = uuid.uuid4().hex[:8]
            contract_to_create = {
                "userContact": {
                    "userId": user_id,
                    "username": f"user_{user_id}"
                },
                "billingPeriod": {
                    "autoRenew": True,
                    "renewalDays": 30
                },
                "contractedServices": {
                    service_name: "1.0.0"
                },
                "subscriptionPlans": {	
                    service_name: "BASIC"
                },
                "subscriptionAddOns": {}
            }
            
            await space_client.contracts.add_contract(contract_to_create)
            print(f"Contract created for user {user_id}")
            
            result = await space_client.featureEvaluators.evaluate(
                user_id=user_id,
                feature_id=f"{service_name.lower()}-api_access",
                options={"server": True}
            )
            
            resultadoAntiguo = result
            print(f" Evaluation with server option completed: {resultadoAntiguo}")
            
            result = await space_client.featureEvaluators.evaluate(
                user_id=user_id,
                feature_id=f"{service_name.lower()}-api_access",
                expected_consumption={f"{service_name.lower()}-api_calls": 1}
            )
            
            resultadoNuevo = result
            assert resultadoAntiguo.used != resultadoNuevo.used
            print(f"Evaluation with expected consumption completed: {resultadoNuevo}")
                
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass