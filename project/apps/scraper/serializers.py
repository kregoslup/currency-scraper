from rest_framework import serializers

from project.apps.scraper.models import Currency, ExchangeRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name')


class ExchangeRateSerializer(serializers.ModelSerializer):
    from_currency = serializers.SlugRelatedField(
        slug_field='from_curr__code',
        read_only=True
    )
    to_currency = serializers.SlugRelatedField(
        slug_field='to_curr__code',
        read_only=True
    )

    class Meta:
        model = ExchangeRate
        fields = ('rate', 'from_currency', 'to_currency', 'date')
