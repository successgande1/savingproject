from django.urls import path

from . import views
from .views import CustomerListView, CustomerCreateView

urlpatterns = [
    path('dashboard/', views.index, name = 'dashboard-index'),
    path('customer_create/', CustomerCreateView.as_view(), name = 'customer_create'),
    path('customers_list/', CustomerListView.as_view(), name = 'customers-list'),
    path('customer/', views.customer, name = 'dashboard-customer'),
    path('deposit/', views.deposit, name = 'dashboard-deposit'),
    path('witdrawal/', views.witdrawal, name = 'dashboard-witdrawal'),
]