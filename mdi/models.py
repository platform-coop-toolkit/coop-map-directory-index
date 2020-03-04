from django.db import models
from django.contrib.gis.db import models
from accounts.models import User, SocialNetwork
from django.conf.global_settings import LANGUAGES
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import HStoreField
from django.urls import reverse
from django.db.models import Manager as GeoManager


class Source(models.Model):
    name = models.CharField(blank=False, max_length=255, unique=True)
    description = models.CharField(blank=True, max_length=255)
    url = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(blank=False, max_length=255, unique=True)
    description = models.CharField(blank=True, default='', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(blank=False, max_length=255, unique=True)
    description = models.CharField(blank=True, default='', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Sector(models.Model):
    name = models.CharField(blank=False, max_length=255, unique=True)
    description = models.CharField(blank=True, default='', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Pricing(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.CharField(blank=True, default='', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name


class Language(models.Model):
    culture_code = models.CharField(primary_key=True, max_length=7, blank=False, null=False, unique=True,)
    iso_name = models.CharField(max_length=64, blank=False, null=False, unique=True,)

    class Meta:
        ordering = ['culture_code']

    def __str__(self):
        return self.iso_name


class License(models.Model):
    name = models.CharField(blank=False, max_length=255)
    spdx = models.CharField(blank=False, max_length=64)
    url = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['spdx',]

    def __str__(self):
        return self.spdx


class Tool(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=True, default='')
    url = models.CharField(blank=False, max_length=255)
    license = models.ForeignKey(License, blank=True, null=True, on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, blank=True, null=True, on_delete=models.CASCADE)
    languages_supported = models.ManyToManyField(Language)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=True, default='')
    address = models.CharField(blank=True, default='', max_length=255)
    city = models.CharField(blank=True, default='', max_length=255)
    state = models.CharField(blank=True, default='', max_length=255)
    postal_code = models.CharField(blank=True, default='', max_length=255)
    country = CountryField()
    email = models.CharField(blank=True, default='', max_length=255)
    url = models.CharField(blank=True, default='', max_length=255)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    geom = models.PointField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    sectors = models.ManyToManyField(Sector)
    socialnetworks = models.ManyToManyField(SocialNetwork, through='OrganizationSocialNetwork')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}, {}'.format(self.name, self.city)


class OrganizationSocialNetwork(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    socialnetwork = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    handle = models.CharField(blank=True, max_length=64)
    url = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Organization's Social Network"

    def clean(self):
        super().clean()
        if self.handle is None and self.url is None:
            raise ValidationError('At least one of Handle or URL must be specified')
