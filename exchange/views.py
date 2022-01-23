from decimal import Decimal

from django.db.transaction import atomic
from rest_framework.decorators import action
from rest_framework.response import Response

from exchange.models import Market, Transaction
from exchange.serializers import RegisterSerializer, MarketBuyInputSerializer, TransactionSerializer, \
    MarketSellInputSerializer
from rest_framework import status, viewsets

from shares.models import Share


class MarketList(viewsets.ReadOnlyModelViewSet):
    queryset = Market.objects.all().order_by("share__symbol", "flow", "-rate")
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['post'])
    @atomic
    def buy(self, request):
        serializer = MarketBuyInputSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            symbol = serializer.validated_data["symbol"]
            quantity = serializer.validated_data["quantity"]
            market_values = Market.objects.filter(share__symbol=symbol, flow=Market.Flow.SELL).exclude(
                share__portfolio__user=request.user).order_by("-rate")
            transactions = []
            share, created = Share.objects.get_or_create(symbol=symbol, portfolio__user=request.user, defaults={
                "symbol": symbol,
                "portfolio": request.user.portfolio_set.all()[0],
                "quantity": Decimal("0")
            })
            for _m in market_values:
                if quantity < _m.quantity:
                    _m.quantity -= quantity
                    _m.save()
                    share.quantity += quantity
                    share.save()
                else:
                    share.quantity += _m.quantity
                    share.save()
                    _m.delete()
                transaction = Transaction.objects.create(from_user=_m.share.portfolio.user, to_user=request.user,
                                                         quantity=quantity, rate=_m.rate, market=_m)
                transactions.append(transaction)
                quantity -= _m.quantity
            return Response(TransactionSerializer(transactions, many=True).data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    @atomic
    def sell(self, request):
        serializer = MarketSellInputSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            symbol = serializer.validated_data["symbol"]
            quantity = serializer.validated_data["quantity"]
            market_values = Market.objects.filter(share__symbol=symbol, flow=Market.Flow.BUY).exclude(
                share__portfolio__user=request.user).order_by("-rate")
            transactions = []
            selling_share = Share.objects.get(symbol=symbol, portfolio__user=request.user)
            for _m in market_values:
                buying_share = _m.share
                if quantity < _m.quantity:
                    _m.quantity -= quantity
                    _m.save()
                    buying_share.quantity += quantity
                    buying_share.save()
                    selling_share.quantity -= quantity
                    selling_share.save()
                else:
                    buying_share.quantity += _m.quantity
                    buying_share.save()
                    selling_share.quantity -= _m.quantity
                    selling_share.save()
                    _m.delete()
                transaction = Transaction.objects.create(from_user=request.user, to_user=_m.share.portfolio.user,
                                                         quantity=quantity, rate=_m.rate, market=_m)
                transactions.append(transaction)
                quantity -= _m.quantity
            return Response(TransactionSerializer(transactions, many=True).data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
