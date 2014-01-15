"""
this file contains all models used by the balance_manager app
"""
from django.db import models
import requests, json, datetime, decimal

class Exchange(models.Model):
    """
    each exchange is stored in the database and works as a
    central hub for apis and currencies
    """
    exchange_id = models.AutoField(primary_key=True)
    exchange_name = models.CharField(max_length=20)
    
    #defines the possible types of currencies traded on an exchange
    EXCHANGE_TYPE_CHOICES = (
        ('CC', 'crypto'),
        ('FC', 'fiat'),
        ('CF', 'crypto and fiat'),
    )
    exchange_type = models.CharField(max_length=2, choices=EXCHANGE_TYPE_CHOICES)
    
    def __str__(self):
        return self.exchange_name
    
class Currency_Pair(models.Model):
    """
    Currency Pairs are used by different APIs
    """
    pair_name = models.CharField(max_length=20)
    currency_from = models.ForeignKey('Currency', related_name="currency_from_set", null=True, blank=True)
    currency_to = models.ForeignKey('Currency', related_name="currency_to_set", null=True, blank=True)
    
    def __str__(self):
        return self.pair_name

class Api(models.Model):
    """
    the api class is always linked to an exchange and a currency pair
    it provides the needed api url for the chosen exchange
    """
    exchange = models.ForeignKey(Exchange)
    api_url = models.CharField(max_length=100)
    pair = models.ForeignKey(Currency_Pair)
    
    def __str__(self):
        return self.api_url

class Currency(models.Model):
    """
    each currency is stored in the database and can be linked to an exchange
    """
    exchanges = models.ManyToManyField(Exchange, null=True, blank=True, related_name="exchanges")
    currency_name = models.CharField(max_length=20)
    
    #defines the type choices a currency can have
    CURRENCY_TYPE_CHOICES = (
        ('CC', 'crypto'),
        ('FC', 'fiat'),
    )
    currency_type = models.CharField(max_length=2, choices=CURRENCY_TYPE_CHOICES, default="CC")
    
    def __str__(self):
        return self.currency_name
    
class Balance(models.Model):
    """
    a balance is where the user can store data about his owned currencies
    """
    currency = models.ForeignKey(Currency)
    amount = models.DecimalField(max_digits=18, decimal_places=8, null=True)
    wallet_adress = models.CharField(max_length=64, null=True)
    exchange = models.ForeignKey(Exchange, null=True)
    fiat_value = models.DecimalField(max_digits=18, decimal_places=8, null=True)
    btc_value = models.DecimalField(max_digits=18, decimal_places=8, null=True)
    
    def __str__(self):
        return self.currency.currency_name

    def calc_btc_value(self):
        """
        calculates and saves the btc value of a balance object based on the chosen exchange
        """
        currency_from = self.currency
        if self.currency == UserData.objects.get(pk=1).crypto_currency:
            self.btc_value = self.amount
            self.save()
            return True
        else:
            # get the pair object that matches the balance currency
            supported_pair = Currency_Pair.objects.get(currency_from=self.currency)
            
            # get the api url by filtering the api objects to only show the ones linked to the picked
            # exchange from the balance object.
            # from this queryset get the api url that matches the supported pair
            api_url = Api.objects.filter(exchange=self.exchange).get(pair=supported_pair).api_url
            ticker = get_ticker(api_url)
            
            if ticker != False:
                self.btc_value = decimal.Decimal(ticker['last']) * self.amount
                self.save()
                return True
            
            else:
                return False

    
    def calc_fiat_value(self):
        """
        calculates the fiat value of a balance object based on the chosen exchange
        """
        used_exchange = UserData.objects.get(pk=1).fiat_exchange
        api_url = Api.objects.get(exchange=used_exchange).api_url
        ticker = get_ticker(api_url)
        
        if ticker != False:
            fiat_value = decimal.Decimal(ticker['last']) * self.btc_value
            return fiat_value
        
        else:
            return False
    
    def save_fiat_value(self, fiat_value):
        """
        saves the fiat value to the database
        
        Argument:
        fiat_value -- fiat value of a chosen balance of type decimal
        """
        try:
            if fiat_value > 0:
                self.fiat_value = fiat_value
                self.save()
                return True
            else:
                return False
        except:
            return False
    
class UserData(models.Model):
    """
    stores basic changable settings and the overall sum the user ownes
    """
    fiat_currency = models.ForeignKey(Currency, related_name="fiat_currency", limit_choices_to = {'currency_type': 'FC'})
    fiat_exchange = models.ForeignKey(Exchange, limit_choices_to = {'exchange_type': 'FC'})
    fiat_sum = models.DecimalField(max_digits=18, decimal_places=8, null=True)
    
    # different conversion crypto currencies might be added later on
    # for now a change is not possible(as not practical) and btc is always used
    crypto_currency = models.ForeignKey(Currency, related_name="crypto_currency", limit_choices_to = {'currency_type': 'CC'})
    
    def save_fiat_sum(self, fiat_sum):
        """
        saves the summed up fiat value of all balances
        
        Argument:
        fiat_sum -- summed up fiat values of all balances of type decimal
        """
        try:
            if fiat_sum > 0:
                self.fiat_sum = fiat_sum
                self.save()
                return True
            
            else:
                return False
        
        except:
            return False
        
# utility functions used by classes or in views
def get_ticker(url):
    """
    performs a request to the api url given as argument which returns a json object.
    the data from the request is converted to a python dictionary and returned
    
    Argument:
    url -- a http url to a json api for a specific exchange and currency
    """
    try:
        r = requests.get(url)
        
        #converts the json data into a python dictionary
        ticker = r.json()
        return ticker
    
    except:
        return False

def timestamp_to_datetime(timestamp):
    """
    simple date conversion function, that converts a unix timestamp to human readable time
    this function is not used in the current version of the app.
    
    Argument:
    timestamp -- a unix timestamp stored as an integer
    """
    time = datetime.datetime.fromtimestamp(timestamp)
    return time