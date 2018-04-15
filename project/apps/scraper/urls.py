from django.urls import path

from project.apps.scraper.views import CurrenciesListView, ExchangeRatesListView


urlpatterns = [
    path('currencies/', CurrenciesListView.as_view()),
    path('rates/', ExchangeRatesListView.as_view(), name="exchange-rates")
]
