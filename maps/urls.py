from django.urls import path
from django.conf.urls import url
from . import views
from .views import INDIVIDUAL_FORMS, IndividualProfileWizard, OrganizationAutocomplete,\
    OrganizationDelete, PrivacyPolicyView, TermsOfServiceView, AboutPageView
from accounts.models import UserSocialNetwork

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/individual', IndividualProfileWizard.as_view(INDIVIDUAL_FORMS, instance_dict={'social_networks': UserSocialNetwork}), name='individual-profile'),
    path('profiles/organization', IndividualProfileWizard.as_view(INDIVIDUAL_FORMS), {'title': 'Organization'}, name='organization-profile'),
    url(r'^organization-autocomplete/$', OrganizationAutocomplete.as_view(create_field='name'), name='organization-autocomplete'),
    path('organizations/<int:organization_id>', views.organization_detail, name='organization_detail'),
    path('organizations/<int:pk>/delete', OrganizationDelete.as_view(), name='organization-delete'),
    path('individuals/<int:user_id>', views.individual_detail, name='individual-detail'),
    path('my-profiles/', views.my_profiles, name='my-profiles'),
    path('accounts/', views.account_settings, name='account-settings'),
    path('about/', AboutPageView.as_view(), {'title': 'About'}, name='about'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), {'title': 'Privacy Policy'}, name='privacy_policy'),
    path('terms-of-service/', TermsOfServiceView.as_view(), {'title': 'Terms of Service'}, name='terms_of_service'),
]
