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
  API endpoint that allows users to be viewed or edited.
  """
  queryset = get_user_model().objects.all().order_by('date_joined')
  serializer_class = UserSerializer
  http_method_names = ['get']


class GroupViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows group to be viewed or edited.
  """
  queryset = Group.objects.all()
  serializer_class = GroupSerializer
  http_method_names = ['get']


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    http_method_names = ['get']


class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    http_method_names = ['get']


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.filter(geom__isnull=False)
    serializer_class  = OrganizationSerializer
    http_method_names = ['get']
