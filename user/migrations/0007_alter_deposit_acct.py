# Generated by Django 4.0.4 on 2023-02-08 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_account_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='acct',
            field=models.CharField(max_length=10, null=True),
        ),
    ]