from django.contrib.postgres.fields import IntegerRangeField
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from datetime import date
from django.utils import timezone
from accounts.models import SocialNetwork, Source
from django_countries.fields import CountryField

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Manager as GeoManager


class Type(models.Model):
    name = models.CharField(blank=False, max_length=255, unique=True)
    description = models.CharField(blank=True, default='', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(blank=False, max_length=255, unique=True)
    category_type = models.ForeignKey(Type, blank=True, null=True, on_delete=models.CASCADE)
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
    license_type = models.CharField(blank=True, default='', max_length=64,
                             choices=[('proprietary', 'Proprietary'), ('proprietary-with-floss-integration-tools', 'Proprietary with free / libre / open source integration tools'), ('floss', 'Free / libre / open source')], verbose_name='License type')
    license = models.ForeignKey(License, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Free / libre / open source license')
    pricing = models.ForeignKey(Pricing, blank=True, null=True, on_delete=models.CASCADE)
    niches = models.ManyToManyField(Niche)
    languages_supported = models.ManyToManyField(Language, blank=True)
    sectors = models.ManyToManyField(Sector, blank=True)
    coop_made = models.CharField(blank=False, default=0, max_length=16,
                             choices=[('unknown', 'Not sure'), ('yes', 'Yes'), ('no', 'No')], verbose_name='Made by a cooperative')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def use_count(self):
        return self.organization_set.count()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=True, default='')
    languages = models.ManyToManyField(Language, blank=True, verbose_name='Operating language')
    address = models.CharField(blank=True, default='', max_length=255)
    city = models.CharField(blank=True, default='', max_length=255)
    state = models.CharField(blank=True, default='', max_length=255)
    postal_code = models.CharField(blank=True, default='', max_length=255)
    country = CountryField()
    email = models.EmailField(max_length=255)
    phone = models.CharField(blank=True, default='', max_length=255)
    url = models.URLField(blank=True, default='', max_length=255)
    media_url = models.URLField(blank=True, default='', max_length=255)
    logo_url = models.URLField(blank=True, default='', max_length=255)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True)
    # founded_ min_ and max_dates are a strategy to represent date specificity (to the year, month, day).
    # See https://softwareengineering.stackexchange.com/a/194294/365490
    founded = models.DateField(blank=True, null=True)
    founded_min_date = models.DateField(blank=True, null=True)
    founded_max_date = models.DateField(blank=True, null=True)
    num_members = models.IntegerField(blank=True, null=True, verbose_name='Number of members', )
    num_workers = models.IntegerField(blank=True, null=True, verbose_name='Number of workers', )
    worker_distribution = models.CharField(blank=True, default='', max_length=64,
                             choices=[('colocated', 'Co-located'), ('regional', 'Regionally distributed'), ('national', 'Nationally distributed'), ('international', 'Internationally distributed')])
    related_individuals = models.ManyToManyField(
        get_user_model(),
        through='EntitiesEntities',
        through_fields=['from_org', 'to_ind']
    )
    related_organizations = models.ManyToManyField('self', through='EntitiesEntities')
    geo_scope = models.CharField(blank=True, max_length=16,
                             choices=[('Local', 'Local'), ('Regional', 'Regional'), ('National', 'National'), ('International', 'International')],
                                 verbose_name='Geographic scope', )
    geo_scope_city = models.CharField(blank=True, default='', max_length=255, verbose_name='Geographic scope – City', )
    geo_scope_region = models.CharField(blank=True, default='', max_length=255, verbose_name='Geographic scope – Region', )
    geo_scope_country = CountryField(blank=True, verbose_name='Geographic scope – Country', )
    impacted_range = IntegerRangeField(blank=True, null=True, default=None)
    impacted_exact_number = models.IntegerField(blank=True, null=True, default=None)
    code_availability = models.CharField(blank=True, max_length=9, choices=[('Yes', 'Yes'), ('Partially', 'Partially'), ('No', 'No')])
    categories = models.ManyToManyField(Category, blank=True,)
    stage = models.ForeignKey(Stage, blank=True, null=True, default=None, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    sectors = models.ManyToManyField(Sector, blank=True,)
    legal_status = models.ManyToManyField(LegalStatus, blank=True,)
    challenges = models.ManyToManyField(Challenge, blank=True,)
    socialnetworks = models.ManyToManyField(SocialNetwork, blank=True, through='OrganizationSocialNetwork')
    tools = models.ManyToManyField(Tool, blank=True, )
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
    
    def murmurate(self):
        return {
            'name': self.name,
            'url': self.url,
            'tagline': '',
            'mission': self.description,
            'nodeTypes': 'co-op', # needs smarter mapping to Murmurations types
            'location': '{} {} {} {}'.format(self.address, self.city, self.state, self.country, self.postal_code).strip(),
            'logo': self.logo_url,
            'feed': '',
            'tags': self.sectors_to_s(),
            'lat': self.geom.y,
            'lon': self.geom.x,
            'updated': timezone.now().timestamp()
        }

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
