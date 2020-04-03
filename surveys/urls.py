from django.urls import path
from django.conf.urls import url
from . import views
from .forms import IndividualForm, OrganizationForm, SocialNetworksForm
from .preview import IndividualFormPreview, OrganizationFormPreview, SocialNetworksFormPreview
from .views import SurveyWizard, FORMS, TEMPLATES, ContactWizard


urlpatterns = [
    # path('', views.index, name='index'),
    url(r'^ecosystem/$', SurveyWizard.as_view(FORMS)),
    url(r'^preview/individual/$', IndividualFormPreview(IndividualForm)),
    url(r'^preview/organization/$', OrganizationFormPreview(OrganizationForm)),
    url(r'^preview/socialnetworks/$', SocialNetworksFormPreview(SocialNetworksForm)),
    url(r'^ecosystem-2020/$', ContactWizard.as_view([IndividualForm, OrganizationForm, SocialNetworksForm])),
]
