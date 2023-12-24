from django.contrib import admin
from .models import (
    UserLoggedinRecord,
    UserLoggedinFailed,
    Shareholder,
)

# Register your models here.


@admin.register(UserLoggedinRecord)
class UserLoggedinRecordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserLoggedinRecord._meta.get_fields()]


@admin.register(Shareholder)
class ShareholderAdmin(admin.ModelAdmin):
    list_display = ["shareholderName", "email", "mobile", "nid", "numberOfFlat"]


@admin.register(UserLoggedinFailed)
class UserLoggedinFailedAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserLoggedinFailed._meta.get_fields()]
