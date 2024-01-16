# Generated by Django 5.0 on 2024-01-11 06:45

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0016_rename_contractorbill_contractorbillpayment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractorBillSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOfBillSubmission', models.DateField(default=datetime.datetime.now)),
                ('description', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ContractorBillSubmission', to='Accounts.contractor')),
            ],
        ),
    ]
