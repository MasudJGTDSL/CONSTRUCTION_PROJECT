from django.urls import path,include
from . import views
app_name = 'Accounts'

urlpatterns = [
    path('', views.index, name="index"),
    path('send_mail/', views.send_mail, name="send_mail"),
    path('expenditure/', views.ExpenditureView.as_view(), name="ExpenditureView"),
    path('chart/', views.chart, name="chart"),

    ]