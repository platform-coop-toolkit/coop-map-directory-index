from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from django.contrib.auth.models import Group
from mdi.models import Organization, SocialNetwork, Sector, Tool, License, Language, Niche
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django_countries.serializers import CountryFieldMixin


class UserSerializer(CountryFieldMixin, GeoFeatureModelSerializer):
    source = serializers.StringRelatedField(source='source.name')

    class Meta:
        model = get_user_model()
        geo_field = 'geom'
        fields = (
            'id',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
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


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ('culture_code', 'iso_name',)


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


class OrganizationSerializer(CountryFieldMixin, GeoFeatureModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    source = serializers.StringRelatedField()
    stage = serializers.StringRelatedField()
    type = serializers.StringRelatedField()
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
            'url',
            'socialnetworks',
            'categories',
            'type',
            'sectors',
            'stage',
            'tools',
            'source',
        )
