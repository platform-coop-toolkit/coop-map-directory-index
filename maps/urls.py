from django.urls import path
from django.conf.urls import url
from . import views
from .views import INDIVIDUAL_FORMS, ORGANIZATION_FORMS, TOOL_FORMS, show_more_about_you_condition, show_scope_and_impact_condition,\
    IndividualProfileWizard, OrganizationProfileWizard, ToolWizard, OrganizationDelete, PrivacyPolicyView, TermsOfServiceView, AboutPageView,\
    SummaryPageView
from accounts.models import UserSocialNetwork
from mdi.models import SocialNetwork

urlpatterns = [
    path('', views.index, name='index'),
    path('add/individual', IndividualProfileWizard.as_view(INDIVIDUAL_FORMS, condition_dict={'more_about_you': show_more_about_you_condition}, instance_dict={'social_networks': UserSocialNetwork}), name='individual-profile'),
    path('add/organization', OrganizationProfileWizard.as_view(ORGANIZATION_FORMS, condition_dict={'scope_and_impact': show_scope_and_impact_condition}, instance_dict={'social_networks': UserSocialNetwork}), name='organization-profile'),
    path('add/tool', ToolWizard.as_view(TOOL_FORMS), name='add-tool'),
    path('organizations/<int:organization_id>', views.organization_detail, name='organization-detail'),
    path('organizations/<int:pk>/delete', OrganizationDelete.as_view(), name='organization-delete'),
    path('individuals/<int:user_id>', views.individual_detail, name='individual-detail'),
    path('my-profiles/', views.my_profiles, name='my-profiles'),
    path('accounts/', views.account_settings, name='account-settings'),
    path('about/', AboutPageView.as_view(), {'title': 'About'}, name='about'),
    path('about/impact/', SummaryPageView.as_view(), {'title': 'Summary of Impact'}, name='impact'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), {'title': 'Privacy Policy'}, name='privacy_policy'),
    path('terms-of-service/', TermsOfServiceView.as_view(), {'title': 'Terms of Service'}, name='terms_of_service'),
]
