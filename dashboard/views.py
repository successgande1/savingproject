from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')

def customer(request):
    return render(request, 'dashboard/customers.html')

def deposit(request):
    return render(request, 'dashboard/deposit.html')

def witdrawal(request):
    return render(request, 'dashboard/witdrawal.html')