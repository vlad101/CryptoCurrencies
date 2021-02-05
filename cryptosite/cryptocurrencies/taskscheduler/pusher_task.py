from datetime import datetime
from pusher import Pusher
from pycoingecko import CoinGeckoAPI

import requests, json, time, plotly, plotly.graph_objs as go
import os

from ..models import Coin, CoinData


class PusherUtil:
    # configure pusher object
    pusher = Pusher(
        app_id=os.environ['PUSHER_APP_ID'],
        key=os.environ['PUSHER_APP_KEY'],
        secret=os.environ['PUSHER_APP_SECRET'],
        cluster=os.environ['PUSHER_APP_CLUSTER'],
        ssl=bool(os.environ['PUSHER_APP_SSL'])
    )

    # define variables for data retrieval
    cg = CoinGeckoAPI()
    times = []
    prices = {}
    coins = []
    for coin in Coin.objects.only('name'):
        coin_name = coin.name.lower().replace(' ', '-')
        coins.append(coin_name)
        prices[coin_name] = []
    """
    1. Makes a request to a remote API to retrieve current Bitcoin prices. We make use of the Crypto API and the Requests library.
    2. Generates traces for the graph and bar chart using the Plotly plotly.graph_objs.Scatter and plotly.graph_objs.Bar.
    3. Encode the graph and bar chart data as JSON using the Plotly Json Encoder.
    4. Trigger a data-updated event using the configured pusher object, broadcasting the needed data on the crypto channel.
    """
    def retrieve_data(self):
        # create dictionary for saving current prices
        current_prices = {}
        # append new time to list of times
        #self.times.append(time.strftime('%Y-%m-%d %I:%M:%S %p'))
        self.times.append(time.strftime('%I:%M:%S %p'))
        if len(self.times) == 10:
            self.times.pop(0)

        # historical data
        # https://api.coingecko.com/api/v3/coins/litecoin/market_chart/range?vs_currency=usd&from=0&to=1609582200
        # get data
        errors = []
        api_data = self.cg.get_price(ids=self.coins, vs_currencies='usd')
        for coin in self.coins:
            price = None
            current_prices[coin] = []
            try:
                price = api_data[coin]['usd']
                print(coin + ' - ' + str(price))
            except ValueError as e:
                errors.append(e)
            except KeyError as e:
                errors.append(e)

            if not errors:
                current_prices[coin] = price
                self.prices[coin].append(price)
                if len(self.prices[coin]) == 10:
                    self.prices[coin].pop(0)

        # create an array of traces for graph data
        for coin in self.coins:

            chart_graph_data = [go.Scatter(
                x=self.times,
                y=self.prices.get(coin),
                name="{} Prices".format(coin)
            )]

            chart_layout=go.Layout(
                title='Realtime Data',
                xaxis={'title':'Date'}, 
                yaxis={'title':'Price'},
            )
            chart_figure = dict(data=chart_graph_data, layout=chart_layout)

            # create an array of traces for bar chart data
            bar_chart_data = [go.Bar(
                x=[coin],
                y=[current_prices[coin]]
            )]

            data = {
                'graph': json.dumps(chart_figure, cls=plotly.utils.PlotlyJSONEncoder),
                'bar_chart': json.dumps(list(bar_chart_data), cls=plotly.utils.PlotlyJSONEncoder)
            }
            # trigger event
            self.pusher.trigger("crypto-" + coin, "data-updated-" + coin, data)