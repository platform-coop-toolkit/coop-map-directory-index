from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('organizations/<int:organization_id>', views.organization_detail, name='organization_detail'),
]
