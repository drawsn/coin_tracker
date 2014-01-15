"""
describes the available views where data can be viewed, entered and manipulated by the app user
"""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext, loader

import requests
import json
import datetime
import decimal

from balance_manager.models import Exchange, Currency_Pair, Api, Currency, Balance, UserData

class IndexView(generic.ListView):
    """
    links to the template of the entry page of the app with links to different parts of the app
    """
    template_name = 'balance_manager/index.html'
    
    def get_queryset(self):
        """
        a query set which simply passes
        
        declared because a generic view expect either a model or a queryset
        usesful queries can be added later if needed
        """
        pass

class ExchangeListView(generic.ListView):
    """
    links to the template showing a list of all supported exchanges
    offers the option to view details about a chosen exchange
    """
    template_name = 'balance_manager/exchange_list.html'
    context_object_name = 'exchange_list'

    def get_queryset(self):
        """
        Return all available exchanges ordered by the exchange name
        """
        return Exchange.objects.all().order_by('exchange_name')
    
class ExchangeDetailView(generic.DetailView):
    """
    shows more information about a selected exchange
    """
    model = Exchange
    template_name = 'balance_manager/exchange_detail.html'
    
def balance_list(request):
    """
    shows a list of all available balances and the option to view details about them
    also checks the apis for up to date price values and save them to the db
    """
    try:
        fiat_sum = decimal.Decimal(0.0)
        
        # calc the values for all balances, sum them up and save them
        for balance in Balance.objects.all():
            btc_value = balance.calc_btc_value()
            fiat_value = balance.calc_fiat_value()
            fiat_sum += fiat_value
            balance.save_fiat_value(fiat_value)
        
        # save the fiat sum to the user data table
        UserData.objects.get(pk=1).save_fiat_sum(fiat_sum)

        balance_list = Balance.objects.all().order_by('currency')
        fiat_sum = UserData.objects.get(pk=1).fiat_sum
        
        # renders the template and passes the defined variables to it
        return render(request, 'balance_manager/balance_list.html', { 'balance_list': balance_list, 'fiat_sum': fiat_sum })
    
    except:
        return False
        

def create_balance(request):
    """
    view for the form to create a crypto currency balance
    """
    
    # list of all available currencies of type crypto currency
    currency_list = Currency.objects.all().filter(currency_type='CC').order_by('currency_name')
    
    try:
        # tries to create a balance object with the users input data
        b = Balance(currency=Currency.objects.get(pk=request.POST['currency']), amount=request.POST['amount'], wallet_adress=request.POST['wallet'])
        save = True
        
        # check if balance for the chosen currency already exists
        # if yes, balance cant be created and therefore shouldnt be saved
        for balance in Balance.objects.all():
            if b.currency == balance.currency:
                save = False
        
        # checks if balance should be saved otherwise returns to the creation form
        if save:
            b.save()    
        else:
            return render(request, 'balance_manager/create_balance.html', {
            'currency_list': currency_list,
            'error_message': "Balance already exists.",
            })
        
        return HttpResponseRedirect(reverse('balance_manager:balance'))
    
    except:
        return render(request, 'balance_manager/create_balance.html', { 'currency_list': currency_list, })

def select_fiat(request):
    """
    view for the form to select a fiat currency to convert to
    """
    
    # list of all available fiat currencies
    currency_list = Currency.objects.all().filter(currency_type='FC').order_by('currency_name')
    
    # currently set currency
    used_currency = UserData.objects.get(pk=1).fiat_currency
    
    try:
        # tries to save the chosen currency object to the user data object
        user_data = UserData.objects.get(pk=1)
        user_data.fiat_currency = Currency.objects.get(pk=request.POST['currency'])
        user_data.save()
        return HttpResponseRedirect(reverse('balance_manager:select_fiat'))
    
    except:
        return render(request, 'balance_manager/select_fiat.html', { 'currency_list': currency_list, 'used_currency': used_currency, })   

def select_fiat_exchange(request):
    """
    view for the form to select a fiat exchange used for calculations
    """
    
    # list of all available exchanges excluding crypto currency exchanges
    exchange_list = Exchange.objects.exclude(exchange_type='CC').order_by('exchange_name')
    
    # currently set fiat exchange
    used_exchange = UserData.objects.get(pk=1).fiat_exchange
    
    try:
        # tries to save the chosen exchange object to the user data object
        user_data = UserData.objects.get(pk=1)
        user_data.fiat_exchange = Exchange.objects.get(pk=request.POST['exchange'])
        user_data.save()
        return HttpResponseRedirect(reverse('balance_manager:select_fiat_exchange'))
    
    except:
        return render(request, 'balance_manager/select_fiat_exchange.html', { 'exchange_list': exchange_list, 'used_exchange': used_exchange, })

def select_crypto_exchange_list(request):
    """
    view to list the currencies of your balances
    gives the user the option to choose the balance to change the exchange for
    """
    balance_list = Balance.objects.all().order_by('currency')
    return render(request, 'balance_manager/select_crypto_exchange_list.html', { 'balance_list': balance_list, })

def select_crypto_exchange(request, pk):
    """
    view that gives the option to change the crypto exchange for a balance choosen before
    
    Argument:
    pk -- takes the id(primary key) of a balance as argument
    """
    
    # gets the balance object that matches the primary key value of the argument
    balance = Balance.objects.get(pk=pk)
    
    # currency object of the selected balance
    selected_currency = Balance.objects.get(pk=pk).currency
    
    # the possible exchanges linked to the balance currency
    exchange_list = selected_currency.exchanges
    
    # the balances currency name
    chosen_balance = Balance.objects.get(pk=pk).currency.currency_name
    
    # the currently selected exchange for the balance 
    used_exchange = Balance.objects.get(pk=pk).exchange
    
    try:
        #tries to save the selected exchange to the chosen balance object
        balance_data = Balance.objects.get(pk=pk)
        balance_data.exchange = Exchange.objects.get(pk=request.POST['exchange'])
        balance_data.save()
        return HttpResponseRedirect(reverse('balance_manager:select_crypto_exchange_list'))
    
    except:
        return render(request, 'balance_manager/select_crypto_exchange.html', { 'exchange_list': exchange_list,
                                                                               'chosen_balance': chosen_balance,
                                                                               'used_exchange': used_exchange,
                                                                               'balance': balance, })


