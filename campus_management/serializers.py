from campus_management.choices import GuestStatusChoices
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import (
	Campus, Space, Room, ElectricityMeter, CommonArea, Guest, Package,
	CommonAreaReservation, CleaningReservation, FaultReport, CustomUser,
	GlobalNotifications, UserNotifications, CleaningType,
)
from .choices import CleaningTypeChoices, FaultTypeChoices


class CampusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Campus
		fields = '__all__'  # Include tutti i campi del modello


class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = '__all__'


class SpaceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Space
		fields = '__all__'


class ElectricityMeterSerializer(serializers.ModelSerializer):
	room_number = serializers.CharField(source='room.number', read_only=True)
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	
	class Meta:
		model = ElectricityMeter
		fields = '__all__'


class CommonAreaSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommonArea
		fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
	room_number = serializers.CharField(source='room.number', read_only=True)
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	time_in_house = serializers.SerializerMethodField()

	resident = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
	room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

	def get_time_in_house(self, obj):
		if obj.status == 'in house' and obj.checkInTime:
			timeDifference = timezone.now() - obj.checkInTime
			return str(timeDifference)
		return None

	def validate(self, data):
		room = data.get('room')
		status = data.get('status')
		checkInTime = data.get('checkInTime')

		if room and status == GuestStatusChoices.IN_HOUSE:
			if Guest.objects.filter(room=room, status__in=GuestStatusChoices.IN_HOUSE).exclude(pk=self.instance.pk if self.instance else None).exists():
				raise serializers.ValidationError("Questa stanza è già occupata da un ospite in arrivo o in casa.")
		
		if checkInTime and checkInTime <= timezone.now():
			data['status'] = GuestStatusChoices.IN_HOUSE
		elif status == GuestStatusChoices.IN_HOUSE and not checkInTime:
			data['checkInTime'] = timezone.now()
		return data

	class Meta:
		model = Guest
		fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)

	recipient = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

	class Meta:
		model = Package
		fields = '__all__'


class CommonAreaReservationSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	room_number = serializers.CharField(source='room.number', read_only=True)
	common_area_name = serializers.CharField(source='commonArea.name', read_only=True)

	resident = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
	room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
	commonArea = serializers.PrimaryKeyRelatedField(queryset=CommonArea.objects.all())

	class Meta:
		model = CommonAreaReservation
		fields = '__all__'


class CleaningReservationSerializer(serializers.ModelSerializer):
	room_number = serializers.CharField(source='room.number', read_only=True)
	space_name = serializers.CharField(source='space.name', read_only=True)

	resident = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
	room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
	# cleaningType = serializers.PrimaryKeyRelatedField(queryset=CleaningType.objects.all())
	space = serializers.PrimaryKeyRelatedField(queryset=Space.objects.all())

	class Meta:
		model = CleaningReservation
		fields = '__all__'


class FaultReportSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	room_number = serializers.CharField(source='room.number', read_only=True)
	space_name = serializers.CharField(source='space.name', read_only=True)

	resident = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
	room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
	# faultType = serializers.PrimaryKeyRelatedField(queryset=FaultType.objects.all())
	space = serializers.PrimaryKeyRelatedField(queryset=Space.objects.all())

	class Meta:
		model = FaultReport
		fields = '__all__'
		# Nota: per FileField come faultPhoto, Django REST Framework gestisce automaticamente gli upload.


class CleaningTypeSerializer(serializers.Serializer):
	class Meta:
		model = CleaningType
		fields = '__all__'


class FaultTypeSerializer(serializers.Serializer):
	value = serializers.CharField(source='0')
	label = serializers.CharField(source='1')


class GlobalNotificationsSerializer(serializers.ModelSerializer):
	class Meta:
		model = GlobalNotifications
		fields = '__all__'


class UserNotificationsSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserNotifications
		fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = (
			'id', 'username', 'email', 'role', 'isFirstAccess', 'first_name', 'last_name', 'room',
			'is_staff', 'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions', 'password'
		)
		read_only_fields = ('date_joined', 'last_login',)
		extra_kwargs = {'password': {'write_only': True, 'required': False}}

	def create(self, validated_data):
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