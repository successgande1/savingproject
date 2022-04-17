from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'dashboard-index'),
    path('customer/', views.customer, name = 'dashboard-customer'),
    path('deposit/', views.deposit, name = 'dashboard-deposit'),
    path('witdrawal/', views.witdrawal, name = 'dashboard-witdrawal'),
]