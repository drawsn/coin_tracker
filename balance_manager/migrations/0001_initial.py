# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = []

    operations = [
        migrations.CreateModel(
            name = 'Exchange',
            options = {},
            bases = (models.Model,),
            fields = [('exchange_id', models.AutoField(serialize=False, primary_key=True),), ('exchange_name', models.CharField(max_length=20),), ('exchange_type', models.CharField(choices=(('CC', 'crypto',), ('FC', 'fiat',), ('CF', 'crypto and fiat',),), max_length=2),)],
        ),
        migrations.CreateModel(
            name = 'Currency',
            options = {},
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID'),), ('currency_name', models.CharField(max_length=20),), ('currency_type', models.CharField(choices=(('CC', 'crypto',), ('FC', 'fiat',),), max_length=2, default='CC'),), ('exchanges', models.ManyToManyField(null=True, to='balance_manager.Exchange', blank=True),)],
        ),
        migrations.CreateModel(
            name = 'Balance',
            options = {},
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID'),), ('currency', models.ForeignKey(to_field='id', to='balance_manager.Currency'),), ('amount', models.DecimalField(null=True, decimal_places=8, max_digits=18),), ('wallet_adress', models.CharField(null=True, max_length=64),), ('exchange', models.ForeignKey(null=True, to='balance_manager.Exchange', to_field='exchange_id'),), ('fiat_value', models.DecimalField(null=True, decimal_places=8, max_digits=18),), ('btc_value', models.DecimalField(null=True, decimal_places=8, max_digits=18),)],
        ),
        migrations.CreateModel(
            name = 'Currency_Pair',
            options = {},
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID'),), ('pair_name', models.CharField(max_length=20),), ('currency_from', models.ForeignKey(to='balance_manager.Currency', null=True, to_field='id', blank=True),), ('currency_to', models.ForeignKey(to='balance_manager.Currency', null=True, to_field='id', blank=True),)],
        ),
        migrations.CreateModel(
            name = 'Api',
            options = {},
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID'),), ('exchange', models.ForeignKey(to_field='exchange_id', to='balance_manager.Exchange'),), ('api_url', models.CharField(max_length=100),), ('pair', models.ForeignKey(to_field='id', to='balance_manager.Currency_Pair'),)],
        ),
        migrations.CreateModel(
            name = 'UserData',
            options = {},
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID'),), ('fiat_currency', models.ForeignKey(to_field='id', to='balance_manager.Currency'),), ('fiat_exchange', models.ForeignKey(to_field='exchange_id', to='balance_manager.Exchange'),), ('fiat_sum', models.DecimalField(null=True, decimal_places=8, max_digits=18),), ('crypto_currency', models.ForeignKey(to_field='id', to='balance_manager.Currency'),)],
        ),
    ]
