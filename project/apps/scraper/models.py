from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, null=False, blank=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.code)


class ExchangeRate(models.Model):
    rate = models.DecimalField(null=False, blank=False, decimal_places=4, max_digits=5)
    base = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='base_rates')
    target = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='target_rates')
    date = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return "{} / base: {} target: {}, date: {}".format(
            self.pk,
            self.base.code,
            self.target.code,
            self.date
        )

    class Meta:
        unique_together = (
            'rate', 'target', 'date'
        )
