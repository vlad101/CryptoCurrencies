from rest_framework import serializers

from ..models import Coin, CoinData

class CoinSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Coin
        fields = __all__


class CoinDataSerializer(serializers.ModelSerializer):
    coin = CoinSerializer(required=True)
    class Meta:
        model = CoinData
        fields = __all__

    def create(self, validated_data):
        coin = CoinSerializer.create(CoinSerializer(), validated_data)
        coindata = CoinData.objects.create(coin=coin)
        return coindata