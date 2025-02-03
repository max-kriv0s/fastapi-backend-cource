from unittest.mock import AsyncMock
import pytest


@pytest.fixture
def fake_redis():
    """Создаём мок Redis"""
    redis_mock = AsyncMock()
    redis_mock.get.return_value = None  # Симулируем отсутствие кеша
    redis_mock.set.return_value = None  # Подменяем set, чтобы он не выполнялся

    return redis_mock