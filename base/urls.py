from django.urls import path, include

from django.http.response import JsonResponse
from rest_framework.views import APIView


class BaseUrls(APIView):

    def get(self, request):
        return JsonResponse({'message': 'API is ready!'})



urlpatterns = [
    path('', BaseUrls.as_view()),
    path('exchange/',  include("exchange.urls")),
    path('shares/',  include("shares.urls")),
    path('clients/',  include("clients.urls")),
]
