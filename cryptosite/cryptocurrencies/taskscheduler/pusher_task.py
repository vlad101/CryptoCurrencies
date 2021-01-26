from datetime import datetime
from pusher import Pusher
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
    times = []
    currencies = ["BTC"]
    prices = {"BTC": []}

    """
    1. Makes a request to a remote API to retrieve current Bitcoin prices. We make use of the CryptoCompare API and the Requests library.
    2. Generates traces for the graph and bar chart using the Plotly plotly.graph_objs.Scatter and plotly.graph_objs.Bar.
    3. Encode the graph and bar chart data as JSON using the Plotly Json Encoder.
    4. Trigger a data-updated event using the configured pusher object, broadcasting the needed data on the crypto channel.
    """
    def retrieve_data(self):
        # create dictionary for saving current prices
        current_prices = {}
        for currency in self.currencies:
            current_prices[currency] = []
        # append new time to list of times
        self.times.append(time.strftime('%m/%d/%Y %H:%M:%S'))

        # make request to API and get response as object
        #api_url = "https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD".format(",".join(self.currencies))
        # append new price to list of prices for graph
        # and set current price for bar chart
        #for currency in self.currencies:
            #price = response[currency]['USD']
            #current_prices[currency] = price
            #self.prices[currency].append(price)
        
        api_url = "https://api.coinbase.com/v2/prices/spot?currency=USD"
        response = json.loads(requests.get(api_url).content)
        for currency in self.currencies:
            price = None
            try:
                price = response['data']['amount']
            except ValueError:
                print('No price found')
                return
            current_prices[currency] = price
            self.prices[currency].append(price)
        # create an array of traces for graph data
        chart_graph_data = [go.Scatter(
            x=self.times,
            y=self.prices.get(currency),
            name="{} Prices".format(currency)
        ) for currency in self.currencies]
        chart_layout=go.Layout(
            title='Realtime Data',
            xaxis={'title':'Date'}, 
            yaxis={'title':'Price'},
        )
        chart_figure = dict(data=chart_graph_data, layout=chart_layout)

        #figure = go.Figure(data=data,layout=layout)

        # create an array of traces for bar chart data
        bar_chart_data = [go.Bar(
            x=self.currencies,
            y=list(current_prices.values())
        )]

        data = {
            'graph': json.dumps(chart_figure, cls=plotly.utils.PlotlyJSONEncoder),
            #'graph': json.dumps(list(graph_data), cls=plotly.utils.PlotlyJSONEncoder),
            'bar_chart': json.dumps(list(bar_chart_data), cls=plotly.utils.PlotlyJSONEncoder)
        }

        # trigger event
        self.pusher.trigger("crypto", "btc-data-updated", data)