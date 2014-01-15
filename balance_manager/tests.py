from django.test import TestCase
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from balance_manager.models import Exchange, Currency_Pair, Api, Currency, Balance, UserData, get_ticker
from balance_manager.views import balance_list


class BalanceMethodTests(TestCase):
    fixtures = ['balance_manager.json']
    
    def test_save_fiat_value_with_value_zero(self):
        """
        save_fiat_value() should return False if the fiat value is 0
        """
        b1 = Balance.objects.all()[0]
        fiat_value = 0
        self.assertEqual(Balance.save_fiat_value(b1, fiat_value), False)
        
    def test_save_fiat_value_with_value_negative(self):
        """
        save_fiat_value() should return False if the fiat value is negative
        """
        b1 = Balance.objects.all()[0]
        fiat_value = -1
        self.assertEqual(Balance.save_fiat_value(b1, fiat_value), False)
        
    def test_save_fiat_value_with_string_argument(self):
        """
        save_fiat_value() should return False if the provided fiat value is a string
        """
        b1 = Balance.objects.all()[0]
        fiat_value = "string"
        self.assertEqual(Balance.save_fiat_value(b1, fiat_value), False)

    def test_save_fiat_value_with_correct_argument(self):
        """
        save_fiat_value() should return true if the provided fiat value is right
        """
        b1 = Balance.objects.all()[0]
        fiat_value = 100
        self.assertEqual(Balance.save_fiat_value(b1, fiat_value), True)
        
class UserDataMethodTest(TestCase):
    fixtures = ['balance_manager.json']
    
    def test_save_fiat_sum_with_value_zero(self):
        """
        save_fiat_value() should return False if the fiat value is 0
        """
        u1 = UserData.objects.all()[0]
        self.assertEqual(UserData.save_fiat_sum(u1, 0), False)
        
    def test_save_fiat_sum_with_value_negative(self):
        """
        save_fiat_value() should return False if the fiat value is negative
        """
        u1 = UserData.objects.all()[0]
        self.assertEqual(UserData.save_fiat_sum(u1, -1), False)
        
    def test_save_fiat_sum_with_string_argument(self):
        """
        save_fiat_value() should return False if the provided fiat value is a string
        """
        u1 = UserData.objects.all()[0]
        self.assertEqual(UserData.save_fiat_sum(u1, "string"), False)
        
    def test_save_fiat_sum_with_correct_data(self):
        """
        save_fiat_value() should return False if the provided fiat value is a string
        """
        u1 = UserData.objects.all()[0]
        self.assertEqual(UserData.save_fiat_sum(u1, 111.1), True)
        
class UtilityFunctionTests(TestCase):
    
    def test_get_ticker_with_no_string(self):
        self.assertEqual(get_ticker(123), False)
        
    def test_get_ticker_with_wrong_url(self):
        self.assertEqual(get_ticker("http://wrong.url"), False)
        
    def test_get_ticker_with_valid_url(self):
        self.assertEqual(isinstance(get_ticker("https://www.bitstamp.net/api/ticker/"), dict), True)
