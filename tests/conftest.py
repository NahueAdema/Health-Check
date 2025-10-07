import pytest
from unittest.mock import AsyncMock, patch
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(scope="session", autouse=True)
def setup_mocks():
    """Mock global que se ejecuta antes de todo"""
    with patch("deps.redis_client") as mock:
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock()
        mock_redis.setex = AsyncMock()
        mock_redis.get = AsyncMock()
        mock_redis.keys = AsyncMock(return_value=[])
        mock_redis.close = AsyncMock()
        mock.return_value = mock_redis
        yield mock_redis