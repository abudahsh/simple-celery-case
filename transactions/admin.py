from django.contrib import admin

# Register your models here.
from .models import Loan, Person

admin.site.register(Person)
admin.site.register(Loan)