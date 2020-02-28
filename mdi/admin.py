# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from accounts.models import SocialNetwork
from .models import Organization, OrganizationSocialNetwork, Tool, License #, Language


# Window dressing
admin.site.site_header = 'Platform Coop : Map / Directory / Index'
admin.site.site_title= 'Admin'
admin.site.index_title= 'Map / Directory / Index'


# Create Admin-related classes
class OrganizationSocialNetworkInline(admin.TabularInline):
    model = OrganizationSocialNetwork
    extra = 3


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country',)
    list_filter = ('type', 'activities', 'country',)
    search_fields = ['name', 'description',]
    inlines = [OrganizationSocialNetworkInline]


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ['name','description',]


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'license',)
    list_filter = ('license',) #  'languages_supported',)
    search_fields = ['name', 'description',]


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    fields = ('spdx', 'name', 'url',)
    list_filter = ('spdx',)
    search_fields = ['spdx', 'name',]
