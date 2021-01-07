from django.contrib import admin

from .models import Coin, CoinData

admin.site.register(Coin)
admin.site.register(CoinData)