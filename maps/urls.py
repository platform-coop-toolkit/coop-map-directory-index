from django.urls import path

from . import views
from .views import PrivacyPolicyView, TermsOfServiceView

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('organizations/<int:organization_id>', views.organization_detail, name='organization_detail'),
    path('individuals/<int:user_id>', views.individual_detail, name='individual_detail'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), {'name': 'privacy_policy', 'title': 'Privacy Policy'}),
    path('terms-of-service/', TermsOfServiceView.as_view(), {'name': 'terms_of_service', 'title': 'Terms of Service'}),
]
