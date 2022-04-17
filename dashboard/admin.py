from sys import implementation
from django.contrib import admin

#Change Admin Site Header
admin.site.site_header = 'Accounting Saving Dashboard'

from . models import Customer, Deposit

#Customize the Display of Customer Model in the Admin Backend in a Table Form
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'othernames', 'accountnumber', 'address', 'phone' )
    list_filter = ['address'] #List needs no comma at the end but Tuple does ('phone',)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('customer', 'staff', 'deposit_amount', 'date',)

# Register your models here.
admin.site.register(Customer, CustomersAdmin)

admin.site.register(Deposit, DepositAdmin)
