from django.conf import settings
from django_cron import CronJobBase, Schedule

from project.apps.scraper.scraper import scrape


class ExchangeRatesCron(CronJobBase):
    RUN_EVERY_MINS = settings.CRON_MINUTES_INTERVAL

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'project.apps.scraper.crons.ExchangeRatesCron'

    def do(self):
        scrape()
