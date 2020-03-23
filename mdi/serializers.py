from rest_framework import serializers
from accounts.models import User, Source
from django.contrib.auth.models import Group
from mdi.models import Organization, SocialNetwork, Sector, Tool, License, Language
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django_countries.serializers import CountryFieldMixin


class UserSerializer(CountryFieldMixin, GeoFeatureModelSerializer):
    source = serializers.StringRelatedField(source='source.name')

    class Meta:
        model = User
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
            'url',
            'bio',
            'notes',
            'source',
        )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class SectorSerializer(serializers.HyperlinkedModelSerializer):
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


class ToolSerializer(serializers.HyperlinkedModelSerializer):
    license = serializers.StringRelatedField(source='license.spdx')
    pricing = serializers.StringRelatedField(source='pricing.name')
    languages_supported = LanguageSerializer(many=True)
    sectors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Tool
        fields = (
            'name',
            'description',
            'url',
            'license',
            'pricing',
            'languages_supported',
            'sectors',
            'notes',
        )


class OrganizationSerializer(CountryFieldMixin, GeoFeatureModelSerializer):
    category = serializers.StringRelatedField(source='category.name')
    source = serializers.StringRelatedField(source='source.name')
    type = serializers.StringRelatedField(source='type.name')
    sectors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Organization
        geo_field = 'geom'
        fields = (
            'id',
            'name',
            'description',
            'category',
            'type',
            'sectors',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'url',
            'source',
        )
