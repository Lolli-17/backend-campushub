from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from backend_def.models import BaseModel


class Campus(BaseModel):
	name = models.CharField(max_length=200)
	location = models.TextField()

	class Meta:
		verbose_name_plural = 'campuses'

	def __str__(self):
		return self.name


class Housing(BaseModel):
	number = models.IntegerField()
	campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

	def __str__(self):
		return f'Stanza numero {self.number}'
	

class Room(BaseModel):
	name = models.CharField(max_length=20, null=False, default=None)
	housing = models.ForeignKey(Housing, on_delete=models.CASCADE, default=None)


class ElectricityMeter(BaseModel): # ha senso avere sia contatore che lettura?
	#? resident = models.OneToOneField(on_delete=models.CASCADE)
	room = models.OneToOneField(Room, on_delete=models.CASCADE, default=None) # serve? la posso ottenere dal resident
	status = models.CharField(max_length=50, null=False, default=None) # è meglio mettere textChoice, choices?
	#! readingPicture = models.FileField(upload_to='./electricMetersImages/') # ovviamente andrà rimessa
	electricityConsumption = models.IntegerField(max_length=10, null=False)
	cost = models.IntegerField(max_length=10, null=False)
	readingDate = models.DateField(max_length=50, null=False)


class CommonArea(BaseModel):
	name = models.CharField(max_length=50, null=False)
	cost = models.IntegerField(max_length=5, null=False)


class Guest(BaseModel):
	#? resident = models.OneToOneField(on_delete=models.CASCADE)
	room = models.OneToOneField(Room, on_delete=models.CASCADE, default=None) # serve? la posso ottenere dal resident
	name = models.CharField(max_length=100, null=False)
	status = models.CharField(max_length=20, null=False, default=None) # è meglio mettere textChoice, choices?
	document = models.CharField(max_length=50, null=False, default=None)
	documentNumber = models.CharField(max_length=20, null=False, default=None)
	#! badgeNumber = models.CharField(max_length=20, null=False) # è il numero di badge dell'utente?
	#! inhouseTime = models.TimeField # a cosa si riferisce?
	nights = models.IntegerField(max_length=1, null=False, default=None)


class Package(BaseModel):
	#? resident = models.OneToOneField(on_delete=models.CASCADE)
	room = models.OneToOneField(Room, on_delete=models.CASCADE, default=None) # serve? la posso ottenere dal resident
	status = models.CharField(max_length=20, null=False, default=None) # è meglio mettere textChoice, choices?
	sender = models.CharField(max_length=50, null=False)
	arrivalDate = models.DateField(max_length=50, null=False)
	storage = models.CharField(max_length=20)
	notes = models.TextField()
	

class CommonAreaReservation(BaseModel): # basta reservation?
	#? resident = models.OneToOneField(on_delete=models.CASCADE)
	room = models.OneToOneField(Room, on_delete=models.CASCADE, default=None) # serve? la posso ottenere dal resident
	commonArea = models.ForeignKey(CommonArea, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, null=False, default=None) # è meglio mettere textChoice, choices?
	reservationDate = models.DateField(max_length=50, null=False)
	timeSlot = models.TimeField(max_length=50, null=False)
	notes = models.TextField()


class CleaningReservation(BaseModel):
	#? resident = models.OneToOneField(on_delete=models.CASCADE)
	room = models.OneToOneField(Room, on_delete=models.CASCADE, default=None) # serve? la posso ottenere dal resident
	status = models.CharField(max_length=20, null=False, default=None) # è meglio mettere textChoice, choices?
	cleaningType = models.CharField(max_length=50, null=False) # è meglio fare una tabella per salvarle?
	cost = models.IntegerField(max_length=10, null=False)
	requestDate = models.DateField(max_length=50, null=False)
	timeSlot = models.TimeField(max_length=50, null=False)
	space = models.OneToOneField(CommonArea, on_delete=models.CASCADE, null=True) # se null allora in camera
	notes = models.TextField()


class FaultReport(BaseModel):
	#? resident = models.OneToOneField(on_delete=models.CASCADE)
	room = models.OneToOneField(Room, on_delete=models.CASCADE, default=None) # serve? la posso ottenere dal resident
	status = models.CharField(max_length=20, null=False, default=None) # è meglio mettere textChoice, choices?
	reportDate = models.DateField(max_length=50, null=False)
	space = models.OneToOneField(CommonArea, on_delete=models.CASCADE, null=True) # se null allora in camera
	faultType = models.CharField(max_length=50, null=False) # è meglio fare una tabella per salvarle?
	#! faultPhoto = models.FileField(upload_to="./faultsImages/")
	notes = models.TextField()


# class Worker(BaseModel):
# 	name = models.CharField(max_length=100)
# 	role = models.CharField(max_length=50)

# 	def __str__(self):
# 		return self.name
	

class CustomUser(AbstractUser, BaseModel):
	ROLE_CHOICES = [
		("resident_manager", "Resident Manager"),
		("front_office_manager", "Front Office Manager"),
		("front_office", "Front Office"),
		("community_ambassador", "Community Ambassador"),
		("marketing", "Marketing"),
		("user", "User"),
		("resident", "Resident"),
	]
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="guest")
	isFirstAccess = models.BooleanField(default=True)
	# phoneNumber = models.IntegerField(max_length=20, null=False)
	# campus = models.OneToOneField(Campus, on_delete=models.DO_NOTHING, null=False)
	# balance = models.FloatField(max_length=10)
	
	def __str__(self):
		return self.username
	