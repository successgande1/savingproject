# Generated by Django 4.0.4 on 2022-08-12 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_deposit_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='acct',
            field=models.CharField(max_length=6, null=True),
        ),
    ]