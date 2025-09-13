from campus_management.choices import GuestStatusChoices
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import (
	Campus, Apartment, CommonArea, Guest, Package,
	CommonAreaReservation, CleaningReservation, FaultReport, CustomUser,
	GlobalNotifications, UserNotifications, ElectricityReading,
)
from .choices import CleaningTypeChoices, FaultTypeChoices, RoleChoices, RoomChoices


class CampusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Campus
		fields = '__all__'  # Include tutti i campi del modello


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

	def validate(self, data):
		meter = data.get('meter')
		reading_space = data.get('reading_space')

		if meter and reading_space:
			# Controlla se il valore di reading_space è una scelta valida
			valid_spaces = [choice[0] for choice in RoomChoices.choices]
			if reading_space not in valid_spaces:
				raise serializers.ValidationError(
					{"reading_space": f"Lo spazio '{reading_space}' non è una scelta valida. Le opzioni sono: {valid_spaces}"}
				)
		return data
	
	class Meta:
		model = ElectricityReading
		fields = '__all__'
		read_only_fields = ['reading_date']
	

class CommonAreaSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommonArea
		fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
	apartment_number = serializers.CharField(source='apartment.number', read_only=True)
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	time_in_house = serializers.SerializerMethodField()

	resident = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

	def create(self, validated_data):
		resident = validated_data.get('resident')
		
		if resident.role not in [RoleChoices.RESIDENT, RoleChoices.GUEST]:
			raise serializers.ValidationError(
				{"resident": "Il residente deve essere un residente o un guest per avere una stanza associata."}
			)
		if not resident.apartment:
			raise serializers.ValidationError(
				{"resident": "Il residente non ha una stanza associata."}
			)
		
		validated_data['apartment'] = resident.apartment
		return super().create(validated_data)

	def get_time_in_house(self, obj):
		if obj.status == GuestStatusChoices.IN_HOUSE and obj.checkInTime:
			timeDifference = timezone.now() - obj.checkInTime
			hours = timeDifference.total_seconds() // 3600
			minutes = (timeDifference.total_seconds() // 3600) // 60
			return f'{int(hours)}h {int(minutes)}m'
		return None

	def validate(self, data):
			apartment = data.get('apartment')
			checkInTime = data.get('checkInTime')

			if checkInTime:
				if checkInTime <= timezone.now():
					data['status'] = GuestStatusChoices.IN_HOUSE
				else:
					data['status'] = GuestStatusChoices.IN_ARRIVO
			elif 'status' in data and data['status'] == GuestStatusChoices.IN_HOUSE and not checkInTime:
				data['checkInTime'] = timezone.now()

			if apartment and data.get('status') == GuestStatusChoices.IN_HOUSE:
				if Guest.objects.filter(apartment=apartment, status=GuestStatusChoices.IN_HOUSE).exclude(pk=self.instance.pk if self.instance else None).exists():
					raise serializers.ValidationError("Questa stanza è già occupata da un ospite in arrivo o in casa.")
			
			return data
	
	def update(self, instance, validated_data):
		if 'resident' in validated_data:
			resident = validated_data['resident']
			if resident.role not in [RoleChoices.RESIDENT, RoleChoices.GUEST]:
				raise serializers.ValidationError(
					{"resident": "Il residente deve essere un residente o un guest per avere una stanza associata."}
				)
			if not resident.aparment:
				raise serializers.ValidationError(
					{"resident": "Il residente non ha una stanza associata."}
				)
			instance.aparment = resident.aparment

		return super().update(instance, validated_data)

	class Meta:
		model = Guest
		fields = '__all__'
		read_only_fields = ['apartment', 'nights']


class PackageSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	apartment_number = serializers.CharField(source='apartment.number', read_only=True)
	recipient = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

	class Meta:
		model = Package
		fields = '__all__'
		read_only_fields = ['apartment']


class CommonAreaReservationSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	apartment_number = serializers.CharField(source='apartment.number', read_only=True)
	common_area_name = serializers.CharField(source='commonArea.name', read_only=True)

	resident = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
	apartment = serializers.PrimaryKeyRelatedField(queryset=Apartment.objects.all())
	commonArea = serializers.PrimaryKeyRelatedField(queryset=CommonArea.objects.all())

	class Meta:
		model = CommonAreaReservation
		fields = '__all__'
		read_only_fields = ['apartment']


class CleaningReservationSerializer(serializers.ModelSerializer):
	apartment_number = serializers.CharField(source='apartment.number', read_only=True)

	resident = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
	apartment = serializers.PrimaryKeyRelatedField(queryset=Apartment.objects.all())

	class Meta:
		model = CleaningReservation
		fields = '__all__'
		read_only_fields = ['apartment']


class FaultReportSerializer(serializers.ModelSerializer):
	resident_name = serializers.CharField(source='resident.get_full_name', read_only=True)
	apartment_number = serializers.CharField(source='apartment.number', read_only=True)
	
	resident = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
	apartment = serializers.PrimaryKeyRelatedField(queryset=Apartment.objects.all())

	class Meta:
		model = FaultReport
		fields = '__all__'
		read_only_fields = ['apartment']
		

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
	apartment = serializers.PrimaryKeyRelatedField(queryset=Apartment.objects.all(), allow_null=True, required=False)
	apartment_number = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = CustomUser
		fields = (
			'id', 'username', 'email', 'role', 'isFirstAccess', 'first_name', 'last_name', 'apartment', 'apartment_number',
			'is_staff', 'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions', 'password'
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

		if role in [RoleChoices.RESIDENT, RoleChoices.GUEST] and not apartment:
			raise serializers.ValidationError("Per il ruolo di residente o guest, è necessario associare una stanza.")
		if role not in [RoleChoices.RESIDENT, RoleChoices.GUEST] and apartment:
			raise serializers.ValidationError("Solo i residenti e i guest possono essere associati a una stanza.")

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

	def get_apartment_number(self, obj):
		return obj.apartment.number if obj.apartment else None