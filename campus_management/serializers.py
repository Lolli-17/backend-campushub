from rest_framework import serializers
from .models import (
	Campus, Housing, Room, ElectricityMeter, CommonArea, Guest, Package,
	CommonAreaReservation, CleaningReservation, FaultReport, CustomUser
)
from django.contrib.auth.hashers import make_password


# Serializzatore per il modello Campus
class CampusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Campus
		fields = '__all__'  # Include tutti i campi del modello


# Serializzatore per il modello Housing
class HousingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Housing
		fields = '__all__'


# Serializzatore per il modello Room
class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = '__all__'


# Serializzatore per il modello ElectricityMeter
class ElectricityMeterSerializer(serializers.ModelSerializer):
	class Meta:
		model = ElectricityMeter
		fields = '__all__'
		# Nota: per FileField come readingPicture, Django REST Framework gestisce automaticamente gli upload.
		# È possibile aggiungere validazioni personalizzate se necessario.


# Serializzatore per il modello CommonArea
class CommonAreaSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommonArea
		fields = '__all__'


# Serializzatore per il modello Guest
class GuestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Guest
		fields = '__all__'


# Serializzatore per il modello Package
class PackageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Package
		fields = '__all__'


# Serializzatore per il modello CommonAreaReservation
class CommonAreaReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommonAreaReservation
		fields = '__all__'


# Serializzatore per il modello CleaningReservation
class CleaningReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model = CleaningReservation
		fields = '__all__'


# Serializzatore per il modello FaultReport
class FaultReportSerializer(serializers.ModelSerializer):
	class Meta:
		model = FaultReport
		fields = '__all__'
		# Nota: per FileField come faultPhoto, Django REST Framework gestisce automaticamente gli upload.


# Serializzatore per il modello Worker
# class WorkerSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Worker
# 		fields = '__all__'


# Serializzatore per il modello CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = (
			'id', 'username', 'email', 'role', 'isFirstAccess', 'first_name', 'last_name',
			'is_staff', 'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions'
		)
		# Campi extra da non includere in scrittura, o che sono di sola lettura
		read_only_fields = ('date_joined', 'last_login',)
		# Per la password, non vogliamo esporla direttamente e potremmo voler gestirla separatamente per l'aggiornamento
		extra_kwargs = {'password': {'write_only': True, 'required': False}}

	def create(self, validated_data):
		# Sovrascrive il metodo create per gestire correttamente la password
		user = CustomUser.objects.create_user(**validated_data)
		return user

	def update(self, instance, validated_data):
		# Sovrascrive il metodo update per gestire correttamente la password
		if 'password' in validated_data:
			password = validated_data.pop('password')
			instance.set_password(password)
		return super().update(instance, validated_data)


class CXAppUserSerializer(serializers.ModelSerializer):
	class Meta: 
		model = CustomUser
		fields = ['username', 'first_name', 'last_name', 'email', 'isFirstAccess']
