from rest_framework import generics
from .serializers import GuestSerializer, CustomUserSerializer, CXAppUserSerializer
from .models import Guest
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response

class GuestViews:
	serializer_class = GuestSerializer

class GuestListCreate(GuestViews, generics.ListCreateAPIView):
	queryset = Guest.objects.all()
	
class GuestRetrieveUpdateDestroy(GuestViews, generics.RetrieveUpdateDestroyAPIView):
	queryset = Guest.objects.all()

class UserCreate(generics.CreateAPIView):
	serializer_class = CustomUserSerializer
	permission_classes = [AllowAny]

class GetCurrentUser(generics.GenericAPIView):
	serializer_class = CustomUserSerializer
	
	def get(self, request, *args, **kwargs):
		user = self.serializer_class(request.user)
		return Response(user.data)
	
class GetCXAppCurrentUser(generics.GenericAPIView):
	serializer_class = CXAppUserSerializer

	def get(self, request, *args, **kwargs):
		user = self.serializer_class(request.user)
		return Response(user.data)