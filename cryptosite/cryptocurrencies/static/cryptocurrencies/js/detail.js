// connect to Pusher
const pusher = new Pusher(
    '42bce06a2833593e1d7a', {
        cluster: 'us2',
        encrypted: true
});
// subscribe to crypto channel
const channel = pusher.subscribe('crypto')
// listen for relevant events
channel.bind('btc-data-updated', data => {
  const graph = JSON.parse(data.graph);
  Plotly.newPlot('btc_price_chart', graph);
  const bar_chart = JSON.parse(data.bar_chart);
  Plotly.newPlot('btc_market_cap_chart', bar_chart);
});