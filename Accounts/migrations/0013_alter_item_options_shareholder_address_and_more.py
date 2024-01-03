# Generated by Django 5.0 on 2024-01-02 11:16

import Accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0012_alter_expenditure_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('ItemCode', 'itemName')},
        ),
        migrations.AddField(
            model_name='shareholder',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='shareholder',
            name='image',
            field=models.ImageField(blank=True, default='ShareholdersImage/default.png', max_length=255, null=True, upload_to='ShareholdersImage/'),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='image',
            field=models.ImageField(blank=True, default='ContractorsImage/default.png', max_length=255, null=True, upload_to=Accounts.models.path_and_rename),
        ),
    ]
