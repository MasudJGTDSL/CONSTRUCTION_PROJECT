# Generated by Django 5.0 on 2024-01-15 12:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Accounts", "0017_contractorbillsubmission"),
    ]

    operations = [
        migrations.AddField(
            model_name="contractorbillpayment",
            name="voucherNo",
            field=models.CharField(default="", max_length=100),
        ),
    ]
