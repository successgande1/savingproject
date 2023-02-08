from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('dashboard/', views.index, name = 'dashboard-index'),
    # path('create_customer/', create_account, name = 'create-customer'),
   
    # path('deposit_list/', DepositListView.as_view(), name = 'deposit-list'),
    # path('customer/', views.customer, name = 'dashboard-customer'),
    # path('create/<int:id>/deposit/', views.customer_deposit, name = 'create-deposit'),
    # path('daily_deposits/', daily_deposits, name = 'daily-deposits'),
    # path('account/<int:id>/statement/', views.account_statement, name = 'account-statement'),
    # path('deposit/slip/<int:customer_id>/', views.deposit_slip, name = 'deposit-slip'),
    # path('witdrawal/<int:id>/customer/', views.witdrawal, name = 'dashboard-witdrawal'), 
    # path('add/charges/', views.Add_Service_Charge, name = 'add-charges'), 
] 