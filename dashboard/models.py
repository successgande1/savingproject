from tabnanny import verbose
from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    surname = models.CharField(max_length=10, null=True)
    othernames = models.CharField(max_length=20, null=True)
    account_number = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=11, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    #Get the url path of the view
    def get_absolute_url(self):
        return reverse('customer_create', args=[self.id])

    #Making Sure Django Display the name of our Models as it is without Pluralizing
    class Meta:
        verbose_name_plural = 'Customer'

    #
    def __str__(self):
        return f'{self.surname} {self.othernames} - {self.account_number}'

class Deposit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    acct = models.CharField(max_length=6, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    deposit_amount = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('create_account', args=[self.id])

    def __str__(self):
        return f'{self.customer} Deposited {self.deposit_amount} by {self.staff.username}'

class Witdrawal(models.Model):
    account = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    withdrawal_amount = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.account}- Withdrawn - {self.withdrawal_amount}'