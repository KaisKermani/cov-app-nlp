from rest_framework import serializers
from .models import Test, Raw, Structured


class RawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raw
        fields = "__all__"


class StructuredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structured
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    id = RawSerializer()

    class Meta:
        model = Structured
        fields = "__all__"
