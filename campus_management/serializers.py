from campus_management.choices import GuestStatusChoices
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import (
	Campus, Apartment, CommonArea, Guest, Package,
	CommonAreaReservation, CleaningReservation, FaultReport, CustomUser,
	GlobalNotifications, UserNotifications, ElectricityReading, CleaningType
)
from .choices import CleaningTypeChoices, FaultTypeChoices, RoleChoices, RoomChoices


class CampusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Campus
		fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
	
	def validate(self, data):
		number = data.get('number')
		campus = data.get('campus')
		instance = self.instance
		qs = Apartment.objects.filter(number=number, campus=campus)
		
		if instance:
			qs = qs.exclude(id=instance.id)
		if qs.exists():
			raise serializers.ValidationError(
				"Una stanza con questo numero esiste già in questo campus."
			)
		return data

	class Meta:
		model = Apartment
		fields = '__all__'


class ElectricityReadingSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	apartment_number = serializers.CharField(source='resident.apartment.number', read_only=True)

	def create(self, validated_data):
		resident = validated_data.get('resident')
		new_reading_value = validated_data.get('value')
		reading_space = validated_data.get('reading_space')
		
		if reading_space:
			if reading_space not in [choice[0] for choice in RoomChoices.choices]:
				raise serializers.ValidationError(f"Invalid reading_space choice: {reading_space}")

		if resident and new_reading_value is not None:
			resident.lastElectricityReading = new_reading_value
			resident.save()

		return super().create(validated_data)

	class Meta:
		model = ElectricityReading
		fields = '__all__'


class CommonAreaSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommonArea
		fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)

	class Meta:
		model = Guest
		fields = '__all__'

	def validate(self, data):
		resident = data.get('resident')
		
		if resident.role not in [RoleChoices.STUDENT, RoleChoices.HOTEL]:
			raise serializers.ValidationError({"resident": "Il residente deve avere il ruolo di Student o Hotel per essere associato a un'istanza Guest."})

		if not resident.apartment:
			raise serializers.ValidationError({"resident": "Il residente non ha una stanza associata."})

		return data


class PackageSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	
	class Meta:
		model = Package
		fields = '__all__'


class CommonAreaReservationSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	
	class Meta:
		model = CommonAreaReservation
		fields = '__all__'


class CleaningReservationSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	
	class Meta:
		model = CleaningReservation
		fields = '__all__'


class FaultReportSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	apartment_number = serializers.CharField(source='apartment.number', read_only=True)
	
	class Meta:
		model = FaultReport
		fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
	apartment = serializers.PrimaryKeyRelatedField(queryset=Apartment.objects.all(), allow_null=True, required=False)
	apartment_number = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = CustomUser
		fields = (
			'id', 'username', 'email', 'role', 'isFirstAccess', 
			'first_name', 'last_name', 'apartment', 'apartment_number',
			'lastElectricityReading', 'is_staff', 'phoneNumber', # Correzione: phoneNumber
			'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions', 'password'
		)
		read_only_fields = ('date_joined', 'last_login',)
		extra_kwargs = {'password': {'write_only': True, 'required': False}}

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		groups_data = validated_data.pop('groups', [])
		user_permissions_data = validated_data.pop('user_permissions', [])
		user = CustomUser(**validated_data)
		if password:
			user.password = make_password(password)
		user.save()
		user.groups.set(groups_data)
		user.user_permissions.set(user_permissions_data)
		return user
	
	def get_apartment_number(self, obj):
		return obj.apartment.number if obj.apartment else None
	
	def validate(self, data):
		role = data.get('role')
		apartment = data.get('apartment')

		if role in [RoleChoices.STUDENT, RoleChoices.HOTEL] and not apartment:
			raise serializers.ValidationError("Per il ruolo di studente o hotel, è necessario associare una stanza.")
		if role not in [RoleChoices.STUDENT, RoleChoices.HOTEL] and apartment:
			raise serializers.ValidationError("Solo gli studenti e gli hotel possono essere associati a una stanza.")

		return data

	def update(self, instance, validated_data):
		password = validated_data.pop('password', None)
		groups_data = validated_data.pop('groups', instance.groups.all())
		user_permissions_data = validated_data.pop('user_permissions', instance.user_permissions.all())
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		if password:
			instance.password = make_password(password)
		instance.groups.set(groups_data)
		instance.user_permissions.set(user_permissions_data)
		instance.save()
		return instance


class CXAppUserSerializer(serializers.ModelSerializer):
	apartment_number = serializers.SerializerMethodField(read_only=True)
	
	class Meta:
		model = CustomUser
		fields = ['id', 'username', 'email', 'first_name', 'last_name', 'balance', 'role', 'isFirstAccess', 'phoneNumber', 'apartment', 'apartment_number']
		extra_kwargs = {'apartment': {'write_only': True}}
		read_only_fields = ['lastElectricityReading']

	def get_apartment_number(self, obj):
		return obj.apartment.number if obj.apartment else None