
from collections import OrderedDict

from rest_framework import status
from rest_framework.reverse import reverse

# Create your views here.
from rest_framework.views import APIView

from expression_interface.contexts import SubBooleanOperatorResourceContext, LogicalOperatorResourceContext
from hyper_resource.models import boolean_operator, logical_operator
from hyper_resource.contexts import EntryPointResourceContext
from hyper_resource.resources.EntryPointResource import NonSpatialEntryPointResource
from rest_framework.response import Response

from hyper_resource.resources.AbstractResource import AbstractResource

HTTP_IF_NONE_MATCH = 'HTTP_IF_NONE_MATCH'
HTTP_IF_MATCH = 'HTTP_IF_MATCH'
HTTP_IF_UNMODIFIED_SINCE = 'HTTP_IF_UNMODIFIED_SINCE'
HTTP_IF_MODIFIED_SINCE = 'HTTP_IF_MODIFIED_SINCE'
HTTP_ACCEPT = 'HTTP_ACCEPT'
CONTENT_TYPE = 'CONTENT_TYPE'
ETAG = 'Etag'
CONTENT_TYPE_GEOJSON = "application/vnd.geo+json"
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_LD_JSON = "application/ld+json"
CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
CONTENT_TYPE_IMAGE_PNG = "image/png"
SUPPORTED_CONTENT_TYPES = (CONTENT_TYPE_GEOJSON, CONTENT_TYPE_JSON,CONTENT_TYPE_LD_JSON, CONTENT_TYPE_OCTET_STREAM, CONTENT_TYPE_IMAGE_PNG)
ACCESS_CONTROL_ALLOW_METHODS = ['GET', 'OPTIONS', 'HEAD']

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-location',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'link',
)

CORS_EXPOSE_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-location',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-access-token',
    'access-control-allow-origin',
    'link',
]

ENABLE_COMPLEX_REQUESTS = True

GEOSGEOMETRY_SUBCLASSES = ['POINT', 'MULTIPOINT', 'LINESTRING', 'MULTILINESTRING', 'POLYGON', 'MULTIPOLYGON', 'GEOMETRYCOLLECTION']

class APIRoot(NonSpatialEntryPointResource):

    def get_root_response(self, request, format=None, *args, **kwargs):
        root_links = {
            'boolean-operators': reverse('expression_interface:sub_boolean_operator', request=request, format=format),
            'logical_operator': reverse('expression_interface:logical_operator', request=request, format=format),
        }
        ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
        return ordered_dict_of_link

class SubBooleanOperatorResource(AbstractResource):
    contextclassname = 'sub-boolean-operators'

    def initialize_context(self):
        self.context_resource = SubBooleanOperatorResourceContext()
        self.context_resource.resource = self

    def get(self, request, format=None, *args, **kwargs):
        dici = {}
        for oper_name in boolean_operator():
            dici[oper_name] = oper_name
        return Response(data=dici, content_type='application/json')


    def options(self, request, *args, **kwargs):
        response = super(SubBooleanOperatorResource, self).options( request, *args, **kwargs)
        #self.basic_get(request, *args, **kwargs)
        response.data = self.context_resource.context()
        response['content-type'] = 'application/ld+json'
        return response

    def supportedOperationsFor(object_model, resource_type):
        return []

class LogicalOperatorResource(AbstractResource):
    contextclassname = 'logical-operators'

    def initialize_context(self):
        self.context_resource = LogicalOperatorResourceContext()
        self.context_resource.resource = self

    def get(self, request, format=None, *args, **kwargs):
        dici = {}
        for oper_name in logical_operator():
            dici[oper_name] = oper_name
        return Response(data=dici, content_type='application/json')


    def options(self, request, *args, **kwargs):
        response = super(LogicalOperatorResource, self).options( request, *args, **kwargs)
        #self.basic_get(request, *args, **kwargs)
        response.data = self.context_resource.context()
        response['content-type'] = 'application/ld+json'
        return response

    def supportedOperationsFor(object_model, resource_type):
        return []