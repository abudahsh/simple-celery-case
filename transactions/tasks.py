from celery.app import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

from .models import Person, Loan



@shared_task()
def check_user_has_bank_account(person_id):
    person = Person.objects.get(pk=person_id)
    try:
        if person.has_bank_account and person.verified_bank_account:
            """
            Here we can check using 3rd party , like sending a request to bank services to check if the user has actual account
            requests.post('https://www.bankwebsite.com/services/api/checkuser',
            data={
            'email':'blah@yahoo.com'
            'first_name':'blah'
            'last_name':'blah'
            }
            
            with some headers according to the api specs of the bank account to get the response
            
            example with stripe 
            stripe.Charge.retrieve(
              "ch_1DHD6T2eZvKYlo2Cf3fRkNLg",
              api_key="sk_test_4eC39HqLyjWDarjtT1zdp7dc"
            )
            """

            return True

    except ConnectionError:
        return False

@shared_task()
def check_agreement_on_amount(loan_id):
    loan = Loan.objects.get(pk=loan_id)
    if loan.loaner_offer == loan.borrower_request:
        print('hiii')
        return True
    else:
        print('bye')
        raise ConnectionError


@shared_task()
def check_loaner_balance(loaner_id):
    loaner = Person.objects.get(pk=loaner_id)
    """
    check the balance of the loaner using his bank account details
    example with stripe
    {
          "object": "balance",
          "available": [
            {
              "currency": "cad",
              "amount": -47651,
              "source_types": {
                "card": -47651,
                "bitcoin_receiver": 0,
                "bank_account": 0
              }
            },
            {
              "currency": "gbp",
              "amount": 7273405,
              "source_types": {
                "card": 7273405,
                "bitcoin_receiver": 0,
                "bank_account": 0
                }
            }
        }
    """

    return True

@periodic_task(
    #making a request every month to reduce the monthly payment from the loaner account
    run_every=(crontab(0, 0, day_of_month='1')),
    name="tasks.schedule_payments",


)
@shared_task()
def schedule_payments(monthly_amount, loaner_id, borrower_id):
    loaner= Person.objects.get(pk=loaner_id)
    borrower = Person.objects.get(pk=borrower_id)

    try:
        loan=Loan.objects.get(loaner=loaner, borrower=borrower)
        """Handle 3rd party request to make the payment
        example with stripe payments
        stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
        
        stripe.Charge.create(
          amount=2000,
          currency="usd",
          description="Charge for jenny.rosen@example.com",
          source="tok_visa", # obtained with Stripe.js
          idempotency_key='fR2zYIw2NY3KsZfx'
        )
        """
        reminder = loan.remain_loan_amount

        if reminder >= monthly_amount:
            loan.remain_loan_amount -=monthly_amount
            loan.save()
            return True
        else :
            return False
    except ConnectionError:
        return False

