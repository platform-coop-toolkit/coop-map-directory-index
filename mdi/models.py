from django.db import models
from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField
from django.urls import reverse
from django.db.models import Manager as GeoManager

class Category(models.Model):
  name = models.CharField(null=False,max_length = 255)
  description = models.CharField(null=True,max_length = 255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


class Type(models.Model):
  name = models.CharField(null=False,max_length = 255)
  description = models.CharField(null=True,max_length = 255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


class Organization(models.Model):
  name = models.CharField(null=False,max_length = 255)
  description = models.TextField(null=True)
  address = models.CharField(null=True,max_length = 255)
  city = models.CharField(null=True,max_length = 255)
  state = models.CharField(null=True,max_length = 255)
  postal_code = models.CharField(null=True,max_length = 255)
  country = models.CharField(null=True,max_length = 3)
  email = models.CharField(null=True,max_length = 255)
  url = models.CharField(null=True,max_length = 255)
  lat = models.FloatField(null=True)
  lng = models.FloatField(null=True)
  geom = models.PointField(null=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  type = models.ForeignKey(Type, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


class Activity(models.Model):
  name = models.CharField(null=False,max_length = 255)
  description = models.CharField(null=True,max_length = 255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

