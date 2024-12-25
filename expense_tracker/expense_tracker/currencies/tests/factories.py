# factories.py
# import factory
# from ..models import Currency, ExchangeRate

# class CurrencyFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Currency

#     code = factory.Faker("currency_code")  # Random currency code like "USD"
#     description = factory.Faker("sentence", nb_words=3)  # Random description
#     is_local = False  # Default is foreign currency

# class ExchangeRateFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = ExchangeRate

#     currency = factory.SubFactory(CurrencyFactory)  # Related currency object
#     rate = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)

import factory
from ..models import Currency, ExchangeRate
from django.conf import settings

User = settings.AUTH_USER_MODEL

class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency

    code = factory.Sequence(lambda n: f"CUR{n}")
    description = factory.Faker("currency_name")
    is_local = False


class ExchangeRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExchangeRate

    currency = factory.SubFactory(CurrencyFactory)
    rate = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)