from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis import admin
from django.contrib.gis.admin import ModelAdmin, OSMGeoAdmin, TabularInline
from .models import UserSocialNetwork, Role
from django.db.models.functions import Lower


class UserSocialNetworkInline(admin.TabularInline):
    model = UserSocialNetwork
    fields = ['socialnetwork', 'identifier', ]
    extra = 3


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin, OSMGeoAdmin):
    list_display = ['username', 'first_name', 'middle_name', 'last_name', 'is_active', ]
    list_filter = ['roles', 'source', 'is_active', 'is_staff', ]
    UserAdmin.fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'first_name',
            'middle_name',
            'last_name',
            'has_profile',
            'bio',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'url',
            'lat',
            'lng',
            'geom',
            'roles',
            'languages',
            'services',
            'community_skills',
            'affiliation',
            'affiliation_url',
            'challenges',
            'source',
        )}),
        ('Free text fields', {'fields': ('notes',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [UserSocialNetworkInline, ]
    ordering = [Lower('email'), ]


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ('name', 'order', 'description')
