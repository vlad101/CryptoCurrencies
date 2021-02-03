import os

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from pusher import Pusher
import plotly.graph_objs as go

import numpy as np
import pandas as pd
import pickle
import quandl
import plotly.offline as py
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
        #context = super().get_context_data(**kwargs)
        context = super(DetailView, self).get_context_data(**kwargs)
        context['detail_num_visits'] = num_visits
        # Get coin data
        coins = Coin.objects.filter(pk=self.kwargs.get('pk'))[:1]

        # Download and cache Quandl dataseries
        graph_data = {}
        graph_data['data_type'] = 'Weighted Price'
        graph_data['title_x_axis'] = 'Time' 
        graph_data['title_y_axis'] = 'Price'
        graph_data['title'] = 'Data Chart'

        kraken_data_str = None
        coin_abbreviation = 'BTC'.lower()
        if coin_abbreviation == 'BTC'.lower():
            kraken_data_str = 'BCHARTS/KRAKENUSD'
        
            #Ethereum
        if kraken_data_str:
            graphUtil = GraphUtil(graph_data)
            usd_price_kraken = graphUtil.get_quandl_data(kraken_data_str)
            # Chart the pricing data
            context['graph'] = graphUtil.get_plot_div(usd_price_kraken)
        return context


class GraphUtil:
    graph_data = {}

    def __init__(self, graph_obj):
        self.graph_data = graph_obj

    def get_quandl_data(self, quandl_id):
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

    def get_plot_div(self, usd_price_kraken):
        data_trace = go.Scatter(x=usd_price_kraken.index, y=usd_price_kraken[self.graph_data['data_type']])
        data = [data_trace]
        layout=go.Layout(
            title=self.graph_data['title'],
            xaxis={'title':self.graph_data['title_x_axis']}, 
            yaxis={'title':self.graph_data['title_y_axis']},
        )
        figure = go.Figure(data=data,layout=layout)
        return py.plot(figure, auto_open=False, output_type='div')