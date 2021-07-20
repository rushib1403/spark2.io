from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Complain(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    complain=models.TextField(max_length=500)
    def __str__(self):
        return self.complain
class Bill(models.Model):
    user2=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.IntegerField()