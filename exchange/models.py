from django.db import models


class Market(models.Model):
    class Flow(models.IntegerChoices):
        SELL = 1, 'sell'
        BUY = 2, 'buy'

    share = models.ForeignKey("shares.Share", on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=32, decimal_places=2)
    rate = models.DecimalField(max_digits=32, decimal_places=2)
    flow = models.PositiveIntegerField(choices=Flow.choices, null=True)


class Transaction(models.Model):
    from_user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name="sell")
    to_user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name="buy")
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=32, decimal_places=2)
    rate = models.DecimalField(max_digits=32, decimal_places=2)
