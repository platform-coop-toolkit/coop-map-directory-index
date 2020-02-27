# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import User, UserSocialNetwork


class UserSocialNetworkInline(admin.TabularInline):
    model = UserSocialNetwork
    extra = 3


class CustomUserAdmin(UserAdmin):
    # list_display = ('email', 'first_name', 'last_name',)

    UserAdmin.fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    inlines = [UserSocialNetworkInline]


admin.site.register(User, CustomUserAdmin)
