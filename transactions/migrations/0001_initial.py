# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-05 13:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loaner_offer', models.IntegerField(default=0)),
                ('borrower_request', models.IntegerField(default=0)),
                ('total_loan_amount', models.IntegerField(default=0)),
                ('remain_loan_amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_bank_account', models.BooleanField(default=False)),
                ('verified_bank_account', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='loan',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='transactions.Person'),
        ),
        migrations.AddField(
            model_name='loan',
            name='loaner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lendings', to='transactions.Person'),
        ),
    ]