from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

import os
import numpy as np
import pandas as pd
import pickle
import quandl
from datetime import datetime

import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
py.init_notebook_mode(connected=True)

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

def get_quandl_data(quandl_id):
    '''Download and cache Quandl dataseries'''
    cache_path = '{}.pkl'.format(quandl_id).replace('/','-')
    try:
        f = open(cache_path, 'rb')
        df = pickle.load(f)   
        print('Loaded {} from cache'.format(quandl_id))
    except (OSError, IOError) as e:
        print('Downloading {} from Quandl'.format(quandl_id))
        df = quandl.get(quandl_id, returns="pandas")
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(quandl_id, cache_path))
    return df

class GraphView(TemplateView):
    template_name = 'cryptocurrencies/graph.html'

    def get_context_data(self, **kwargs):
        context = super(GraphView, self).get_context_data(**kwargs)
        # Chart the BTC pricing data
        btc_usd_price_kraken = get_quandl_data('BCHARTS/KRAKENUSD')
        btc_trace = go.Scatter(x=btc_usd_price_kraken.index, y=btc_usd_price_kraken['Weighted Price'])
        data=go.Data([btc_trace])
        layout=go.Layout(title="BCHARTS", xaxis={'title':'x1'}, yaxis={'title':'x2'})
        figure=go.Figure(data=data,layout=layout)
        div = py.plot(figure, auto_open=False, output_type='div')
        context['graph'] = div

        return context