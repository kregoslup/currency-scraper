# Generated by Django 2.0.4 on 2018-04-14 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=4, max_digits=5)),
                ('date', models.DateTimeField()),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='base_rates', to='scraper.Currency')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='target_rates', to='scraper.Currency')),
            ],
        ),
    ]
