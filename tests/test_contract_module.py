
import os
import tempfile
import uuid
import pytest

from app.models.contracts import UserContact


class TestContractModule:
	
	@pytest.mark.asyncio
	async def test_contract_correct_creation(self, space_client):
		#Creación del servicio dummy sobre el que generar el contrato
		service_name = f"Service_{uuid.uuid4().hex[:8]}"
		yaml = f"""saasName: {service_name}
syntaxVersion: "3.0"
version: "1.0.0"
createdAt: "2025-01-01"
currency: USD
features:
  basic:
    description: Test
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
		finally:
			try:
				os.unlink(temp_path)
			except:
				pass
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
		#Generamos el contrato y comprobamos que existe
		response= await space_client.contracts.add_contract(contract_to_create)
		assert response["userContact"]["userId"] == user_id
		print("Test OK :) Created Contract:", response)

	@pytest.mark.asyncio
	async def test_contract_invalid_data_creation(self, space_client):
		#Creación del servicio dummy sobre el que generar el contrato
		service_name = f"Service_{uuid.uuid4().hex[:8]}"
		yaml = f"""saasName: {service_name}
syntaxVersion: "3.0"
version: "1.0.0"
createdAt: "2025-01-01"
currency: USD
features:
  basic:
    description: Test
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
		finally:
			try:
				os.unlink(temp_path)
			except:
				pass
		user_id = uuid.uuid4().hex[:8]
		user_name = f"user_{user_id}"
		contract_to_create_errors = {
			"userContact": {
				"userId": user_id,
				"username": user_name
			},
			"billingPeriod": {
				"autoRenew": True,
				"renewalDays": 30
			},
			"contractedServices": {
				'TomatoMeter': "1.0.0"
       		},
			"subscriptionPlans": {	
				service_name: "BASIC"
			},
			"subscriptionAddOns": {}
		}
		#Generamos el contrato y comprobamos que existe
		try:
			await space_client.contracts.add_contract(contract_to_create_errors)
		except Exception as e:
			assert True
			print("Test OK :) Caught expected exception for invalid data:", e)
	

	@pytest.mark.asyncio
	async def test_get_user_id_contract_from_client(self, space_client):
		#Creación del servicio dummy sobre el que generar el contrato
		service_name = f"Service_{uuid.uuid4().hex[:8]}"
		yaml = f"""saasName: {service_name}
syntaxVersion: "3.0"
version: "1.0.0"
createdAt: "2025-01-01"
currency: USD
features:
  basic:
    description: Test
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
		finally:
			try:
				os.unlink(temp_path)
			except:
				pass
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
		contract_to_create2 = {
			"userContact": {
				"userId": user_id,
				"username": user_name
			},
			"billingPeriod": {
				"autoRenew": True,
				"renewalDays": 45
			},
			"contractedServices": {
				service_name: "1.0.0"
       		},
			"subscriptionPlans": {	
				service_name: "BASIC"
			},
			"subscriptionAddOns": {}
		}
		#Generamos el contrato y comprobamos que existe
		await space_client.contracts.add_contract(contract_to_create)
		#await space_client.contracts.add_contract(contract_to_create2)
		contract = await space_client.contracts.get_user_id_contract(user_id)
		#print("Retrieved contracts:", contract)
		assert contract["userContact"]["userId"] == user_id
		print("Test OK :) user contract correctly retrieved:", contract)

    
