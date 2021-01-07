from django.db import models
from django.utils import timezone

class Coin(models.Model):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=200)
    valid = models.BooleanField(default=True)
    created_date = models.DateTimeField('date created',default=timezone.now(), editable=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        verbose_name_plural = "Coins"


    def __str__(self):
        return self.name

class CoinData(models.Model):
    coin = models.OneToOneField(
                            Coin, 
                            on_delete=models.CASCADE,
                            primary_key=True,)
    price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    direct_volume = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    total_volume = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    top_tier_volume = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    market_cap = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    valid = models.BooleanField(default=True)
    created_date = models.DateTimeField('date created',default=timezone.now(), editable=True)

    class Meta:
        verbose_name_plural = "Coin Data"


    def __str__(self):
        return self.coin.name