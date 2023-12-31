# Generated by Django 4.2.5 on 2023-12-21 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0006_contractor_email_contractor_mobile_contractor_nid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareholder',
            name='numberOfFlat',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Number of Flats'),
        ),
        migrations.AlterField(
            model_name='shareholder',
            name='shareholderName',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
    ]
