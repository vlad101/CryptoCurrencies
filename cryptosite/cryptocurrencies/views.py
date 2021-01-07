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

    def get_context_data(self, **kwargs):
        # Number of visits to the index page, as counted in the session variable.
        num_visits = self.request.session.get('num_visits', 1)
        self.request.session['num_visits'] = num_visits + 1
        # Build context data
        context = super().get_context_data(**kwargs)
        context['num_visits'] = num_visits
        return context

class DetailView(generic.DetailView):
    model = Coin
    template_name = 'cryptocurrencies/detail.html'