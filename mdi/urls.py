from django.urls import path, include
from .views import api_root, UserViewSet, GroupViewSet, OrganizationViewSet, ActivityViewSet
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

activity_list = ActivityViewSet.as_view({
    'get': 'list'
})
activity_detail = ActivityViewSet .as_view({
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
    path('activities', activity_list, name=activity_list),
    path('activities/<int:pk>/', activity_detail, name=activity_detail),
    path('organizations', organization_list, name=organization_list),
    path('organization/<int:pk>/', organization_detail, name=organization_detail),
]
# Login and logout views for the browsable API
urlpatterns += [
    path('api-auth/', include('rest_framework.urls',
namespace='rest_framework')),
]
