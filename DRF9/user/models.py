from django.db import models

# Create your models here.

class user_detail(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

