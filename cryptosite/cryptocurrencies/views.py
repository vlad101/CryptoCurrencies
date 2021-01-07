from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Coin, CoinData

class IndexView(generic.ListView):
    context_object_name = 'coin_list'
    template_name = 'cryptocurrencies/index.html'

    def get_queryset(self):
        """Return all coins."""
        return Coin.objects.all()

class DetailView(generic.DetailView):
    model = Coin
    template_name = 'cryptocurrencies/detail.html'