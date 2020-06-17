from django.urls import path
from django.conf.urls import url
from . import views
from .views import INDIVIDUAL_FORMS, ORGANIZATION_FORMS, show_more_about_you_condition, show_scope_and_impact_condition,\
    IndividualProfileWizard, OrganizationAutocomplete, OrganizationProfileWizard, OrganizationDelete, PrivacyPolicyView, TermsOfServiceView, AboutPageView
from accounts.models import UserSocialNetwork
from mdi.models import SocialNetwork

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/individual', IndividualProfileWizard.as_view(INDIVIDUAL_FORMS, condition_dict={'more_about_you': show_more_about_you_condition}, instance_dict={'social_networks': UserSocialNetwork}), name='individual-profile'),
    path('profiles/organization', OrganizationProfileWizard.as_view(ORGANIZATION_FORMS, condition_dict={'scope_and_impact': show_scope_and_impact_condition}, instance_dict={'social_networks': UserSocialNetwork}), name='organization-profile'),
    url(r'^organization-autocomplete/$', OrganizationAutocomplete.as_view(create_field='name'), name='organization-autocomplete'),
    path('organizations/<int:organization_id>', views.organization_detail, name='organization-detail'),
    path('organizations/<int:pk>/delete', OrganizationDelete.as_view(), name='organization-delete'),
    path('individuals/<int:user_id>', views.individual_detail, name='individual-detail'),
    path('my-profiles/', views.my_profiles, name='my-profiles'),
    path('about/', AboutPageView.as_view(), {'title': 'About'}, name='about'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), {'title': 'Privacy Policy'}, name='privacy_policy'),
    path('terms-of-service/', TermsOfServiceView.as_view(), {'title': 'Terms of Service'}, name='terms_of_service'),
]
