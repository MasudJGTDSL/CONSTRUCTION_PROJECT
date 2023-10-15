from django.urls import path,include
from . import views
app_name = 'Accounts'

urlpatterns = [
    path('', views.index, name="index"),

    ]