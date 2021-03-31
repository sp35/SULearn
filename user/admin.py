from django.contrib import admin
from .models import CreatorProfile,ViewerProfile

@admin.register(CreatorProfile)
class Admin(admin.ModelAdmin):
    pass
@admin.register(ViewerProfile)
class Admin(admin.ModelAdmin):
    pass
