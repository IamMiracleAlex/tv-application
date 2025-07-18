from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
	pass
