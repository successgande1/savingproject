# from sys import implementation
# from django.contrib import admin

# #Change Admin Site Header
# admin.site.site_header = 'Accounting Saving Dashboard'

# from . models import *

# #Customize the Display of Customer Model in the Admin Backend in a Table Form
# class CustomersAdmin(admin.ModelAdmin):
#     list_display = ('account_number', 'date' )
#     list_filter = ['account_number'] #List needs no comma at the end but Tuple does ('phone',)

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'surname', 'othernames', 'gender', 'address', 'phone', 'image', )

# class DepositAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'staff', 'deposit_amount', 'date',)

# class WitdrawalAdmin(admin.ModelAdmin):
#     list_display = ('account', 'staff', 'withdrawal_amount', 'date',)

# class FeeAdmin(admin.ModelAdmin):
#     list_display = ('description', 'charge_amount', 'due_day', 'staff', 'date',)

# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('account', 'description', 'charge_amount', 'date',)

# # Register your models here.
# admin.site.register(Customer, CustomersAdmin)

# admin.site.register(Deposit, DepositAdmin)

# admin.site.register(Witdrawal, WitdrawalAdmin)

# admin.site.register(Fee, FeeAdmin)

# admin.site.register(Payment, PaymentAdmin)

# admin.site.register(Profile, ProfileAdmin)
