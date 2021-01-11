from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Coin, CoinData


class IndexView(LoginRequiredMixin, ListView):
    context_object_name = 'coin_list'
    template_name = 'cryptocurrencies/index.html'

    def get_queryset(self):
        """Return all coins."""
        return Coin.objects.all()

    def get_context_data(self, **kwargs):
        # Number of visits to the index page, as counted in the session variable.
        num_visits = self.request.session.get('index_num_visits', 1)
        self.request.session['index_num_visits'] = num_visits + 1
        # Build context data
        context = super().get_context_data(**kwargs)
        context['index_num_visits'] = num_visits
        return context


class DetailView(LoginRequiredMixin, DetailView):
    model = Coin
    template_name = 'cryptocurrencies/detail.html'

    def get_context_data(self, **kwargs):
        # Number of visits to the index page, as counted in the session variable.
        num_visits = self.request.session.get('detail_num_visits', 1)
        self.request.session['detail_num_visits'] = num_visits + 1
        # Build context data
        context = super().get_context_data(**kwargs)
        context['detail_num_visits'] = num_visits
        return context