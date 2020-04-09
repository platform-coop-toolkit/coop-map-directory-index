from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from accounts.models import SocialNetwork, Source
from django_countries.fields import CountryField
from datetime import date
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Manager as GeoManager


class Category(models.Model):
    name = models.CharField(blank=False, max_length=255, unique=True)
    description = models.CharField(blank=True, default='', max_length=255)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order']

    def __str__(self):
        return self.name


class Challenge(models.Model):
    name = models.CharField(blank=False, max_length=255, unique=True)
    description = models.CharField(blank=True, default='', max_length=255)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class LegalStatus(models.Model):
    name = models.CharField(blank=False, max_length=255, unique=True)
    description = models.CharField(blank=True, default='', max_length=255)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Legal Statuses"
        ordering = ['order']

    def __str__(self):
        return self.name


class Service(models.Model):
    '''A service provided by an Individual. Organization TBD.'''
    name = models.CharField(blank=False, max_length=255, unique=True)
    description = models.CharField(blank=True, default='', max_length=255)
    order = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Stage(models.Model):
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


class Relationship(models.Model):
    '''The character of the relationship between Individuals and Organizations.'''
    name = models.CharField(blank=False, max_length=255, unique=True)
    description = models.CharField(blank=True, default='', max_length=255)
    order = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return self.name


class Niche(models.Model):
    '''The primary function of an object in the Tool class. To be matched with the needs of an Organization or Individual.'''
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
        ordering = ['iso_name']

    def __str__(self):
        return self.iso_name


class License(models.Model):
    name = models.CharField(blank=False, max_length=255)
    spdx = models.CharField(blank=False, max_length=64)
    url = models.URLField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['spdx', ]

    def __str__(self):
        return self.spdx


class Tool(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=True, default='')
    url = models.URLField(blank=False, max_length=255)
    license = models.ForeignKey(License, blank=True, null=True, on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, blank=True, null=True, on_delete=models.CASCADE)
    niches = models.ManyToManyField(Niche)
    languages_supported = models.ManyToManyField(Language, blank=True,)
    sectors = models.ManyToManyField(Sector, blank=True,)
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
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True, default='', max_length=255)
    media_url = models.URLField(blank=True, default='', max_length=255)
    logo_url = models.URLField(blank=True, default='', max_length=255)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True)
    founded = models.DateField(blank=True, null=True)
    num_workers = models.IntegerField(blank=True, null=True)
    related_individuals = models.ManyToManyField(
        get_user_model(),
        through='EntitiesEntities',
        through_fields=['from_org', 'to_ind']
    )
    related_organizations = models.ManyToManyField('self', through='EntitiesEntities')
    # num_impacted = models.IntegerField(blank=True)
    categories = models.ManyToManyField(Category, blank=True,)
    stage = models.ForeignKey(Stage, blank=True, null=True, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    sectors = models.ManyToManyField(Sector, blank=True,)
    legal_status = models.ManyToManyField(LegalStatus, blank=True,)
    challenges = models.ManyToManyField(Challenge, blank=True,)
    socialnetworks = models.ManyToManyField(SocialNetwork, blank=True, through='OrganizationSocialNetwork')
    notes = models.TextField(blank=True, default='')
    admin_email = models.EmailField(default='', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def years_operating(self):
        if self.founded:
            return round((date.today() - self.founded).days/365.2425)
        else:
            return 'Unknown'

    def sectors_to_s(self):
        if self.sectors.count() > 0:
            sector_string = ''
            for s in self.sectors.all():
                sector_string += '{}, '.format(s)
            sector_string = sector_string.rstrip(', ')
        else:
            sector_string = 'Unknown'
        return sector_string

    def legal_status_to_s(self):
        if self.legal_status.count() > 0:
            legal_status_string = ''
            for ls in self.legal_status.all():
                legal_status_string += '{}, '.format(ls)
            legal_status_string = legal_status_string.rstrip(', ')
        else:
            legal_status_string = 'Unknown'
        return legal_status_string

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class OrganizationSocialNetwork(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    socialnetwork = models.ForeignKey(SocialNetwork, blank=True, on_delete=models.CASCADE)
    identifier = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Organization's Social Network"


class EntitiesEntities(models.Model):
    from_org = models.ForeignKey(Organization, blank=True, null=True, related_name='from_org_set', on_delete=models.CASCADE)
    from_ind = models.ForeignKey(get_user_model(), blank=True, null=True, related_name='from_ind_set', on_delete=models.CASCADE)
    to_org = models.ForeignKey(Organization, blank=True, null=True, related_name='to_org_set', on_delete=models.CASCADE)
    to_ind = models.ForeignKey(get_user_model(), blank=True, null=True, related_name='to_ind_set', on_delete=models.CASCADE)
    relationship = models.ForeignKey(Relationship, blank=True, on_delete=models.CASCADE)
    vetted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Entity to Entity Relationships"
