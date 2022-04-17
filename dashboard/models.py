from tabnanny import verbose
from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    firstname = models.CharField(max_length=10, null=True)
    othernames = models.CharField(max_length=10, null=True)
    accountnumber = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=11, null=True)

    #Making Sure Django Display the name of our Models as it is without Pluralizing
    class Meta:
        verbose_name_plural = 'Customer'

    #
    def __str__(self):
        return f'{self.firstname} {self.othernames} - {self.accountnumber}'

class Deposit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    deposit_amount = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer} Deposited {self.deposit_amount} by {self.staff.username}'

    