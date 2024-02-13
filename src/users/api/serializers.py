from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, Serializer
from rest_framework import serializers
from ..models import User









class ResetPasswordSerializer(Serializer):
    email = serializers.EmailField()