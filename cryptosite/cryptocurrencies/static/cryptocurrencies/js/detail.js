// get coin name
const coinName = document.getElementById("coin-name");
if(coinName != null) {
    const name = coinName.innerHTML.toLowerCase();
    // get coin name
    // connect to Pusher
    const pusher = new Pusher(
        '42bce06a2833593e1d7a', {
            cluster: 'us2',
            encrypted: true
    });
    // subscribe to crypto channel
    const channel = pusher.subscribe('crypto-' + name);
    // listen for relevant events
    channel.bind('data-updated-' + name, data => {
      const graph = JSON.parse(data.graph);
      Plotly.newPlot('price_chart', graph);
      const bar_chart = JSON.parse(data.bar_chart);
      Plotly.newPlot('market_cap_chart', bar_chart);
    });
}