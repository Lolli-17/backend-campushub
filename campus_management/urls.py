from django.urls import include, path
from . import views

guest_patterns = [
	path("lc", views.GuestListCreate.as_view(), name='guest-lc'),
	path("<str:id>/rud", views.GuestRetrieveUpdateDestroy.as_view(), name='guest-rud'),
]

urlpatterns = [
	path("guest/", include((guest_patterns, "guest"))),
]
