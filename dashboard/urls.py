from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('dashboard/', views.index, name = 'dashboard-index'),
    path('create_customer/', create_account, name = 'customer_create'),
    path('customers_list/', CustomerListView.as_view(), name = 'customers-list'),
    path('deposit_list/', DepositListView.as_view(), name = 'deposit-list'),
    path('customer/', views.customer, name = 'dashboard-customer'),
    path('create/<int:id>/deposit/', views.customer_deposit, name = 'create-deposit'),
    path('confirm/<int:id>/deposit/', views.approve_deposit, name = 'approve-deposit'),
    path('deposit/slip/', views.deposit_slip, name = 'deposit-slip'),
    path('deposit/<int:id>', views.deposit, name = 'dashboard-deposit'),
    path('witdrawal/', views.witdrawal, name = 'dashboard-witdrawal'),
] 