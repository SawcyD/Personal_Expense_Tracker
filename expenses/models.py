from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'
        app_label = 'expenses'


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 9999999.99

    class Meta:
        app_label = 'expenses'


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 9999999.99
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        app_label = 'expenses'
