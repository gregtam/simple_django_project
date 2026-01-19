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