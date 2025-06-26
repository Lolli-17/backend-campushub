from django.contrib import admin
from .models import Campus, Room, Guest, CustomUser

admin.site.register(Campus)
admin.site.register(Room)
admin.site.register(Guest)
admin.site.register(CustomUser)