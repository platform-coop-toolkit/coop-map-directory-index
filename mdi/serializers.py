from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from django.contrib.auth.models import Group
from accounts.models import Role
from mdi.models import Organization, Type, SocialNetwork, Sector, Tool, License, Language, Niche
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django_countries.serializer_fields import CountryField


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ('culture_code', 'iso_name',)


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'icon')


class UserSerializer(GeoFeatureModelSerializer):
    source = serializers.StringRelatedField(source='source.name')
    country = CountryField(country_dict=True)
    languages = LanguageSerializer(many=True)
    roles = RoleSerializer(many=True)

    class Meta:
        model = get_user_model()
        geo_field = 'geom'
        fields = (
            'id',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'roles',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'languages',
            'phone',
            'url',
            'bio',
            'source',
        )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class SectorSerializer(serializers.HyperlinkedModelSerializer):
    # sectors_in_taxonomy = SerializerMethodField()

    # def get_sectors_in_taxonomy(self, Sector):
    #     sectors_in_taxonomy = Sector.objects.filter(name__regex=r'^[A-Z]')
    #     serializer =

    class Meta:
        model = Sector
        fields = ('name', 'description',)


class LicenseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = License
        fields = ('spdx', 'name', 'url',)


class NicheSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Niche
        fields = ('name', 'description',)


class ToolSerializer(serializers.HyperlinkedModelSerializer):
    license = serializers.StringRelatedField()
    pricing = serializers.StringRelatedField()
    niches = NicheSerializer(many=True)
    languages_supported = LanguageSerializer(many=True)
    sectors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Tool
        fields = (
            'id',
            'updated_at',
            'name',
            'description',
            'url',
            'license_type',
            'license',
            'pricing',
            'niches',
            'languages_supported',
            'coop_made',
            'sectors',
            'use_count',
        )


class OrganizationSerializer(GeoFeatureModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    source = serializers.StringRelatedField()
    stage = serializers.StringRelatedField()
    type = serializers.StringRelatedField()
    languages = LanguageSerializer(many=True)
    country = CountryField(country_dict=True)
    sectors = serializers.StringRelatedField(many=True)
    socialnetworks = serializers.StringRelatedField(many=True)
    tools = serializers.StringRelatedField(many=True)

    class Meta:
        model = Organization
        geo_field = 'geom'
        fields = (
            'id',
            'name',
            'description',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'languages',
            'url',
            'socialnetworks',
            'categories',
            'type',
            'sectors',
            'stage',
            'tools',
            'source',
        )
