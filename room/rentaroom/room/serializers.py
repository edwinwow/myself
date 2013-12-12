from django.forms import widgets
from rest_framework import serializers
from .models import RoomForRent, 

class RoomForRentSerializer(serializers.ModelSerializer):
  room_for_rent = serializers.PrimaryKeyRelatedField(many=True)
  
  class Meta:
    model = RoomForRent
    fields = ('room_status', 'start_date', 'price', 'rating', 'comments')
    
    
    

