import asyncio
from reprlib import Repr

import pytest
from httpx import AsyncClient
from integration.app.fastapi import create_app

my_repr = Repr()
my_repr.maxstring = 50


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture
async def client():
    async with AsyncClient(app=create_app(), base_url="http://testserver") as client:
        yield client


@pytest.fixture
def non_mocked_hosts() -> list:
    return ["testserver"]
