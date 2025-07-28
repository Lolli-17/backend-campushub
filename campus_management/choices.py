from django.db import models
from django.db.models import TextChoices


class RoleChoices(TextChoices):
    RESIDENT_MANAGER = "resident_manager", "Resident Manager"
    FRONT_OFFICE_MANAGER = "front_office_manager", "Front Office Manager"
    FRONT_OFFICE = "front_office", "Front Office"
    COMMUNITY_AMBASSADOR = "community_ambassador", "Community Ambassador"
    MARKETING = "marketing", "Marketing"
    GUEST = "guest", "Guest"
    RESIDENT = "resident", "Resident"


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
