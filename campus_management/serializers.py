from rest_framework import serializers
from .models import Guest, CustomUser
from django.contrib.auth.hashers import make_password


class GuestSerializer(serializers.ModelSerializer):
	room_number = serializers.CharField(source="room.number", read_only=True)  
	
	class Meta:
		model = Guest
		exclude = ['room']
		extra_fields = ['room_number']
	
	def to_representation(self, instance):
		data = super().to_representation(instance)
		data["room_number"] = instance.room.number
		return data
	

class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = '__all__'
		
	def create(self, validated_data):
		validated_data['password'] = make_password(validated_data['password'])
		return super().create(validated_data)
	
class CXAppUserSerializer(serializers.ModelSerializer):
	class Meta: 
		model = CustomUser
		fields = ['username', 'first_name', 'last_name', 'email', 'isFirstAccess']