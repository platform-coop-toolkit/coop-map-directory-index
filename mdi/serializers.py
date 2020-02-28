from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.models import Group
from mdi.models import Organization, Activity, Tool, License, Language
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django_countries.serializers import CountryFieldMixin


class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'id', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('id', 'name')


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
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
    languages_supported = serializers.StringRelatedField(many=True)

    class Meta:
        model = Tool
        fields = ('name', 'description', 'url', 'license', 'languages_supported')


class OrganizationSerializer(CountryFieldMixin, GeoFeatureModelSerializer):
    category = serializers.StringRelatedField(source='category.name')
    type = serializers.StringRelatedField(source='type.name')
    activities = serializers.StringRelatedField(many=True)

    class Meta:
        model = Organization
        geo_field = 'geom'
        fields = (
            'name',
            'description',
            'category',
            'type',
            'activities',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'url',
        )
