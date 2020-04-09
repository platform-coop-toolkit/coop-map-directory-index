from django.urls import path
from django.conf.urls import url
from .forms import SocialNetworksForm
from . views import index, ECOSYSTEM_FORMS, EcosystemWizard
from mdi.models import OrganizationSocialNetwork

urlpatterns = [
    url(r'^$', index),
    path(r'ecosystem-2020/',
         EcosystemWizard.as_view(ECOSYSTEM_FORMS, instance_dict={'social_networks': OrganizationSocialNetwork}),
         name='ecosystem-2020'),
]
