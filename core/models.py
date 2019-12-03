from django.db import models
from django.utils import timezone


class NewsSubscription(models.Model):
    time = models.DateTimeField(default=timezone.now)
    email = models.EmailField()

    def as_json(self):
        return {"time": self.time, "email": self.email}

    def __str__(self):
        return self.email


class TokenMetric(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    rank = models.IntegerField()
    price_usd = models.DecimalField(max_digits=12, decimal_places=7)
    price_btc = models.DecimalField(max_digits=24, decimal_places=16)
    day_volume_usd = models.DecimalField(max_digits=12, decimal_places=2)
    market_cap_usd = models.DecimalField(max_digits=12, decimal_places=2)
    available_supply = models.DecimalField(max_digits=24, decimal_places=8)
    total_supply = models.DecimalField(max_digits=24, decimal_places=8)
    percent_change_1h = models.DecimalField(max_digits=12, decimal_places=2)
    percent_change_24h = models.DecimalField(max_digits=12, decimal_places=2)
    percent_change_7d = models.DecimalField(max_digits=12, decimal_places=2)
