from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Sum
from django.db.models.functions import Abs
from uuid import uuid4
from decimal import Decimal


# Create your models here.

class Costumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    rank = models.CharField(max_length=15, default="Basic")
    is_employee = models.BooleanField(default=False)

    @property
    def can_make_loans(self):
        if self.rank == "Gold" or self.rank == "Silver":
            return True
        else:
            return False

    def __str__(self):
        return f"{self.user} - {self.rank} - {self.can_make_loans}"


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    is_account = models.BooleanField(default=True)

    
    @property
    def balance(self):
        # return Ledger.objects.filter(account=self).aggregate(Sum('amount') or Decimal(0)
        return Ledger.objects.filter(account=self).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)


    def __str__(self):
        return f"{self.user} - {self.name}"



class Ledger(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    text = models.CharField(max_length=75)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)

    @classmethod
    def transaction(cls, amount, text, debit_account, credit_account):
        transaction_id = uuid4()
        amount_negative = -int(amount)

        debit_account = Account.objects.get(id=debit_account)
        credit_account = Account.objects.get(id=credit_account)


        with transaction.atomic():

            credit = Ledger()
            credit.account = credit_account
            credit.amount = amount_negative
            credit.text = text
            credit.transaction_id = transaction_id
            credit.save()

            debit = Ledger()
            debit.account = debit_account
            debit.amount = int(amount)
            debit.text = text
            debit.transaction_id = transaction_id
            debit.save()

    
    def __str__(self):
        return f"{self.account} - {self.amount} - {self.transaction_id}"



