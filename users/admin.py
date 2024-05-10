from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.forms import RegisterForm
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
