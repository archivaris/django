from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)

    date_of_birth = models.DateField(blank=True, null=True)
    roll = models.CharField(max_length=6, unique=True)
    registration_number = models.CharField(max_length=6, unique=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ['roll']
