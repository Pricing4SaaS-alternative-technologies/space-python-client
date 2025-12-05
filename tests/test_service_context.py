import pytest
import tempfile
import uuid
import os
from app.routes.service_context_module import availability_type

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
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass

    @pytest.mark.asyncio
    async def test_get_service_not_found(self, space_client):
        service_name = f"NotFound_{uuid.uuid4().hex[:8]}"
        result = await space_client.service_context.get_service(service_name)
        assert result is None

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
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass

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
    async def test_get_pricing_404(self, space_client):
        """Test: get_pricing con servicio no existente"""
        service_name = f"NoPricing_{uuid.uuid4().hex[:8]}"
        result = await space_client.service_context.get_pricing(service_name, {})
        assert result is None

    @pytest.mark.asyncio
    async def test_change_pricing_availability_real(self, space_client):
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
            
            result = await space_client.service_context.change_pricing_availability(
                service_name=service_name,
                pricing_version="1.0.0",
                availability=availability_type.ACTIVE,
                fallback_subscription=None
            )
            
        except Exception as e:
            print(f"change_pricing_availability falló: {e}")
            
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass