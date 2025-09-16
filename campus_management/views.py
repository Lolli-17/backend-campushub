from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth import logout
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
from .choices import RoleChoices


class RegisterUser(generics.CreateAPIView):
	serializer_class = CustomUserSerializer
	permission_classes = [AllowAny]


class GetCurrentUser(APIView):
	permission_classes = [IsAuthenticated]
	
	def get(self, request, *args, **kwargs):
		serializer = CXAppUserSerializer(request.user)
		return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        logout(request)
        return Response({"detail": "Successfully logged out."})


class CampusViewSet(viewsets.ModelViewSet):
	queryset = Campus.objects.all()
	serializer_class = CampusSerializer
	permission_classes = [IsAuthenticated]


class ApartmentViewSet(viewsets.ModelViewSet):
	queryset = Apartment.objects.all()
	serializer_class = ApartmentSerializer
	permission_classes = [IsAuthenticated]


class ElectricityReadingViewSet(viewsets.ModelViewSet):
	queryset = ElectricityReading.objects.all()
	serializer_class = ElectricityReadingSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.role in [RoleChoices.STUDENT, RoleChoices.HOTEL]:
			return Guest.objects.filter(resident=user)
		else:
			return Guest.objects.all()
	
	
class CommonAreaViewSet(viewsets.ModelViewSet):
	queryset = CommonArea.objects.all()
	serializer_class = CommonAreaSerializer
	permission_classes = [IsAuthenticated]


class GuestViewSet(viewsets.ModelViewSet):
	queryset = Guest.objects.all()
	serializer_class = GuestSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.role in [RoleChoices.STUDENT, RoleChoices.HOTEL]:
			return Guest.objects.filter(resident=user)
		else:
			return Guest.objects.all()

	def perform_update(self, serializer):
		instance = self.get_object()
		if 'resident' in serializer.validated_data:
			resident = serializer.validated_data.get('resident')
			if resident.role not in [RoleChoices.STUDENT, RoleChoices.HOTEL]:
				raise generics.serializers.ValidationError({"resident": "Il residente deve avere il ruolo di Student o Hotel per essere assegnato a un'istanza Guest."})

			if not resident.apartment:
				raise generics.serializers.ValidationError({"resident": "Il residente non ha una stanza associata."})

		serializer.save()


class PackageViewSet(viewsets.ModelViewSet):
	queryset = Package.objects.all()
	serializer_class = PackageSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.role in [RoleChoices.STUDENT, RoleChoices.HOTEL]:
			return Guest.objects.filter(resident=user)
		else:
			return Guest.objects.all()


class CommonAreaReservationViewSet(viewsets.ModelViewSet):
	queryset = CommonAreaReservation.objects.all()
	serializer_class = CommonAreaReservationSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.role in [RoleChoices.STUDENT, RoleChoices.HOTEL]:
			return Guest.objects.filter(resident=user)
		else:
			return Guest.objects.all()


class CleaningReservationViewSet(viewsets.ModelViewSet):
	queryset = CleaningReservation.objects.all()
	serializer_class = CleaningReservationSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.role in [RoleChoices.STUDENT, RoleChoices.HOTEL]:
			return Guest.objects.filter(resident=user)
		else:
			return Guest.objects.all()


class FaultReportViewSet(viewsets.ModelViewSet):
	queryset = FaultReport.objects.all()
	serializer_class = FaultReportSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.role in [RoleChoices.STUDENT, RoleChoices.HOTEL]:
			return Guest.objects.filter(resident=user)
		else:
			return Guest.objects.all()


class GlobalNotificationsViewSet(viewsets.ModelViewSet):
	queryset = GlobalNotifications.objects.all()
	serializer_class = GlobalNotificationsSerializer
	permission_classes = [IsAuthenticated]


class UserNotificationsViewSet(viewsets.ModelViewSet):
	queryset = UserNotifications.objects.all()
	serializer_class = UserNotificationsSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.role in [RoleChoices.STUDENT, RoleChoices.HOTEL]:
			return Guest.objects.filter(resident=user)
		else:
			return Guest.objects.all()


class CustomUserViewSet(viewsets.ModelViewSet):
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer
	
	def get_queryset(self):
		user_type = self.request.query_params.get("type")
		if user_type == "site":
			return CustomUser.objects.filter(role__in=[
				RoleChoices.COMMUNITY_AMBASSADOR,
				RoleChoices.FRONT_OFFICE,
				RoleChoices.FRONT_OFFICE_MANAGER,
				RoleChoices.MARKETING,
				RoleChoices.RESIDENT_MANAGER,
			])
		elif user_type == "app":
			return CustomUser.objects.filter(role__in=[
				RoleChoices.STUDENT,
				RoleChoices.HOTEL,
			])
		return CustomUser.objects.all()
	
	def perform_create(self, serializer):
		groups_data = serializer.validated_data.pop('groups', [])
		permissions_data = serializer.validated_data.pop('user_permissions', [])
		user = serializer.save()
		
		user.groups.set(groups_data)
		user.user_permissions.set(permissions_data)