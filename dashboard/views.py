from multiprocessing import context
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.urls import reverse_lazy

from . models import Customer, Deposit, Witdrawal
from django.db.models import Count, Sum

from . forms import CustomerAccountForm
from datetime import datetime
import datetime
from django.contrib.auth.models import User
from random import randint
from django.views.generic.list import ListView

'''
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
'''
from django.views.generic.edit import CreateView

#Class Based Views
# Create your views here.
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerAccountForm
    success_url = reverse_lazy('customer_create')
    template_name = 'dashboard/customers.html'
    

class CustomerListView(ListView):
    model = Customer
    template_name = 'dashboard/customers.html'
    context_object_name = 'customers'










#Function based Views
@login_required(login_url='user-login')
def index(request):
    #GET ALL USERS
    all_users = User.objects.all()
    #Count users
    count_users = all_users.count()

    user_accounts = Customer.objects.all()
    #Count Number of User Accounts
    count_accounts = user_accounts.count()

     #Retrieve all Desposits
    deposits = Deposit.objects.all()

    #Retrieve all Withdrawals
    withdrawals = Witdrawal.objects.all()
    
    #Get Day of today from current date and time
    now = datetime.datetime.now()

    #Get the date today
    date_today = datetime.datetime.now().date

    #Count Number of Deposits today
    count_deposits_today = deposits.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()

    #Count Number of withdrawals today
    count_withdrawals_today = withdrawals.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()

    context = {
        'count_accounts':count_accounts,
        'count_deposits_today':count_deposits_today,
        'count_withdrawals_today':count_withdrawals_today,
        'count_users':count_users,
    }

    return render(request, 'dashboard/index.html', context)

#Method for Reading and Creating Customer Accounts
@login_required(login_url='user-login')
def customer(request):
    generated_account = random_with_N_digits(4)
    #Readd all Accounts
    user_accounts = Customer.objects.all()[:10]
    #Count Number of User Accounts
    count_accounts = user_accounts.count()

    #Retrieve all Desposits
    deposits = Deposit.objects.all()

    #Retrieve all Withdrawals
    withdrawals = Witdrawal.objects.all()
    
    #Get Day of today from current date and time
    now = datetime.datetime.now()

    #Get the date today
    date_today = datetime.datetime.now().date

    #Count Number of Deposits today
    count_deposits_today = deposits.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
    
    #Count Number of withdrawals today
    count_withdrawals_today = withdrawals.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
    
    #Create New Customer Account
    if request.method == 'POST':
        account_form = CustomerAccountForm(request.POST or None)
        if account_form.is_valid():
            account_form.save()
            return redirect('dashboard-customer')
    else:
        account_form = CustomerAccountForm()
    
    context = {
        'user_accounts':user_accounts,
        'account_form':account_form,
        'count_accounts':count_accounts,
        'count_deposits_today':count_deposits_today,
        'count_withdrawals_today':count_withdrawals_today,
    }
    return render(request, 'dashboard/customers.html', context)

#Add Customer Deposit
@login_required(login_url='user-login')
def deposit(request):
     #GET ALL USERS
    all_users = User.objects.all()
    #Count users
    count_users = all_users.count()
    #Retrieve all Desposits according to recent dates
    deposits = Deposit.objects.order_by('-date')

    #Retrieve all Withdrawals
    withdrawals = Witdrawal.objects.all()
    
    #Get Day of today from current date and time
    now = datetime.datetime.now()

    #Get the date today
    date_today = datetime.datetime.now().date

    #Count Number of Deposits today
    count_deposits_today = deposits.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
    
    #Count Number of withdrawals today
    count_withdrawals_today = withdrawals.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
    
    #Read all Accounts
    user_accounts = Customer.objects.all()[:10]
    #Count Number of User Accounts
    count_accounts = user_accounts.count()

    #Add Deposit
    #if request.method == 'POST':

    context = {
        'deposits':deposits,
        'count_accounts':count_accounts,
        'count_deposits_today':count_deposits_today,
        'count_withdrawals_today':count_withdrawals_today,
        'count_users':count_users,
    }
    return render(request, 'dashboard/deposit.html', context)

@login_required(login_url='user-login')
def witdrawal(request):
     #GET ALL USERS
    all_users = User.objects.all()
    #Count users
    count_users = all_users.count()
    #Read all Accounts
    user_accounts = Customer.objects.all()[:10]
    #Count Number of User Accounts
    count_accounts = user_accounts.count()

    #Retrieve all Desposits
    deposits = Deposit.objects.all()

    #Retrieve all Withdrawals
    withdrawals = Witdrawal.objects.all()
    
    #Get Day of today from current date and time
    now = datetime.datetime.now()

    #Get the date today
    date_today = datetime.datetime.now().date

    #Count Number of Deposits today
    count_deposits_today = deposits.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()

    #Count Number of withdrawals today
    count_withdrawals_today = withdrawals.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()

    context = {
        'count_accounts':count_accounts,
        'count_deposits_today':count_deposits_today,
        'count_withdrawals_today':count_withdrawals_today,
        'withdrawals':withdrawals,
        'count_users':count_users,
    }
    return render(request, 'dashboard/witdrawal.html', context)