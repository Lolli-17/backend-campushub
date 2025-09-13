from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from campus_management import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include('campus_management.urls')), # Includi gli URL della tua app sotto il prefisso '/api/'
	path("user/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
	path("user/register", views.RegisterUser.as_view(), name="create_user"),
	path("user/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
	path('user/get-current', views.GetCurrentUser.as_view(), name='current_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

