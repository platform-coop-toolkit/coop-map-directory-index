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
from rest_framework import routers, permissions
from mdi.views import UserViewSet, GroupViewSet, OrganizationViewSet, SectorViewSet, ToolViewSet
router = routers.DefaultRouter()
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Platform Co-op API",
      default_version='v0.1.0',
      description="Platform Co-op API",
      terms_of_service="https://demo.directory.platform.coop/terms-of-service/",
      contact=openapi.Contact(email="info@platform.coop"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'sectors', SectorViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'tools', ToolViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),
    path('', include('maps.urls')),
    path('surveys/', include('surveys.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
urlpatterns += [
    path('api/', include(router.urls))
]
