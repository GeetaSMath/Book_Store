from django.db import models
# from user.models import User
from user.models import User


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    price = models.IntegerField()
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
