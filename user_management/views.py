from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from hyper_resource.contexts import EntryPointResourceContext
from hyper_resource.resources.EntryPointResource import NonSpatialEntryPointResource
from user_management.models import *
from user_management.serializers import *
from user_management.contexts import *

from hyper_resource.resources.CollectionResource import CollectionResource
from hyper_resource.resources.NonSpatialResource import NonSpatialResource

class APIRoot(NonSpatialEntryPointResource):

    def get_root_response(self, request, format=None, *args, **kwargs):
        root_links = {

          'api-resource-list': reverse('user_management:APIResource_list' , request=request, format=format),
          'hyper-user-list': reverse('user_management:HyperUser_list' , request=request, format=format),
          'hyper-user-group-list': reverse('user_management:HyperUserGroup_list' , request=request, format=format),
          'hyper-user-group-api-resource-list': reverse('user_management:HyperUserGroupAPIResource_list' , request=request, format=format),
        }

        ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
        return ordered_dict_of_link

    '''
    def __init__(self):
        super(APIRoot, self).__init__()
        self.base_context = BaseContext('api-root')

    def options(self, request, *args, **kwargs):
        context = self.base_context.getContextData(request)
        root_links = get_root_response(request)
        context.update(root_links)
        response = Response(context, status=status.HTTP_200_OK, content_type="application/ld+json")
        response = self.base_context.addContext(request, response)
        return response

    def get(self, request, format=None, *args, **kwargs):
        root_links = get_root_response(request)
        response = Response(root_links)
        return self.base_context.addContext(request, response)
    '''

class APIResourceList(CollectionResource):
    queryset = APIResource.objects.all()
    serializer_class = APIResourceSerializer
    contextclassname = 'api-resource-list'
    def initialize_context(self):
        self.context_resource = APIResourceListContext()
        self.context_resource.resource = self

class APIResourceDetail(NonSpatialResource):
    serializer_class = APIResourceSerializer
    contextclassname = 'api-resource-list'
    def initialize_context(self):
        self.context_resource = APIResourceDetailContext()
        self.context_resource.resource = self

class HyperUserList(CollectionResource):
    queryset = HyperUser.objects.all()
    serializer_class = HyperUserSerializer
    contextclassname = 'hyper-user-list'
    def initialize_context(self):
        self.context_resource = HyperUserListContext()
        self.context_resource.resource = self

class HyperUserDetail(NonSpatialResource):
    serializer_class = HyperUserSerializer
    contextclassname = 'hyper-user-list'
    def initialize_context(self):
        self.context_resource = HyperUserDetailContext()
        self.context_resource.resource = self

class HyperUserGroupList(CollectionResource):
    queryset = HyperUserGroup.objects.all()
    serializer_class = HyperUserGroupSerializer
    contextclassname = 'hyper-user-group-list'
    def initialize_context(self):
        self.context_resource = HyperUserGroupListContext()
        self.context_resource.resource = self

class HyperUserGroupDetail(NonSpatialResource):
    serializer_class = HyperUserGroupSerializer
    contextclassname = 'hyper-user-group-list'
    def initialize_context(self):
        self.context_resource = HyperUserGroupDetailContext()
        self.context_resource.resource = self

class HyperUserGroupAPIResourceList(CollectionResource):
    queryset = HyperUserGroupAPIResource.objects.all()
    serializer_class = HyperUserGroupAPIResourceSerializer
    contextclassname = 'hyper-user-group-api-resource-list'
    def initialize_context(self):
        self.context_resource = HyperUserGroupAPIResourceListContext()
        self.context_resource.resource = self

class HyperUserGroupAPIResourceDetail(NonSpatialResource):
    serializer_class = HyperUserGroupAPIResourceSerializer
    contextclassname = 'hyper-user-group-api-resource-list'
    def initialize_context(self):
        self.context_resource = HyperUserGroupAPIResourceDetailContext()
        self.context_resource.resource = self


class HyperUserRegister(CollectionResource):
    queryset = HyperUser.objects.all()
    serializer_class = HyperUserSerializer
    contextclassname = 'user-list'
    def initialize_context(self):
        self.context_resource = HyperUserContext()
        self.context_resource.resource = self

    def post(self, request, *args, **kwargs):
        #print(request)
        resp = super(HyperUserRegister, self).post(request, *args, **kwargs)
        resp['x-access-token'] = self.object_model.getToken()
        return resp

class HyperUserLogin(CollectionResource):
    queryset = HyperUser.objects.all()
    serializer_class = HyperUserSerializer
    contextclassname = 'user-list'
    def initialize_context(self):
        self.context_resource = HyperUserContext()
        self.context_resource.resource = self

    def post(self, request, *args, **kwargs):

        res = HyperUser.getOneOrNone(request.data['user_name'], request.data['password'])

        if res is None:
            res = Response(status=status.HTTP_401_UNAUTHORIZED, content_type='application/json')
            res['WWW-Authenticate'] = 'Bearer'
            return res
        response = Response(status=status.HTTP_201_CREATED, content_type='application/json')
        response['Content-Location'] = request.path + str(res.id) + '/'
        response['x-access-token'] = res.getToken()
        return response