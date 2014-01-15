"""
sets the browser urls inside the balance_manager app and the used view functions/classes
name is a value that can be used in django templates
"""

from django.conf.urls import patterns, url
from balance_manager import views

urlpatterns = patterns('',
    # app starting page with links to the implemented functions
    url(r'^$', views.IndexView.as_view(), name='index'),
    
    # page to select an exchange from a list to retrieve more information about it
    url(r'^exchanges/$', views.ExchangeListView.as_view(), name='exchanges'),
    
    # page showing details about the exchange chosen from the exchange list, the chosen object is is part of the url
    url(r'^exchanges/(?P<pk>\d+)/$', views.ExchangeDetailView.as_view(), name='detail'),
    
    # balance list page showing fiat values
    url(r'^balance/$', views.balance_list, name='balance_list'),
    
    # page to create a balance
    url(r'^create_balance/$', views.create_balance, name='create_balance'),
    
    # page to select the users fiat currency
    url(r'^select_fiat/$', views.select_fiat, name='select_fiat'),
    
    # page to select the users fiat exchange
    url(r'^select_fiat_exchange/$', views.select_fiat_exchange, name='select_fiat_exchange'),
    
    # page to select a balance to set a crypto currency exchange for
    url(r'^select_crypto_exchange_list/$', views.select_crypto_exchange_list, name='select_crypto_exchange_list'),
    
    # page to select a crypto currency exchange for a chosen balance, the chosen object is is part of the url
    url(r'^select_crypto_exchange_list/(?P<pk>\d+)/$', views.select_crypto_exchange, name='select_crypto_exchange'),

)