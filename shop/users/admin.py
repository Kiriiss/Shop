from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username','password', 'first_name', 'last_name', 'email', 'is_staff', 'photo')
