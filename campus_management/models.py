from django.db import models
from django.contrib.auth.models import AbstractUser
from backend_def.models import BaseModel
from .choices import RoleChoices, StatusChoices, CleaningTypeChoices, FaultTypeChoices, GuestStatusChoices, RoomChoices
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

	def __str__(self):
		return self.username


class ElectricityReading(BaseModel):
	resident = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
	reading_space = models.CharField(max_length=50, choices=RoomChoices.choices)
	reading_date = models.DateField(default=timezone.now)
	value = models.FloatField(null=False)

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
    guest_name = models.CharField(max_length=255)
	

class Package(BaseModel):
	resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
	sender = models.CharField(max_length=50)
	arrivalDate = models.DateField()
	storage = models.CharField(max_length=20)
	notes = models.TextField(blank=True)


class CommonAreaReservation(BaseModel):
	resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
	commonArea = models.ForeignKey(CommonArea, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
	reservationDate = models.DateField()
	timeSlot = models.TimeField()
	notes = models.TextField(blank=True)


class CleaningReservation(BaseModel):
	resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
	cleaningType = models.CharField(max_length=50, choices=CleaningTypeChoices.choices)
	requestDate = models.DateField()
	timeSlot = models.TimeField()
	space = models.OneToOneField(CommonArea, on_delete=models.CASCADE, null=True)
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
	# background = models.ImageField()
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.title


class UserNotifications(BaseModel):
	resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	title = models.CharField(max_length=100, null=False)
	body = models.TextField(null=True)
	is_read = models.BooleanField(default=False)
	
	def __str__(self):
		return f'Notifica per {self.user.username}: {self.title}'
