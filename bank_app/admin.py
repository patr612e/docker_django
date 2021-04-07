from django.contrib import admin

from .models import Costumer, Account, Ledger

# Register your models here.

admin.site.register(Costumer)
admin.site.register(Account)
admin.site.register(Ledger)

