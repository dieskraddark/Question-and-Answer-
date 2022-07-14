from dataclasses import field
from xml.parsers.expat import model
from rest_framework.serializers import ModelSerializer
from base.models import Room



class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields ='__all__'