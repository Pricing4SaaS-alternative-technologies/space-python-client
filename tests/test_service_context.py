import aiohttp
import pytest
import tempfile
import uuid
import os

class TestServiceContext:
    
    @pytest.mark.asyncio
    async def test_get_service(self, space_client):
        unique_id = uuid.uuid4().hex[:8]
        service_name = f"Test_{unique_id}"
        
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
    type: DOMAIN"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml)
            temp_path = f.name
        try:
            await space_client.service_context.add_service(temp_path)
            service = await space_client.service_context.get_service(service_name)
            
            assert service is not None
            assert service["name"] == service_name
            
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
            
        print(f"Servicio obtenido: {service}")

    @pytest.mark.asyncio
    async def test_get_service_not_found(self, space_client):
        service_name = f"NotFound_{uuid.uuid4().hex[:8]}"
        try:
            
            await space_client.service_context.get_service(service_name)

        except aiohttp.ClientResponseError as e:
            assert e.status == 404
            assert e.message == "Not Found"

    @pytest.mark.asyncio
    async def test_add_service(self, space_client):
        service_name = f"New_{uuid.uuid4().hex[:8]}"
        
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
    type: DOMAIN"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml)
            temp_path = f.name
        
        try:
            result = await space_client.service_context.add_service(temp_path)
            assert result is not None
            assert result["name"] == service_name
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
        print(f"Servicio añadido: {result}")
    @pytest.mark.asyncio
    async def test_add_pricing_validation(self, space_client):
        """Test: validaciones de add_pricing"""
        with pytest.raises(ValueError, match="Se requiere url o service_file"):
            await space_client.service_context.add_pricing("test")
        
        with pytest.raises(ValueError, match="Solo se permite url o service_file"):
            await space_client.service_context.add_pricing(
                service_name="test",
                url="dummy",
                service_file=b"dummy"
            )

    @pytest.mark.asyncio
    async def test_get_pricing(self, space_client):
        unique_id = uuid.uuid4().hex[:8]
        service_name = f"Test_{unique_id}"
        
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
    type: DOMAIN"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml)
            temp_path = f.name
        try:
            await space_client.service_context.add_service(temp_path)
            pricing = await space_client.service_context.get_pricing(service_name,"1.0.0")
            
            assert pricing is not None
            assert pricing["currency"] == "USD"
            assert "basic" in pricing["features"]
            
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
        print(f"Pricing obtenido: {pricing}")

    @pytest.mark.asyncio 
    async def test_get_pricing_not_found(self, space_client):
        """Test: get_pricing con servicio no existente"""
        service_name = f"NoPricing_{uuid.uuid4().hex[:8]}"
        try:
            
            await space_client.service_context.get_pricing(service_name, "1.0.0")
        except aiohttp.ClientResponseError as e:
            assert e.status == 404
            assert e.message == "Not Found"
            

    @pytest.mark.asyncio
    async def test_change_pricing_availability_without_fallback_subscription(self, space_client):
        """Test de change_pricing_availability"""
        unique_id = uuid.uuid4().hex[:8]
        service_name = f"ChangeTest_{unique_id}"
        
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
    type: DOMAIN"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml)
            temp_path = f.name
        
        try: 
            await space_client.service_context.add_service(temp_path)
            await space_client.service_context.change_pricing_availability(
                service_name=service_name,
                pricing_version="1.0.0",
                availability="ARCHIVED",
                fallback_subscription=None
            )
  
        except ValueError as e:
            #si entramos aqui es corredcto
            assert str(e) == "Fallback subscription is required when archiving a pricing version"
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass


    @pytest.mark.asyncio
    async def test_change_pricing_availability_to_non_existent(self, space_client):
        """Test de change_pricing_availability"""
        unique_id = uuid.uuid4().hex[:8]
        service_name = f"ChangeTest_{unique_id}"
        
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
    type: DOMAIN"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml)
            temp_path = f.name
        
        try: 
            await space_client.service_context.add_service(temp_path)
            await space_client.service_context.change_pricing_availability(
                service_name=service_name,
                pricing_version="1.0.0",
                availability="PUBLISHED",
                fallback_subscription=None
            )
  
        except ValueError as e:
            #si entramos aqui es corredcto
            assert str(e) == "Invalid availability type"
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
            
            
    @pytest.mark.asyncio
    async def test_change_pricing_availability_with_fallback_subscription(self, space_client):
        """Test de change_pricing_availability con fallback_subscription"""
        unique_id = uuid.uuid4().hex[:8]
        service_name = f"FallbackTest_{unique_id}"
        
        unique_id2 = uuid.uuid4().hex[:8]
        service_name2 = f"FallbackTest_{unique_id2}"
        
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

        yaml2 = f"""saasName: {service_name}
syntaxVersion: "3.0"
version: "1.0.1"
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
    price: 1.0
    unit: user/month
    features: null
    usageLimits: null"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml)
            temp_path = f.name
            
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml2)
            temp_path2 = f.name
        
        try:
            await space_client.service_context.add_service(temp_path)
            await space_client.service_context.add_pricing(
                service_name=service_name,
                url=temp_path2
            )
            
            # Crear un objeto de suscripción de fallback
            fallback_subscription = {
                "subscriptionPlan": "BASIC",
                "additionalAddOns": {}
            }
            print('este es el name', await space_client.service_context.get_service(service_name))
            
            # Intentar archivar con fallback subscription
            result = await space_client.service_context.change_pricing_availability(
                service_name=service_name,
                pricing_version="1.0.0",
                availability="ARCHIVED",
                fallback_subscription=fallback_subscription
            )
            
            print('resultado final:', result)
            assert result is not None
            
        finally:
            try:
                os.unlink(temp_path)
                os.unlink(temp_path2)
            except:
                pass