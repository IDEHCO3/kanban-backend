from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from user_management import views 

app_name = "user_management"

urlpatterns = format_suffix_patterns((
    url(r'^$', views.APIRoot.as_view(), name='api_root'),

    url(r'^api-resource-list/(?P<pk>[0-9]+)/$', views.APIResourceDetail.as_view(), name='APIResource_detail'),
    url(r'^api-resource-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.APIResourceDetail.as_view(), name='APIResource_detail_af'),
    url(r'^api-resource-list/$', views.APIResourceList.as_view(), name='APIResource_list'),
    url(r'^api-resource-list/(?P<attributes_functions>.*)/?$', views.APIResourceList.as_view(), name='APIResource_list_af'),

    url(r'^hyper-user-list/(?P<pk>[0-9]+)/$', views.HyperUserDetail.as_view(), name='HyperUser_detail'),
    url(r'^hyper-user-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.HyperUserDetail.as_view(), name='HyperUser_detail_af'),
    url(r'^hyper-user-list/$', views.HyperUserList.as_view(), name='HyperUser_list'),
    url(r'^hyper-user-list/(?P<attributes_functions>.*)/?$', views.HyperUserList.as_view(), name='HyperUser_list_af'),

    url(r'^hyper-user-group-list/(?P<pk>[0-9]+)/$', views.HyperUserGroupDetail.as_view(), name='HyperUserGroup_detail'),
    url(r'^hyper-user-group-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.HyperUserGroupDetail.as_view(), name='HyperUserGroup_detail_af'),
    url(r'^hyper-user-group-list/$', views.HyperUserGroupList.as_view(), name='HyperUserGroup_list'),
    url(r'^hyper-user-group-list/(?P<attributes_functions>.*)/?$', views.HyperUserGroupList.as_view(), name='HyperUserGroup_list_af'),

    url(r'^hyper-user-group-api-resource-list/(?P<pk>[0-9]+)/$', views.HyperUserGroupAPIResourceDetail.as_view(), name='HyperUserGroupAPIResource_detail'),
    url(r'^hyper-user-group-api-resource-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.HyperUserGroupAPIResourceDetail.as_view(), name='HyperUserGroupAPIResource_detail_af'),
    url(r'^hyper-user-group-api-resource-list/$', views.HyperUserGroupAPIResourceList.as_view(), name='HyperUserGroupAPIResource_list'),
    url(r'^hyper-user-group-api-resource-list/(?P<attributes_functions>.*)/?$', views.HyperUserGroupAPIResourceList.as_view(), name='HyperUserGroupAPIResource_list_af'),


))
