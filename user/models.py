from email.policy import default
from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11, null=True)
    image = models.ImageField(default = 'avatar.jpeg', upload_to = 'Profile_images')

    def __str__(self):
        return f'{self.staff.username}--Profile'
