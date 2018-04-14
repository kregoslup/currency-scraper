from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, null=False, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True)


class ExchangeRate(models.Model):
    rate = models.DecimalField(null=False, blank=False, decimal_places=4, max_digits=5)
    from_curr = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='from_rates')
    to_curr = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='to_rates')
    date = models.DateTimeField(null=False, blank=False)
