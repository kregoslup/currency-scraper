from project.apps.scraper.models import Currency, ExchangeRate


def populate_from_scraper(scraped):
    for rate in scraped:
        base, _ = Currency.objects.get_or_create(
            code=rate['base']
        )
        target, _ = Currency.objects.get_or_create(
            code=rate['target']
        )
        ExchangeRate.objects.get_or_create(
            base=base,
            target=target,
            date=rate['date'],
            defaults={
                'rate': rate['rate']
            }
        )
