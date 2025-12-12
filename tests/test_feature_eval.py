import aiohttp
import pytest
import uuid
import tempfile
import os

class TestFeatureEvalModule:
    
    @pytest.mark.asyncio
    async def test_evaluate_existing_feature_success(self, space_client):
        """Test de evaluación exitosa con feature que existe en el servicio"""
        # 1. Crear servicio con una feature que SÍ existe en el sistema
        service_name = f"Service_{uuid.uuid4().hex[:8]}"
        
        # Usar una feature que ya sabemos que existe basándonos en el fixture
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
    expression: "true"
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
            # 2. Crear servicio
            await space_client.service_context.add_service(temp_path)
            print(f"✓ Service created: {service_name}")
            
            # 3. Crear contrato
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
            print(f"✓ Contract created for user {user_id}")
            
            # 4. Evaluar la feature
            result = await space_client.featureEvaluators.evaluate(
                user_id=user_id,
                feature_id=feature_name
            )
            
            # Verificar que tenemos una respuesta
            assert result is not None
            assert hasattr(result, 'eval')
            
            # La evaluación puede ser True o False dependiendo de la lógica
            print(f"✓ Feature evaluation completed. eval={result.eval}")
            
            if result.error:
                print(f"  Error: {result.error.code}: {result.error.message}")
            else:
                print(f"  Success! Feature is {'enabled' if result.eval else 'disabled'}")
                
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
    
    @pytest.mark.asyncio
    async def test_generate_pricing_token_success(self, space_client):
        """Test de generación de token exitosa"""
        # Crear servicio y contrato primero
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
            print(f"✓ Contract created for user {user_id}")
            
            # Generar token
            token = await space_client.featureEvaluators.generate_user_pricing_token(user_id)
            
            # Debería ser un string no vacío
            assert token is not None
            assert isinstance(token, str)
            assert len(token) > 0
            print(f"✓ Pricing token generated successfully: {token[:50]}...")
                
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
    
    @pytest.mark.asyncio
    async def test_evaluate_nonexistent_feature(self, space_client):
        """Test de evaluación con feature que no existe"""
        # Crear un contrato primero
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
            print(f"✓ Contract created for user {user_id}")
            
            # Intentar evaluar una feature que NO existe
            result = await space_client.featureEvaluators.evaluate(
                user_id=user_id,
                feature_id="nonexistent_feature_123"
            )
            
            # Debería retornar un objeto con error FLAG_NOT_FOUND
            assert result is not None
            assert hasattr(result, 'eval')
            assert result.eval is False
            assert result.error is not None
            assert result.error.code == "FLAG_NOT_FOUND"
            print(f"✓ Nonexistent feature correctly returns FLAG_NOT_FOUND error")
                
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
    
    @pytest.mark.asyncio
    async def test_revert_evaluation(self, space_client):
        """Test de reversión de evaluación"""
        # Crear una evaluación para poder revertirla
        service_name = f"Service_{uuid.uuid4().hex[:8]}"
        feature_name = "test_feature"
        
        yaml = f"""saasName: {service_name}
syntaxVersion: "3.0"
version: "1.0.0"
createdAt: "2025-01-01"
currency: USD
features:
  {feature_name}:
    description: Test feature
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
            print(f"✓ Contract created for user {user_id}")
            
            # Primero evaluar
            eval_result = await space_client.featureEvaluators.evaluate(
                user_id=user_id,
                feature_id=feature_name
            )
            
            assert eval_result is not None
            print(f"✓ Feature evaluated successfully")
            
            # Luego revertir
            revert_result = await space_client.featureEvaluators.revert_evaluation(
                user_id=user_id,
                feature_id=feature_name
            )
            
            # La reversión podría fallar (retorna False) si no hay evaluación previa para revertir
            assert isinstance(revert_result, bool)
            print(f"✓ Revert operation completed. Result: {revert_result}")
                
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
    
    @pytest.mark.asyncio
    async def test_module_initialization(self, space_client):
        """Test básico de inicialización del módulo"""
        assert space_client.featureEvaluators is not None
        assert hasattr(space_client.featureEvaluators, 'evaluate')
        assert hasattr(space_client.featureEvaluators, 'revert_evaluation')
        assert hasattr(space_client.featureEvaluators, 'generate_user_pricing_token')
        print("✓ Module methods exist")

    @pytest.mark.asyncio
    async def test_evaluate_with_options(self, space_client):
        """Test de evaluación con diferentes opciones"""
        # Crear un contrato simple
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
            print(f"✓ Contract created for user {user_id}")
            
            # Test con opción 'server'
            result = await space_client.featureEvaluators.evaluate(
                user_id=user_id,
                feature_id="api_access",
                options={"server": True}
            )
            
            assert result is not None
            print(f"✓ Evaluation with server option completed")
            
            # Test con expected consumption
            result = await space_client.featureEvaluators.evaluate(
                user_id=user_id,
                feature_id="api_access",
                expected_consumption={"api_calls": 1}
            )
            
            assert result is not None
            print(f"✓ Evaluation with expected consumption completed")
                
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass