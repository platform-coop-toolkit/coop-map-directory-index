from django.urls import path

from . import views
from .views import PrivacyPolicyView, TermsOfServiceView

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('organizations/<int:organization_id>', views.organization_detail, name='organization_detail'),
    path('individuals/<int:user_id>', views.individual_detail, name='individual_detail'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), {'title': 'Privacy Policy'}, name='privacy_policy'),
    path('terms-of-service/', TermsOfServiceView.as_view(), {'title': 'Terms of Service'}, name='terms_of_service'),
]
