from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager
from django_countries.fields import CountryField
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError


class MyUserManager(UserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, first and last name, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, first and last name, and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class SocialNetwork(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=True, default='')
    url = models.CharField(blank=False, max_length=255)
    format = models.CharField(blank=False, max_length=8, choices=[('handle', 'handle'), ('url', 'url')])
    base_url = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


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


class User(AbstractUser):
    email = models.EmailField(
      verbose_name='email address',
      max_length=255,
      unique=True,
    )
    middle_name = models.CharField(blank=True, max_length=255, unique=False)
    bio = models.TextField(blank=True, default='')
    address = models.CharField(blank=True, default='', max_length=255)
    city = models.CharField(blank=True, default='', max_length=255)
    state = models.CharField(blank=True, default='', max_length=255)
    postal_code = models.CharField(blank=True, default='', max_length=255)
    country = CountryField(blank=True)
    url = models.CharField(blank=True, default='', max_length=255)
    geom = models.PointField(blank=True, null=True)
    socialnetworks = models.ManyToManyField(SocialNetwork, through='UserSocialNetwork')
    notes = models.TextField(blank=True, default='')
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    # created_at: would normally add this but django-registration gives us date_joined
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @classmethod
    def get_email_field_name(cls):
        return 'email'

    class Meta:
        db_table = 'auth_user'
        ordering = [Lower('email'), ]


# Because User extends AbstractUser the underlying model includes a `username` field with a `unique` constraint.
# Because we don't use it, PostgreSQL complains that uniqueness is violated when an empty string comes in. This
# relies on the pre_save signal to set the `username` field equal to the `email` field. `username` does not and
# should never elsewhere appear in the codebase.
@receiver(pre_save, sender=User)
def mirror_username_from_email(sender, instance, *args, **kwargs):
    instance.username = instance.email



class UserSocialNetwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    socialnetwork = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    identifier = models.CharField(blank=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['socialnetwork',]
        verbose_name = "User's Social Network"
