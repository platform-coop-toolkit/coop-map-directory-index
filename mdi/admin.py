from django.contrib.gis import admin
from django.contrib.gis.admin import ModelAdmin, OSMGeoAdmin, TabularInline
from accounts.models import SocialNetwork
from .models import \
    Category, Challenge, LegalStatus, Organization, OrganizationSocialNetwork, Stage, Type, Tool, License, \
    Pricing, Niche, Relationship, EntitiesEntities, Service
from django.db.models.functions import Lower


# Window dressing
admin.site.site_header = 'Platform Coop : Map / Directory / Index'
admin.site.site_title= 'Admin'
admin.site.index_title= 'Map / Directory / Index'


# Create Admin-related classes
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'order', 'category_group', 'description' )


@admin.register(Challenge)
class LegalStatusAdmin(ModelAdmin):
    list_display = ('name', 'order', 'description', )


@admin.register(LegalStatus)
class LegalStatusAdmin(ModelAdmin):
    list_display = ('name', 'order', 'description', )


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('name', 'order', 'description', )

@admin.register(Type)
class TypeAdmin(ModelAdmin):
    list_display = ('name', 'description' )

class OrganizationSocialNetworkInline(TabularInline):
    model = OrganizationSocialNetwork
    extra = 3


@admin.register(Organization)
class OrganizationAdmin(OSMGeoAdmin):
    list_display = ('name', 'city', 'country',)
    list_filter = ('source', 'categories', 'type', 'sectors', 'country',)
    search_fields = ['name', 'description', ]
    inlines = [OrganizationSocialNetworkInline]
    ordering = [Lower('name'), ]


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_filter = ('name', 'format', )
    search_fields = ['name','description', ]


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(EntitiesEntities)
class EntitiesEntitiesAdmin(admin.ModelAdmin):
    list_display = ('from_ind', 'from_org', 'relationship', 'to_ind', 'to_org', )


@admin.register(Stage)
class ToolAdmin(ModelAdmin):
    list_display = ('name', 'description', )


@admin.register(Niche)
class NicheAdmin(ModelAdmin):
    list_display = ('name', 'description', )


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'license', )
    list_filter = ('niches', 'license', 'pricing') # 'languages_supported',)
    search_fields = ['name', 'description',]


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    fields = ('spdx', 'name', 'url', )
    list_display = ('spdx', 'name', 'url', )
    list_filter = ('spdx', )
    search_fields = ['spdx', 'name', ]


@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    fields = ('name', )
