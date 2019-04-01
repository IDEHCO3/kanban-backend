
from django.conf.urls import include,  url
from rest_framework.urlpatterns import format_suffix_patterns
from expression_interface import views
app_name = "expression_interface"
urlpatterns = (
    url(r'^$', views.APIRoot.as_view(), name='api_root'),
    url(r'^'+ views.SubBooleanOperatorResource.contextclassname +'/?$', views.SubBooleanOperatorResource.as_view(), name='sub_boolean_operator' ),
    url(r'^'+ views.LogicalOperatorResource.contextclassname +'/?$', views.LogicalOperatorResource.as_view(), name='logical_operator' )

)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'png', 'jsonld'])

