# -*- coding: utf-8 -*-
from django.contrib.gis import admin
from accounts.models import SocialNetwork
from .models import Organization, OrganizationSocialNetwork, Tool, License, Pricing
from django.db.models.functions import Lower


# Window dressing
admin.site.site_header = 'Platform Coop : Map / Directory / Index'
admin.site.site_title= 'Admin'
admin.site.index_title= 'Map / Directory / Index'


# Create Admin-related classes
class OrganizationSocialNetworkInline(admin.TabularInline):
    model = OrganizationSocialNetwork
    extra = 3


@admin.register(Organization)
class OrganizationAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'city', 'country',)
    list_filter = ('source', 'type', 'sectors', 'country',)
    search_fields = ['name', 'description', ]
    inlines = [OrganizationSocialNetworkInline]
    ordering = [Lower('name'), ]


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_filter = ('name', 'format', )
    search_fields = ['name','description', ]


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'license', )
    list_filter = ('license', 'pricing') # 'languages_supported',)
    search_fields = ['name', 'description',]


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    fields = ('spdx', 'name', 'url', )
    list_filter = ('spdx', )
    search_fields = ['spdx', 'name', ]

@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    fields = ('name', )
