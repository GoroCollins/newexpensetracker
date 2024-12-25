# tests_models.py
import pytest
from ..models import Currency, ExchangeRate
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_create_local_currency(currency_factory):
    currency = currency_factory(code="USD", is_local=True)
    assert currency.is_local is True

@pytest.mark.django_db
def test_prevent_multiple_local_currencies(currency_factory):
    currency_factory(is_local=True)
    with pytest.raises(ValidationError):
        currency_factory(code="EUR", is_local=True)

@pytest.mark.django_db
def test_update_currency_to_local(currency_factory):
    foreign_currency = currency_factory(is_local=False)
    currency_factory(is_local=True)
    with pytest.raises(ValidationError):
        foreign_currency.is_local = True
        foreign_currency.save()

@pytest.mark.django_db
def test_prevent_foreign_currency_without_local(currency_factory):
    with pytest.raises(ValidationError):
        currency_factory(is_local=False)

@pytest.mark.django_db
def test_create_exchange_rate(currency_factory, exchange_rate_factory):
    currency = currency_factory(is_local=False)
    exchange_rate = exchange_rate_factory(currency=currency, rate=1.25)
    assert exchange_rate.currency == currency
    assert exchange_rate.rate == 1.25

@pytest.mark.django_db
def test_prevent_negative_exchange_rate(currency_factory):
    currency = currency_factory(is_local=False)
    with pytest.raises(ValidationError):
        ExchangeRate.objects.create(currency=currency, rate=-5.00)

@pytest.mark.django_db
def test_prevent_zero_exchange_rate(currency_factory):
    currency = currency_factory(is_local=False)
    with pytest.raises(ValidationError):
        ExchangeRate.objects.create(currency=currency, rate=0.00)

@pytest.mark.django_db
def test_local_currency_cannot_have_exchange_rate(currency_factory):
    local_currency = currency_factory(is_local=True)
    with pytest.raises(ValidationError):
        ExchangeRate.objects.create(currency=local_currency, rate=1.00)

@pytest.mark.django_db
def test_exchange_rate_string_representation(exchange_rate_factory):
    exchange_rate = exchange_rate_factory(rate=1.15)
    expected_str = f"Exchange rate for {exchange_rate.currency} as at {exchange_rate.created_at.strftime('%I:%M:%S %p')} on {exchange_rate.created_at.strftime('%B')}, {exchange_rate.created_at.strftime('%d')}, {exchange_rate.created_at.strftime('%Y')}"
    assert str(exchange_rate) == expected_str