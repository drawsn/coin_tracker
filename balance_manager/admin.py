"""
all models are registered here for admin view
some views are customzied for special purpose
"""
from django.contrib import admin
from balance_manager.models import Exchange, Api, Currency_Pair, Currency, Balance, UserData

class ApiInline(admin.TabularInline):
    """
    defines the Api model so it can be created from the exchange creation view
    """
    model = Api
    extra = 1
    
class ExchangeAdmin(admin.ModelAdmin):
    """
    uses the api model for inline creation. also list display is customized
    """
    inlines = [ApiInline]
    
    list_display = ('exchange_name', 'exchange_type')
    
admin.site.register(Exchange, ExchangeAdmin)

class ApiAdmin(admin.ModelAdmin):
    """
    custom field layout for api creation and api list display
    """
    fields = ['exchange', 'pair', 'api_url']

    list_display = ('exchange', 'pair', 'api_url')

admin.site.register(Api, ApiAdmin)

admin.site.register(Currency_Pair)

admin.site.register(Currency)

admin.site.register(Balance)

admin.site.register(UserData)