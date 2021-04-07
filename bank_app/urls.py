from django.contrib import admin
from django.urls import path
from . import views

app_name = 'bank_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('add_user', views.add_user, name="add_user"),
    path('change_rank', views.change_rank, name="change_rank"),
    path('add_account', views.add_account, name="add_account"),
    path('transfer_money', views.transfer_money, name="transfer_money"),
    path('make_loan', views.make_loan, name="make_loan"),
    path('<int:Costumer_id>/', views.account_detail, name="account_detail"),

 ]
