from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Person (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_bank_account =models.BooleanField(default=False)
    verified_bank_account =models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

class Loan(models.Model):
    loaner=models.ForeignKey(Person, related_name='lendings')
    borrower = models.ForeignKey(Person , related_name='loans')
    loaner_offer =models.IntegerField(default=0)
    borrower_request = models.IntegerField(default=0)
    total_loan_amount = models.IntegerField(default=0)
    remain_loan_amount = models.IntegerField(default=0)

    def __str__(self):
        return str('loan from: ' + str(self.loaner) + ' to: '+ str(self.borrower))