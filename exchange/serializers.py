from rest_framework import serializers

from exchange.models import Market


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Market
        fields = '__all__'
        depth = 2