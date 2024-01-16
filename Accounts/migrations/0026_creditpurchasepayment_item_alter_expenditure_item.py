# Generated by Django 5.0 on 2024-01-16 08:14

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0025_contractor_isarchive'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditpurchasepayment',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Item', to='Accounts.item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expenditure',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Expenditure_Item', to='Accounts.item'),
        ),
    ]
