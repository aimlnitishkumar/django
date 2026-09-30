from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    age = models.IntegerField()
    grade = models.CharField(max_length= 50, blank = True)


    def __str__(self):
        return self.first_name

