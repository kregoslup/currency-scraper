from rest_framework.generics import ListAPIView

from project.apps.scraper.models import ExchangeRate, Currency
from project.apps.scraper.serializers import ExchangeRateSerializer, CurrencySerializer


class ExchangeRatesListView(ListAPIView):
    serializer_class = ExchangeRateSerializer
    queryset = ExchangeRate.objects.all()


class CurrenciesListView(ListAPIView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
