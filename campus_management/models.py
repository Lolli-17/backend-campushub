from django.db import models
from django.contrib.auth.models import AbstractUser
from backend_def.models import BaseModel
from .choices import RoleChoices, StatusChoices, CleaningTypeChoices, FaultTypeChoices
from .mixin import ChoiceFieldMixin;


class Campus(BaseModel):
    name = models.CharField(max_length=200)
    location = models.TextField()

    class Meta:
        verbose_name_plural = 'campuses'

    def __str__(self):
        return self.name


class CustomUser(AbstractUser, BaseModel):
    role = models.CharField(max_length=30, choices=RoleChoices.choices, default=RoleChoices.GUEST)
    isFirstAccess = models.BooleanField(default=True)
    phoneNumber = models.BigIntegerField(null=True)
    campus = models.OneToOneField(Campus, on_delete=models.DO_NOTHING, null=True)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.username


class Room(BaseModel):
    number = models.IntegerField()
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self):
        return f'Stanza numero {self.number}'


class Space(BaseModel):
    name = models.CharField(max_length=20)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class ElectricityMeter(BaseModel):
    resident = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    room = models.OneToOneField(Room, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    # readingPicture = models.FileField(upload_to='./electricMetersImages/')
    electricityConsumption = models.IntegerField()
    cost = models.FloatField()
    readingDate = models.DateField()


class CommonArea(BaseModel):
    name = models.CharField(max_length=50)
    cost = models.FloatField()


class Guest(BaseModel):
#    resident = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    document = models.CharField(max_length=50)
    documentNumber = models.CharField(max_length=20)
    # badgeNumber = models.CharField(max_length=20)
    # inhouseTime = models.TimeField()
    nights = models.IntegerField()


class Package(BaseModel):
#    resident = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    sender = models.CharField(max_length=50)
    arrivalDate = models.DateField()
    storage = models.CharField(max_length=20)
    notes = models.TextField()


class CommonAreaReservation(BaseModel):
#    resident = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    commonArea = models.ForeignKey(CommonArea, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    reservationDate = models.DateField()
    timeSlot = models.TimeField()
    notes = models.TextField()


class CleaningReservation(BaseModel):
#    resident = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    cleaningType = models.CharField(max_length=50, choices=CleaningTypeChoices.choices)
    cost = models.FloatField()
    requestDate = models.DateField()
    timeSlot = models.TimeField()
    space = models.OneToOneField(CommonArea, on_delete=models.CASCADE, null=True)
    notes = models.TextField()


class FaultReport(BaseModel):
#    resident = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    reportDate = models.DateField()
    space = models.OneToOneField(CommonArea, on_delete=models.CASCADE, null=True)
    faultType = models.CharField(max_length=50, choices=FaultTypeChoices.choices)
    # faultPhoto = models.FileField(upload_to="./faultsImages/")
    notes = models.TextField()


class Notifications(BaseModel):
    pass
