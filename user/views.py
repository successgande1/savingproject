from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

from . forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.models import User
from datetime import datetime
import datetime

from dashboard.models import Customer, Deposit, Witdrawal



# Create your views here.
@login_required
def addUser(request):
    all_users = User.objects.all()
    count_users = all_users.count()

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

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-register')
    else:
        form = CreateUserForm()

    context = {
        'form':form,
        'count_users':count_users,
        'count_deposits_today':count_deposits_today,
        'count_withdrawals_today':count_withdrawals_today,
        'count_users':count_users,
        'all_users':all_users,
    }
    return render(request, 'user/user.html', context)

@login_required
def profile(request):
    return render(request, 'user/profile.html')

#Update User Profile Method
@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request, 'user/profile_update.html', context)
