from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username', 'password', 'gender', 'date_of_birth')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(CustomUser, UserAdmin)