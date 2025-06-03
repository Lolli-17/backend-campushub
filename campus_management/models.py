from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from backend_def.models import BaseModel

# Create your models here.
class Campus(BaseModel):
	name = models.CharField(max_length=200)
	location = models.TextField()

	class Meta:
		verbose_name_plural = 'campuses'

	def __str__(self):
		return self.name

class Room(BaseModel):
	number = models.IntegerField()
	campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

	def __str__(self):
		return f'Stanza numero {self.number}'

class Worker(BaseModel):
	name = models.CharField(max_length=100)
	role = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Guest(BaseModel):
	name = models.CharField(max_length=100)
	check_in_date = models.DateTimeField(auto_now_add=True)
	room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.name

class CustomUser(AbstractUser, BaseModel):
	ROLE_CHOICES = [
		("worker_admin", "Admin Worker"),
		("worker_maintenance", "Maintenance Worker"),
		("worker_staff", "General Staff"),
		("guest", "Guest"),
	]
	
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="guest")
	
	def __str__(self):
		return self.username
	