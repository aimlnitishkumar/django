from django.db import models

# Create your models here.

class Account(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    account_holder = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_holder} - {self.account_number}"