# Generated by Django 5.0 on 2024-01-16 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0024_creditpurchasepayment_voucherno'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractor',
            name='IsArchive',
            field=models.BooleanField(default=False),
        ),
    ]
