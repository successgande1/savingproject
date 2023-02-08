"""savingproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings 

#import user view for urls routing in the main project urls file
from user import views as user_view
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('addUser/', user_view.addUser, name = 'user-register'),
    path('profile/<int:pk>/detail/', user_view.view_profile, name = 'user-profile'), 
    path('create_customer/', user_view.create_account, name = 'create-customer'),
    path('update_profile/<int:pk>/', user_view.update_profile, name = 'update-profile'),
    path('customer/', user_view.customer, name = 'dashboard-customer'),
    path('update/<int:pk>/customer/', user_view.update_customer_profile, name = 'update-customer'),
    # path('deposit_list/', user_view.DepositListView, name = 'deposit-list'), 
    
    path('create/<int:id>/deposit/', user_view.customer_deposit, name = 'create-deposit'),
    path('daily_deposits/', user_view.daily_deposits, name = 'daily-deposits'),
    path('account/<int:id>/statement/', user_view.account_statement, name = 'account-statement'),
    path('deposit/slip/<int:id>/', user_view.deposit_slip, name = 'deposit-slip'),
    path('witdrawal/<int:id>/customer/', user_view.witdrawal, name = 'dashboard-witdrawal'), 
    path('add/charges/', user_view.Add_Service_Charge, name = 'add-charges'), 

    path('', auth_views.LoginView.as_view(template_name='user/login.html'), name = 'user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name = 'user-logout'),
] + static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
