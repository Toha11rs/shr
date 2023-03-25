from django.db import models
from django.contrib import auth
from django.utils.translation import gettext as _
from django.contrib.auth.models import User, Permission, Group


class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.FloatField()

    class Meta:
        db_table = 'balance'

    def __init__(self, *args, **kwargs):
        super(Balance, self).__init__(*args, **kwargs)
        if self.amount is None:
            self.amount = 0.0

    def add_funds(self, amount):
        self.amount += amount


class Share(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    price = models.FloatField()

    def __str__(self):
        return self.ticker

    class Meta:
        db_table = 'share'


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.ForeignKey(Share, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    price = models.FloatField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    is_buy = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} {self.transaction_type} {self.quantity} {self.share.ticker} @ {self.price}"

    class Meta:
        db_table = 'Transaction'


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.ForeignKey(Share, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.FloatField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_buy = models.BooleanField(default=True)

    @property
    def balance(self):
        return self.user.balance

    def __str__(self):
        return f"{self.user.username} - {self.quantity} {self.share.ticker} @ {self.purchase_price}"

    class Meta:
        db_table = 'Portfolio'
