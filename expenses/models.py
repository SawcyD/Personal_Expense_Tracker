from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField

class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    goal_amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    achieved = models.BooleanField(default=False)

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'
        app_label = 'expenses'




class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default = '2023-01-01' )

    def __str__(self):
        return self.category



class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 9999999.99
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField( default = '2023-01-01' )

    class Meta:
        app_label = 'expenses'
