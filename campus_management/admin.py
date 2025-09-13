from django.contrib import admin
from .models import Campus, Apartment, Guest, CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm
	form = UserChangeForm
	fieldsets = BaseUserAdmin.fieldsets + (
		(None, {'fields': ('role',)}),  # aggiungi 'role' qui
	)
	list_display = BaseUserAdmin.list_display + ('role',)  # mostra il ruolo anche in lista utenti

admin.site.register(Campus)
admin.site.register(Apartment)
admin.site.register(Guest)
admin.site.register(CustomUser, UserAdmin)