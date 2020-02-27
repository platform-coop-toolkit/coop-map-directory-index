# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from accounts.models import SocialNetwork
from .models import Organization, OrganizationSocialNetwork, Tool


admin.site.site_header = 'Platform Coop : Map / Directory / Index'
admin.site.site_title= 'Admin'
admin.site.index_title= 'Map / Directory / Index'


class OrganizationSocialNetworkInline(admin.TabularInline):
    model = OrganizationSocialNetwork
    extra = 3


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country',)
    list_filter = ('type', 'activities', 'country',)
    search_fields = ['name', 'description',]
    inlines = [OrganizationSocialNetworkInline]


class SocialNetworkAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ['name','description',]


class ToolAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ['name','description',]


# register models
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)
admin.site.register(Tool, ToolAdmin)
