from rest_framework import generics
from rest_framework.permissions import AllowAny, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import Group
from .models import (
	Campus, Apartment, CommonArea, Guest, Package,
	CommonAreaReservation, CleaningReservation, FaultReport, CustomUser,
	GlobalNotifications, UserNotifications, ElectricityReading,
)
from .serializers import (
	CampusSerializer, ApartmentSerializer,
	CommonAreaSerializer, GuestSerializer, PackageSerializer, ElectricityReadingSerializer,
	CommonAreaReservationSerializer, CleaningReservationSerializer, 
	FaultReportSerializer, CustomUserSerializer, CXAppUserSerializer,
	GlobalNotificationsSerializer, UserNotificationsSerializer,
)
from .choices import GuestStatusChoices


class RegisterUser(generics.CreateAPIView):
	serializer_class = CustomUserSerializer
	permission_classes = [DjangoModelPermissions]


class GetCurrentUser(generics.GenericAPIView):
	serializer_class = CustomUserSerializer
	permission_classes = [DjangoModelPermissions]
	
	def get(self, request, *args, **kwargs):
		user = self.serializer_class(request.user)
		return Response(user.data)


class CampusViewSet(viewsets.ModelViewSet):
	queryset = Campus.objects.all()
	serializer_class = CampusSerializer
	permission_classes = [DjangoModelPermissions]


class ApartmentViewSet(viewsets.ModelViewSet):
	queryset = Apartment.objects.all()
	serializer_class = ApartmentSerializer
	permission_classes = [DjangoModelPermissions]


class ElectricityReadingViewSet(viewsets.ModelViewSet):
	queryset = ElectricityReading.objects.all()
	serializer_class = ElectricityReadingSerializer
	permission_classes = [DjangoModelPermissions]


class CommonAreaViewSet(viewsets.ModelViewSet):
	queryset = CommonArea.objects.all()
	serializer_class = CommonAreaSerializer
	permission_classes = [DjangoModelPermissions]


class GuestViewSet(viewsets.ModelViewSet):
	queryset = Guest.objects.all()
	serializer_class = GuestSerializer

	def list(self, request, *args, **kwargs):
		guests_to_update = []
		now = timezone.now()
		
		for guest in self.get_queryset():
			if guest.status == GuestStatusChoices.IN_ARRIVO and guest.checkInTime and guest.checkInTime <= now:
				guest.status = GuestStatusChoices.IN_HOUSE
				guests_to_update.append(guest)

			if guest.status == GuestStatusChoices.IN_HOUSE and guest.checkInTime:
				days_since_checkin = (now.date() - guest.checkInTime.date()).days				
				if days_since_checkin > guest.nights:
					guest.nights = days_since_checkin
					guests_to_update.append(guest)
					
		if guests_to_update:
			Guest.objects.bulk_update(guests_to_update, ['status', 'nights'])

		return super().list(request, *args, **kwargs)


class PackageViewSet(viewsets.ModelViewSet):
	queryset = Package.objects.all()
	serializer_class = PackageSerializer
	permission_classes = [DjangoModelPermissions]


class CommonAreaReservationViewSet(viewsets.ModelViewSet):
	queryset = CommonAreaReservation.objects.all()
	serializer_class = CommonAreaReservationSerializer
	permission_classes = [DjangoModelPermissions]


class CleaningReservationViewSet(viewsets.ModelViewSet):
	queryset = CleaningReservation.objects.all()
	serializer_class = CleaningReservationSerializer
	permission_classes = [DjangoModelPermissions]


class FaultReportViewSet(viewsets.ModelViewSet):
	queryset = FaultReport.objects.all()
	serializer_class = FaultReportSerializer
	permission_classes = [DjangoModelPermissions]


class GlobalNotificationsViewSet(viewsets.ModelViewSet):
	queryset = GlobalNotifications.objects.all()
	serializer_class = GlobalNotificationsSerializer
	permission_classes = [DjangoModelPermissions]


class UserNotificationsViewSet(viewsets.ModelViewSet):
	queryset = UserNotifications.objects.all()
	serializer_class = UserNotificationsSerializer
	permission_classes = [DjangoModelPermissions]


class CustomUserViewSet(viewsets.ModelViewSet):
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer
	
	def get_queryset(self):
		user_type = self.request.query_params.get("type")
		if user_type == "site":
			return CustomUser.objects.filter(role__in=[
				'community_ambassador',
				'front_office',
				'front_office_manager',
				'marketing',
				'resident_manager',
			])
		elif user_type == "app":
			return CustomUser.objects.filter(role__in=[
				'resident',
				'guest',
			])
		return CustomUser.objects.all()
	
	def perform_create(self, serializer):
		groups_data = serializer.validated_data.pop('groups', [])
		permissions_data = serializer.validated_data.pop('user_permissions', [])
		user = serializer.save()
		
		user.groups.set(groups_data)
		user.user_permissions.set(permissions_data)
	

class GetCXAppCurrentUser(generics.GenericAPIView):
	serializer_class = CXAppUserSerializer
	permission_classes = [DjangoModelPermissions]

	def get(self, request, *args, **kwargs):
		user = self.serializer_class(request.user)
		return Response(user.data)