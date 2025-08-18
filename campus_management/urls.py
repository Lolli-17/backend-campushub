from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CampusViewSet, SpaceViewSet, RoomViewSet, ElectricityMeterViewSet, CommonAreaViewSet,
    GuestViewSet, PackageViewSet, CommonAreaReservationViewSet, CleaningReservationViewSet,
    FaultReportViewSet, CustomUserViewSet, UserNotificationsViewSet, GlobalNotificationsViewSet
)

# Crea un router e registra i nostri ViewSet con esso.
router = DefaultRouter()
router.register(r'campuses', CampusViewSet)
router.register(r'space', SpaceViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'electricity-meters', ElectricityMeterViewSet, basename='electricitymeter') # Specificare basename per OneToOneField o se il nome è diverso
router.register(r'common-areas', CommonAreaViewSet, basename='commonarea')
router.register(r'guests', GuestViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'common-area-reservations', CommonAreaReservationViewSet, basename='commonareareservation')
router.register(r'cleaning-reservations', CleaningReservationViewSet, basename='cleaningreservation')
router.register(r'fault-reports', FaultReportViewSet, basename='faultreport')
router.register(r'user-notifications', UserNotificationsViewSet, basename='usernotification')
router.register(r'global-notifications', GlobalNotificationsViewSet, basename='globalnotification')
router.register(r'custom-users', CustomUserViewSet, basename='customuser')


# Le pattern URL per l'API.
urlpatterns = [
    path('', include(router.urls)),
]

'''
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMDQwMjcwLCJpYXQiOjE3NTA5NTM4NzAsImp0aSI6IjE0YWMzMmE3ZGI1MDQ2OTc5ZmQzYWRmNzJlOTE4OWFkIiwidXNlcl9pZCI6IjFhZGYwMWNiLWUxNTctNDc2MC05NTUzLWE5MzAwNDUyYzViOSJ9.8oa-WejYOKuCuOnJSSalE3enP2MMPMGw7fqIEDdhoKk
'''