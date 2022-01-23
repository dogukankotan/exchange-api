from decimal import Decimal

from django.core.validators import MinLengthValidator
from rest_framework import serializers

from exchange.models import Market, Transaction
from shares.models import Share


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'
        depth = 2


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class MarketBuyInputSerializer(serializers.Serializer):
    symbol = serializers.CharField(validators=[MinLengthValidator(3)], max_length=3)
    quantity = serializers.DecimalField(max_digits=32, decimal_places=2)

    def validate_symbol(self, value):
        return value.upper()

    def validate(self, data):
        symbol = data["symbol"]
        quantity = data["quantity"]
        user = self.context["user"]
        market_values = Market.objects.filter(share__symbol=symbol, flow=Market.Flow.SELL).exclude(share__portfolio__user=user)
        market_quantities = Decimal("0")
        for _m in market_values:
            market_quantities += _m.quantity
        if quantity > market_quantities:
            raise serializers.ValidationError(
                f"{symbol} does not have sufficient shares. Total market quantity is {market_quantities}")

        return data

class MarketSellInputSerializer(MarketBuyInputSerializer):

    def validate(self, data):
        symbol = data["symbol"]
        quantity = data["quantity"]
        user = self.context["user"]
        try:
            share = Share.objects.get(symbol=symbol, portfolio__user=user)
            if quantity > share.quantity:
                raise serializers.ValidationError(
                    f"{quantity} is too much. You can sell {share.quantity} quantity.")
        except Share.DoesNotExist:
            raise serializers.ValidationError(
                f"{symbol} does not exist in your portfolio.")

        market_values = Market.objects.filter(share__symbol=symbol, flow=Market.Flow.BUY).exclude(share__portfolio__user=user)
        market_quantities = Decimal("0")
        for _m in market_values:
            market_quantities += _m.quantity
        if quantity > market_quantities:
            raise serializers.ValidationError(
                f"{symbol} does not have sufficient shares. Total market quantity is {market_quantities}.")

        return data
