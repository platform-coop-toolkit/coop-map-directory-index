# -*- coding: utf-8 -*-
# from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis import admin
from .models import User, UserSocialNetwork, Role, Source
from django.db.models.functions import Lower


class UserSocialNetworkInline(admin.TabularInline):
    model = UserSocialNetwork
    fields = ['socialnetwork', 'identifier', ]
    extra = 3


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'role', 'is_active', ]
    list_filter = ['role', 'is_active', 'is_staff', ]
    UserAdmin.fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'bio', 'city', 'state', 'postal_code', 'country', 'url', 'geom', 'role', 'languages', 'source')}),
        ('Free text fields', {'fields': ('notes',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [UserSocialNetworkInline, ]
    ordering = [Lower('email'), ]


admin.site.register(User, CustomUserAdmin)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'description')


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_filter = ('name', )
    search_fields = ['name','description', ]
