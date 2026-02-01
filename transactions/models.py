import uuid

from django.db import models

# Create your models here.
class TransactionsModel(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user_uuid = models.UUIDField(
        default=uuid.uuid4
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class PlaidTransactionsModel(models.Model):
    user_uuid = models.UUIDField(
        default=uuid.uuid4
    )
    account_id = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_name = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)