# conftest.py
import pytest
from .factories import CurrencyFactory, ExchangeRateFactory

@pytest.fixture
def currency_factory():
    return CurrencyFactory

@pytest.fixture
def exchange_rate_factory():
    return ExchangeRateFactory