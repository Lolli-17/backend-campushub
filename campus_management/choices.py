from django.db import models
from django.db.models import TextChoices


class RoleChoices(TextChoices):
	RESIDENT_MANAGER = "Resident Manager", "Resident Manager"
	FRONT_OFFICE_MANAGER = "Front Office Manager", "Front Office Manager"
	FRONT_OFFICE = "Front Office", "Front Office"
	COMMUNITY_AMBASSADOR = "Community Ambassador", "Community Ambassador"
	MARKETING = "Marketing", "Marketing"
	GUEST = "Guest", "Guest"
	RESIDENT = "Resident", "Resident"


class StatusChoices(TextChoices):
	PENDING = "pending", "Pending"
	APPROVED = "approved", "Approved"
	REJECTED = "rejected", "Rejected"
	DELIVERED = "delivered", "Delivered"
	RECEIVED = "received", "Received"


class CleaningTypeChoices(TextChoices):
	STANDARD = "standard", "Standard"
	DEEP = "deep", "Deep"
	EXPRESS = "express", "Express"


class FaultTypeChoices(TextChoices):
	ELECTRICAL = "electrical", "Electrical"
	PLUMBING = "plumbing", "Plumbing"
	INTERNET = "internet", "Internet"
	OTHER = "other", "Other"

class GuestStatusChoices(TextChoices):
	IN_ARRIVO = "In Arrivo", "In Arrivo"
	IN_HOUSE = "In House", "In House"
	OFF_HOUSE = "Off House", "Off House"
