"""
URL configuration for backend_def project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from campus_management import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("management/", include("campus_management.urls")),
	path("api/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
	path("user/create", views.UserCreate.as_view(), name="create_user"),
	path('/get-current-user/', views.GetCurrentUser.as_view(), name='ciao'),
	path('api/get-current-user/', views.GetCXAppCurrentUser.as_view(), name='ciao'),
]
