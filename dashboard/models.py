# from tabnanny import verbose
# from django.db import models
# import uuid
# from django.urls import reverse
# from django.contrib.auth.models import User
# from PIL import Image

# GENDER = (
# 	('Male', 'Male'),
# 	('Female', 'Female'),
# )



# class Profile(models.Model):
#     customer = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
#     surname = models.CharField(max_length=20, null=True)
#     othernames = models.CharField(max_length=40, null=True)
#     gender = models.CharField(max_length=6, choices=GENDER, blank=True, null=True)
#     address = models.CharField(max_length=200, null=True)
#     phone = models.CharField(max_length=11, null=True)
#     image = models.ImageField(default='avatar.jpg', blank=False, null=False, upload_to ='profile_images', 
   
#     )
    

#     #Method to save Image
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         img = Image.open(self.image.path)
#     #Check for Image Height and Width then resize it then save
#         if img.height > 200 or img.width > 150:
#             output_size = (150, 250)
#             img.thumbnail(output_size)
#             img.save(self.image.path)
            

    
 
#     def __str__(self):
#         return f'{self.customer.username}-Profile'


# # Create your models here.
# class Customer(models.Model): 
#     account_number = models.CharField(max_length=10, null=True)
#     date = models.DateTimeField(auto_now_add=True, null=True) 
#     staff = models.OneToOneField(Profile, on_delete=models.CASCADE, null = True)
    
#     #Get the url path of the view
#     def get_absolute_url(self):
#         return reverse('customer_create', args=[self.id])

#     #Making Sure Django Display the name of our Models as it is without Pluralizing
#     class Meta:
#         verbose_name_plural = 'Customer'

#     #
#     def __str__(self):
#         return f'{self.surname} {self.othernames} - {self.account_number}' 

# class Deposit(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
#     acct = models.CharField(max_length=6, null=True)
#     staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     deposit_amount = models.PositiveIntegerField(null=True) 
#     date = models.DateTimeField(auto_now_add=True)  
 
#     def get_absolute_url(self):
#         return reverse('create_account', args=[self.id])

#     def __str__(self):
#         return f'{self.customer} Deposited {self.deposit_amount} by {self.staff.username}'

# class Witdrawal(models.Model): 
#     account = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
#     staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     withdrawal_amount = models.PositiveIntegerField(null=True)
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.account}- Withdrawn - {self.withdrawal_amount}'

# #Service Charge Model
# class Fee(models.Model): 
#     description = models.CharField(max_length=30, null=True)
#     staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     charge_amount = models.PositiveIntegerField(null=True)
#     due_day = models.PositiveIntegerField(null=True) 
#     date = models.DateTimeField(auto_now_add=True, blank=True)

#     def __str__(self):
#         return f'{self.description}- Charges - {self.charge_amount}'

# #Charges Payment Model
# class Payment(models.Model): 
#     account = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
#     description = models.ForeignKey(Fee, on_delete=models.CASCADE, null=True)
#     charge_amount = models.PositiveIntegerField(null=True)
#     date = models.CharField(max_length=30, null=True)

#     def __str__(self):
#         return f'{self.account}- Charges - {self.charge_amount}'