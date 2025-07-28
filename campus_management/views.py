from rest_framework import generics
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from rest_framework import viewsets
from .models import (
	Campus, Space, Room, ElectricityMeter, CommonArea, Guest, Package,
	CommonAreaReservation, CleaningReservation, FaultReport, CustomUser
)
from .serializers import (
	CampusSerializer, SpaceSerializer, RoomSerializer, ElectricityMeterSerializer,
	CommonAreaSerializer, GuestSerializer, PackageSerializer, 
	CommonAreaReservationSerializer, CleaningReservationSerializer, 
	FaultReportSerializer, CustomUserSerializer, CXAppUserSerializer
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


# ViewSet per il modello Campus
class CampusViewSet(viewsets.ModelViewSet):
	queryset = Campus.objects.all()
	serializer_class = CampusSerializer

# ViewSet per il modello Room
class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

# ViewSet per il modello Space
class SpaceViewSet(viewsets.ModelViewSet):
	queryset = Space.objects.all()
	serializer_class = SpaceSerializer

# ViewSet per il modello ElectricityMeter
class ElectricityMeterViewSet(viewsets.ModelViewSet):
	queryset = ElectricityMeter.objects.all()
	serializer_class = ElectricityMeterSerializer

# ViewSet per il modello CommonArea
class CommonAreaViewSet(viewsets.ModelViewSet):
	queryset = CommonArea.objects.all()
	serializer_class = CommonAreaSerializer

# ViewSet per il modello Guest
class GuestViewSet(viewsets.ModelViewSet):
	queryset = Guest.objects.all()
	serializer_class = GuestSerializer

# ViewSet per il modello Package
class PackageViewSet(viewsets.ModelViewSet):
	queryset = Package.objects.all()
	serializer_class = PackageSerializer

# ViewSet per il modello CommonAreaReservation
class CommonAreaReservationViewSet(viewsets.ModelViewSet):
	queryset = CommonAreaReservation.objects.all()
	serializer_class = CommonAreaReservationSerializer

# ViewSet per il modello CleaningReservation
class CleaningReservationViewSet(viewsets.ModelViewSet):
	queryset = CleaningReservation.objects.all()
	serializer_class = CleaningReservationSerializer

# ViewSet per il modello FaultReport
class FaultReportViewSet(viewsets.ModelViewSet):
	queryset = FaultReport.objects.all()
	serializer_class = FaultReportSerializer


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