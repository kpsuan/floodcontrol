from rest_framework import serializers
from .models import FloodControl

class FloodControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloodControl
        fields = '__all__'