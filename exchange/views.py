from rest_framework.decorators import action
from rest_framework.response import Response

from exchange.models import Market
from exchange.serializers import RegisterSerializer
from rest_framework import status, viewsets


class MarketList(viewsets.ReadOnlyModelViewSet):
    queryset = Market.objects.all()
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['post'])
    def buy(self, request):
        return Response("buy",
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def sell(self, request):
        return Response("sell",
                        status=status.HTTP_400_BAD_REQUEST)
