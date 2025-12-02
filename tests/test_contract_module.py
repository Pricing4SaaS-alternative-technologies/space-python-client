import aiohttp
import pytest
from types import SimpleNamespace


class MockResponse:
	def __init__(self, json_data=None, status=200, raise_exc=False, error_text="error"):
		self._json = json_data
		self.status = status
		self._raise = raise_exc
		self._error_text = error_text

	async def __aenter__(self):
		return self

	async def __aexit__(self, exc_type, exc, tb):
		return False

	async def json(self):
		return self._json

	async def text(self):
		return self._error_text

	def raise_for_status(self):
		if self._raise:
			req = SimpleNamespace(real_url="mock://test")
			raise aiohttp.ClientResponseError(request_info=req, history=(), status=self.status, message=self._error_text)
		return None


class MockSession:
	def __init__(self, method_response_map=None):
		# method_response_map: dict of (method, url) -> MockResponse
		self.method_response_map = method_response_map or {}
		self.last_call = None

	def _make(self, method, url, json=None):
		self.last_call = (method, url, json)
		key = (method, url)
		return self.method_response_map.get(key, MockResponse(json_data=None))

	def get(self, url, **kwargs):
		return self._make("GET", url, None)

	def post(self, url, json=None, **kwargs):
		return self._make("POST", url, json)

	def put(self, url, json=None, **kwargs):
		return self._make("PUT", url, json)


@pytest.mark.asyncio
async def test_get_contracts_success(monkeypatch):
	from app.routes.config import SpaceClient

	client = SpaceClient("http://localhost:5403", "apikey")

	expected = [{"id": "c1"}]
	url = f"{client.http_url}/contracts/user1"
	session = MockSession({("GET", url): MockResponse(json_data=expected)})

	async def _get_session():
		return session

	monkeypatch.setattr(client, "_get_session", _get_session)

	result = await client.contracts.get_contracts("user1")
	assert result == expected
	assert session.last_call[0] == "GET"


@pytest.mark.asyncio
async def test_get_contracts_client_error(monkeypatch):
	from app.routes.config import SpaceClient

	client = SpaceClient("http://localhost:5403", "apikey")
	url = f"{client.http_url}/contracts/user1"
	session = MockSession({("GET", url): MockResponse(json_data=None, raise_exc=True, status=404, error_text="Not Found")})

	async def _get_session():
		return session

	monkeypatch.setattr(client, "_get_session", _get_session)

	result = await client.contracts.get_contracts("user1")
	assert result is None


@pytest.mark.asyncio
async def test_add_contract_success(monkeypatch):
	from app.routes.config import SpaceClient
	from app.models.contracts import ContractToCreate

	client = SpaceClient("http://localhost:5403", "apikey")
	payload = {"name": "contract1"}
	url = f"{client.http_url}/contracts"
	session = MockSession({("POST", url): MockResponse(json_data={"id": "c1"}, status=201)})

	async def _get_session():
		return session

	monkeypatch.setattr(client, "_get_session", _get_session)

	# Using a plain dict is fine for the contract_to_create param in tests
	result = await client.contracts.add_contract(payload)
	assert result == {"id": "c1"}
	assert session.last_call[0] == "POST"


@pytest.mark.asyncio
async def test_add_contract_client_error(monkeypatch):
	from app.routes.config import SpaceClient

	client = SpaceClient("http://localhost:5403", "apikey")
	url = f"{client.http_url}/contracts"
	session = MockSession({("POST", url): MockResponse(json_data=None, raise_exc=True, status=400, error_text="Bad Request")})

	async def _get_session():
		return session

	monkeypatch.setattr(client, "_get_session", _get_session)

	result = await client.contracts.add_contract({"name": "x"})
	assert result is None


@pytest.mark.asyncio
async def test_update_contract_subscription_success(monkeypatch):
	from app.routes.config import SpaceClient

	client = SpaceClient("http://localhost:5403", "apikey")
	url = f"{client.http_url}/contracts/user1"
	session = MockSession({("PUT", url): MockResponse(json_data={"ok": True})})

	async def _get_session():
		return session

	monkeypatch.setattr(client, "_get_session", _get_session)

	result = await client.contracts.update_contract_subscription("user1", {"plan": "pro"})
	assert result == {"ok": True}


@pytest.mark.asyncio
async def test_update_contract_subscription_client_error(monkeypatch):
	from app.routes.config import SpaceClient

	client = SpaceClient("http://localhost:5403", "apikey")
	url = f"{client.http_url}/contracts/user1"
	session = MockSession({("PUT", url): MockResponse(json_data=None, raise_exc=True, status=500, error_text="Server Error")})

	async def _get_session():
		return session

	monkeypatch.setattr(client, "_get_session", _get_session)

	result = await client.contracts.update_contract_subscription("user1", {"plan": "pro"})
	assert result is None

