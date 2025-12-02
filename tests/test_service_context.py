import os
import pytest
import aiohttp
from unittest.mock import AsyncMock, Mock

from app.routes.service_context_module import ServiceContextModule, availability_type


class _DummyCtx:
	def __init__(self, resp):
		self._resp = resp

	async def __aenter__(self):
		return self._resp

	async def __aexit__(self, exc_type, exc, tb):
		return False


@pytest.mark.asyncio
async def test_get_service_success(space_client, mock_aiohttp_session, mock_aiohttp_response):
	mock_aiohttp_response.json.return_value = {"name": "svc"}
	space_client._get_session = AsyncMock(return_value=mock_aiohttp_session)

	module = ServiceContextModule(space_client)
	result = await module.get_service("svc")

	assert result == {"name": "svc"}
	mock_aiohttp_session.get.assert_awaited()


@pytest.mark.asyncio
async def test_get_pricing_success(space_client, mock_aiohttp_session, mock_aiohttp_response):
	mock_aiohttp_response.json.return_value = {"price": 9.99}
	space_client._get_session = AsyncMock(return_value=mock_aiohttp_session)

	module = ServiceContextModule(space_client)
	result = await module.get_pricing("svc", {"units": 10})

	assert result == {"price": 9.99}
	mock_aiohttp_session.post.assert_awaited()


@pytest.mark.asyncio
async def test_post_with_file_path_success(space_client, mock_aiohttp_session, mock_aiohttp_response, monkeypatch):
	# usar fixture de resource real
	from tests.conftest import TEST_SERVICE_PATH

	mock_aiohttp_response.json.return_value = {"ok": True}
	# algunos métodos usan get_session (sin guion), así que exponemos ambos
	space_client.get_session = AsyncMock(return_value=mock_aiohttp_session)

	# Dummy FormData que acepta add_field con posicionals o keyword filename
	class DummyFormData:
		def __init__(self):
			self.fields = []
		def add_field(self, name, value, *args, **kwargs):
			self.fields.append((name, value, args, kwargs))

	monkeypatch.setattr(aiohttp, "FormData", DummyFormData)

	module = ServiceContextModule(space_client)
	result = await module._post_with_file_path("/services/x/pricings", TEST_SERVICE_PATH)

	assert result == {"ok": True}
	mock_aiohttp_session.post.assert_awaited()


@pytest.mark.asyncio
async def test_post_with_file_success(space_client, mock_aiohttp_session, mock_aiohttp_response, monkeypatch):
	mock_aiohttp_response.json.return_value = {"ok": True}
	space_client.get_session = AsyncMock(return_value=mock_aiohttp_session)

	class DummyFormData:
		def __init__(self):
			self.fields = []
		def add_field(self, name, value, *args, **kwargs):
			self.fields.append((name, value, args, kwargs))

	monkeypatch.setattr(aiohttp, "FormData", DummyFormData)

	module = ServiceContextModule(space_client)
	result = await module._post_with_file("/services/x/pricings", b"content: yaml")

	assert result == {"ok": True}
	mock_aiohttp_session.post.assert_awaited()


@pytest.mark.asyncio
async def test_post_with_url_success(space_client, mock_aiohttp_session, mock_aiohttp_response):
	mock_aiohttp_response.json.return_value = {"ok": True}
	space_client.get_session = AsyncMock(return_value=mock_aiohttp_session)

	module = ServiceContextModule(space_client)
	result = await module._post_with_url("/services/x/pricings", "http://example.com/pricing.yml")

	assert result == {"ok": True}
	mock_aiohttp_session.post.assert_awaited()


@pytest.mark.asyncio
async def test_add_pricing_errors(space_client):
	module = ServiceContextModule(space_client)

	with pytest.raises(ValueError):
		await module.add_pricing("svc")

	with pytest.raises(ValueError):
		await module.add_pricing("svc", url="u", service_file=b"x")


@pytest.mark.asyncio
async def test_add_pricing_routes_calls(space_client):
	module = ServiceContextModule(space_client)

	module._post_with_url = AsyncMock(return_value={"ok": "url"})
	r = await module.add_pricing("svc", url="http://remote/file.yml")
	assert r == {"ok": "url"}

	module._post_with_file_path = AsyncMock(return_value={"ok": "path"})
	# ruta local detectada (no comienza por http)
	r2 = await module.add_pricing("svc", url="./relative/path.yml")
	assert r2 == {"ok": "path"}

	module._post_with_file = AsyncMock(return_value={"ok": "file"})
	r3 = await module.add_pricing("svc", service_file=b"bytes")
	assert r3 == {"ok": "file"}


@pytest.mark.asyncio
async def test_change_pricing_availability_validation(space_client):
	module = ServiceContextModule(space_client)

	with pytest.raises(ValueError):
		await module.change_pricing_availability("svc", "v1", "invalid")

	with pytest.raises(ValueError):
		await module.change_pricing_availability("svc", "v1", availability_type.ARCHIVED, None)


@pytest.mark.asyncio
async def test_change_pricing_availability_success(space_client, mock_aiohttp_session, mock_aiohttp_response):
	mock_aiohttp_response.json.return_value = {"ok": True}
	# parchear sesión
	mock_aiohttp_session.patch = AsyncMock(return_value=mock_aiohttp_response)
	space_client.get_session = AsyncMock(return_value=mock_aiohttp_session)

	module = ServiceContextModule(space_client)
	fb = {"subscriptionId": "sub-1"}
	res = await module.change_pricing_availability("svc", "v1", availability_type.ARCHIVED, fb)

	assert res == {"ok": True}
	mock_aiohttp_session.patch.assert_awaited()


@pytest.mark.asyncio
async def test_add_service_file_not_found(space_client):
	module = ServiceContextModule(space_client)
	missing = os.path.join(os.path.dirname(__file__), "no-such-file.yml")

	with pytest.raises(FileNotFoundError):
		await module.add_service(missing)


@pytest.mark.asyncio
async def test_add_service_success(space_client, mock_aiohttp_response, monkeypatch):
	from tests.conftest import TEST_SERVICE_PATH

	mock_aiohttp_response.json.return_value = {"created": True}

	# session.post es usado con 'async with', así que devolvemos un contexto
	session = AsyncMock()
	# usar Mock para que session.post(...) devuelva directamente el contexto (no una coroutine)
	session.post = Mock(return_value=_DummyCtx(mock_aiohttp_response))
	space_client._get_session = AsyncMock(return_value=session)

	class DummyFormData:
		def __init__(self):
			self.fields = []
		def add_field(self, name, value, *args, **kwargs):
			self.fields.append((name, value, args, kwargs))

	monkeypatch.setattr(aiohttp, "FormData", DummyFormData)

	module = ServiceContextModule(space_client)
	res = await module.add_service(TEST_SERVICE_PATH)

	assert res == {"created": True}

