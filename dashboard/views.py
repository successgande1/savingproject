from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from user.models import *
from . models import *
from django.db.models import Count, Sum
from django.db.models import Q
from . forms import *


from django.contrib.auth.models import User
from random import randint
from django.views.generic.list import ListView
from django.views import generic
from django.contrib import messages
from django.views.generic.edit import CreateView, FormView
from decimal import Decimal
from datetime import datetime
import datetime
import calendar
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractYear, ExtractMonth



#Function based Views
@login_required(login_url='user-login')
def index(request):
    #GET ALL USERS
    all_users = User.objects.filter(is_staff=True)
    
    #Count users
    count_users = all_users.count()
    #Count all Customer Accounts
    count_accounts = Account.objects.count()
     

     #Retrieve all Desposits
    deposits = Deposit.objects.all()

    #Retrieve all Withdrawals
    withdrawals = Witdrawal.objects.all()
    
    

    #Get the date today
    current_date = datetime.datetime.now() 

    #Count Number of Deposits today
    count_deposits_today = deposits.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).count()
    
    #Get Current Month Name from Calendar
    #current_month_name = calendar.month_name[date.today().month] 
    #Count Number of withdrawals today
    count_withdrawals_today = withdrawals.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).count()
    #Get Daily Saving Total Amount
    daily_deposits = Deposit.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
    #Get Today's Total Withdrawn
    daily_withdrawals = Witdrawal.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
    
    context = {
        'daily_deposits':daily_deposits,
        'daily_withdrawals':daily_withdrawals,
        'count_deposits_today':count_deposits_today,
        'count_withdrawals_today':count_withdrawals_today,
        'count_users':count_users,
        'count_accounts':count_accounts,
    }

    return render(request, 'dashboard/index.html', context)

# #Create Customer Account Function View
# def create_account(request): 
#     form = CustomerAccountForm(request.POST or None)

#     #Get Day of today from current date and time
#     now = datetime.datetime.now()
   
#     #Get Current Month Name from Calendar
#     #current_month_name = calendar.month_name[date.today().month]
    
    
#     #get all customers
#     customers = Customer.objects.order_by('-date')[:8]
#     #Count Users
#     count_users = User.objects.count() 
#     #Get Today's Total Deposit 
#     daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
#     #Get Today's Total Withdrawal
#     daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
#     #Count Customers
#     count_accounts = Customer.objects.count()

#     #Search Customer Form
#     searchForm = SearchCustomerForm(request.GET or None)
    
#     #Search Customer
#     if searchForm.is_valid():
#         #Value of search form
#         value = searchForm.cleaned_data['value']
#         #Filter Customer by Surname, Othernames , Account Number using Q Objects
#         user_filter = Q(surname__iexact = value) | Q(othernames__iexact = value) | Q(account_number__iexact = value)
#         #Apply the Customer Object Filter
#         list_customers = Profile.objects.filter(user_filter) 
       
#     else:
#         list_customers = Profile.objects.all()

#     paginator = Paginator(list_customers, 10)
#     page = request.GET.get('page')
#     paged_list_customers = paginator.get_page(page)


#     if request.method == 'POST':
#         form = CustomerAccountForm(request.POST or None)
#         if form.is_valid():
#             acct = form.cleaned_data.get('account_number')
            
#             try:
#                 acct_no = Customer.objects.get(account_number=acct)
#             except Customer.DoesNotExist:
#                 form.save()
#                 messages.success(request, f'Saving Acct. No:{acct} created Successfully for ')        
#                 context = {
#                 'daily_deposits':daily_deposits,
#                 'daily_withdrawals':daily_withdrawals,
#                 'acct':acct,
                
#                 'count_accounts':count_accounts,
#                 'count_users':count_users,
#                 'form':form,
#                 'customers':customers,
#                 'current_month_name':current_month_name,

#                 }
#                 return render(request, 'dashboard/registration_slip.html', context)
#             else:
#                 messages.error(request, f'Account Number Already Exist, Try Again')
#                 return redirect('create-customer')
                
#     else:
#         form = CustomerAccountForm()

    

#     context = {
#         'daily_deposits':daily_deposits,
#         'daily_withdrawals':daily_withdrawals,
#         'count_accounts':count_accounts,
#         'count_users':count_users,
#         'form':form,
#         'customers':customers,
#         'customers':paged_list_customers,
#         'searchForm':searchForm,
#         'page_title':"Customers",
#     }
#     return render(request, 'dashboard/customers.html', context)



# #Customer Deposit Function View
# def customer_deposit(request, id):
#     user = request.user
#     context = {}
#     form = CustomerDepositForm(request.POST or None)
#     #Set Page Title
#     page_title = "Customer Deposit"
#     #Get Service Charge
#     service_charge = Fee.objects.filter(description='Saving')
#     #Count Customers
#     count_accounts = Customer.objects.count()

#     #Get Date of the Day
#     now = datetime.datetime.now()
    
#     #Get Current Month Name from Calendar
#     #current_month_name = calendar.month_name[date.today().month]
#     #Get Total Deposited this Month for the customer by ID
#     deposited_this_month = Deposit.objects.filter(customer__id=id, date__year=now.year, date__month=now.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0
#     #Count Customers
#     count_accounts = Customer.objects.count()
#     #Get Today's Total Deposit 
#     daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
#     #Get Today's Total Withdrawal
#     daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0

     
#     try:
#         #Check the Customer ID in DB
#         customer = Customer.objects.get(id=id)
#         #Customer Account
#         acct = customer.account_number
#     except Customer.DoesNotExist:
#         messages.error(request, 'Customer Does Not Exist')
#         return redirect('create-customer')
#     else:
#          #Get the Customer Total Deposit by ID
#         deposit = Deposit.objects.filter(customer_id = id).aggregate(total=Sum('deposit_amount')
#         )['total'] or Decimal()
#         #Get the Customer Deposit Details
#         customer_deposits = Deposit.objects.filter(customer__id = id)

#         if request.method == 'POST':
#             #Deposit Form
#             form = CustomerDepositForm(request.POST or None)
            
#             if form.is_valid():
#                 #Get  Deposit Details for form variable
#                 amount = form.cleaned_data['deposit_amount']
                
#                 #Set Minimum Deposit
#                 minimum_deposit = 100
#                 #Check if Customer Deposit is Less than the Minimum Deposit
#                 if amount < minimum_deposit:
#                     messages.error(request, f'N{amount} is less than the Minimum Deposit of N{minimum_deposit}')
#                 else:
#                     #Add Customer Deposit
#                     credit_acct = Deposit.objects.create(customer=customer, acct=acct, staff=user, deposit_amount=amount)
#                     #Save the Customer Deposit
#                     credit_acct.save()
                   
#                     #Get Total Deposited this Month for the customer BY ID
#                     deposited_this_month = Deposit.objects.filter(customer__id=id, date__year=now.year, date__month=now.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0
#                     #Get Total Daily Deposits
#                     daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
#                     #Get Today's Total Withdrawal
#                     daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0

#                     #Group Customers Desposits for the Current Month by Accounts 
#                     group_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month).order_by('acct')
#                     customers_total_savings = group_deposits.annotate(total=Sum('deposit_amount')).order_by('-date')[:5]

#                     context.update(  {
#                     'amount':amount,
#                     'customer_deposits':customer_deposits,
#                     'daily_deposits':daily_deposits,
#                     'daily_withdrawals':daily_withdrawals,
#                     'customers':customers_total_savings,
#                     'page_title':page_title,
#                     'acct':acct,
#                     'now':now,
#                     'count_accounts':count_accounts,
#                     })
                    
#                     messages.success(request, f'N{amount} Deposited to Account {acct} Successfully.')
                    
#                     return render(request, 'dashboard/deposit_slip.html', context)
                
#         else:
#             form = CustomerDepositForm()
#         context.update(  {
#                 'daily_deposits':daily_deposits,
#                 'daily_withdrawals':daily_withdrawals,
#                 'count_accounts':count_accounts,
#                 'deposit':deposit,
#                 'page_title':page_title,
#                 'customer':customer,
#                 'now':now,
               
#                 'form':form,
#                 'deposited_this_month':deposited_this_month,
#                 'acct':acct,
#                 })
#         return render(request, 'dashboard/deposit.html', context)

# #Customer Account Statement View
# def account_statement(request, id):
#     try:
#         customer = Customer.objects.get(id=id)
        
#     except Customer.DoesNotExist:
#         messages.error(request, 'Customer Does Not Exist')
#         return redirect('create-customer')
#     else:
#         #Get Customer Deposits by ID and order by Current Date with 5 Displayed
#         deposits = Deposit.objects.filter(customer__id=id).order_by('-date')[:5]
#         #deposits = deposits.order_by('-date')
#         current_date = datetime.datetime.now()
#         #Get Current Month Name from Calendar
#         #current_month_name = calendar.month_name[date.today().month] 
#         #get Current Month total deposited by customer ID   
#         deposited_this_month = Deposit.objects.filter(customer__id=id, date__year=current_date.year, date__month=current_date.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0
#         #Get Current Year Deposited by customer ID
#         deposited_this_year = Deposit.objects.filter(customer__id=id, date__year=current_date.year).aggregate(deposited_this_year=Sum('deposit_amount')).get('deposited_this_year') or 0
#         #Count number of Customers
#         count_accounts = Customer.objects.count()
#         #Get Today's Total Deposits
#         daily_deposits = Deposit.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
#         #Get Today's Total Withdrawn
#         daily_withdrawals = Witdrawal.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
#         #get Current Month total Withdrawn by customer ID   
#         withdrawn_this_month = Witdrawal.objects.filter(account__id=id, date__year=current_date.year, date__month=current_date.month).aggregate(withdrawn_this_month=Sum('withdrawal_amount')).get('withdrawn_this_month') or 0
#         #Get Current Year Total Withdrawn by customer ID
#         withdrawn_this_year = Witdrawal.objects.filter(account__id=id, date__year=current_date.year).aggregate(withdrawn_this_year=Sum('withdrawal_amount')).get('withdrawn_this_year') or 0

#         context = {
#             'withdrawn_this_month':withdrawn_this_month,
#             'withdrawn_this_year':withdrawn_this_year,
#             'count_accounts':count_accounts,
#             'daily_deposits':daily_deposits,
#             'daily_withdrawals':daily_withdrawals,
#             'deposits':deposits,
#             'customer':customer,
#             'deposited_this_month':deposited_this_month,
            
#             'current_date':current_date,
#             'deposited_this_year':deposited_this_year,

#         }
#         return render(request, 'dashboard/statement.html', context)

# #Deposit Slip
# def deposit_slip(request, customer_id):
#     #Get Day from current date and time
#     date_today = datetime.datetime.now()
#     #Get Today's Total Deposit 
#     daily_deposits = Deposit.objects.filter(date__year=date_today.year, date__month=date_today.month, date__day=date_today.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
#     #Get Today's Total Withdrawal
#     daily_withdrawals = Witdrawal.objects.filter(date__year=date_today.year, date__month=date_today.month, date__day=date_today.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
#     #Count Customers
#     count_accounts = Customer.objects.count()
    
#     try:
#         customer_deposit = Deposit.objects.get(id=customer_id)
        
#     except Deposit.DoesNotExist:
#         messages.error(request, 'Deposit Does Not Exist')
        
#     else:
#         customer_deposit = Deposit.objects.get(id=customer_id)
        
#         context = {
#             'customer_deposit':customer_deposit,  
#             'count_accounts':count_accounts,
#             'daily_deposits':daily_deposits,
#             'daily_withdrawals':daily_withdrawals,
                
#         }
#         return render(request, 'dashboard/deposit_slip.html', context)

# #Add Service Charge
# @login_required(login_url='user-login')
# def Add_Service_Charge(request):
#     #get login user
#     user = request.user
    
#     page_title = 'Add Charges'

#     #User Accounts
#     user_accounts = Customer.objects.all()[:10]

#     #Get Day from current date and time
#     date_today = datetime.now().date()
#     #Get Today's Total Deposit 
#     daily_deposits = Deposit.objects.filter(date__year=date_today.year, date__month=date_today.month, date__day=date_today.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
#     #Get Today's Total Withdrawal
#     daily_withdrawals = Witdrawal.objects.filter(date__year=date_today.year, date__month=date_today.month, date__day=date_today.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0


#     form = ServiceChargeForm(request.POST or None)

#     if request.method == 'POST' and form.is_valid():
#             #Charges Form
#             charge_name = form.cleaned_data['description']

#             amount = form.cleaned_data['charge_amount']

#             charged_day = form.cleaned_data['due_day']
            
#             service_charge_name = Fee.objects.filter(description=charge_name)

            

#             if service_charge_name:
#                 messages.error(request, f' {charge_name} Already Existed')
            
#             elif charged_day >= 31:
#                 messages.error(request, f' {charge_name} Can Not be More than 30')

#             else:
#                 added_charges = Fee.objects.create(description=charge_name, staff=user, charge_amount=amount, due_day = charged_day)
#                 #Save the Customer Deposit
#                 added_charges.save()
#                 messages.success(request, f' {charge_name} Added Successfully')

#     else:
#         form = ServiceChargeForm()
    
#     context = {
#         'form':form,
#         'page_title':page_title,
#         'daily_deposits':daily_deposits,
#         'daily_withdrawals':daily_withdrawals,

#     }
#     return render(request, 'dashboard/service_charge.html', context)

# #Customer Withdrawal View
# @login_required(login_url='user-login')
# def witdrawal(request, id):
#     page_title = 'Add Withdrawal'
#     #Create an Empty Dictionary
#     context = {

#     }
#     #Get Login user
#     user = request.user

#     form = CustomerwithdrawalForm(request.POST or None)
#     #GET ALL USERS
#     all_users = User.objects.all()
#     #Count users
#     count_users = all_users.count()
#     #Read all Accounts
#     user_accounts = Customer.objects.all()[:10]
#     #Count Number of User Accounts
#     count_accounts = user_accounts.count()

#     #Retrieve all Withdrawals
#     withdrawals = Witdrawal.objects.all()

#     #Get Current Date
#     current_date = datetime.datetime.now()

#     #Get Day of the Month from the current Date
#     day_of_month = current_date.day

#     #Get Service Charge 
#     saving_fee = Fee.objects.get(description='Saving')
    
#     #Get the exact charge date
#     charge_date = saving_fee.due_day

#     #Saving Fee Amount
#     saving_charge_amount = saving_fee.charge_amount

#     #Get Current Month Name from Calendar
#     #current_month_name = calendar.month_name[date.today().month] 
#     #get Current Month total deposited by customer ID   
#     deposited_this_month = Deposit.objects.filter(customer__id=id, date__year=current_date.year, date__month=current_date.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0
#     #Get Current Year Deposited by customer ID
#     deposited_this_year = Deposit.objects.filter(customer__id=id, date__year=current_date.year).aggregate(deposited_this_year=Sum('deposit_amount')).get('deposited_this_year') or 0
#     #Count number of Customers
#     count_accounts = Customer.objects.count()
#     #Get Today's Total Deposits
#     daily_deposits = Deposit.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
#     #Get Today's Total Withdrawn
#     daily_withdrawals = Witdrawal.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
#     #get Current Month total Withdrawn by customer ID   
#     withdrawn_this_month = Witdrawal.objects.filter(account__id=id, date__year=current_date.year, date__month=current_date.month).aggregate(withdrawn_this_month=Sum('withdrawal_amount')).get('withdrawn_this_month') or 0
#     #Get Current Year Total Withdrawn by customer ID
#     withdrawn_this_year = Witdrawal.objects.filter(account__id=id, date__year=current_date.year).aggregate(withdrawn_this_year=Sum('withdrawal_amount')).get('withdrawn_this_year') or 0
    
#     #Group Customer's Deposits for Agregation
#     group_deposits = Deposit.objects.filter(date__year=current_date.year, date__month=current_date.month).order_by('acct')
    
#     #Get Totals of Customer's Savings
#     customers_total_savings = group_deposits.annotate(total=Sum('deposit_amount')).order_by('-date')[:5]
    
#     #Get Customer Total Withdrawal
#     customer_withdrawals = Witdrawal.objects.filter(account__id = id).aggregate(total=Sum('withdrawal_amount')
#     )['total'] or Decimal()

#     #Get the Customer total deposit
#     customer_deposit = Deposit.objects.filter(customer_id = id).aggregate(total=Sum('deposit_amount')
#     )['total'] or Decimal()

    
#     #Customer Account Balance
#     acct_balance = deposited_this_month - saving_charge_amount 
    
#     #Minus the Customer Account Balance from the Service Charge Amount
#     available_balance = acct_balance - withdrawn_this_month
#     try:
#         #Check the Customer ID in DB
#         customer = Customer.objects.get(id=id)
        
#         #Customer Account
#         acct = customer.account_number
#     except Customer.DoesNotExist:
#         messages.error(request, 'Customer Does Not Exist')
#         return redirect('create-customer')
#     else:
  
#         if request.method == 'POST':

            
#             #Deposit Form
#             form = CustomerwithdrawalForm(request.POST or None)
            
#             if form.is_valid():
#                 #Withdrawal amount form value
#                 amount = form.cleaned_data['withdrawal_amount']

#                 #Check if Customer Withdrawal is a Positive Figure
#                 if amount < 1:
#                     messages.error(request, f'N{amount} is NOT a Valid Withdrawal Amount')
                
#                 #Check if Inputed Amount is Greater Than Customer Available Balance
#                 elif amount > available_balance: 
#                     messages.error(request, f'N{amount} is More Than Customer Aval. Balance of N{available_balance}')

                
#                     #messages.error(request, f'Sorry, You can NOT Empty Your Acct. at the Moment')
#                 else:
                    
                    
#                     #Add Customer Deposit
#                     debit_acct = Witdrawal.objects.create(account=customer, staff=user, withdrawal_amount=amount)
#                     #Save the Customer Deposit
#                     debit_acct.save()

#                     now = datetime.datetime.now()
#                     #Get Total Daily Deposits
#                     daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
#                     #Get Today's Total Withdrawal
#                     daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0

#                     #Get Customer Deposits by ID 
#                     customer_withdrawals = Witdrawal.objects.filter(account_id=id)

#                     #get Current Month total deposited by customer ID   
#                     deposited_this_month = Deposit.objects.filter(customer__id=id, date__year=now.year, date__month=now.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0

#                     #get Current Month total Withdrawn by customer ID   
#                     withdrawn_this_month = Witdrawal.objects.filter(account__id=id, date__year=current_date.year, date__month=current_date.month).aggregate(withdrawn_this_month=Sum('withdrawal_amount')).get('withdrawn_this_month') or 0

#                     #Customer Account Balance
#                     acct_balance = deposited_this_month - saving_charge_amount 
    
#                     #Minus the Customer Account Balance from the Service Charge Amount
#                     available_balance = acct_balance - withdrawn_this_month

                    

#                     context.update(  {
#                     'customer':customer,
#                     'customer_withdrawals':customer_withdrawals,
#                     'deposited_this_month':deposited_this_month, 
#                     'daily_deposits':daily_deposits,
#                     'daily_withdrawals':daily_withdrawals,
#                     'customers':customers_total_savings,
#                     'page_title':page_title,
#                     'count_accounts':count_accounts,
#                     'now':now,
#                     'amount':amount,
#                     })
                    
                    
#                     messages.success(request, f'N{amount} Withdrawn Successfully from {acct}. New Bal. N{available_balance}')
                    
#                     return render(request, 'dashboard/withdrawal_slip.html', context)
#             else:
#                 form = CustomerwithdrawalForm()
    
    
#     context = {
#         'saving_charge_amount':saving_charge_amount,
#         'available_balance':available_balance,
#         'day_of_month':day_of_month,
#         'charge_date':charge_date,
#         'acct_balance':acct_balance,
#         'customer_withdrawals':customer_withdrawals,
#         'deposited_this_month':deposited_this_month, 
#         'customer':customer, 
        
#         'customer_deposit':customer_deposit,
#         'current_date':current_date,
#         'count_accounts':count_accounts,
#         'daily_deposits':daily_deposits,
#         'daily_withdrawals':daily_withdrawals,
#         'withdrawn_this_month':withdrawn_this_month,
#         'withdrawn_this_year':withdrawn_this_year,
#         'count_users':count_users,
#         'form':form,
#         'page_title':page_title,
#     }
#     return render(request, 'dashboard/witdrawal.html', context)

# #Daily Deposit List
# def daily_deposits(request):
#     page_title = 'Deposits Today'

#     #Count Customers
#     count_accounts = Customer.objects.count()

    

    
    
#     #Get Date
#     now = datetime.datetime.now() 
#     #Group Customer's Deposits for Agregation
#     group_deposits_today = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).order_by('-date')
    
#     #Get Daily Total Savings of Customers
#     deposits_today = group_deposits_today.annotate(total=Sum('deposit_amount')).order_by('-date')[:5]

#     #Get Total Daily Deposits
#     daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
#     #Get Today's Total Withdrawal
#     daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0


    


   
#     context = {
#         'deposits_today':deposits_today,
#         'daily_deposits':daily_deposits,
#         'daily_withdrawals':daily_withdrawals,
#         'count_accounts':count_accounts,
#         'customer':customer,
        


#     }
#     return render(request, 'dashboard/daily_deposits.html', context)




# #Function based Views
# @login_required(login_url='user-login')
# def index(request):
#     #GET ALL USERS
#     all_users = User.objects.all()
#     #Count users
#     count_users = all_users.count()

#     #Get Number of Customers
#     user_accounts = Customer.objects.all()
#     #Count Number of Customer Accounts
#     count_accounts = user_accounts.count()

#      #Retrieve all Desposits
#     deposits = Deposit.objects.all()

#     #Retrieve all Withdrawals
#     withdrawals = Witdrawal.objects.all()
    
    

#     #Get the date today
#     current_date = datetime.datetime.now() 

#     #Count Number of Deposits today
#     count_deposits_today = deposits.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).count()
    
#     #Get Current Month Name from Calendar
#     #current_month_name = calendar.month_name[date.today().month] 
#     #Count Number of withdrawals today
#     count_withdrawals_today = withdrawals.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).count()
#     #Get Daily Saving Total Amount
#     daily_deposits = Deposit.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
#     #Get Today's Total Withdrawn
#     daily_withdrawals = Witdrawal.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
    
#     context = {
#         'daily_deposits':daily_deposits,
#         'daily_withdrawals':daily_withdrawals,
#         'count_accounts':count_accounts,
#         'count_deposits_today':count_deposits_today,
#         'count_withdrawals_today':count_withdrawals_today,
#         'count_users':count_users,
#     }

#     return render(request, 'dashboard/index.html', context)

# #Method for Reading and Creating Customer Accounts
# @login_required(login_url='user-login')
# def customer(request):
#     #generated_account = random_with_N_digits(4)
#     #Readd all Accounts
#     user_accounts = Customer.objects.all()[:10]
#     #Count Number of User Accounts
#     count_accounts = user_accounts.count()

#     #Retrieve all Desposits
#     deposits = Deposit.objects.all()

#     #Retrieve all Withdrawals
#     withdrawals = Witdrawal.objects.all()
    
#     #Get Day of today from current date and time
#     now = datetime.datetime.now()

#     #Get the date today
#     date_today = datetime.datetime.now().date

#     #Count Number of Deposits today
#     count_deposits_today = deposits.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
    
#     #Count Number of withdrawals today
#     count_withdrawals_today = withdrawals.filter(date__year=now.year, date__month=now.month, date__day=now.day).count()
    
#     #Create New Customer Account
#     if request.method == 'POST':
#         account_form = CustomerAccountForm(request.POST or None)
#         if account_form.is_valid():
#             account_form.save()
#             return redirect('dashboard-customer')
#     else:
#         account_form = CustomerAccountForm()
    
#     context = {
#         'user_accounts':user_accounts,
#         'account_form':account_form,
#         'count_accounts':count_accounts,
#         'count_deposits_today':count_deposits_today,
#         'count_withdrawals_today':count_withdrawals_today,
#     }
#     return render(request, 'dashboard/customers.html', context)


# class DepositListView(ListView):
#     model = Deposit
#     template_name = 'dashboard/deposit_list'
#     content_object_name = 'deposits'



