# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# import random
# from django import forms

# from .models import *

# import secrets

# #Create Customer Form
# class CreateUserForm(UserCreationForm):
#     email = forms.EmailField

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


# #Generate Account Number
# account = secrets.randbits(7)

# #class for Customer Account Form
# class CustomerAccountForm(forms.ModelForm): 
#     account = "".join(str(random.randint(0, 10)) for _ in range(4))
#     #Set Read Only Field on Form
#     account_number = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), initial=account)
    

#     class Meta:
#         model = Customer
#         fields = ['account_number'] 

# #class for Deposit Form
# class CustomerDepositForm(forms.ModelForm):
   
#     class Meta:
#        model = Deposit
#        fields = ['deposit_amount']

# #class for Deposit Form
# class CustomerwithdrawalForm(forms.ModelForm):
   
#     class Meta:
#        model = Witdrawal
#        fields = ['withdrawal_amount']

# #class for Deposit Form
# class ServiceChargeForm(forms.ModelForm):

   
#     class Meta:
#        model = Fee
#        fields = ['description', 'charge_amount', 'due_day']

# #Search Applicant form
# class SearchCustomerForm(forms.Form):
#     value = forms.CharField(label = 'Enter Name or Acct. Number', max_length=30)