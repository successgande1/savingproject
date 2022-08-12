from sys import implementation
from django.contrib import admin

#Change Admin Site Header
admin.site.site_header = 'Accounting Saving Dashboard'

from . models import Customer, Deposit, Witdrawal

#Customize the Display of Customer Model in the Admin Backend in a Table Form
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('surname', 'othernames', 'account_number', 'address', 'phone' )
    list_filter = ['address'] #List needs no comma at the end but Tuple does ('phone',)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('customer', 'staff', 'deposit_amount', 'date',)

class WitdrawalAdmin(admin.ModelAdmin):
    list_display = ('account', 'staff', 'withdrawal_amount', 'date',)

# Register your models here.
admin.site.register(Customer, CustomersAdmin)

admin.site.register(Deposit, DepositAdmin)

admin.site.register(Witdrawal, WitdrawalAdmin)
