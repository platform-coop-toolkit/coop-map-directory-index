from rest_framework import serializers
from django.contrib.auth.models import User, Group
from mdi.models import Organization
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'id', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('id', 'name')


class OrganizationSerializer(GeoFeatureModelSerializer):
    category = serializers.StringRelatedField(source='category.name')
    type = serializers.StringRelatedField(source='type.name')

    class Meta:
        model = Organization
        geo_field = 'geom'
        fields = ('name', 'description', 'category', 'type', 'address', 'city', 'state', 'postal_code', 'country', 'url',)
