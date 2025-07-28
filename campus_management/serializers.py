from rest_framework import serializers
from .models import (
	Campus, Space, Room, ElectricityMeter, CommonArea, Guest, Package,
	CommonAreaReservation, CleaningReservation, FaultReport, CustomUser
)
from django.contrib.auth.hashers import make_password

# Serializzatore per il modello Campus
class CampusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Campus
		fields = '__all__'  # Include tutti i campi del modello


# Serializzatore per il modello Room
class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = '__all__'


# Serializzatore per il modello Space
class SpaceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Space
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
			'is_staff', 'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions', 'password'
		)
		read_only_fields = ('date_joined', 'last_login',)
		extra_kwargs = {'password': {'write_only': True, 'required': False}}

		# user = User.objects.create(
		# 	email=validated_data['email'],
		# 	username=validated_data['username'],
		# 	password = make_password(validated_data['password'])
		# )
		
	def create(self, validated_data):
		# rimane più ordinato per poter mantenere la password sicura
		password = validated_data.pop('password', None)
		if password:
			hashed_password = make_password(password)
		else:
			hashed_password = None

		user = CustomUser(**validated_data)
		if hashed_password:
			user.password = hashed_password
		user.save()
		return user

	def update(self, instance, validated_data):
		password = validated_data.pop('password', None)
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		if password:
			instance.password = make_password(password)
		instance.save()
		return instance



class CXAppUserSerializer(serializers.ModelSerializer):
	class Meta: 
		model = CustomUser
		fields = ['username', 'first_name', 'last_name', 'email', 'isFirstAccess']
