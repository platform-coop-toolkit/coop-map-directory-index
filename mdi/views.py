from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import render, reverse
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import UserSerializer, GroupSerializer, OrganizationSerializer, SectorSerializer, ToolSerializer
from .models import Organization, Sector, Tool, License
from rest_framework.response import Response

def map(request):
  return HttpResponse("Where's ma maps?")

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'groups': reverse('group-list', request=request, format=format),
        'sectors': reverse('sectors-list', request=request, format=format),
        'organizations': reverse('organizations-list', request=request, format=format),
        'tools': reverse('tools-list', request=request, format=format),
    })


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows Users to be viewed.
  """
  queryset = get_user_model().objects.all().order_by('date_joined')
  serializer_class = UserSerializer
  http_method_names = ['get',]


class GroupViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows Groups to be viewed.
  """
  queryset = Group.objects.all()
  serializer_class = GroupSerializer
  http_method_names = ['get',]


class SectorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Sectors to be viewed.
    """
    queryset = Sector.objects.filter(name__regex=r'^[A-Z]')
    serializer_class = SectorSerializer
    http_method_names = ['get',]


class ToolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tools to be viewed.
    """
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    http_method_names = ['get',]


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Organizations to be viewed.
    """
    queryset = Organization.objects.all() # filter(geom__isnull=False)
    serializer_class  = OrganizationSerializer
    http_method_names = ['get',]
