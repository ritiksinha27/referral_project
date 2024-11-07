from django.contrib import admin
from .models import CustomUser, UserStructure
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'mobile_no', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']

@admin.register(UserStructure)
class UserStructureAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'points']