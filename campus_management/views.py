from rest_framework import generics
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from rest_framework import viewsets
from django.utils import timezone
from .models import (
	Campus, Space, Room, ElectricityMeter, CommonArea, Guest, Package,
	CommonAreaReservation, CleaningReservation, FaultReport, CustomUser,
	GlobalNotifications, UserNotifications,
)
from .serializers import (
	CampusSerializer, SpaceSerializer, RoomSerializer, ElectricityMeterSerializer,
	CommonAreaSerializer, GuestSerializer, PackageSerializer, 
	CommonAreaReservationSerializer, CleaningReservationSerializer, 
	FaultReportSerializer, CustomUserSerializer, CXAppUserSerializer,
	GlobalNotificationsSerializer, UserNotificationsSerializer,
)


class RegisterUser(generics.CreateAPIView):
	serializer_class = CustomUserSerializer
	permission_classes = [AllowAny]


class GetCurrentUser(generics.GenericAPIView):
	serializer_class = CustomUserSerializer
	permission_classes = [AllowAny]
	
	def get(self, request, *args, **kwargs):
		user = self.serializer_class(request.user)
		return Response(user.data)



class CampusViewSet(viewsets.ModelViewSet):
	queryset = Campus.objects.all()
	serializer_class = CampusSerializer


class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer


class SpaceViewSet(viewsets.ModelViewSet):
	queryset = Space.objects.all()
	serializer_class = SpaceSerializer


class ElectricityMeterViewSet(viewsets.ModelViewSet):
	queryset = ElectricityMeter.objects.all()
	serializer_class = ElectricityMeterSerializer


class CommonAreaViewSet(viewsets.ModelViewSet):
	queryset = CommonArea.objects.all()
	serializer_class = CommonAreaSerializer


class GuestViewSet(viewsets.ModelViewSet):
	queryset = Guest.objects.all()
	serializer_class = GuestSerializer

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		if 'status' in request.data and request.data['status'] == 'in house' and instance.status != 'in house':
			instance.check_in_time = timezone.now()
		elif 'status' in request.data and request.data['status'] != 'in house' and instance.status == 'in house':
			instance.check_in_time = None
		return super().update(request, *args, **kwargs)


class PackageViewSet(viewsets.ModelViewSet):
	queryset = Package.objects.all()
	serializer_class = PackageSerializer


class CommonAreaReservationViewSet(viewsets.ModelViewSet):
	queryset = CommonAreaReservation.objects.all()
	serializer_class = CommonAreaReservationSerializer


class CleaningReservationViewSet(viewsets.ModelViewSet):
	queryset = CleaningReservation.objects.all()
	serializer_class = CleaningReservationSerializer


class FaultReportViewSet(viewsets.ModelViewSet):
	queryset = FaultReport.objects.all()
	serializer_class = FaultReportSerializer


class GlobalNotificationsViewSet(viewsets.ModelViewSet):
	queryset = GlobalNotifications.objects.all()
	serializer_class = GlobalNotificationsSerializer


class UserNotificationsViewSet(viewsets.ModelViewSet):
	queryset = UserNotifications.objects.all()
	serializer_class = UserNotificationsSerializer


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
	

class GetCXAppCurrentUser(generics.GenericAPIView):
	serializer_class = CXAppUserSerializer

	def get(self, request, *args, **kwargs):
		user = self.serializer_class(request.user)
		return Response(user.data)