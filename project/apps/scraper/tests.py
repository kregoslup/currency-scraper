from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from project.apps.scraper.models import ExchangeRate


class ExchangeRatesViewTest(APITestCase):

    fixtures = [
        'currencies.json',
        'rates.json'
    ]

    def test_list_rates(self):
        url = reverse('exchange-rates')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), ExchangeRate.objects.count())

