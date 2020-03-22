"""cmdi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from mdi.views import UserViewSet, GroupViewSet, OrganizationViewSet, SectorViewSet, ToolViewSet
router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'sectors', SectorViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'tools', ToolViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('allauth.urls')),
    path('', include('maps.urls')),
    path('surveys/', include('surveys.urls')),
]
urlpatterns += [
    path('api/', include(router.urls))
]
