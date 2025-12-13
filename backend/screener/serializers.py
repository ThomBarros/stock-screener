from rest_framework import serializers
from .models import Screener

class ScreenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screener
        fields = ('id', 'title', 'description', 'completed')