# Generated by Django 4.0.4 on 2022-08-11 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_customer_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='accountnumber',
            new_name='account_number',
        ),
    ]