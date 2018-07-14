from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from project.apps.scraper.models import ExchangeRate, Currency


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


class TestParseExchangeLinks(TestCase):
    payload = """
    <ul class="zebraList">
	<li><a class="rss" href="/rss/press.html">Press releases, speeches, interviews, press conference transcripts</a> </li>
	<li><a class="rss"
		href="/rss/statpress.html">Statistical press releases </a> </li>
	<li><a class="rss" href="/rss/pub.html">Publications, in pdf format </a> </li>
	<li><a class="rss"
		href="/rss/wppub.html">Working Papers, in pdf format </a> </li>
	<li><a class="rss"
		href="/rss/legalacts.html">Legal acts, Opinions, Decisions </a> </li>
	<li><a
		class="rss" href="/rss/operations.html">Recent open market operations and ad hoc ECB communication </a> </li>
	<li><a
		class="rss" href="/rss/procurements.html">Open procurements, award notices and lists of suppliers </a> </li>
	<li><a class="rss" href="/rss/yc.html">Euro area yield curve </a> </li>
	<li> <a class="rss" href="/rss/rbu.html">Research bulletin </a> </li>
    </ul>
    <h2>Euro foreign exchange reference rates RSS links</h2>
    <ul class="zebraList">
	<li><a class="rss" href="/rss/fxref-usd.html">US dollar (USD)</a></li>
	<li><a class="rss" href="/rss/fxref-jpy.html">Japanese yen (JPY)</a></li>
	</ul>
    """

    def test_parse_links(self):
        from project.apps.scraper.scraper import _parse_exchange_links as parse
        links = list(parse(self.payload))

        self.assertEqual(len(links), 2)
        self.assertIn('/rss/fxref-usd.html', links)
        self.assertIn('/rss/fxref-jpy.html', links)


class TestParseExchangeRates(TestCase):
    payload = """
    <item>
    </item>
        <item rdf:about="http://www.ecb.europa.eu/stats/exchange/eurofxref/html/eurofxref-graph-usd.en.html?date=2018-04-13&amp;rate=1.2317">
        <title xml:lang="en">1.2317 USD = 1 EUR 2018-04-13 ECB Reference rate</title>
        <link/>http://www.ecb.europa.eu/stats/exchange/eurofxref/html/eurofxref-graph-usd.en.html?date=2018-04-13&amp;rate=1.2317
        <description xml:lang="en">1 EUR buys 1.2317 US dollar (USD) - The reference exchange rates are published both by electronic market information providers and on the ECB's website shortly after the concertation procedure has been completed. Reference rates are published according to the same  calendar as the TARGET system.</description>
        <dc:date>2018-04-13T14:15:00+01:00</dc:date>
        <dc:language>en</dc:language>
        <cb:statistics>
        <cb:country>U2</cb:country>
        <cb:institutionabbrev>ECB</cb:institutionabbrev>
        <cb:exchangerate>
        <cb:value decimals="4" frequency="daily">1.2317</cb:value>
        <cb:basecurrency unit_mult="0">EUR</cb:basecurrency>
        <cb:targetcurrency>USD</cb:targetcurrency>
        <cb:ratetype>Reference rate</cb:ratetype>
        </cb:exchangerate>
        </cb:statistics>
        </item>
    """

    def test_parse_exchange_rate(self):
        from project.apps.scraper.scraper import _parse_exchange_rates as parse

        rates = parse(self.payload)

        self.assertEqual(len(rates), 1)
        rates = next(iter(rates))

        expected = {
            'date': '2018-04-13T14:15:00+01:00',
            'rate': '1.2317',
            'base': 'EUR',
            'target': 'USD'
        }

        self.assertEqual(rates['base'], expected['base'])
        self.assertEqual(rates['target'], expected['target'])
        self.assertEqual(rates['date'], expected['date'])
        self.assertEqual(rates['rate'], expected['rate'])


class TestPopulateFromScraper(TestCase):
    def test_populate(self):
        scraped = [
            {
                'date': '2018-04-13T14:15:00+01:00',
                'rate': '1.2317',
                'base': 'EUR',
                'target': 'USD'
            },
            {
                'date': '2018-04-13T14:15:00+01:00',
                'rate': '1.2317',
                'base': 'EUR',
                'target': 'USD'
            },
            {
                'date': '2018-04-13T14:15:00+01:00',
                'rate': '1.2317',
                'base': 'EUR',
                'target': 'PLN'
            }
        ]

        from project.apps.scraper.tasks import populate_from_scraper

        populate_from_scraper(scraped)

        self.assertEqual(Currency.objects.count(), 3)
        self.assertEqual(ExchangeRate.objects.count(), 2)
