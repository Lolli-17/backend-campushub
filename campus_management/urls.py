from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CampusViewSet, ApartmentViewSet, ElectricityMeterViewSet, CommonAreaViewSet,
    GuestViewSet, PackageViewSet, CommonAreaReservationViewSet, CleaningReservationViewSet,
    FaultReportViewSet, CustomUserViewSet, UserNotificationsViewSet, 
	GlobalNotificationsViewSet, CleaningTypeViewSet, ElectricityReadingViewSet,
)

# Crea un router e registra i nostri ViewSet con esso.
router = DefaultRouter()
router.register(r'campuses', CampusViewSet)
router.register(r'apartments', ApartmentViewSet)
router.register(r'electricity-meters', ElectricityMeterViewSet, basename='electricitymeter')
router.register(r'electricity-readings', ElectricityReadingViewSet, basename='electricityreading')
router.register(r'common-areas', CommonAreaViewSet, basename='commonarea')
router.register(r'guests', GuestViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'common-area-reservations', CommonAreaReservationViewSet, basename='commonareareservation')
router.register(r'cleaning-types', CleaningTypeViewSet, basename='cleaningtype')
router.register(r'cleaning-reservations', CleaningReservationViewSet, basename='cleaningreservation')
router.register(r'fault-reports', FaultReportViewSet, basename='faultreport')
router.register(r'user-notifications', UserNotificationsViewSet, basename='usernotification')
router.register(r'global-notifications', GlobalNotificationsViewSet, basename='globalnotification')
router.register(r'custom-users', CustomUserViewSet, basename='customuser')


# Le pattern URL per l'API.
urlpatterns = [
    path('', include(router.urls)),
]
