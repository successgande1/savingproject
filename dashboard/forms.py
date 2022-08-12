from django.contrib.auth.models import User
import random
from django import forms

from .models import Customer, Deposit

import secrets
#Generate Account Number
account = secrets.randbits(7)

#class for Customer Account Form
class CustomerAccountForm(forms.ModelForm): 
    account = "".join(str(random.randint(0, 10)) for _ in range(4))
    #Set Read Only Field on Form
    account_number = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), initial=account)
    

    class Meta:
        model = Customer
        fields = ['account_number','surname','othernames','address','phone']

#class for Deposit Form
class CustomerDepositForm(forms.ModelForm):
   
    class Meta:
       model = Deposit
       fields = ['deposit_amount']