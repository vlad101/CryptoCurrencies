from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Coin, CoinData

class IndexView(generic.ListView):
    template_name = 'cryptocurrencies/index.html'
    context_object_name = 'coin_list'

    def get_queryset(self):
        """Return all crypto ccoins."""
        return Coins.objects.all()

class DetailView(generic.DetailView):
    model = Coin
    template_name = 'cryptocurrencies/detail.html'