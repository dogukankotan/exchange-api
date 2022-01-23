from django.urls import path, include
from rest_framework import routers

from exchange.views import MarketList

router = routers.DefaultRouter()
router.register("market", MarketList)

urlpatterns = [
    path('', include(router.urls)),
]