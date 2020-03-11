from django.urls import path, include
from .views import api_root, UserViewSet, GroupViewSet, OrganizationViewSet, SectorViewSet, ToolViewSet
from rest_framework.urlpatterns import format_suffix_patterns

user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    # 'post': 'create',
    # 'put': 'update',
    # 'delete': 'destroy'
})

group_list = GroupViewSet.as_view({
    'get': 'list'
})
group_detail = GroupViewSet.as_view({
    'get': 'retrieve',
    # 'post': 'create',
    # 'put': 'update',
    #'delete': 'destroy'
})

sector_list = SectorViewSet.as_view({
    'get': 'list'
})
sector_detail = SectorViewSet .as_view({
    'get': 'retrieve',
    # 'post': 'create',
    # 'put': 'update',
    # 'delete': 'destroy'
})


tool_list = ToolViewSet.as_view({
    'get': 'list'
})
tool_detail = ToolViewSet .as_view({
    'get': 'retrieve',
    # 'post': 'create',
    # 'put': 'update',
    # 'delete': 'destroy'
})

organization_list = OrganizationViewSet.as_view({
    'get': 'list'
})
organization_detail = OrganizationViewSet.as_view({
    'get': 'retrieve',
    # 'post': 'create',
    # 'put': 'update',
    # 'delete': 'destroy'
})

urlpatterns = [
    path('', api_root),
    path('users', user_list, name=user_list),
    path('user/<int:pk>/', user_detail, name=user_detail),
    path('groups', user_list, name=group_list),
    path('groups/<int:pk>/', user_detail, name=group_detail),
    path('sectors', sector_list, name=sector_list),
    path('sectors/<int:pk>/', sector_detail, name=sector_detail),
    path('organizations', organization_list, name=organization_list),
    path('organization/<int:pk>/', organization_detail, name=organization_detail),
    path('tools', tool_list, name=tool_list),
    path('tool/<int:pk>/', tool_detail, name=tool_detail),
]
# Login and logout views for the browsable API
urlpatterns += [
    path('api-auth/', include('rest_framework.urls',
namespace='rest_framework')),
]
