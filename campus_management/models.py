from django.db import models
from django.contrib.auth.models import AbstractUser
from backend_def.models import BaseModel
from .choices import (RoleChoices, StatusChoices, CleaningReservationStatusChoices,
					  FaultTypeChoices, GuestStatusChoices, RoomChoices,
					  PackageStatusChoices, SpaceReservationStatusChoices,
)
from .mixin import ChoiceFieldMixin;
from django.utils import timezone

class Campus(BaseModel):
	name = models.CharField(max_length=200)
	location = models.TextField()

	class Meta:
		verbose_name_plural = 'campuses'

	def __str__(self):
		return self.name


class Apartment(BaseModel):
	number = models.IntegerField()
	campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

	def __str__(self):
		return f'Stanza numero {self.number}'


class CustomUser(AbstractUser, BaseModel):
	role = models.CharField(max_length=30, choices=RoleChoices.choices, default=RoleChoices.GUEST)
	isFirstAccess = models.BooleanField(default=True)
	phoneNumber = models.BigIntegerField(null=True)
	campus = models.OneToOneField(Campus, on_delete=models.DO_NOTHING, null=True)
	balance = models.FloatField(default=0.0)
	apartment = models.ForeignKey(Apartment, on_delete=models.DO_NOTHING, null=True)
	phoneNumber = models.CharField(max_length=20, null=True)
	lastElectricityReading = models.FloatField(null=True, default=0, blank=True)

	def __str__(self):
		return self.username


class ElectricityReading(BaseModel):
	resident = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
	reading_space = models.CharField(max_length=50, choices=RoomChoices.choices)
	reading_date = models.DateField(default=timezone.now)
	value = models.FloatField(null=False)
	cost= models.FloatField(null=True, blank=True)

	def __str__(self):
		return f'Lettura del {self.reading_date} per {self.meter.room.number}'
	

class CommonArea(BaseModel):
	name = models.CharField(max_length=50)
	cost = models.FloatField()

	def __str__(self):
		return self.name


class Guest(BaseModel):
	resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE, null=True)
	checkInTime = models.DateTimeField(null=True, blank=True)
	nights = models.IntegerField(default=0)
	status = models.CharField(max_length=20, choices=GuestStatusChoices.choices, default=GuestStatusChoices.IN_ARRIVO)
	notes = models.TextField(null=True)
	document = models.CharField(max_length=50)
	documentNumber = models.CharField(max_length=20)
	guest_name = models.CharField(max_length=255)
	

class Package(BaseModel):
	resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=PackageStatusChoices.choices, default=PackageStatusChoices.IN_CONSEGNA)
	sender = models.CharField(max_length=50)
	arrivalDate = models.DateField()
	storage = models.CharField(max_length=20)
	notes = models.TextField(blank=True)


class CommonAreaReservation(BaseModel):
	resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
	commonArea = models.ForeignKey(CommonArea, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=SpaceReservationStatusChoices.choices, default=SpaceReservationStatusChoices.FUTURE)
	reservationDate = models.DateField()
	timeSlot = models.TimeField()
	notes = models.TextField(blank=True)


class CleaningReservation(BaseModel):
	resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=CleaningReservationStatusChoices.choices, default=CleaningReservationStatusChoices.TUTTI)
	cleaningType = models.CharField(max_length=50, null=False)
	requestDate = models.DateField()
	timeSlot = models.CharField(max_length=20, null=False, default="9:00 - 10:00")
	space = models.CharField(max_length=20, null=False)
	notes = models.TextField(blank=True)


class FaultReport(BaseModel):
	resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
	reportDate = models.DateField()
	space = models.ForeignKey(CommonArea, on_delete=models.CASCADE, null=True)
	faultType = models.CharField(max_length=50, choices=FaultTypeChoices.choices)
	# faultPhoto = models.FileField(upload_to="./faultsImages/")
	notes = models.TextField(blank=True)


class GlobalNotifications(BaseModel):
	campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
	title = models.CharField(max_length=100, null=False)
	body = models.TextField(null=True)
	sendingTime = models.DateTimeField(default=timezone.now(), null=False)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.title


class UserNotifications(BaseModel):
	resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	title = models.CharField(max_length=100, null=False)
	body = models.TextField(null=True)
	sendingTime = models.DateTimeField(default=timezone.now(), null=False)
	is_read = models.BooleanField(default=False)
	
	def __str__(self):
		return f'Notifica per {self.user.username}: {self.title}'
