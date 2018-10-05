from celery.schedules import crontab
from celery.task import periodic_task
from django.shortcuts import render

# Create your views here.
from .models import Person, Loan
from .tasks import schedule_payments, check_user_has_bank_account, check_agreement_on_amount, check_loaner_balance

def on_raw_message(body):
    print(body)

def home(request):
    loaner=Person.objects.get(pk=1)
    borrower = Person.objects.get(pk=2)
    loan= Loan.objects.get(loaner=loaner, borrower=borrower)
    account1=check_user_has_bank_account.delay(loaner.pk)
    account2=check_user_has_bank_account.delay(borrower.pk)
    total_loan = loan.total_loan_amount
    if account1.get() == True and account2.get() ==True:

        agreed=check_agreement_on_amount.apply_async((loan.pk,) , retry=True, retry_policy={
            'max_retries': 3,
            'interval_start': 0,
            'interval_step': 0.2,
            'interval_max': 0.2,
        })
        if agreed.get()==True:
            balance = check_loaner_balance.apply_async((loaner.pk,) , retry=True, retry_policy={
            'max_retries': 3,
            'interval_start': 3,
            'interval_step': 0.2,
            'interval_max': 0.2,
        })
            if balance.get() == True:
                schedule_payments.delay(total_loan/6, loaner.pk, borrower.pk)
            else:
                print("loaner doesn't have the required balance")
        else:
            print("Users Didn't agree on the amount")
    else:
        print( "One of the users or both doesn't have bank account")
    return render(request, 'index.html')