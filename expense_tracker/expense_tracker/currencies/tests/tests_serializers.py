import pytest
from ..api.serializers import CurrencySerializer, ExchangeRateSerializer
from ..models import Currency, ExchangeRate
from rest_framework.exceptions import ValidationError

@pytest.mark.django_db
def test_currency_serializer_valid(currency_factory):
    currency = currency_factory(is_local=True)
    serializer = CurrencySerializer(currency)
    expected_data = {
        "code": currency.code,
        "description": currency.description,
        "is_local": currency.is_local,
        "created_by": None,  # Replace with username if `created_by` is set
        "created_at": currency.created_at.isoformat(),
        "modified_by": None,  # Replace with username if `modified_by` is set
        "modified_at": currency.modified_at.isoformat(),
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_currency_serializer_validation(currency_factory):
    currency_factory(is_local=True)  # Existing local currency
    serializer = CurrencySerializer(data={"code": "EUR", "description": "Euro", "is_local": True})
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    assert "Only one local currency can exist." in str(excinfo.value)


@pytest.mark.django_db
def test_exchange_rate_serializer_valid(currency_factory, exchange_rate_factory):
    currency = currency_factory(is_local=False)
    exchange_rate = exchange_rate_factory(currency=currency, rate=1.25)
    serializer = ExchangeRateSerializer(exchange_rate)
    expected_data = {
        "id": exchange_rate.id,
        "currency": {
            "code": currency.code,
            "description": currency.description,
            "is_local": currency.is_local,
        },
        "rate": str(exchange_rate.rate),
        "created_by": None,  # Replace with username if `created_by` is set
        "created_at": exchange_rate.created_at.isoformat(),
        "modified_by": None,  # Replace with username if `modified_by` is set
        "modified_at": exchange_rate.modified_at.isoformat(),
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_exchange_rate_serializer_local_currency(currency_factory):
    local_currency = currency_factory(is_local=True)
    serializer = ExchangeRateSerializer(data={"currency": local_currency.id, "rate": 1.25})
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    assert "Cannot assign exchange rates to the local currency." in str(excinfo.value)