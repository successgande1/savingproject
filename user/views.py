from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

from . forms import *

from datetime import *

from django.db.models import Count, Sum

from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
import random
import secrets


#Create Customer Account Function View
@login_required(login_url='user-login')
def create_account(request): 
    #get logged in user
    user = request.user
    #check if logged user is staff
    if user.is_staff:
        form = CustomerAccountForm(request.POST or None)
        userForm = CreateUserForm(request.POST or None)

        #Get Day of today from current date and time
        now = datetime.datetime.now()
    
        #Get Current Month Name from Calendar
        current_month_name = now.strftime('%B')
        
        
        #get all customers
        customer = Account.objects.all()
        #Count Users
        count_users = User.objects.count() 
        
        #Get Today's Total Deposit 
        daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
        #Get Today's Total Withdrawal
        daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
        #Count Customers
        count_accounts = Account.objects.count()

        #Search Customer Form
        searchForm = SearchCustomerForm(request.GET or None)
        
        #Search Customer
        if searchForm.is_valid():
            #Value of search form
            value = searchForm.cleaned_data['value']
            #Filter Customer by Surname or Othernames or Account Number using Q Objects
            user_filter = Q(customer__profile__surname__exact = value) | Q(customer__profile__othernames__exact = value) | Q(account_number__exact = value)
            #Apply the Customer Object Filter
            list_customers = Account.objects.filter(user_filter) 
        
        else:
            list_customers = Account.objects.order_by('-date')[:8]
            now = datetime.datetime.now()
            
        paginator = Paginator(list_customers, 10)
        page = request.GET.get('page')
        paged_list_customers = paginator.get_page(page)

        if request.method == 'POST':
            #Account Number Form
            form = CustomerAccountForm(request.POST or None)
            #User Registration form
            userForm = CreateUserForm(request.POST or None)

            if form.is_valid() and userForm.is_valid():
                #Get customer Account Number from Account Form
                acct = form.cleaned_data.get('account_number')
                acct_user = userForm.cleaned_data.get('username')
                
                try:
                    acct_no = Account.objects.get(account_number=acct)
                except Account.DoesNotExist:
                    
                    #Save the Guest User Form to get an instance of the user
                    new_user = userForm.save()
                    #Create a New Customer User
                    Account.objects.create(customer=new_user, account_number=acct)
                    
                    
                    messages.success(request, f'Saving Acct. No:{acct} created Successfully ')        
                    
                    return redirect('create-customer')
                else:
                    messages.error(request, f'Something Went Wrong, Please Try Again')
                    
                    
        else:
            form = CustomerAccountForm()
        
        context = {
            
            'daily_deposits':daily_deposits,
            'daily_withdrawals':daily_withdrawals,
            'count_accounts':count_accounts,
            'count_users':count_users,
            'form':form,
            'userForm':userForm,
            'now':now,
            'customers':paged_list_customers,
            #'customers':customer,
            'searchForm':searchForm,
            'page_title':"Customers",
        }
        return render(request, 'dashboard/customers.html', context)
    else:
        return redirect('user-login')

#View User Profile
@login_required(login_url='user-login')
def view_profile(request, pk):
    #get logged in user
    user = request.user
    #check if logged in user is staff
    if user.is_staff:
        count_users = User.objects.all().count()
        try:
            staff_user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return redirect('user-register')
        else:
            #Get Day of today from current date and time
            now = datetime.datetime.now()
        
            #Get Current Month Name from Calendar
            #current_month_name = calendar.month_name[date.today().month]
            
            #Get Today's Total Deposit 
            daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
            #Get Today's Total Withdrawal
            daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
            #Count Customers
            count_accounts = Account.objects.count()

            context = {
                'daily_deposits':daily_deposits,
                'daily_withdrawals':daily_withdrawals,
                'count_accounts':count_accounts,
                'count_users':count_users,
                'page_title': 'User Profile',
                'staff_user':staff_user,
            }
            return render(request, 'user/profile.html', context)
    else:
        return redirect('user-login')

#Update Customer Profile
@login_required(login_url='user-login')
def update_profile(request, pk):
    #get logged in user
    user = request.user
    #check if logged in user is staff
    if user.is_staff==True:
        try:
            staff_user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return redirect('user-register')
        else:
            count_users = User.objects.count() 
            #Get the Customer User's Profile from the User above
            user_profile = Profile.objects.get(customer=staff_user.profile.customer)
            if request.method == 'POST':
                #Instantiate the Profile Update Form with the User Profile above
                profile_form = ProfileUpdateForm(request.POST, request.FILES,
                instance=user_profile)
            #Check if form is valid
                if profile_form.is_valid():
                    profile_form.save()
                    
                    messages.success(request, f' {user_profile} Updated Successfully')
                    return redirect('user-register') 
            else:
                
                profile_form = ProfileUpdateForm(instance=user_profile)

            context = {
                
                'profile_form': profile_form,
                'staff_user':staff_user,
                'user_profile':user_profile,
                'count_users':count_users,
                
            }
            return render(request, 'user/profile_update.html', context)
    else:
        return redirect('user-login')

#Update Customer Profile
@login_required(login_url='user-login')
def update_customer_profile(request, pk):
    #get logged in user
    user = request.user
    #check if logged in user is staff
    
    try:
        customer_user = User.objects.get(id=pk)
       
    except User.DoesNotExist:
        return redirect('user-register')
    else:
        count_users = User.objects.count() 
        #Get the Customer User's Profile from the User above
        user_profile = Profile.objects.get(customer=customer_user.profile.customer) 
        
        if request.method == 'POST':
            #Instantiate the Profile Update Form with the User Profile above
            profile_form = ProfileUpdateForm(request.POST, request.FILES,
            instance=user_profile)
            #Check if form is valid
            if profile_form.is_valid():
                profile_form.save()
                    
                messages.success(request, f'{customer_user.username} Profile Updated Successfully')
                return redirect('create-customer') 
        else:
            profile_form = ProfileUpdateForm()
       

        context = {
                
                'profile_form': profile_form,
                'customer_user':customer_user,
                'user_profile':user_profile,
                'count_users':count_users,
                
        }
        return render(request, 'user/customer_update.html', context)
   



#Customer Deposit Function View
@login_required(login_url='user-login')
def customer_deposit(request, id):
    #Get logged in user
    user = request.user
    #check if logged in user is staff
    if user.is_staff:
        context = {}
        form = CustomerDepositForm(request.POST or None)
        #Set Page Title
        page_title = "Customer Deposit"
        #Get Service Charge
        service_charge = Fee.objects.filter(description='Saving')
        #Count Customers
        count_accounts = Account.objects.count()

        #Get Date of the Day
        now = datetime.datetime.now()
        current_year = now.year
        #Get Current Month Name from Calendar
        current_month_name = now.strftime('%B')
        
        #Get Total Monthly Deposited of customer by ID
        deposited_this_month = Deposit.objects.filter(customer__id=id, date__year=now.year, date__month=now.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0
        #Get Customer Current Monthly Total Withdrawal by ID
        withdrawn_this_month = Witdrawal.objects.filter(account_id=id,  date__month=now.month).aggregate(withdrawn_this_month=Sum('withdrawal_amount')).get('withdrawn_this_month') or 0
        
        count_accounts = Account.objects.count()
        #Get Today's Total Deposit 
        daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
        #Get Today's Total Withdrawal
        daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
        
        service_charge = Fee.objects.get(description='Saving')
        monthly_charge = service_charge.charge_amount

        
        
        try:
            #Check the Customer ID in DB
            customer = Account.objects.get(id=id)
            #Customer Account
            acct = customer.account_number
            #Get Customer Account ID
            customerID = customer.customer.id
            #Get Customer Profile by his ID
            profile = Profile.objects.get(customer=customer.customer.id)
            profile_surname = profile.surname
            
        except Account.DoesNotExist:
            messages.error(request, 'Customer Does Not Exist')
            return redirect('create-customer')
        else:
            
            #Get Customer Current Month Deposit
            deposited_this_month = Deposit.objects.filter(customer__id=customerID, date__month=now.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0
            #Get Customer Current Year Deposit
            deposited_this_year = Deposit.objects.filter(customer__id = customerID, date__year=now.year, date__month=now.month).aggregate(deposited_this_year=Sum('deposit_amount')).get('deposited_this_year') or 0
            #Get Current Month Withdrawal 
            withdrawn_this_month = Witdrawal.objects.filter(account_id=customerID,  date__month=now.month).aggregate(withdrawn_this_month=Sum('withdrawal_amount')).get('withdrawn_this_month') or 0
            #Get the Customer Total Deposit by ID
            deposit = Deposit.objects.filter(customer_id = customerID).aggregate(total=Sum('deposit_amount')
            )['total'] or Decimal()
            #Get the Customer Deposit Details
            customer_deposits = Deposit.objects.filter(customer__id = customerID)
            #Available balance
            available_balance = deposited_this_month - withdrawn_this_month
            #Get Customer Service charge from balance
            available_balance = available_balance - monthly_charge
            if request.method == 'POST':
                #Deposit Form
                form = CustomerDepositForm(request.POST or None)
                
                if form.is_valid():
                    #Get  Deposit Details for form variable
                    amount = form.cleaned_data['deposit_amount']

                    
                    
                    #Set Minimum Deposit
                    minimum_deposit = 100
                    #Check if Customer Deposit is Less than the Minimum Deposit
                    if amount < minimum_deposit:
                        messages.error(request, f'N{amount} is less than the Minimum Deposit of N{minimum_deposit}')
                    else:
                        #Generate Transaction ID
                        refID = "".join(str(random.randint(0, 10)) for _ in range(8))

                        #Add Customer Deposit
                        credit_acct = Deposit.objects.create(customer=profile, transID = refID, acct=acct, staff=user, deposit_amount=amount)
                        #Save the Customer Deposit
                        credit_acct.save()
                    
                        #Get Total Deposited this Month for the customer BY ID
                        deposited_this_month = Deposit.objects.filter(customer__id=customerID, date__year=now.year, date__month=now.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0
                        #Get Total Daily Deposits
                        daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
                        #Get Today's Total Withdrawal
                        daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0

                        #Group Customers Desposits for the Current Month by Accounts 
                        group_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month).order_by('acct')
                        customers_total_savings = group_deposits.annotate(total=Sum('deposit_amount')).order_by('-date')[:5]

                        context.update(  {
                        'amount':amount,
                        'customer_deposits':customer_deposits,
                        'daily_deposits':daily_deposits,
                        'daily_withdrawals':daily_withdrawals,
                        'customers':customers_total_savings,
                        'page_title':page_title,
                        'acct':acct,
                        'now':now,
                        'refID':refID,
                        'profile_surname':profile_surname,
                        'deposited_this_year':deposited_this_year,
                        'count_accounts':count_accounts,
                        'current_month_name':current_month_name,
                        })
                        
                        messages.success(request, f'N{amount} Deposited to Account {acct} Successfully.')
                        
                        return render(request, 'dashboard/deposit_slip.html', context)
                    
            else:
                form = CustomerDepositForm()
            context.update(  {
                    'daily_deposits':daily_deposits,
                    'daily_withdrawals':daily_withdrawals,
                    'count_accounts':count_accounts,
                    'deposit':deposit,
                    'page_title':page_title,
                    'customer':customer,
                    'now':now,
                    'current_year':current_year,
                    'current_month_name':current_month_name,
                    'form':form,
                    'deposited_this_month':deposited_this_month,
                    'deposited_this_year':deposited_this_year,
                    'acct':acct,
                    'monthly_charge':monthly_charge,
                    'available_balance':available_balance,
                    'withdrawn_this_month':withdrawn_this_month,
                    })
            return render(request, 'dashboard/deposit.html', context)
    else:
        return redirect('user-login')

#Customer Account Statement View
@login_required(login_url='user-login')
def account_statement(request, id):
    page_title = 'Account Statement'
    #Get the logged in user
    user = request.user
    #check if logged in user is staff
    if user.is_staff:
        try:
            customer = Account.objects.get(id=id)
            #Get Customer ID
            customerID = customer.customer.id
            
        except Account.DoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return redirect('create-customer')
        else:
            service_charge = Fee.objects.get(description='Saving')
            monthly_charges = service_charge.charge_amount
            #Get Customer Deposits by ID and order by Current Date with 5 Displayed
            deposits = Deposit.objects.filter(customer__id=customerID).order_by('-date')[:5]
            #deposits = deposits.order_by('-date')
            current_date = datetime.datetime.now()
            #Get Current Month Name from Calendar
            current_month_name = current_date.strftime('%B')
            #get Current Month total deposited by customer ID   
            deposited_this_month = Deposit.objects.filter(customer__id=customerID, date__year=current_date.year, date__month=current_date.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0
            #Get Current Year Deposited by customer ID
            deposited_this_year = Deposit.objects.filter(customer__id=customerID, date__year=current_date.year).aggregate(deposited_this_year=Sum('deposit_amount')).get('deposited_this_year') or 0
            #Count number of Customers
            count_accounts = Account.objects.count()
            #Get Today's Total Deposits
            daily_deposits = Deposit.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
            #Get Today's Total Withdrawn
            daily_withdrawals = Witdrawal.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
            #get Current Month total Withdrawn by customer ID   
            withdrawn_this_month = Witdrawal.objects.filter(account__id=customerID, date__year=current_date.year, date__month=current_date.month).aggregate(withdrawn_this_month=Sum('withdrawal_amount')).get('withdrawn_this_month') or 0
            #Get Current Year Total Withdrawn by customer ID
            withdrawn_this_year = Witdrawal.objects.filter(account__id=customerID, date__year=current_date.year).aggregate(withdrawn_this_year=Sum('withdrawal_amount')).get('withdrawn_this_year') or 0
            #Available Balance
            available_balance = deposited_this_month - withdrawn_this_month
            available_balance = available_balance - monthly_charges
            context = {
                'withdrawn_this_month':withdrawn_this_month,
                'withdrawn_this_year':withdrawn_this_year,
                'count_accounts':count_accounts,
                'daily_deposits':daily_deposits,
                'daily_withdrawals':daily_withdrawals,
                'deposits':deposits,
                'available_balance':available_balance,
                'customer':customer,
                'deposited_this_month':deposited_this_month,
                'page_title':page_title,
                'now':current_date,
                'current_month_name':current_month_name,
                'deposited_this_year':deposited_this_year,
                'monthly_charges':monthly_charges,

            }
            return render(request, 'dashboard/statement.html', context)
    else:
        return redirect('user-login')

#Deposit Slip
@login_required(login_url='user-login')
def deposit_slip(request, id):
    context = {}
    user = request.user
    if user.is_staff:
        #Get Day from current date and time
        date_today = datetime.datetime.now()
        #Get Today's Total Deposit 
        daily_deposits = Deposit.objects.filter(date__year=date_today.year, date__month=date_today.month, date__day=date_today.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
        #Get Today's Total Withdrawal
        daily_withdrawals = Witdrawal.objects.filter(date__year=date_today.year, date__month=date_today.month, date__day=date_today.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
        #Count Customers
        count_accounts = Account.objects.count()
        
        try:
            customer_deposit = Deposit.objects.get(id=id)
            
        except Deposit.DoesNotExist:
            messages.error(request, 'Something Went Wrong')
            
        else:
            customer_detail = customer_deposit
           
            
            context.update( {
            'customer_deposit':customer_detail,  
            'count_accounts':count_accounts,
            'daily_deposits':daily_deposits,
            'daily_withdrawals':daily_withdrawals,
            'now':date_today,
                    
                })
        return render(request, 'dashboard/slip.html', context)
    else:
        return redirect('user-login')

#Add Service Charge
@login_required(login_url='user-login')
def Add_Service_Charge(request):
    #get login user
    user = request.user
    #Check if logged in User is a Staff or Super User
    if user.is_staff and user.is_superuser:
        #Page Title
        page_title = 'Add Charges'

        #User Accounts
        user_accounts = Account.objects.all()[:10]

        #Get Day from current date and time
        date_today = datetime.now().date()
        #Get Today's Total Deposit 
        daily_deposits = Deposit.objects.filter(date__year=date_today.year, date__month=date_today.month, date__day=date_today.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
        #Get Today's Total Withdrawal
        daily_withdrawals = Witdrawal.objects.filter(date__year=date_today.year, date__month=date_today.month, date__day=date_today.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0


        form = ServiceChargeForm(request.POST or None)

        if request.method == 'POST' and form.is_valid():
                #Charges Form
                charge_name = form.cleaned_data['description']
                #Get amount from Charges For
                amount = form.cleaned_data['charge_amount']
                #Get value of charge Day
                charged_day = form.cleaned_data['due_day']
                #Filter to get Charge Name form from DB
                service_charge_name = Fee.objects.filter(description=charge_name)
                       
                #Check if the New Name already Exist
                if service_charge_name:
                    messages.error(request, f' {charge_name} Already Existed')
                #Check if the New Charge Day is not 31 or more
                elif charged_day >= 31:
                    messages.error(request, f' {charge_name} Can Not be More than 30')
                #if not then create a new Service Charge in DB
                else:
                    added_charges = Fee.objects.create(description=charge_name, staff=user, charge_amount=amount, due_day = charged_day)
                    #Save the New Charges Name
                    added_charges.save()
                    messages.success(request, f' {charge_name} Added Successfully')

        else:
            form = ServiceChargeForm()
        
        context = {
            'form':form,
            'page_title':page_title,
            'daily_deposits':daily_deposits,
            'daily_withdrawals':daily_withdrawals,

        }
        return render(request, 'dashboard/service_charge.html', context)
    else:
        return redirect('user-login')

#Customer Withdrawal View
@login_required(login_url='user-login')
def witdrawal(request, id):
    #Check whether Customer ACCOUNT EXIST USING ID
    try:
        customerID = Account.objects.get(id=id)
        #Get the Customer ID from Account
        customerID = customerID.customer.id
        profile = Profile.objects.get(customer=customerID)
    except Account.DoesNotExist:
        messages.error(request, 'Something Went Wrong')
        return redirect('create-customer')
    else:
        #Get the logged in User
        user = request.user
        #Check if the logged in User is Staff User
        if user.is_staff:
            page_title = 'Add Withdrawal'
            #Create an Empty Dictionary
            context = {

            }
            #Get Login user
            user = request.user

            form = CustomerwithdrawalForm(request.POST or None)
            #GET ALL USERS
            all_users = User.objects.all()
            #Count users
            count_users = all_users.count()
            #Read all Accounts
            user_accounts = Account.objects.all()[:10]
            #Count Number of User Accounts
            count_accounts = user_accounts.count()

            #Retrieve all Withdrawals
            withdrawals = Witdrawal.objects.all()

            #Get Current Date
            current_date = datetime.datetime.now()

            #Get Day of the Month from the current Date
            day_of_month = current_date.day

            #Get Service Charge 
            # try:
            saving_fee = Fee.objects.get(description='Saving')
            # except Fee.DoesNotExist:
            #     return redirect('create-customer')
            # else:
            
            #Get the exact charge date
            charge_date = saving_fee.due_day

            #Saving Fee Amount
            saving_charge_amount = saving_fee.charge_amount

            #Get Current Month Name from Current Date
            current_month_name = current_date.strftime('%B')
            #get Current Month total deposited by customer ID   
            deposited_this_month = Deposit.objects.filter(customer__id=customerID, date__year=current_date.year, date__month=current_date.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0
            #Get Current Year Deposited by customer ID
            deposited_this_year = Deposit.objects.filter(customer__id=customerID, date__year=current_date.year).aggregate(deposited_this_year=Sum('deposit_amount')).get('deposited_this_year') or 0
            #Count number of Customers
            count_accounts = Account.objects.count()
            #Get Today's Total Deposits
            daily_deposits = Deposit.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
            #Get Today's Total Withdrawn
            daily_withdrawals = Witdrawal.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0
            #get Current Month total Withdrawn by customer ID   
            withdrawn_this_month = Witdrawal.objects.filter(account__id=customerID, date__year=current_date.year, date__month=current_date.month).aggregate(withdrawn_this_month=Sum('withdrawal_amount')).get('withdrawn_this_month') or 0
            #Get Current Year Total Withdrawn by customer ID
            withdrawn_this_year = Witdrawal.objects.filter(account__id=customerID, date__year=current_date.year).aggregate(withdrawn_this_year=Sum('withdrawal_amount')).get('withdrawn_this_year') or 0
            
            #Group Customer's Deposits for Agregation
            group_deposits = Deposit.objects.filter(date__year=current_date.year, date__month=current_date.month).order_by('acct')
            
            #Get Totals of Customer's Savings
            customers_total_savings = group_deposits.annotate(total=Sum('deposit_amount')).order_by('-date')[:5]
            
            #Get Customer Total Withdrawal
            customer_withdrawals = Witdrawal.objects.filter(account__id = customerID).aggregate(total=Sum('withdrawal_amount')
            )['total'] or Decimal()

            #Get the Customer total deposit
            customer_deposit = Deposit.objects.filter(customer_id = customerID).aggregate(total=Sum('deposit_amount')
            )['total'] or Decimal()

            
            #Customer Account Balance
            acct_balance = deposited_this_month - saving_charge_amount 
            
            #Minus the Customer Account Balance from the Service Charge Amount
            available_balance = acct_balance - withdrawn_this_month

            try:
                #Check the Customer ID in DB
                customer = Account.objects.get(id=id)
                
                #Customer Account
                acct = customer.account_number
                
                
            except Account.DoesNotExist:
                messages.error(request, 'Customer Does Not Exist')
                return redirect('create-customer')
            else:
        
                if request.method == 'POST':

                    
                    #Deposit Form
                    form = CustomerwithdrawalForm(request.POST or None)
                    
                    if form.is_valid():
                        

                        #Withdrawal amount form value
                        amount = form.cleaned_data['withdrawal_amount']

                        #Check if Customer Withdrawal is a Positive Figure
                        if amount < 1:
                            messages.error(request, f'N{amount} is NOT a Valid Withdrawal Amount')
                        
                        #Check if Inputed Amount is Greater Than Customer Available Balance
                        elif amount > available_balance: 
                            messages.error(request, f'N{amount} is More Than Customer Aval. Balance of N{available_balance}')

                        
                            #messages.error(request, f'Sorry, You can NOT Empty Your Acct. at the Moment')
                        else:
                            #Withdrawal ID
                            refID = "".join(str(random.randint(0, 9)) for _ in range(7))
                            
                            
                            #Add Customer Deposit
                            debit_acct = Witdrawal.objects.create(account=profile, transID = refID, staff=user, withdrawal_amount=amount)
                            #Save the Customer Deposit
                            debit_acct.save()

                            now = datetime.datetime.now()
                            #Get Total Daily Deposits
                            daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
                            #Get Today's Total Withdrawal
                            daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0

                            #Get Customer Deposits by ID 
                            customer_withdrawals = Witdrawal.objects.filter(account_id=customerID)

                            #get Current Month total deposited by customer ID   
                            deposited_this_month = Deposit.objects.filter(customer__id=customerID, date__year=now.year, date__month=now.month).aggregate(deposited_this_month=Sum('deposit_amount')).get('deposited_this_month') or 0

                            #get Current Month total Withdrawn by customer ID   
                            withdrawn_this_month = Witdrawal.objects.filter(account__id=customerID, date__year=current_date.year, date__month=current_date.month).aggregate(withdrawn_this_month=Sum('withdrawal_amount')).get('withdrawn_this_month') or 0

                            #Customer Account Balance
                            acct_balance = deposited_this_month - saving_charge_amount 
            
                            #Minus the Customer Account Balance from the Service Charge Amount
                            available_balance = acct_balance - withdrawn_this_month

                            

                            context.update(  {
                            'customer':customer,
                            'customer_withdrawals':customer_withdrawals,
                            'deposited_this_month':deposited_this_month, 
                            'daily_deposits':daily_deposits,
                            'daily_withdrawals':daily_withdrawals,
                            'customers':customers_total_savings,
                            'page_title':page_title,
                            'count_accounts':count_accounts,
                            'now':now,
                            'amount':amount,
                            'acct':acct,
                            'refID':refID,
                            'profile':profile,
                            'available_balance':available_balance,
                            'current_month_name':current_month_name,
                            })
                            
                            
                            messages.success(request, f'N{amount} Withdrawn Successfully from Acct. No:{acct}. New Bal. N{available_balance}')
                            
                            return render(request, 'dashboard/withdrawal_slip.html', context)
                    else:
                        form = CustomerwithdrawalForm()
            
            
            context = {
                'saving_charge_amount':saving_charge_amount,
                'available_balance':available_balance,
                'day_of_month':day_of_month,
                'charge_date':charge_date,
                'acct_balance':acct_balance,
                'customer_withdrawals':customer_withdrawals,
                'deposited_this_month':deposited_this_month, 
                'customer':customer, 
                'deposited_this_year':deposited_this_year,
                'customer_deposit':customer_deposit,
                'now':current_date,
                'count_accounts':count_accounts,
                'daily_deposits':daily_deposits,
                'daily_withdrawals':daily_withdrawals,
                'withdrawn_this_month':withdrawn_this_month,
                'withdrawn_this_year':withdrawn_this_year,
                'count_users':count_users,
                'form':form,
                'current_month_name':current_month_name,
                'page_title':page_title,
            }
            return render(request, 'dashboard/witdrawal.html', context)
        else:
            return redirect('user-login')

#Daily Deposit List
@login_required(login_url='user-login')
def daily_deposits(request):
    #Get the logged in user
    user = request.user
    #Check if the logged in user is a Staff User
    if user.is_staff==True:
        #Get Staff Users
        all_users = User.objects.filter(is_staff=True)
        #Count Staff users
        count_users = all_users.count()
        #Page Title
        page_title = 'Deposits Today'

        #Count Customers
        count_accounts = Account.objects.count()

        #Get Date
        now = datetime.datetime.now() 
        #Group Customer's Deposits for Agregation
        group_deposits_today = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).order_by('-date')
        
        #Get Daily Total Savings of Customers
        deposits_today = group_deposits_today.annotate(total=Sum('deposit_amount')).order_by('-date')[:5]

        #Get Total Daily Deposits
        daily_deposits = Deposit.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
        #Get Today's Total Withdrawal
        daily_withdrawals = Witdrawal.objects.filter(date__year=now.year, date__month=now.month, date__day=now.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0

        context = {
            'deposits_today':deposits_today,
            'daily_deposits':daily_deposits,
            'daily_withdrawals':daily_withdrawals,
            'count_accounts':count_accounts,
            'customer':customer,
            'count_users':count_users,
            'page_title':page_title,
        }
        return render(request, 'dashboard/daily_deposits.html', context)
    #If Logged in User is NOT Staff User Redirect to login Page
    else:
        return redirect('user-login')


#Method for Reading and Creating Customer Accounts
@login_required(login_url='user-login')
def customer(request):
    #Get the logged in User
    user = request.user
    #Check if the logged in User is Staff User
    if user.is_staff:
        #Readd all Accounts
        user_accounts = Account.objects.all()[:10]
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
    else:
        return redirect('user-login')


# Create your views here.
@login_required(login_url='user-login')
def addUser(request):
    #Get the logged in User
    user = request.user
    #Check if the logged in User is Staff and Super User
    if user.is_staff and user.is_superuser:
        #Get all staff users
        all_users = User.objects.filter(is_staff=True)
        #Count all staff users
        count_users = all_users.count()

        #Retrieve all Desposits
        deposits = Deposit.objects.all()

        #Retrieve all Withdrawals
        withdrawals = Witdrawal.objects.all()
        
        #Get Day of today from current date and time
        current_date = datetime.datetime.now()

        
        # #Get Current Month Name from Calendar 
        current_month_name = calendar.month_name[date.today().month] 
        
        
        #Get Current Year Deposited by customer ID
        deposited_this_year = Deposit.objects.filter( date__year=current_date.year).aggregate(deposited_this_year=Sum('deposit_amount')).get('deposited_this_year') or 0
        #Count number of Customers
        count_accounts = Account.objects.count()
        #Get Daily Saving Total Amount
        daily_deposits = Deposit.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_deposits=Sum('deposit_amount')).get('daily_deposits') or 0
        #Get Today's Total Withdrawn
        daily_withdrawals = Witdrawal.objects.filter(date__year=current_date.year, date__month=current_date.month, date__day=current_date.day).aggregate(daily_withdrawals=Sum('withdrawal_amount')).get('daily_withdrawals') or 0

        if request.method == 'POST':
            #Create User Form
            userForm = CreateUserForm(request.POST or None)

            if userForm.is_valid():
                #Get username value from User Form
                user_name = userForm.cleaned_data.get('username')
                #Get Password value from User Form
                user_pass = userForm.cleaned_data.get('password1')
                #Create a new user and set it as Staff
                user = User.objects.create(username=user_name, is_staff=True)
                #Set the User Password as the User Form value password
                user.set_password(user_pass)
                user.save()
                return redirect('user-register')
        else:
            
            userForm = CreateUserForm()

        context = {
            
            'count_users':count_users,
            'userForm':userForm,
            
            
            'count_users':count_users,
            'all_users':all_users,
            'daily_deposits':daily_deposits,
            'daily_withdrawals':daily_withdrawals,
        }
        return render(request, 'user/user.html', context)
    else:
        return redirect('user-login')

# @login_required
# def profile(request):
#     return render(request, 'user/profile.html')

#Update User Profile Method
# @login_required
# def profile_update(request):
#     if request.method == 'POST':
        
#         profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.customer)

#         if user_form.is_valid and profile_form.is_valid:
#             user_form.save()
#             profile_form.save()
#             return redirect('user-profile')
#     else:
        
#         profile_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         'user_form':user_form,
#         'profile_form':profile_form,
#     }
#     return render(request, 'user/profile_update.html', context)
