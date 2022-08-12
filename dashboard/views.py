from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponse
from django.urls import reverse_lazy

from . models import Customer, Deposit, Witdrawal
from django.db.models import Count, Sum

from . forms import CustomerAccountForm, CustomerDepositForm
from datetime import datetime
import datetime
from django.contrib.auth.models import User
from random import randint
from django.views.generic.list import ListView
from django.views import generic
from django.contrib import messages
from django.views.generic.edit import CreateView, FormView
from decimal import Decimal
from datetime import *
import calendar
from django.db.models.functions import TruncMonth

#Create Customer Account Function View
def create_account(request):
    form = CustomerAccountForm(request.POST or None)
    
    #Get Day of today from current date and time
    now = datetime.now()
    #Get the date today
    date_today = datetime.now().date
    count_withdrawals_today = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
    count_deposits_today = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
    count_accounts = Customer.objects.count()
    customers = Customer.objects.all()
    count_users = User.objects.count() 
    #Calculate today Deposit Today
    total_deposit= Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(total_deposit=Sum('deposit_amount')).get('total_deposit') or 0
    #Calculate today Withdrawal Today
    total_withdrawal= Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(total_withdrawal=Sum('withdrawal_amount')).get('total_withdrawal') or 0
    
    if request.method == 'POST':
        form = CustomerAccountForm(request.POST or None)
        if form.is_valid():
            acct = form.cleaned_data.get('account_number')
            name = form.cleaned_data.get('surname')
            try:
                acct_no = Customer.objects.get(account_number=acct)
            except Customer.DoesNotExist:
                form.save()
                messages.success(request, f'Saving Acct. No:{acct} created Successfully for {name}')        
                return redirect('customer_create')
            else:
                messages.error(request, f'Account Number Already Exist, Try Again')
                return redirect('customer_create')
                
    else:
        form = CustomerAccountForm()

    context = {
        'count_withdrawals_today':count_withdrawals_today,
        'count_deposits_today':count_deposits_today,
        'count_accounts':count_accounts,
        'count_users':count_users,
        'total_desposit':total_deposit,
        'total_withdrawal':total_withdrawal,
        'form':form,
        'customers':customers,

    }
    return render(request, 'dashboard/customers.html', context)

#Customer Deposit Function View
def customer_deposit(request, id):
    context = {}
    form = CustomerDepositForm(request.POST or None)
    #Set Page Title
    page_title = "Customer Deposit"
    #Get Current Date
    current_date = datetime.now().date()
    #Get Current Month Name from Calendar
    current_month_name = calendar.month_name[date.today().month]
    
    try:
        #Check the Customer ID in DB
        customer = Customer.objects.get(id=id)
        #Customer Account
        acct = customer.account_number
    except Customer.DoesNotExist:
        messages.error(request, 'Customer Does Not Exist')
        return redirect('customer_create')
    else:
        #Get the Customer total deposit
        deposit = Deposit.objects.filter(customer_id = id).aggregate(total=Sum('deposit_amount')
        )['total'] or Decimal()
        if request.method == 'POST':
            #Deposit Form
            form = CustomerDepositForm(request.POST or None)
            if form.is_valid():
                amount = form.cleaned_data['deposit_amount']
                context.update(  {
                'deposit':deposit,
                'page_title':page_title,
                'customer':customer,
                'current_date':current_date,
                'current_month_name':current_month_name,
                'form':form,
                'amount':amount,
                'acct':acct,
                })
                return render(request, 'dashboard/deposit_approval_form.html', context)
                
        else:
            form = CustomerDepositForm()
        context = {
            'deposit':deposit,
            'page_title':page_title,
            'customer':customer,
            'current_date':current_date,
            'current_month_name':current_month_name,
            'form':form,
            
            'acct':acct,
        }
        return render(request, 'dashboard/deposit.html', context)

def approve_deposit(request, id):
    user = request.user
    form = CustomerDepositForm(request.POST or None)
    amount = form.cleaned_data['deposit_amount'].value()
    try:
        #Check the Customer ID in DB
        customer = Customer.objects.get(id=id)
        #Customer Account
        acct = customer.account_number
    except Customer.DoesNotExist:
        messages.error(request, 'Customer Does Not Exist')
        return redirect('customer_create')
    else:
        if request.method == 'POST':
            #Create Customer Deposit
            credit_acct = Deposit.objects.create(customer=customer, acct=acct, staff=user, deposit_amount=amount)
            credit_acct.save()
            messages.success(request, f'N{amount} Credited for Account {acct} Successfully.')
            return redirect('deposit-slip')
                
                
                    
                    
        else:
            form = CustomerDepositForm()
    context = {

    }
    return render(request, 'dashboard/deposit_approval_form.html', context)

#Customer Deposit Slip
def deposit_slip(request):
    page_title = "Deposit Slip"
    #Get Current Date
    current_date = datetime.now().date()
    #Get Current Month Name from Calendar
    current_month_name = calendar.month_name[date.today().month]

    context = {
        'page_title':page_title,
        'current_date':current_date,
        'current_month_name':current_month_name,
    }
    return render(request, 'dashboard/deposit_slip.html', context)




#Class Based Views
# Create your views here.
#Create New Customer Account Method
# class CustomerCreateView(SuccessMessageMixin, CreateView):
#     form_class = CustomerAccountForm
#     template_name = 'dashboard/create_customer.html'
#     success_url = reverse_lazy('customers-list')
#     success_message = "Customer Account Created Successfully"
   
#     #Get Form Field Initial Value Function
#     def get_initial(self, *args, **kwargs):
#         initial = super(CustomerCreateView, self).get_initial(**kwargs)
#         #Generate Account Number
#         account = "".join(str(random.randint(0, 10)) for _ in range(4))
#         #Set Initial Value for Account Number Field
#         initial['accountnumber'] = account
#         return initial
    
#     #Function to context data from queries
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#          #Get Day of today from current date and time
#         now = datetime.datetime.now()
#         #Get the date today
#         date_today = datetime.datetime.now().date
#         #Count Number of Withdrawals Today and passing in context
#         context_data['count_withdrawals_today'] = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
#         context_data['count_deposits_today'] = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
#         context_data['count_accounts'] = Customer.objects.count()
#         context_data['count_users'] = User.objects.count()
#         #Calculate today Deposit Today
#         context_data['total_deposit']= Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(total_deposit=Sum('deposit_amount')).get('total_deposit') or 0
#         #Calculate today Withdrawal Today
#         context_data['total_withdrawal']= Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(total_withdrawal=Sum('withdrawal_amount')).get('total_withdrawal') or 0
#         return context_data

class DepositFormView(SuccessMessageMixin, FormView):
    form_class = CustomerDepositForm
    template_name = 'dashboard/create_deposit.html'
    success_url = reverse_lazy('dashboard-deposit')
    success_message = "Deposit Added Successully"
   

class CustomerListView(ListView):
    model = Customer
    template_name = 'dashboard/customers.html'
    paginate_by = 5
    ordering = ['-date']
    #Function to context data from queries
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
         #Get Day of today from current date and time
        now = datetime.datetime.now()
        #Get the date today
        date_today = datetime.datetime.now().date
        #Count Number of Withdrawals Today and passing in context
        context_data['count_withdrawals_today'] = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
        context_data['count_deposits_today'] = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
        context_data['count_accounts'] = Customer.objects.count()
        context_data['count_users'] = User.objects.count()
        #Calculate today Deposit Today
        context_data['total_deposit']= Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(total_deposit=Sum('deposit_amount')).get('total_deposit') or 0
        #Calculate today Withdrawal Today
        context_data['total_withdrawal']= Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(total_withdrawal=Sum('withdrawal_amount')).get('total_withdrawal') or 0
        return context_data
    










#Function based Views
@login_required(login_url='user-login')
def index(request):
    #GET ALL USERS
    all_users = User.objects.all()
    #Count users
    count_users = all_users.count()

    #Get Number of Customers
    user_accounts = Customer.objects.all()
    #Count Number of Customer Accounts
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
    #generated_account = random_with_N_digits(4)
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


class DepositListView(ListView):
    model = Deposit
    template_name = 'dashboard/deposit_list'
    content_object_name = 'deposits'

#Add Customer Deposit
@login_required(login_url='user-login')
def deposit(request):
    customer = Customer.objects.get()
    
    if request.method == "POST":
        deposit_form = CustomerDepositForm(request.POST)
        deposit_form['customer'] = customer.accountnumber
        deposit_form['staff'] = request.user
        amount = deposit_form.cleaned_data['deposit_amount']
        if deposit_form.is_valid():
            deposit_form.save()
            messages.success(request, f'{amount} Deposited Successfully')
            return redirect('')
    else:
        deposit_form = CustomerDepositForm()

    context = {
        'form':deposit_form,
        
    }
    return render(request, 'dashboard/deposit_list.html', context)


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