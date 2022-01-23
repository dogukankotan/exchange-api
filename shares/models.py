from django.core.validators import MinLengthValidator
from django.db import models

class Portfolio(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

class Share(models.Model):
    symbol = models.CharField(max_length=3, validators=[MinLengthValidator(3)])
    quantity = models.DecimalField(max_digits=32, decimal_places=2)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("symbol", "portfolio")