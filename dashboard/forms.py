from django.contrib.auth.models import User

from django import forms

from .models import Customer, Deposit

#class for Customer Account Form
class CustomerAccountForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['accountnumber','surname','othernames','address','phone']

#class for Deposit Form
#class CustomerDepositForm(forms.ModelForm):
   # class Meta:
       # model = Deposit
        #fields = ['accountnumber','surname','othernames','address','phone']