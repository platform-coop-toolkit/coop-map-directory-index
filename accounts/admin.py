# -*- coding: utf-8 -*-
# from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis import admin
from .models import User, UserSocialNetwork


class UserSocialNetworkInline(admin.TabularInline):
    model = UserSocialNetwork
    fields = ['socialnetwork', 'identifier',]
    extra = 3


class CustomUserAdmin(UserAdmin):
    UserAdmin.fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'bio', 'city', 'state', 'postal_code', 'country', 'url', 'geom',)}),
        ('Free text fields', {'fields': ('notes',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [UserSocialNetworkInline]


admin.site.register(User, CustomUserAdmin)
