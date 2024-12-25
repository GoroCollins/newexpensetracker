import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Currency, ExchangeRate


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_currency_list(api_client, currency_factory):
    # Arrange: Create sample currencies
    currency_factory.create_batch(3)

    # Act: Fetch the list of currencies
    url = reverse("currency-list")
    response = api_client.get(url)

    # Assert: Ensure all currencies are returned
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


@pytest.mark.django_db
def test_currency_create(api_client):
    # Arrange: New currency data
    url = reverse("currency-list")
    data = {"code": "USD", "description": "US Dollar", "is_local": True}

    # Act: Create a new currency
    response = api_client.post(url, data)

    # Assert: Ensure the currency is created successfully
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["code"] == "USD"


@pytest.mark.django_db
def test_currency_filter_by_is_local(api_client, currency_factory):
    # Arrange: Create local and foreign currencies
    currency_factory(is_local=True)
    currency_factory(is_local=False)

    # Act: Filter by local currencies
    url = reverse("currency-list")
    response = api_client.get(url, {"is_local": "true"})

    # Assert: Ensure only the local currency is returned
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["is_local"] is True


@pytest.mark.django_db
def test_exchange_rate_list(api_client, exchange_rate_factory):
    # Arrange: Create sample exchange rates
    exchange_rate_factory.create_batch(3)

    # Act: Fetch the list of exchange rates
    url = reverse("exchangerate-list")
    response = api_client.get(url)

    # Assert: Ensure all exchange rates are returned
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


@pytest.mark.django_db
def test_exchange_rate_create(api_client, currency_factory):
    # Arrange: Create a currency and prepare exchange rate data
    currency = currency_factory()
    url = reverse("exchangerate-list")
    data = {"currency": currency.id, "rate": "1.25"}

    # Act: Create a new exchange rate
    response = api_client.post(url, data)

    # Assert: Ensure the exchange rate is created successfully
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["rate"] == "1.25"


@pytest.mark.django_db
def test_get_local_currency(api_client, currency_factory):
    # Arrange: Create a local currency
    currency_factory(is_local=True)

    # Act: Fetch the local currency using the API
    url = reverse("get-local-currency")
    response = api_client.get(url)

    # Assert: Ensure the correct local currency code is returned
    assert response.status_code == status.HTTP_200_OK
    assert response.data["local_currency_code"]


@pytest.mark.django_db
def test_get_local_currency_not_found(api_client):
    # Act: Attempt to fetch the local currency when none exists
    url = reverse("get-local-currency")
    response = api_client.get(url)

    # Assert: Ensure a 404 error is returned
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "error" in response.data

@pytest.mark.django_db
def test_create_exchange_rate_with_local_currency(api_client, currency_factory):
    # Create a local currency
    local_currency = currency_factory(is_local=True)
    
    # Attempt to create an exchange rate for the local currency
    response = api_client.post(
        "/api/exchangerates/",
        {"currency": local_currency.code, "rate": "1.50"},
        format="json",
    )
    
    # Assert that the response returns a 400 Bad Request
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Exchange rates cannot be assigned to local currencies." in response.data["non_field_errors"]

@pytest.mark.django_db
def test_create_exchange_rate_with_foreign_currency(api_client, currency_factory):
    # Create a foreign currency
    foreign_currency = currency_factory(is_local=False)
    
    # Create an exchange rate for the foreign currency
    response = api_client.post(
        "/api/exchangerates/",
        {"currency": foreign_currency.code, "rate": "1.50"},
        format="json",
    )
    
    # Assert that the response is successful
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["currency"]["code"] == foreign_currency.code