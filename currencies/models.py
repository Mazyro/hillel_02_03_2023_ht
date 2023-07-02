from django.db import models

from project.mixins.models import PKMixin
from project.model_choices import Currencies


def get_usd_rate():
    return CurrencyHistory.objects.filter(
        code=Currencies.USD
    ).latest('created_at').sale


def get_euro_rate():
    return CurrencyHistory.objects.filter(
        code=Currencies.EUR
    ).latest('created_at').sale


class CurrencyHistory(PKMixin):
    code = models.CharField(
        max_length=16,
        choices=Currencies.choices,
        default=Currencies.UAH
    )
    buy = models.DecimalField(
        default=1,
        max_digits=18,
        decimal_places=2
    )
    sale = models.DecimalField(
        default=1,
        max_digits=18,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.code} - {self.buy} / {self.sale}"
