from django.contrib import admin
from .models import Campus, Room, Worker, Guest, CustomUser

admin.site.register(Campus)
admin.site.register(Room)
admin.site.register(Worker)
admin.site.register(Guest)
admin.site.register(CustomUser)