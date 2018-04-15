import urllib.parse

import requests
from bs4 import BeautifulSoup

BASE_ADDRESS = 'https://www.ecb.europa.eu/'
EXCHANGE_RATES_RSS_HOME_ADDRESS = 'home/html/rss.en.html'


def _get_exchange_rates_links(address):
    response = requests.get(address)
    yield from _parse_exchange_links(response.text)


def _parse_exchange_links(payload):
    soup = BeautifulSoup(payload, 'html.parser')
    links = soup.find_all('a', href=lambda x: x and x.startswith('/rss/fxref-'))
    for link in links:
        if link:
            yield link.get('href')
        else:
            continue


def _get_exchange_rate(address):
    response = requests.get(address)
    return _parse_exchange_rates(response.text)


def _parse_exchange_rates(payload):
    soup = BeautifulSoup(payload)
    rates = soup.find_all('item')

    result = []
    for rate in rates:
        try:
            result.append({
                'date': rate.find('dc:date').string,
                'rate': rate.find('cb:value').string,
                'base': rate.find('cb:basecurrency').string,
                'target': rate.find('cb:targetcurrency').string
            })
        except AttributeError:
            continue

    return result


def scrape():
    result = []
    for link in _get_exchange_rates_links(urllib.parse.urljoin(
            BASE_ADDRESS,
            EXCHANGE_RATES_RSS_HOME_ADDRESS
    )):
        result.extend(_get_exchange_rate(
            urllib.parse.urljoin(
                BASE_ADDRESS,
                link
            )
        ))

    return result
