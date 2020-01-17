# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Organization

# customize header
admin.site.site_header = 'My Organization API'
# set title
admin.site.site_title= 'Admin'
admin.site.index_title= 'My Organization API'
class OrganizationAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ['name','description']
# register models
admin.site.register(Organization, OrganizationAdmin)
