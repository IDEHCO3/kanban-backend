# -*- coding: utf-8 -*-

# Create your views here.

'''
SECRET_KEY = '-&t&pd%%((qdof5m#=cp-=-3q+_+pjmu(ru_b%e+6u#ft!yb$$'

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
CONTENT_TYPE_IMAGE_TIFF = "image/tiff"
SUPPORTED_CONTENT_TYPES = (CONTENT_TYPE_GEOJSON, CONTENT_TYPE_JSON,CONTENT_TYPE_LD_JSON, CONTENT_TYPE_OCTET_STREAM, CONTENT_TYPE_IMAGE_PNG, CONTENT_TYPE_IMAGE_TIFF)
ACCESS_CONTROL_ALLOW_METHODS = ['GET', 'OPTIONS', 'HEAD', 'PUT', 'DELETE', 'POST']

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

if ENABLE_COMPLEX_REQUESTS:
    print ('***************************************************************************************************************************')
    print("** WARNING: Complex requests is enabled                                                                                  **")
    print("** Certify that your API isn't using the follow caracter(s) for especific purposes:                                      **")
    print("** '!' (exclamation point)                                                                                               **")
    print ('***************************************************************************************************************************')

class IgnoreClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        """
        Select the first parser in the `.parser_classes` list.
        """
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)
'''

'''
class AbstractResource(APIView):
    """
    AbstractResource is the main view class.
    All other views are subclasses of this,
    directly or indirectly
    """

    __metaclass__ = ABCMeta

    # store the serializer_class for this view
    serializer_class = None
    contextclassname= ''


    def __init__(self):
        super(AbstractResource, self).__init__()
        self.current_object_state = None
        self.object_model = None
        self.name_of_last_operation_executed = None
        self.context_resource = None
        self.initialize_context()
        self.iri_metadata = None
        self.operation_controller = BaseOperationController()
        self.token_need = self.token_is_need()
        self.e_tag = None
        self.temporary_content_type = None
        self.resource_type = None
        self.is_entry_point = False

    # indicates wich is the content negotiation class
    content_negotiation_class = IgnoreClientContentNegotiation

    def cache_enabled(self):
        return False

    def generate_e_tag(self, data):
        return str(hash(data))

    def set_etag_in_header(self, response, e_tag):
        if not response.streaming:
            response[ETAG] = e_tag
        return response

    #should be overrided
    def hashed_value(self, object):
        return hash(self.object)

    #should be overrided
    def inject_e_tag(self, etag=None):
        """
        If the 'object_model' attribute of this view is not None
        and the 'e_tag' attribute is None, this method attributes
        a Etag for the 'e_tag' attribute.
        If the 'object_model' is not None and the 'e_tag' is not None
        this method just append the received 'etag' to the 'e_tag' attribute
        of this view
        :param etag:
        :return:
        """

        # ATENTION: if self.object_model is None we can have a e_tag without a object_model
        if self.e_tag is None and self.object_model is not None:
            self.e_tag = self.hashed_value(self.object_model)
            return
        if etag is not None:
            self.e_tag += str(etag)
            return

    def jwt_algorithm(self):
        return 'HS256'

    def token_is_ok(self, a_token):
        try:
            payload = jwt.decode(a_token, SECRET_KEY, algorithm=self.jwt_algorithm())
            return True
        except jwt.InvalidTokenError:
            return False

    def token_is_need(self):
        return  False

    def token_is_http_or_https(self, token):
        return  token.lower() in ['http:', 'https:']

    def token_is_http(self, token):
        return 'http:' == token

    def token_is_https(self, token):
        return 'https:' == token

    def token_is_www(self, token):
        return True if token.find('www.') > -1 else False

    def token_is_http_or_https_or_www(self, token):
        return  self.token_is_http_or_https(token) or self.token_is_www(token)

    def is_end_of_term(self, term):
        return term in self.logical_operators()

    def logical_operators(self):
        return FactoryComplexQuery().logical_operators()

    def add_key_value_in_header(self, response, key, value ):
        response[key] = value

    def add_url_in_header(self, url, response, rel):
        link = ' <'+url+'>; rel=\"'+rel+'\" '
        if "Link" not in response:
            response['Link'] = link
        else:
            response['Link'] += "," + link
        return response

    def access_control_allow_origin_str(self):
        return '*'

    def access_control_allow_methods_str(self):
        allow_methods_str = ''
        for header_value in ACCESS_CONTROL_ALLOW_METHODS:
            allow_methods_str += header_value + ', '
        return allow_methods_str[:-2]

    def access_control_allow_headers_str(self):
        allow_headers_str = ''
        for header_value in CORS_ALLOW_HEADERS:
            allow_headers_str += header_value + ', '
        return allow_headers_str[:-2]

    def access_control_expose_headers_str(self):
        expose_headers_str = ''
        for header_value in CORS_EXPOSE_HEADERS:
            expose_headers_str += header_value + ', '
        return expose_headers_str[:-2]

    def add_cors_header_in_header(self, response):
        response['access-control-allow-origin'] = self.access_control_allow_origin_str()
        response['access-control-allow-methods'] = self.access_control_allow_methods_str()
        response['access-control-allow-headers'] = self.access_control_allow_headers_str()
        response['access-control-expose-headers'] = self.access_control_expose_headers_str()


    def add_base_headers(self, request, response):
        """
        Adds the 'Link' header in the Response object containing
        a url representing the father url for this request and
        a url representing a context for the requested resource
        :param request:
        :param response:
        :return:
        """
        iri_base = request.build_absolute_uri() # the absolute iri for this request
        if self.contextclassname not in iri_base: # if the context class name isn't in the absolute iri ...
            return; #...  do nothing
        idx = iri_base.index(self.contextclassname)
        # gets the absolute iri from the begin until the context class name
        iri_father = iri_base[:idx]
        # adds 'Link' header in the Response object,
        # relating the father iri from this request with a 'up' relationship
        self.add_url_in_header(iri_father,response, 'up')
        # the second url appended to 'Link' header is the absolute url minus the bar
        # with '.jsonld', the 'rel' is the relationship represented by w3.org url
        self.add_url_in_header(iri_base[:-1] + '.jsonld',response, rel='http://www.w3.org/ns/json-ld#context"; type="application/ld+json')
        self.add_cors_header_in_header(response)
        if self.is_entry_point:
            self.add_url_in_header(iri_base,response, rel='http://schema.org/EntryPoint')

    def dispatch(self, request, *args, **kwargs):
        """
        If the request needs authentication this method
        verifies the authenticity of token (passed through HTTP_AUTHORIZATION header)
        and pass the request forward if everything is ok or send a 401 (unauthorized)
        response otherwise. If the request don't need authentication we simply pass the
        request forward
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        if self.token_is_need():
            http_auth = 'HTTP_AUTHORIZATION'

            # the HTTP_AUTHORIZATION header, if this exists in the request, needs to starts with 'Bearer'
            if http_auth in request.META and request.META[http_auth].startswith('Bearer'):
                # get the HTTP_AUTHORIZATION header value (without 'Bearer' and edge whitespaces)
                a_token = request.META['HTTP_AUTHORIZATION'][7:].strip()
                if self.token_is_ok(a_token):
                    # if token is valid, pass the request forward for APIView dispatch method
                    return super(AbstractResource, self).dispatch(request, *args, **kwargs)

            # if HTTP_AUTHORIZATION header does'nt exists or not starts with 'Bearer',
            # a response saing 'token is need' is returned with a 401 (unauthorized) code
            resp = HttpResponse(json.dumps({"token": "token is needed or it is not ok"}), status=401,  content_type=CONTENT_TYPE_JSON)
            # plus a WWW-Authenticate header is send informing how to access the resource
            resp['WWW-Authenticate'] = 'Bearer realm="Access to the staging site"'
            return resp
        else:
            # if token isn't needed, just call the superclsse dispath method
            return  super(AbstractResource, self).dispatch(request, *args, **kwargs)

    #@abstractmethod #Could be override
    def initialize_context(self):
        context_module_name = self.__class__.__module__.split('.')[0] + '.contexts'
        context_module = importlib.import_module(context_module_name)
        context_class_name = self.__class__.__name__ + 'Context'
        context_class = getattr(context_module, context_class_name )
        self.context_resource = context_class()
        self.context_resource.resource = self

    def required_context_for_simple_path(self, request):
        resource_type = self.resource_type_or_default_resource_type(request)
        return RequiredObject(self.context_resource.context(resource_type), CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_only_attributes(self, request, attributes_functions_str):
        context = self.get_context_by_only_attributes(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_operation(self, request, attributes_functions_str):
        if self.get_operation_name_from_path(attributes_functions_str) is None:
            return RequiredObject(
                representation_object={"This request has invalid attribute or operation: ": attributes_functions_str},
                content_type=CONTENT_TYPE_JSON, origin_object=self, status_code=400)

        context = self.get_context_for_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def get_context_by_only_attributes(self, request, attributes_functions_str):
        attrs_list = self.remove_last_slash(attributes_functions_str).split(",")
        if len(attrs_list) > 1:
            self._set_context_to_attributes(attrs_list)
        else:
            self._set_context_to_only_one_attribute(attrs_list[0])

        context = self.context_resource.dict_context
        return context

    def get_context_for_operation(self, request, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        self.context_resource.set_context_to_operation(self.object_model, operation_name)
        context = self.context_resource.dict_context
        resource_type = self.define_resource_type_by_operation(request, operation_name)
        self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)
        context['hydra:supportedOperations'] = self.context_resource.supportedOperationsFor(self.object_model, resource_type)

        return context

    # todo
    def path_request_is_ok(self, a_path):
        return True

    def operations_with_parameters_type(self):
        dic = self.object_model.operations_with_parameters_type()
        return dic

    def model_class(self):
        return self.serializer_class.Meta.model #return self.object_model.model_class()

    def model_class_name(self):
        return self.model_class().__name__

    def table_name(self):
        return self.model_class().objects.model._meta.db_table

    def pk_name(self):
        return self.model_class().objects.model._meta.pk.name

    def attribute_names_to_web(self):
        return [field.name for field in self.object_model.fields()]
        #return self.serializer_class.Meta.fields

    def field_for(self, attribute_name):
        fields_model = self.object_model.fields()
        for field in fields_model:
            if field.name == attribute_name:
                return field
        return None

    def fields_to_web_for_attribute_names(self, attribute_names):
        fields_model = self.object_model.fields()
        return [field for field in fields_model if field.name in attribute_names ]

    def fields_to_web(self):
        return self.fields_to_web_for_attribute_names(self.attribute_names_to_web())

    def _base_path(self, full_path):
        arr = full_path.split('/')
        ind = arr.index(self.contextclassname)
        return '/'.join(arr[:ind+1])

    def _set_context_to_attributes(self, attribute_name_array):
        self.context_resource.set_context_to_attributes(attribute_name_array)

    def _set_context_to_only_one_attribute(self, attribute_name):
        attribute_type = self.field_for(attribute_name)
        self.context_resource.set_context_to_only_one_attribute(self.current_object_state, attribute_name, attribute_type)

    def _set_context_to_operation(self, operation_name):
        self.context_resource.set_context_to_operation(self.current_object_state, operation_name)

    def set_basic_context_resource(self, request ):
        self.context_resource.host = request.META['HTTP_HOST']
        self.context_resource.basic_path = self._base_path(request.META['PATH_INFO'])
        if len(self.kwargs.values()):
            self.context_resource.complement_path = list(self.kwargs.values())[0]
        else:
            self.context_resource.complement_path = ''

    def key_is_identifier(self, key):
        return key in self.serializer_class.Meta.identifiers

    def dic_with_only_identitier_field(self, dict_params):
        dic = dict_params.copy()
        a_dict = {}
        for key, value in dic.items():
            if self.key_is_identifier(key):
                a_dict[key] = value

        return a_dict

    """
    def get_object(self, arr_of_term=[]):
        first_term = arr_of_term[0]
        if self.is_attribute(self, first_term):
            self.current_object_state =  getattr(self.object_model, first_term, None)
            arr_of_term = arr_of_term[1:]

        for term in arr_of_term:
            self.current_object_state = getattr(self.current_object_state, term, None)
        return  self.current_object_state
    """
    def attributes_functions_name_template(self):
        return 'attributes_functions'

    def get_object(self, a_dict):
        """
        Receives a_dict, get only the identifier fields
        and use them to query the instaces in the database
        that matches with the identifiers dict
        :param a_dict:
        :return:
        """
        dicti = self.dic_with_only_identitier_field(a_dict)
        #queryset = self.model_class().objects.all()
        #obj = get_object_or_404(queryset, **dicti)
        obj = get_object_or_404(self.model_class(), **dicti)
        #self.check_object_permissions(self.request, obj)
        return obj

    def serialized_data(self, request, object_or_list_of_object, is_many):
        return self.serializer_class(object_or_list_of_object, many=is_many, context={'request': request}).data

    def default_content_type(self):
        return CONTENT_TYPE_JSON

    def default_resource_type(self):
        return 'Thing'

    # must be overrided
    def define_resource_type(self, request, attributes_functions_str):
        pass

    # must be overrided
    def define_resource_type_by_only_attributes(self, request, attributes_functions_str):
        pass

    # must be overrided
    def define_resource_type_by_operation(self, request, operation_name):
        pass

    def content_type_or_default_content_type(self, requestOrNone):
        if requestOrNone is None:
            return self.default_content_type()

        a_content_type = requestOrNone.META.get(HTTP_ACCEPT, '')
        if a_content_type not in SUPPORTED_CONTENT_TYPES:
            return self.default_content_type()
        return a_content_type

    def dict_by_accept_resource_type(self):
        dict = {}
        dict[CONTENT_TYPE_OCTET_STREAM] = bytes
        return dict

    def resource_type_for_accept_header(self, accept):
        return self.dict_by_accept_resource_type()[accept] if accept in self.dict_by_accept_resource_type() else None

    def resource_type_or_default_resource_type(self, requestOrNone):
        if requestOrNone is None:
            return self.default_resource_type()

        accept = requestOrNone.META.get(HTTP_ACCEPT, '')
        if accept not in SUPPORTED_CONTENT_TYPES:
            return self.default_resource_type()
        return self.resource_type_for_accept_header(accept)

    #todo
    def basic_response(self, request, serialized_object, status, content_type):
        return Response(data=serialized_object, status=status, content_type=content_type)

    #Answer if a client's etag is equal server's etag
    def conditional_etag_match(self, request):
        """
        Return True if Request If-None-Match header value matches with the Etag cached value.
        If the generated request key is not in the cache key set or if Request If-None-Match header
        value not matches with the Etag cache value, return False
        :param request:
        :return:
        """
        # mounts a key based on Request Accept header or default Content-Type
        key = self.get_key_cache(request)
        # the cache stores a tuple of Etag and the serialized data
        tuple_etag_serialized_data = cache.get(key)
        # if typle_etag_serialized_data is None, this means that the key not correspond none of the cache keys
        # hence the resource isn't in cache
        if tuple_etag_serialized_data is None:
            return False
        # compare the Request If-None-Match header value with the Etag value of the cache
        return tuple_etag_serialized_data[0] == request.META.get(HTTP_IF_NONE_MATCH, '')

    #Answer if a get(request) is conditional
    def is_conditional_get(self, request):
        return request.META.get(HTTP_IF_NONE_MATCH, None) is not None or \
               request.META.get(HTTP_IF_UNMODIFIED_SINCE,  None) is not None

    #Should be overrided
    # Answer a formatted string(iri + accept) which is a key to retrieve an object in the cache
    def get_key_cache(self, request, a_content_type=None):
        """
        Mounts a cache key based on the request. If a_content_type is defined
        the key returned is the absolute uri + a_content_type. Otherwise, the
        key will be the absolute_uri + the content-type returned by
        AbstractResource.content_type_or_default_content_type()
        :param request:
        :param a_content_type:
        :return:
        """
        if a_content_type is not None:
            return self.request.build_absolute_uri() + a_content_type
        return self.request.build_absolute_uri() + self.content_type_or_default_content_type(request)

    def set_key_with_data_in_cache(self, key, etag, data, seconds=3600):
        """
        Sets 'etag' and 'data' in cache as a tuple indexed by 'key'.
        If 'key' already corresponds a cache key, nothing is done.
        :param key:
        :param etag:
        :param data:
        :param seconds:
        :return:
        """
        if isinstance(data, memoryview) or not self.cache_enabled():
            return
        if cache.get(key) is None:
            cache.set(key,(etag, data), 3600)

    def resource_in_cache_or_None(self, request):
        """
        Return the cached resource if the generated request key
        (generated through AbstractResource.get_key_cache()) and the
        If-None-Match header value matches with the cache key and cached
        etag respectivitly. Return False otherwise
        :param request:
        :return:
        """
        if not self.cache_enabled():
            return

        key = self.get_key_cache(request)
        return cache.get(key)

    def is_image_content_type(self, request, **kwargs):
        return self.content_type_or_default_content_type(request) == CONTENT_TYPE_IMAGE_PNG or kwargs.get('format', None) == "png"

    def accept_is_binary(self, request):
        return request.META.get(HTTP_ACCEPT, '') == CONTENT_TYPE_OCTET_STREAM

    # Should be overrided
    def is_binary_content_type(self,required_object ):
        return required_object.content_type == CONTENT_TYPE_OCTET_STREAM

    # Should be overrided
    def response_base_get_binary(self, request, required_object):
        # 'key' will be absolute uri + application/octet-stream
        key = self.get_key_cache(request, CONTENT_TYPE_OCTET_STREAM)
        if isinstance(required_object.representation_object, dict) and 'type' in required_object.representation_object:
            # if representation object is a dict is an GeoJson
            # geobuf minimize the response size
            result = geobuf.encode(required_object.representation_object) # GeoJSON or TopoJSON -> Geobuf string
        else:
            result = str(required_object.representation_object).encode()

        if isinstance(result, dict):
            value_to_e_tag = json.dumps(result)
        else:
            value_to_e_tag =  result
        e_tag = self.generate_e_tag(value_to_e_tag)
        self.set_key_with_data_in_cache(key, e_tag, result)
        resp = HttpResponse(result, content_type=CONTENT_TYPE_OCTET_STREAM)
        self.set_etag_in_header(resp, e_tag)
        return resp

    # todo: verify image responses processment
    #Should be overrided
    def response_base_get_with_image(self, request, required_object):
        # 'queryset' is the requested resource without serialization
        queryset = required_object.origin_object

        image = self.get_png(queryset, request)
        required_object.representation_object = image
        key = self.get_key_cache(request, CONTENT_TYPE_IMAGE_PNG)
        e_tag = self.generate_e_tag(image)
        self.set_key_with_data_in_cache(key,e_tag, image)
        resp = HttpResponse(image, content_type=CONTENT_TYPE_IMAGE_PNG)
        self.set_etag_in_header(resp, e_tag)
        return resp

    #Should be overrided
    def response_base_object_in_cache(self, request ):
        """
        Returns a cached Response (if this is in cache)
        defining wich Content-Type the response has
        :param request:
        :return:
        """
        # AbstractResource.resource_in_cache_or_None return de cached data
        # if the mounted key based on Accept Request header matches one of the cached keys
        tuple_etag_serialized_data = self.resource_in_cache_or_None(request)
        if tuple_etag_serialized_data is not None:
            if request.META[HTTP_ACCEPT] in [CONTENT_TYPE_IMAGE_PNG, CONTENT_TYPE_OCTET_STREAM]:
                # if Accept Request header value is application/octet-stream or image/png
                # the Response Content-Type will be the same value
                resp = HttpResponse(tuple_etag_serialized_data[1], content_type=request.META[HTTP_ACCEPT])
            else:
                # if Accept Request header value isn't application/octet-stream nor image/png
                # the Content-Type will be the Accept value or the default Content-Type
                resp = Response(data=tuple_etag_serialized_data[1],status=200, content_type=self.content_type_or_default_content_type(request))

            # set etag in Response header
            self.set_etag_in_header(resp, tuple_etag_serialized_data[0])
            return resp

    #Should be overrided
    def response_base_get(self, request, *args, **kwargs):
        """
        Returns a Response for the Request. If the response is in cache

        """

        # AbstractResource.resource_in_cache_or_None() returns the requested resource from cache
        # if the key formed by absolute uri + accept or absolute uri + default Content-Type
        # matches one of the cache keys. Returns None othewise
        resource = self.resource_in_cache_or_None(request)
        if resource is not None:
            # returns a response from the cache
            return self.response_base_object_in_cache(request )

        # if the resource is not in cache, use the subclass basic_get() that returns a RequiredObject instance
        required_object = self.basic_get(request, *args, **kwargs)
        # if Required object has some error, return this
        status = required_object.status_code
        if status in [400,401,404]:
            return Response(required_object.representation_object, status=status)
        if status in [500]:
            return Response({'Error ': 'The server can not process this request. Status:' + str(status)}, status=status)

        # todo: verify image responses processment
        if self.is_image_content_type(request, **kwargs):
            return self.response_base_get_with_image(request, required_object)

        # if RequiredObject has application/octect-stream Content-Type
        # the Response is a geobuf (smaller than a regular JSON)
        if self.is_binary_content_type(required_object):
            return self.response_base_get_binary(request, required_object)

        # mounts a cache key with RequiredObject.content_type
        key = self.get_key_cache(request, a_content_type=required_object.content_type)
        # sets the e_tag and data in cache binding to the key
        self.set_key_with_data_in_cache(key, self.e_tag, required_object.representation_object )

        # return the Response with the requested resource representation and Etag header
        resp =  Response(data=required_object.representation_object,status=200, content_type=required_object.content_type)
        self.set_etag_in_header(resp, self.e_tag)
        return resp

    #Should be overrided
    def response_conditional_get(self, request, *args, **kwargs):
        """
        Return a 304 Response, if If-None-Math header matches with
        the cached Etag, or a regular Response otherwise
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 'a_content_type' is the Accept Request header of a default Content-Type
        a_content_type = self.content_type_or_default_content_type(request)
        # verify if the Request If-None-Match header match with cached Etag
        if self.conditional_etag_match(request):
            # if matches, a 304 (Not modified) Response is returnes
            return Response(data={},status=304, content_type=a_content_type)
        # if not matches return a regular Response (with database requests)
        return self.response_base_get(request, *args, **kwargs)

    #If client request .png  into IRI chance header's accept to image/png and removes .png fron IRI. Affordance for user.
    def change_request_if_image_png_into_IRI(self, request):
        if 'attributes_functions' in self.kwargs and self.kwargs['attributes_functions'][-4:] == '.png':
            self.kwargs['attributes_functions'] = self.kwargs['attributes_functions'][:-4]
            request.META[HTTP_ACCEPT] = 'image/png'

    #Could be overrided
    def get(self, request, *args, **kwargs):
        """
        Receive the request and decide if this will be a regular response
        or a cached response
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if 'HTTP_ETAG' in request.META:
            etag = request.META['HTTP_ETAG']

        #return super(AbstractResource, self).get(request, *args, **kwargs)
        resp = None
        # responds with a conditional get if the request has If-None-Match or If-Unmodified-Since header
        if self.is_conditional_get(request):
           resp = self.response_conditional_get(request, *args, **kwargs)
        else:
        # otherwise responds with a regular get (can be responsed with cached data)
        # QUESTION: AbstractResource.response_base_get() must consider cache check?
        # After all, if AbstractResouce.is_conditional_get() return False this means that the Request hasn't
        # If-None-Match or If-Unmodified-Since headers
           resp = self.response_base_get(request, *args, **kwargs)

        # add the Link header in Response
        self.add_base_headers(request, resp)

        return resp

    # Could be overrided
    def patch(self, request, *args, **kwargs):
        return super(AbstractResource, self).patch(request, *args, **kwargs)

    # Could be overrided
    def head(self, request, *args, **kwargs):
        resp =  Response(data={}, status=status.HTTP_200_OK, content_type=self.content_type_or_default_content_type(request))
        self.add_base_headers(request, resp)
        return resp

    # Could be overrided
    def put(self, request, *args, **kwargs):
        obj = self.get_object(kwargs)
        # get the PUT request body and compares to the database resouce to determines if the request body is valid or not
        serializer = self.serializer_class(obj, data=request.data, context={'request': request})
        if serializer.is_valid():
            # if the request data is valid, alter the database resouce and returns a 204 response
            serializer.save()
            resp =  Response(status=status.HTTP_204_NO_CONTENT)
            return resp
        # if request data isn't valid, return a 400 response status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Could be overrided
    def delete(self, request, *args, **kwargs):
        obj = self.get_object(kwargs)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def options(self, request, *args, **kwargs):
        response = super(AbstractResource, self).options( request, *args, **kwargs)
        self.add_base_headers(request, response)
        return response

    def operation_names_model(self):
        return self.object_model.operation_names()

    def attribute_names_model(self):
        return self.object_model.attribute_names()

    def is_private(self, attribute_or_method_name):
        return attribute_or_method_name.startswith('__') and attribute_or_method_name.endswith('__')

    def is_not_private(self, attribute_or_method_name):
        return not self.is_private(attribute_or_method_name)

    def is_operation(self, operation_name):
        return operation_name in self.operation_names_model()

    def is_attribute(self, attribute_name):
        return self.object_model.is_attribute(attribute_name)

    def is_spatial_attribute(self, attribute_name):
        return False

    def _has_method(self,  method_name):
        return method_name in self.operation_names_model()

    def is_simple_path(self, attributes_functions_str):
        return attributes_functions_str is None or len(attributes_functions_str) == 0

    def path_has_operations(self, attributes_functions_name):

        attrs_functs = self.remove_last_slash(attributes_functions_name).split('/')

        operations = self.operation_names_model()

        for att_func in attrs_functs:
            oper_name = att_func[1:] if '*' in att_func else att_func
            if  oper_name in operations:
                return True
        return False

    def path_has_only_attributes(self, attributes_functions_name):
        attrs_functs = self.remove_last_slash(attributes_functions_name).split('/')

        if len(attrs_functs) > 1:
            return False

        if ',' in attrs_functs[0]:
            return True

        if self._has_method(attrs_functs[0]):
            return False

        return self.object_model.is_attribute(attrs_functs[0])

    def is_complex_request(self, request):
        absolute_uri = request.scheme + '://' + request.get_host() + request.path
        compx_req_marker_idx = absolute_uri.find('!')
        if compx_req_marker_idx == -1 or absolute_uri.count('!') != 1:
            return False
        else:
            uri_after_marker = absolute_uri[compx_req_marker_idx:]
            operation_name = uri_after_marker[1:uri_after_marker.index('/')]
            return operation_name in self.operation_controller.dict_all_operation_dict()

    def transform_path_with_url_as_array(self, arr_of_term):
        """
        Receive url parameters (arr_of_term) each parameter as a array element.
        If there is some url inside this array (any element 'www.' or 'http:' or 'https:'),
        each element of this array references to this url is merged in a single element.
        :param arr_of_term - url parameters:
        :return:
        """
        arr = []
        http_str = ''
        # remove empty strings from list
        arr_term =  [ele for ele in arr_of_term if ele != '']
        found_url = False
        # storing the number of elements of the list
        size_of_term = len(arr_term)
        for idx, token in enumerate(arr_term): # token is each url parameter
            # if 'token' is 'https', 'http' or has 'www.', 'found_url' turns True
            if self.token_is_http_or_https_or_www(token.lower()):
                found_url = True
            if found_url:
                if self.token_is_http_or_https(token):
                    # if token is 'http' or 'https', append it to 'http_str' with '//'
                    http_str += token + '//'
                elif self.is_end_of_term(token):
                    # if 'token' is a logical operator (or, and, *or, *and), 'found_url' turns False
                    found_url = False
                    # append 'http_str' (may be a empty string or 'http//' or 'https//') and 'token' to 'arr'
                    arr.append(http_str)
                    arr.append(token)
                    # 'http_str' turn a empty string
                    http_str = ''
                elif (idx == size_of_term -1):
                    # if the current index represents the penultimate element
                    # of the array of terms, 'found_url' turns False
                    found_url = False
                    # so, we concatenate 'token' to '/' and append to 'arr'. 'http_str' turns a empty string again
                    http_str+= token + '/'
                    arr.append(http_str)
                    http_str = ''
                else:
                    # if 'token' isn't 'http:', 'https:', a logical operator nor the penultimate element of list
                    # we just concatenate 'token' with '/' and then concatenate with 'http_str'
                    http_str += token + '/'
            else:
                # if token, in this iteration, hasn't 'http', 'https' nor 'www.', just append token to 'arr'
                arr.append(token)
        return arr


    def dict_as_geojson(self, a_dict):
        d = {}
        d["type"] = "Feature"
        d["geometry"] = a_dict[self.geometry_field_name()]
        a_dict.pop(self.geometry_field_name(), None)
        d["properties"] = a_dict
        return d


    def attributes_functions_splitted_by_url(self, attributes_functions_str_url):
        res = attributes_functions_str_url.lower().find('http:')
        if res == -1:
            res = attributes_functions_str_url.lower().find('https:')
            if res == -1:
                res = attributes_functions_str_url.lower().find('www.')
                if res == -1:
                    return [attributes_functions_str_url]

        if '/*' in attributes_functions_str_url:
            param_inx = attributes_functions_str_url.index('/*')
            param = attributes_functions_str_url[param_inx+2:]
            return [attributes_functions_str_url[0:res], attributes_functions_str_url[res:param_inx], param]

        return [attributes_functions_str_url[0:res], attributes_functions_str_url[res:], None]

    def path_has_url(self, attributes_functions_str_url):
        return (attributes_functions_str_url.find('http:') > -1) or (attributes_functions_str_url.find('https:') > -1)\
               or (attributes_functions_str_url.find('www.') > -1)

    def get_url_arr_from_arr_of_tuples(self, arr_of_tuples):
        url_as_arr = []
        for url_tuple in arr_of_tuples:
            url_arr = list(url_tuple)
            url = [self.remove_last_slash(url) for url in url_arr if url != ''][0]
            url_as_arr.append(url)
        return url_as_arr

    def remove_last_slash(self, url_as_str):
        url = url_as_str.strip()
        url = url[:-1] if url[-1] == '*' else url
        return url[:-1] if url[-1] == '/' else url

    def attribute_functions_str_with_url_splitted_by_slash(self, attributes_functions_str_url):
        att_functions_str_url = attributes_functions_str_url
        #exp = r"(?=https{0,1}:.+?\*)https{0,1}:.+?\*"
        exp = r'(?=https{0,1}:.+?\*)(https{0,1}:.+?\*)|(https{0,1}:.+?\/?$)'
        #exp = r'(?=https{0,1}:.+?\*)https{0,1}:.+?[*]|[/]$'
        url_as_arr_of_tuples = re.findall(exp, att_functions_str_url, re.IGNORECASE)

        url_as_arr = self.get_url_arr_from_arr_of_tuples(url_as_arr_of_tuples)
        #url_as_arr = [self.remove_last_slash(url_tuple[0]) for url_tuple in url_as_arr_of_tuple]

        token = '_*+_TOKEN__$URL-#_Num:'
        for index, url_str in enumerate(url_as_arr):
            att_functions_str_url = att_functions_str_url.replace(url_str, token + str(index), 1)# + '/*', 1)
        att_functions_str_url_as_array = att_functions_str_url.split('/')
        for idx, url_str in enumerate(url_as_arr):
            att_functions_str_url_as_array[att_functions_str_url_as_array.index(token + str(idx))] = url_str if url_str[-1] not in ['*', '/'] else url_str[:-1]

        return att_functions_str_url_as_array if att_functions_str_url_as_array[-1] != '*' else att_functions_str_url_as_array[:-1]

    def attribute_functions_str_splitted_by_slash(self, attributes_functions_str_url):

        att_functions_str_url = att_functions_str_url = self.remove_last_slash(attributes_functions_str_url)
        if self.path_has_url(att_functions_str_url):
             return self.attribute_functions_str_with_url_splitted_by_slash(att_functions_str_url)
        else:
           return att_functions_str_url.split('/')

    def _execute_attribute_or_method(self, object, attribute_or_method_name, array_of_attribute_or_method_name):
        dic = {}
        parameters = []
        if self.operation_controller.is_operation(object, attribute_or_method_name):
            if self.operation_controller.operation_has_parameters(object, attribute_or_method_name):

                parameters = array_of_attribute_or_method_name[0].split('&') if len(array_of_attribute_or_method_name) > 0 else []
                array_of_attribute_or_method_name = array_of_attribute_or_method_name[1:]

        obj = self._value_from_object(object, attribute_or_method_name, parameters)

        if len(array_of_attribute_or_method_name) == 0:
            return obj

        return self._execute_attribute_or_method(obj, array_of_attribute_or_method_name[0], array_of_attribute_or_method_name[1:])

    def array_of_operation_name(self):
        collection_operations_array = list(self.operation_controller.dict_all_operation_dict().keys())
        return collection_operations_array

    def get_operation_name_from_path(self, attributes_functions_str):
        attributes_functions_str = attributes_functions_str.lower()
        arr_att_funcs = self.remove_last_slash(attributes_functions_str).split('/')
        first_part_name = arr_att_funcs[0]
        if first_part_name not in self.array_of_operation_name():
            return None
        return first_part_name

    def is_operation_and_has_parameters(self, attribute_or_method_name):
        dic = self.operations_with_parameters_type()
        return (attribute_or_method_name in dic) and len(dic[attribute_or_method_name].parameters)

    # method without use
    def function_name(self, attributes_functions_str):
        functions_dic = self.operations_with_parameters_type()
        if str(attributes_functions_str[-1]) in functions_dic:
            return str(attributes_functions_str[-1])
        return str(attributes_functions_str[-2])

    def response_resquest_with_attributes(self,  attributes_functions_name):
        """
        Return a response to the requested resource containing
        only the requested attributes/methods values (not the entire resource)
        :param attributes_functions_name - the attributes from the request resource:
        :return:
        """
        a_dict = {}
        # transform the parameters (separated by ',') in a list of arguments
        attributes = attributes_functions_name.strip().split(',')
        #self.current_object = self.object_model
        for attr_name in attributes:
            # gets the attribute value from the object model of this resource and stores in 'obj'
            # notice: we consider that 'attr_name' represents a attribute of object model or
            # a method without parameters ([])
            obj = self._value_from_object(self.object_model, attr_name, [])
            # sets 'a_dict' (the response data) with the name of the attribute/method as the index
            # and 'obj' as his respective value
            a_dict[attr_name] = obj

        # 'a_dict' turns the AbstractResource.current_object_state
        self.current_object_state = a_dict

        # return 'a_dict' as response body, application/json as Content-Type and 200 as response status code
        return (a_dict, CONTENT_TYPE_JSON, self.object_model, {'status': 200})

    def all_parameters_converted(self, attribute_or_function_name, parameters):
        parameters_converted = []
        if self.is_operation_and_has_parameters(attribute_or_function_name):

            parameters_type = self.operations_with_parameters_type()[attribute_or_function_name].parameters
            for i in range(0, len(parameters)):

                if parameters_type[i] == GEOSGeometry:
                    ct = ConverterType()
                    if ct.path_is_feature_collection(parameters[i]):
                        param_converted = ct.make_geometrycollection_from_featurecollection(json.loads(parameters[i]))
                    else: # if parameters[i] is GeometryCollection (GeoJson) or WKT ...
                        param_converted = parameters_type[i](parameters[i])
                    parameters_converted.append(param_converted)

                else:
                    parameters_converted.append(parameters_type[i](parameters[i]))

            return parameters_converted
        return self.parametersConverted(parameters)

    def is_attribute_for(self, object, attribute_or_function_name):
        return  hasattr(object, attribute_or_function_name) and not callable(getattr(object, attribute_or_function_name))

    def _value_from_object(self, object, attribute_or_function_name, parameters):
        attribute_or_function_name_striped = attribute_or_function_name.strip()
        self.name_of_last_operation_executed = attribute_or_function_name_striped

        if self.is_attribute_for(object, attribute_or_function_name):
            return getattr(object, attribute_or_function_name_striped)

        if len(parameters)> 0:

            if (isinstance(object, BusinessModel) or isinstance(object, GEOSGeometry)):
                params = self.all_parameters_converted(attribute_or_function_name_striped, parameters)
            else:
                params = ConverterType().convert_parameters(type(object), attribute_or_function_name, parameters)

            return getattr(object, attribute_or_function_name_striped)(*params)

        return getattr(object, attribute_or_function_name_striped)()

    def parametersConverted(self, params_as_array):
        """
        Convert each string in 'params_as_array' to one of this type:
        bool, int, float, GEOSGeometry or if the string is an url, try to
        request this url and convert the response data to GEOSGeometry.
        If the request fails or return a status code representing a error,
        raise ConnectionError or HTTPError
        :param params_as_array - a array of strings (probably pieces from url):
        :return:
        """
        paramsConveted = []

        for value in params_as_array:

            # if the parameter is 'true' or 'false'
            # convert it to bool and append to list
            if value.lower() == 'true':
                paramsConveted.append(True)
                continue
            elif value.lower() == 'false':
                paramsConveted.append(False)
                continue

            # if parameter is not 'true' nor 'false'
            # we try to convert to int, if it fails,
            # we try to convert to float, if it still fails,
            # we tru to convert to GEOSGeometry
            try:
                paramsConveted.append(int( value ) )
                continue
            except ValueError:
                pass
            try:
               paramsConveted.append( float( value ) )
               continue
            except ValueError:
                pass
            try:
               paramsConveted.append( GEOSGeometry( value ) )
               continue
            except ValueError:
                pass
            try:
                # if the parameter starts with 'http', we make a request to this parameter
                http_str = (value[0:4]).lower()
                if (http_str == 'http'):
                    resp = requests.get(value)
                    # if this request return a response status between 400 and 599, we raise a HttpError
                    if 400 <= resp.status_code <= 599:
                        raise HTTPError({resp.status_code: resp.reason})

                    # if the request not return an error status, we get the response body in JSON format
                    js = resp.json()

                    # if 'type' is 'feature' or 'featurecollection' it has an 'geometry'
                    if (js.get("type") and js["type"].lower() in ['feature', 'featurecollection']):
                        # in this case, we get the geometric data from this JSON response
                        a_geom = js["geometry"]
                    else:
                        # otherwise, we simply get the entire dict
                        a_geom = js
                    # finally, we convert 'a_geom' to json and then convert the result to GEOSGeometry
                    # appending this to paramsConvertd list. OBS: you must notice that we consider that
                    # the request from the parameter will bring us a geometric resource
                    paramsConveted.append(GEOSGeometry((json.dumps(a_geom))))
            except (ConnectionError,  HTTPError) as err:
                print('Error: '.format(err))
                #paramsConveted.append (value)

        return paramsConveted

    def generate_tmp_file(self, suffix='', length_name=10):
        return ''.join([random.choice('0123456789ABCDEF') for i in range(length_name)]) + suffix

    def get_style_file(self, request):
        if 'HTTP_LAYERSTYLE' in request.META:
            layer_style_url = request.META['HTTP_LAYERSTYLE']
            response = requests.get(layer_style_url)
            if response.status_code == 200:
                file_name = self.generate_tmp_file(suffix="_tmp_style.xml")
                with open(file_name, "w+") as st:
                    st.write(response.text.encode('UTF-8'))
                    st.close()
                return file_name
        return None

    def get_png(self, queryset, request):
        style = self.get_style_file(request)

        if isinstance(queryset, GEOSGeometry):
            wkt = queryset.wkt
            geom_type = queryset.geom_type
        else:
            wkt = queryset.geom.wkt
            geom_type = queryset.geom.geom_type

        config = {'wkt': wkt, 'type': geom_type}
        if style is not None:
            config["style"] = style
            config["deleteStyle"] = True
        builder_png = BuilderPNG(config)
        return builder_png.generate()

    def split_complex_uri(self, complex_uri):
        marker_idx = complex_uri.index('!')
        uri_before_marker = complex_uri[:marker_idx]
        uri_after_marker = complex_uri[marker_idx:]
        operation_name = uri_after_marker[:uri_after_marker.index('/')+1]
        uri_after_oper_name = uri_after_marker.replace(operation_name, '')
        clean_operation_name = operation_name[1:-1]

        uri_arr = [uri_before_marker, clean_operation_name, uri_after_oper_name]
        return uri_arr

    #must be overrided
    def execute_complex_request(self, request):
        pass

class NonSpatialResource(AbstractResource):

    def response_of_request(self,  attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        if (not self.is_operation(att_funcs[0])) and self.is_attribute(att_funcs[0]):
            att_funcs = att_funcs[1:]

        self.current_object_state = self._execute_attribute_or_method(self.object_model, att_funcs[0], att_funcs[1:])

        if hasattr(self.current_object_state, 'model') and issubclass(self.current_object_state.model, Model):
            class_name = self.current_object_state.model.__name__ + 'Serializer'
            serializer_cls = self.object_model.class_for_name(self.serializer_class.__module__, class_name)
            if isinstance(self.current_object_state, QuerySet):
                self.current_object_state = serializer_cls(self.current_object_state, many=True,
                                                           context={'request': self.request}).data
            elif isinstance(self.current_object_state.field, OneToOneField):
                self.current_object_state = serializer_cls(self.current_object_state, context={'request': self.request}).data
            else:
                self.current_object_state = serializer_cls(self.current_object_state, many=True, context={'request': self.request}).data

        a_value = {self.name_of_last_operation_executed: self.current_object_state}

        return (a_value, CONTENT_TYPE_JSON, self.object_model, {'status': 200})

    def basic_get(self, request, *args, **kwargs):

        self.object_model = self.get_object(kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        # self.request.query_params.
        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if self.is_simple_path(attributes_functions_str):

            serializer = self.serializer_class(self.object_model, context={'request': self.request})
            output = (serializer.data, CONTENT_TYPE_JSON, self.object_model, {'status': 200})

        elif self.path_has_only_attributes(attributes_functions_str):
            output = self.response_resquest_with_attributes(attributes_functions_str.replace(" ", ""))
            dict_attribute = output[0]
            if len(attributes_functions_str.split(',')) > 1:
                self._set_context_to_attributes(dict_attribute.keys())
            else:
                self._set_context_to_only_one_attribute(attributes_functions_str)
        elif self.path_has_url(attributes_functions_str.lower()):
            output = self.response_request_attributes_functions_str_with_url( attributes_functions_str)
            self.context_resource.set_context_to_object(self.current_object_state, self.name_of_last_operation_executed)
        else:
            output = self.response_of_request(attributes_functions_str)
            self._set_context_to_operation(self.name_of_last_operation_executed)

        return output

    def get(self, request, *args, **kwargs):

        dict_for_response = self.basic_get(request, *args, **kwargs)
        status = dict_for_response[3]['status']
        if status in [400, 401,404]:
            return Response({'Error ': 'The request has problem. Status:' + str(status)}, status=status)

        if status in [500]:
           return Response({'Error ': 'The server can not process this request. Status:' + str(status)}, status=status)

        accept = request.META['HTTP_ACCEPT']

        response = Response(data=dict_for_response[0], content_type=dict_for_response[1])
        self.add_base_headers(request, response)
        return response

    def options(self, request, *args, **kwargs):
        response = super(NonSpatialResource, self).options( request, *args, **kwargs)
        self.basic_get(request, *args, **kwargs)
        response.data = self.context_resource.context()
        response['content-type'] = 'application/ld+json'
        return response
        #return self.context_resource.context()

class StyleResource(AbstractResource):
    pass

class SpatialResource(AbstractResource):

    def __init__(self):
        super(SpatialResource, self).__init__()
        self.iri_style = None

    def basic_get(self, request, *args, **kwargs):
        pass

    def spatial_field_name(self):
        return self.serializer_class.Meta.geo_field

    def make_geometrycollection_from_featurecollection(self, feature_collection):
        geoms = []
        features = json.loads(feature_collection)
        for feature in features['features']:
            feature_geom = json.dumps(feature['geometry'])
            geoms.append(GEOSGeometry(feature_geom))
        return GeometryCollection(tuple(geoms))

    def all_parameters_converted(self, attribute_or_function_name, parameters):
        parameters_converted = []
        if self.is_operation_and_has_parameters(attribute_or_function_name):
            parameters_type = self.operations_with_parameters_type()[attribute_or_function_name].parameters
            for i in range(0, len(parameters)):
                if GEOSGeometry == parameters_type[i]:
                    if not (parameters[i][0] == '{' or parameters[i][0] == '['):
                        parameters_converted.append(GEOSGeometry(parameters[i]))

                    else:
                        geometry_dict = json.loads(parameters[i])

                        if isinstance(geometry_dict, dict) and geometry_dict['type'].lower() == 'feature':
                            parameters_converted.append(parameters_type[i](json.dumps(geometry_dict['geometry'])))
                        elif isinstance(geometry_dict, dict) and geometry_dict['type'].lower() == 'featurecollection':
                            geometry_collection = self.make_geometrycollection_from_featurecollection(parameters[i])
                            parameters_converted.append(parameters_type[i](geometry_collection))
                        else:
                            parameters_converted.append(parameters_type[i](parameters[i]))
                else:
                    parameters_converted.append(parameters_type[i](parameters[i]))


            return parameters_converted

        return self.parametersConverted(parameters)

    def parametersConverted(self, params_as_array):
        paramsConveted = []

        for value in params_as_array:
            if value.lower() == 'true':
                paramsConveted.append(True)
                continue
            elif value.lower() == 'false':
                paramsConveted.append(False)
                continue

            try:
                paramsConveted.append(int( value ) )
                continue
            except ValueError:
                pass
            try:
               paramsConveted.append( float( value ) )
               continue
            except ValueError:
                pass
            try:
               paramsConveted.append( GEOSGeometry( value ) )
               continue
            except ValueError:
                pass
            try:
                http_str = (value[0:4]).lower()
                if (http_str == 'http'):
                    resp = requests.get(value)
                    if 400 <= resp.status_code <= 599:
                        raise HTTPError({resp.status_code: resp.reason})
                    js = resp.json()

                    if (js.get("type") and js["type"].lower() in ['feature', 'featurecollection']):
                        a_geom = js["geometry"]
                    else:
                        a_geom = js
                    paramsConveted.append(GEOSGeometry((json.dumps(a_geom))))
            except (ConnectionError,  HTTPError) as err:
                print('Error: '.format(err))
                #paramsConveted.append (value)

        return paramsConveted

    def options(self, request, *args, **kwargs):
        self.basic_get(request, *args, **kwargs)
        #return self.context_resource.context()
        resp = Response ( data=self.context_resource.context(), content_type='application/ld+json' )
        self.add_base_headers(request, resp)
        return resp

class FeatureResource(SpatialResource):

    def __init__(self):
        super(FeatureResource, self).__init__()

    def default_resource_type(self):
        return 'Feature'

    def dict_by_accept_resource_type(self):
        dict = {}
        dict[CONTENT_TYPE_OCTET_STREAM] = 'Geobuf'
        return dict

    # Must be override
    def initialize_context(self):
        pass

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def is_spatial_attribute(self, attribute_name):
        return self.model.geo_field_name() == attribute_name.lower()

    def operations_with_parameters_type(self):

        dic = self.object_model.operations_with_parameters_type()
        return dic

    #Responds a List with four elements: value of what was requested, content_type, object, dict=>dic[status] = status_code
    def response_resquest_with_attributes(self, attributes_functions_name, request=None):
        a_dict ={}
        attributes = attributes_functions_name.strip().split(',')

        for attr_name in attributes:
           obj = self._value_from_object(self.object_model, attr_name, [])
           if isinstance(obj, GEOSGeometry):
               geom = obj
               obj = json.loads(obj.geojson)
               if len(attributes) == 1:
                   return RequiredObject(obj, self.content_type_or_default_content_type(request), geom, 200)
           a_dict[attr_name] = obj
        if self.spatial_field_name() in attributes:
            a_dict = self.dict_as_geojson(a_dict)
        self.current_object_state = a_dict
        return RequiredObject(a_dict, CONTENT_TYPE_JSON, self.object_model,  200)

    def response_request_attributes_functions_str_with_url(self, attributes_functions_str, request=None):
        # r':/+' matches string like: ':' followed by at least 1 occurence of '/'
        # substitute any occurences of ':/' to '://' in 'attributes_functions_str'
        attributes_functions_str = re.sub(r':/+', '://', attributes_functions_str)
        arr_of_two_url_and_param = self.attributes_functions_splitted_by_url(attributes_functions_str)
        resp = requests.get(arr_of_two_url_and_param[1])
        if resp.status_code in[400, 401, 404]:
            return RequiredObject({},CONTENT_TYPE_JSON, self.object_model,  resp.status_code)
        if resp.status_code == 500:
            return RequiredObject({},CONTENT_TYPE_JSON, self.object_model,resp.status_code)
        j = resp.text

        if arr_of_two_url_and_param[2] is not None:
            attributes_functions_str = arr_of_two_url_and_param[0] + j + arr_of_two_url_and_param[2]
        else:
            attributes_functions_str = arr_of_two_url_and_param[0] + j
        #external_etag = resp.headers['etag']
        #self.inject_e_tag(external_etag)
        return self.response_of_request(attributes_functions_str)

    def response_of_request(self,  attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        self.current_object_state = self._execute_attribute_or_method(self.object_model, att_funcs[0], att_funcs[1:])
        a_value = self.current_object_state
        if isinstance(a_value, GEOSGeometry):
            geom = a_value
            a_value = json.loads(a_value.geojson)
            return RequiredObject(a_value, CONTENT_TYPE_GEOJSON, self.object_model,  200)
        elif isinstance(a_value, SpatialReference):
           a_value = { self.name_of_last_operation_executed: a_value.wkt.strip('\n')}
        elif isinstance(a_value, memoryview) or isinstance(a_value, buffer):
           return RequiredObject(a_value.obj, CONTENT_TYPE_OCTET_STREAM, self.object_model,200)
        else:
            a_value = {self.name_of_last_operation_executed: a_value}

        return RequiredObject(a_value, CONTENT_TYPE_JSON, self.object_model, 200)


    def response_base_get(self, request, *args, **kwargs):
        resource = self.resource_in_cache_or_None(request)
        if resource is not None:
            return self.response_base_object_in_cache(request )

        required_object = self.basic_get(request, *args, **kwargs)
        status = required_object.status_code
        if status in [400,401,404]:
            return Response({'Error ': 'The request has problem. Status:' + str(status)}, status=status)
        if status in [500]:
           return Response({'Error ': 'The server can not process this request. Status:' + str(status)}, status=status)

        if self.is_image_content_type(request, **kwargs):
           return self.response_base_get_with_image(request, required_object)

        if self.is_binary_content_type(required_object) or self.accept_is_binary(request):
            return self.response_base_get_binary(request, required_object)

        key = self.get_key_cache(request, a_content_type=required_object.content_type)

        self.set_key_with_data_in_cache(key, self.e_tag, required_object.representation_object )

        resp =  Response(data=required_object.representation_object,status=200, content_type=required_object.content_type)
        self.set_etag_in_header(resp, self.e_tag)
        return resp

    def basic_get(self, request, *args, **kwargs):

        self.object_model = self.get_object(kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        self.e_tag = str(hash(self.object_model))
        # self.request.query_params.
        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())
        if self.is_simple_path(attributes_functions_str):
            serializer = self.serializer_class(self.object_model)
            required_object = RequiredObject(serializer.data, self.content_type_or_default_content_type(request), self.object_model, 200)

        elif self.path_has_only_attributes(attributes_functions_str):
            str_attribute = attributes_functions_str.replace(" ", "").replace("/","")
            required_object = self.response_resquest_with_attributes(str_attribute , request)

            att_names = attributes_functions_str.split(',')
            if len(att_names) > 1:
                self._set_context_to_attributes(att_names)
            else:
                self._set_context_to_only_one_attribute(attributes_functions_str)
        elif self.path_has_url(attributes_functions_str.lower()):
            required_object = self.response_request_attributes_functions_str_with_url(attributes_functions_str, request)
            self.context_resource.set_context_to_object(self.current_object_state, self.name_of_last_operation_executed)
        else:
            s = str(attributes_functions_str)
            if s[-1] == '/':
               s = s[:-1]
            required_object = self.response_of_request(s)
            self._set_context_to_operation(self.name_of_last_operation_executed)
        self.inject_e_tag()
        self.temporary_content_type= required_object.content_type
        return required_object

    def basic_required_object(self, request, *args, **kwargs):
        return self.basic_get(request, *args, **kwargs)

    def basic_options(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get("attributes_functions", None)

        if self.is_simple_path(attributes_functions_str):
            return self.required_context_for_simple_path(request)
        if self.path_has_only_attributes(attributes_functions_str):
            return self.required_context_for_only_attributes(request, attributes_functions_str)
        if self.path_has_operations(attributes_functions_str):
            return self.required_context_for_operation(request, attributes_functions_str)

        return RequiredObject(
            representation_object={"This request has invalid attribute or operation: ": attributes_functions_str},
            content_type=CONTENT_TYPE_JSON, origin_object=self, status_code=400)

    def options(self, request, *args, **kwargs):
        required_object = self.basic_options(request, *args, **kwargs)
        if required_object.status_code == 200:
            response = Response(required_object.representation_object, content_type=required_object.content_type,
                                status=200)
            self.add_base_headers(request, response)
        else:
            response = Response(data={"This request is not supported": self.kwargs.get("attributes_functions", None)},
                                status=required_object.status_code)
        return response

    def get_context_by_only_attributes(self, request, attributes_functions_str):
        attrs_funcs_str = self.remove_last_slash(attributes_functions_str)
        super(FeatureResource, self).get_context_by_only_attributes(request, attrs_funcs_str)

        resource_type = self.define_resource_type_by_only_attributes(request, attrs_funcs_str)
        self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)
        supported_operation_dict = self.context_resource.supportedOperationsFor(self.object_model, resource_type)

        context = self.context_resource.dict_context
        context['hydra:supportedOperations'] = supported_operation_dict
        return context

    def default_content_type(self):
        return self.temporary_content_type if self.temporary_content_type is not None else CONTENT_TYPE_GEOJSON

    def define_resource_type_by_only_attributes(self, request, attributes_functions_str):
        attrs_functs_arr = self.remove_last_slash(attributes_functions_str).split(',')
        r_type = self.resource_type_or_default_resource_type(request)
        if r_type != self.default_resource_type():
            return r_type if self.geometry_field_name() in attrs_functs_arr else bytes

        if len(attrs_functs_arr) == 1:
            # the field type has priority over default resource type
            return type(self.field_for(attrs_functs_arr[0]))

        return r_type if self.geometry_field_name() in attrs_functs_arr else 'Thing'

    def define_resource_type_by_operation(self, request, operation_name):
        operation_type_called = self.operation_controller.dict_all_operation_dict()[operation_name]
        res_type_by_accept = self.resource_type_or_default_resource_type(request)

        if operation_type_called.return_type == GEOSGeometry:
            return res_type_by_accept
        elif issubclass(operation_type_called.return_type, GEOSGeometry):
            return res_type_by_accept if res_type_by_accept != self.default_resource_type() else operation_type_called.return_type
        else:
            res_type_by_accept = bytes if res_type_by_accept == 'Geobuf' else res_type_by_accept

        return operation_type_called.return_type if res_type_by_accept == self.default_resource_type() else res_type_by_accept

    def get(self, request, *args, **kwargs):
       self.change_request_if_image_png_into_IRI(request)
       return super(FeatureResource,self).get(request, *args, **self.kwargs)

class RasterResource(SpatialResource):
    def default_file_name(self):
        return self.object_model.model_class_name() + '_' + str(self.object_model.pk) + '.tiff'

    def default_resource_type(self):
        return 'Raster'

    def get_object_model_raster(self, kwargs):
        pass

class TiffResource(RasterResource):

    def default_content_type(self):
        return CONTENT_TYPE_IMAGE_TIFF

    def response_of_request(self,  attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        self.current_object_state = self._execute_attribute_or_method(self.object_model, att_funcs[0], att_funcs[1:])
        a_value = self.current_object_state
        if isinstance(a_value, GEOSGeometry):
            geom = a_value
            a_value = json.loads(a_value.geojson)
            return RequiredObject(a_value, CONTENT_TYPE_GEOJSON, self.object_model,  200)
        elif isinstance(a_value, SpatialReference):
           a_value = { self.name_of_last_operation_executed: a_value.wkt.strip('\n')}
        elif isinstance(a_value, memoryview) or isinstance(a_value, buffer):
           return RequiredObject(a_value.obj, CONTENT_TYPE_IMAGE_TIFF, self.object_model,200)
        else:
            a_value = {self.name_of_last_operation_executed: a_value}

        return RequiredObject(a_value, CONTENT_TYPE_JSON, self.object_model, 200)

    def basic_get(self, request, *args, **kwargs):

        self.object_model = BaseModel().get_model_object_raster(self, kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        self.e_tag = str(hash(self.object_model))
        # self.request.query_params.
        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())
        if self.is_simple_path(attributes_functions_str):
            required_object = RequiredObject(self.object_model.vsi_buffer(),  self.content_type_or_default_content_type(request), self.object_model, 200)

        elif self.path_has_only_attributes(attributes_functions_str):
            str_attribute = attributes_functions_str.replace(" ", "").replace("/","")
            required_object = self.response_resquest_with_attributes(str_attribute , request)

            att_names = attributes_functions_str.split(',')
            if len(att_names) > 1:
                self._set_context_to_attributes(att_names)
            else:
                self._set_context_to_only_one_attribute(attributes_functions_str)
        elif self.path_has_url(attributes_functions_str.lower()):
            required_object = self.response_request_attributes_functions_str_with_url(attributes_functions_str, request)
            self.context_resource.set_context_to_object(self.current_object_state, self.name_of_last_operation_executed)
        else:
            s = str(attributes_functions_str)
            if s[-1] == '/':
               s = s[:-1]
            required_object = self.response_of_request(s)
            self._set_context_to_operation(self.name_of_last_operation_executed)
        self.inject_e_tag()
        self.temporary_content_type= required_object.content_type
        return required_object

    def get(self, request, *args, **kwargs):

        required_object = self.basic_get(request, *args, **kwargs)

        if required_object.content_type == CONTENT_TYPE_IMAGE_TIFF:
            response = HttpResponse(required_object.representation_object, required_object.content_type)
            response['Content-Disposition'] = 'attachment; filename=' + self.default_file_name()
            return response
        response = Response(data=required_object.representation_object,status=200, content_type=required_object.content_type)
        return response

    def get_old(self, request, *args, **kwargs):
        self.object_model = self.get_object_model_raster(kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        # self.request.query_params.
        #attributes_functions_str = kwargs.get(self.attributes_functions_name_template())
        #response = StreamingHttpResponse(self.object_model.get_spatial_object().vsi_buffer, content_type="image/tiff")
        #vsi_buf = self.object_model.get_spatial_object().bands[0].data()
        #vsi_buf = self.object_model.get_spatial_object()
        #vsi_buf = self.object_model.get_spatial_object().vsi_buffer
        #vsi_buf.driver = 'GTiff'

        response = HttpResponse(self.object_model.rast.vsi_buffer, content_type="image/tiff")
        response['Content-Disposition'] = 'attachment; filename=' + self.default_file_name()
        #response['Content-Length'] = vsi_buf.width * 8*vsi_buf.height * 8
        #response = StreamingHttpResponse(vsi_buf, content_type="image/tiff")
        #response = FileResponse(vsi_buf, content_type="image/tiff")
        #response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        return response

class AbstractCollectionResource(AbstractResource):

    def __init__(self):
        super(AbstractCollectionResource, self).__init__()
        self.queryset = None
        #self.operation_controller = CollectionResourceOperationController()
        #self.operation_controller.initialize()

    def default_resource_type(self):
        return 'Collection'

    def attributes_functions_str_is_filter_with_spatial_operation(self, attributes_functions_str):

        arr_str = attributes_functions_str.split('/')[1:]

        geom_ops = self.operation_controller.geometry_operations_dict()

        for str in arr_str:
            if self.is_spatial_attribute(str):
              ind = arr_str.index(str)
              if ind +1 <= len(arr_str):
                return arr_str[ind + 1] in geom_ops()

        return False

    def split_combined_operation(self, attributes_functions_str):
        oc = BaseOperationController()
        operators_list = ['*' + key for key in oc.expression_operators_dict().keys()]
        operators_list.extend( ['*' + key for key in oc.logical_operators_dict().keys()] )

        attrs_functs_str = self.remove_last_slash(attributes_functions_str)
        attrs_funcs_arr = attrs_functs_str.split('/')
        if '/*' in attrs_functs_str:
            second_oper_init = None
            for attr_func in attrs_funcs_arr:
                if attr_func.startswith('*') and attr_func not in operators_list:
                    second_oper_init = attr_func
                    break

            if second_oper_init is None:
                first_oper_snippet = attrs_functs_str
                second_oper_snippet = None
            else:
                first_oper_snippet = attrs_functs_str[:attrs_functs_str.index(second_oper_init)-1]
                second_oper_snippet = attrs_functs_str[attrs_functs_str.index(second_oper_init)+1:]
        else:
            first_oper_snippet = attrs_functs_str
            second_oper_snippet = None
        return (first_oper_snippet, second_oper_snippet)

    def path_has_only_attributes(self, attributes_functions_name):
        if self.path_has_projection(attributes_functions_name):
            attrs_functs_str = self.remove_projection_from_path(attributes_functions_name, remove_only_name=True)
        else:
            attrs_functs_str = attributes_functions_name
        return super(AbstractCollectionResource, self).path_has_only_attributes(attrs_functs_str)

    def path_has_projection(self, attributes_functions_name):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_name).split("/")
        return attrs_funcs_arr[0] == "projection"

    def remove_projection_from_path(self, attributes_functions_str, remove_only_name=False):
        attrs_functs_arr = self.remove_last_slash(attributes_functions_str).split('/')
        if attrs_functs_arr[0] == "projection":
            attrs_functs_arr.pop(0)
            if not remove_only_name:
                attrs_functs_arr.pop(0)
        return "/".join(attrs_functs_arr)

    def extract_projection_snippet(self, attributes_functions_str, as_string=False):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split("/")
        projection_snippet = "/".join(attrs_funcs_arr[:2])
        return projection_snippet

    def extract_projection_attributes(self, attributes_functions_str, as_string=False):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split("/")
        if as_string:
            return attrs_funcs_arr[1]
        else:
            return attrs_funcs_arr[1].split(",")

    def extract_collect_operation_snippet(self, attributes_functions_str):
        collect_oper_snippet = self.remove_last_slash(attributes_functions_str)
        if self.path_has_projection(collect_oper_snippet):
            collect_oper_snippet = self.remove_projection_from_path(collect_oper_snippet)

        if '/*' + self.operation_controller.collect_collection_operation_name in collect_oper_snippet:
            collect_oper_snippet = collect_oper_snippet[collect_oper_snippet.index("*")+1:]

        return collect_oper_snippet

    def extract_collect_operation_attributes(self, attributes_functions_str, as_string=False):
        collect_oper_snippet_arr = self.extract_collect_operation_snippet(attributes_functions_str).split("/")
        collect_attrs = collect_oper_snippet_arr[1]
        return collect_attrs.replace('&', ',') if as_string else collect_attrs.split('&')

    def extract_offset_limit_operation_snippet(self, attributes_functions_str):
        offset_limit_oper_snippet = self.remove_last_slash(attributes_functions_str)
        if self.path_has_projection(attributes_functions_str):
            offset_limit_oper_snippet = self.remove_projection_from_path(attributes_functions_str)

        if '/*' + self.operation_controller.collect_collection_operation_name in offset_limit_oper_snippet:
            offset_limit_oper_snippet = offset_limit_oper_snippet[:offset_limit_oper_snippet.index("*")-1]

        return offset_limit_oper_snippet

    def extract_offset_limit_operation_attrs(self, attributes_functions_str, as_string=False):
        offset_limit_oper_snippet = self.extract_offset_limit_operation_snippet(attributes_functions_str)
        offset_limit_oper_snippet_arr = offset_limit_oper_snippet.split('/')

        if as_string:
            if len(offset_limit_oper_snippet_arr) == 3:
                return offset_limit_oper_snippet_arr[-1]
            else:
                return None

        if len(offset_limit_oper_snippet_arr) == 3:
            return offset_limit_oper_snippet_arr[-1].split(',')
        else:
            return None

    def projection_attrs_equals_offset_limit_attributes(self, attributes_functions_str):
        offset_limit_attrs = self.extract_offset_limit_operation_attrs(attributes_functions_str)
        if offset_limit_attrs == None:
            return True

        projection_attrs = self.extract_projection_attributes(attributes_functions_str)
        projection_attrs.sort()
        offset_limit_attrs.sort()
        return projection_attrs == offset_limit_attrs

    def projection_attrs_equals_collect_attrs(self, attributes_functions_str):
        projection_attrs = self.extract_projection_attributes(attributes_functions_str)
        collected_attributes = self.extract_collect_operation_attributes(attributes_functions_str)
        projection_attrs.sort()
        collected_attributes.sort()
        return projection_attrs == collected_attributes

    def offset_limit_attrs_equals_collect_attrs(self, attributes_function_str):
        offset_limit_attrs = self.extract_offset_limit_operation_attrs(attributes_function_str)
        if offset_limit_attrs == None:
            return True

        collect_attrs = self.extract_collect_operation_attributes(attributes_function_str)
        offset_limit_attrs.sort()
        collect_attrs.sort()
        return offset_limit_attrs == collect_attrs

    def path_has_filter_operation(self, attributes_functions_str):
        att_funcs = self.remove_last_slash(attributes_functions_str).split('/')
        return len(att_funcs) > 1 and  (att_funcs[0].lower() == self.operation_controller.filter_collection_operation_name)

    def path_has_groupy_operation(self, attributes_functions_str):
        att_funcs = self.remove_last_slash(attributes_functions_str).split('/')
        return len(att_funcs) == 2 and (att_funcs[0].lower() == self.operation_controller.group_by_collection_operation_name)

    def path_has_groupbycount_operation(self, attributes_functions_str):
        att_funcs = self.remove_last_slash(attributes_functions_str).split('/')
        return len(att_funcs) == 2 and (att_funcs[0].lower() == self.operation_controller.group_by_collection_operation_name)

    def path_has_distinct_operation(self, attributes_functions_str):
        att_funcs = self.remove_last_slash(attributes_functions_str).split('/')
        return len(att_funcs) == 2 and (att_funcs[0].lower() == self.operation_controller.distinct_collection_operation_name)

    def path_has_countresource_operation(self, attributes_functions_str):
        att_funcs = self.remove_last_slash(attributes_functions_str).split('/')
        return len(att_funcs) == 1 and  (att_funcs[0].lower() == self.operation_controller.count_resource_collection_operation_name)

    def path_has_offsetlimit_operation(self, attributes_functions_str):
        att_funcs = self.remove_last_slash(attributes_functions_str).split('/')
        att_funcs = [ele for ele in att_funcs if ele != '']
        return len(att_funcs) == 2 and  (att_funcs[0].lower() == self.operation_controller.offset_limit_collection_operation_name)

    #Responds an array of operations name.
    # Shoud be overrided
    def array_of_operation_name(self):
        collection_operations_array = list(self.operation_controller.collection_operations_dict().keys())
        collection_operations_array.extend(self.operation_controller.internal_collection_operations_dict().keys())
        return collection_operations_array

    def _dict_all_operation_dict(self):
        operations_dict = self.operation_controller.internal_collection_operations_dict()
        operations_dict.update(self.operation_controller.dict_all_operation_dict())
        return operations_dict

    def get_operation_type_called(self, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        operations_dict = self._dict_all_operation_dict()
        type_called = operations_dict[operation_name]
        return type_called

    def get_real_operation_name(self, operation_name_from_path):
        all_collection_operations = dict(self.operation_controller.collection_operations_dict(),
                                                  **self.operation_controller.internal_collection_operations_dict())
        type_called = all_collection_operations[operation_name_from_path]
        return type_called.name

    def get_operation_name_from_path(self, attributes_functions_str):
        attributes_functions_str = attributes_functions_str.lower()
        arr_att_funcs = self.remove_last_slash(attributes_functions_str).split('/')
        first_part_name = arr_att_funcs[2] if self.path_has_projection(attributes_functions_str) else arr_att_funcs[0]
        if first_part_name not in self.array_of_operation_name():
            return None
        if (first_part_name == self.operation_controller.offset_limit_collection_operation_name or
            first_part_name == self.operation_controller.filter_collection_operation_name) and '/*collect' in attributes_functions_str:
            return first_part_name + '_and_collect'
        if first_part_name == self.operation_controller.collect_collection_operation_name and '/*filter' in attributes_functions_str:
            return first_part_name + '_and_filter'
        if first_part_name == self.operation_controller.filter_collection_operation_name and '/*count_resource' in attributes_functions_str:
            return first_part_name + '_and_count_resource'
        return first_part_name

    def required_object_for_count_resource_operation(self,request, attributes_functions_str):
        return RequiredObject({"count_resource": self.model_class().objects.count()}, CONTENT_TYPE_JSON, self.object_model, 200)

    def required_object_for_offset_limit_operation(self, request, attributes_functions_str):
        offset_limit_snippet = self.remove_last_slash(attributes_functions_str)
        offset_limit_snippet_arr = offset_limit_snippet.split("/")
        if self.path_has_projection(attributes_functions_str):
            if self.projection_attrs_equals_offset_limit_attributes(attributes_functions_str):
                offset_limit_snippet = self.remove_projection_from_path(attributes_functions_str) +\
                    '/' + self.extract_projection_attributes(attributes_functions_str, as_string=True)
            else:
                message = "Projection list must be same as offset_limit attributes list"
                return self.required_object_for_invalid_sintax(attributes_functions_str, message)

        queryset_or_objects = self.get_objects_from_offset_limit_operation(offset_limit_snippet)

        if self.path_has_projection(attributes_functions_str):
            projection_atts_str = self.extract_projection_attributes(attributes_functions_str, as_string=True)
            objects = self.get_objects_serialized_by_only_attributes(projection_atts_str, queryset_or_objects)
            return RequiredObject(objects, self.content_type_or_default_content_type(request), queryset_or_objects, 200)
        elif len(offset_limit_snippet_arr) == 3:
            offset_limit_attrs = offset_limit_snippet_arr[2]
            objects = self.get_objects_serialized_by_only_attributes(offset_limit_attrs, queryset_or_objects)
            return RequiredObject(objects, self.content_type_or_default_content_type(request), queryset_or_objects, 200)
        else:
            return self.required_object(request, queryset_or_objects)

    def required_object_for_distinct_operation(self,request, attributes_functions_str):
        queryset_or_objects =  self.get_objects_from_distinct_operation(attributes_functions_str)

        if self.path_has_projection(attributes_functions_str):
            projection_attrs = self.extract_projection_attributes(attributes_functions_str, as_string=True)
            serialized_data = self.get_objects_serialized_by_only_attributes(projection_attrs, queryset_or_objects)
            return RequiredObject(serialized_data, self.content_type_or_default_content_type(request),
                                          queryset_or_objects, 200)

        return self.required_object(request, queryset_or_objects)

    def required_object_for_group_by_operation(self, request, attributes_functions_str):
        objects =  self.get_objects_from_group_by_operation(attributes_functions_str)
        return self.required_object_for_aggregation_operation(request, objects)

    def required_object_for_group_by_count_operation(self,request, attributes_functions_str):
            objects =  self.get_objects_from_group_by_count_operation(attributes_functions_str)
            return self.required_object_for_aggregation_operation(request, objects)

    def required_object_for_filter_operation(self, request, attributes_functions_str):
        business_objects = self.get_objects_from_filter_operation(attributes_functions_str)
        if self.path_has_projection(attributes_functions_str):
            attrs_funcs_str = self.extract_projection_attributes(attributes_functions_str, as_string=True)
            serialized_data = self.get_objects_serialized_by_only_attributes(attrs_funcs_str, business_objects)
        else:
            serialized_data = self.serializer_class(business_objects, many=True, context={'request': request}).data
        return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), business_objects, 200)

    def required_object_for_collect_operation(self, request, attributes_functions_str):
        collect_operation_snippet = self.remove_last_slash(attributes_functions_str)
        if self.path_has_projection(collect_operation_snippet):
            if self.projection_attrs_equals_collect_attrs(collect_operation_snippet):
                collect_operation_snippet = self.remove_projection_from_path(attributes_functions_str)
            else:
                message = "Projection attributes list must be the same as collect operation attributes list"
                return self.required_object_for_invalid_sintax(attributes_functions_str, message)

        business_objects = self.get_objects_from_collect_operation(collect_operation_snippet)
        return RequiredObject(business_objects, self.content_type_or_default_content_type(request), business_objects, 200)

    def required_object_for_filter_and_collect_collection_operation(self, request, attributes_functions_str):
        filter_and_collect_operation_snippet = self.remove_last_slash(attributes_functions_str)
        if self.path_has_projection(filter_and_collect_operation_snippet) and not self.projection_attrs_equals_collect_attrs(filter_and_collect_operation_snippet):
            message = "Projection attributes list must be the same as collect operation attributes list"
            return self.required_object_for_invalid_sintax(attributes_functions_str, message)

        business_objects = self.get_objects_from_filter_and_collect_operation(filter_and_collect_operation_snippet)

        collect_operation_snippet = self.extract_collect_operation_snippet(filter_and_collect_operation_snippet)
        serialized_data = self.get_objects_serialized_by_collect_operation(collect_operation_snippet, business_objects)
        return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), business_objects, 200)

    def required_object_for_offset_limit_and_collect_collection_operation(self, request, attributes_functions_str):
        offset_limit_and_collect_snippet = self.remove_last_slash(attributes_functions_str)
        if self.path_has_projection(attributes_functions_str):
            if  not self.projection_attrs_equals_offset_limit_attributes(attributes_functions_str) or\
                not self.offset_limit_attrs_equals_collect_attrs(attributes_functions_str) or\
                not self.projection_attrs_equals_collect_attrs(attributes_functions_str):
                    message = "Projection attributes list and offset_limit attributes list must be the same as collect operation attributes list"
                    return self.required_object_for_invalid_sintax(attributes_functions_str, message)
            else:
                offset_limit_and_collect_snippet = self.remove_projection_from_path(offset_limit_and_collect_snippet)

        else:
            if not self.offset_limit_attrs_equals_collect_attrs(attributes_functions_str):
                message = "offset_limit attributes list must be the same as collect operation attributes list"
                return self.required_object_for_invalid_sintax(attributes_functions_str, message)

        business_objects = self.get_objects_from_offset_limit_and_collect_operation(offset_limit_and_collect_snippet)
        collect_operation_snippet = self.extract_collect_operation_snippet(offset_limit_and_collect_snippet)
        serialized_data = self.get_objects_serialized_by_collect_operation(collect_operation_snippet, business_objects)
        return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), business_objects, 200)

    def required_object_for_filter_and_count_resource_collection_operation(self, request, attributes_functions_str):
        attrs_funcs_str = self.remove_projection_from_path(attributes_functions_str)
        filter_operation_params = attrs_funcs_str[0:attrs_funcs_str.index('/*')]
        q_object = self.q_object_for_filter_expression(filter_operation_params)
        num_objs = self.model_class().objects.filter(q_object).count()
        return RequiredObject({"count_resource": num_objs}, CONTENT_TYPE_JSON, self.object_model, 200)

    def required_object(self, request, business_objects):
        serialized_data = self.serializer_class(business_objects, many=True, context={'request': request}).data
        required_obj =  RequiredObject(serialized_data,self.content_type_or_default_content_type(request), business_objects, 200)
        return required_obj

    def required_object_for_invalid_sintax(self, attributes_functions_str, message=None):
        representation_object = {
            "This request has invalid attribute or operation: ": attributes_functions_str,
        }
        if message is not None:
            representation_object["Explanation"] = message
        required_obj =  RequiredObject(representation_object,CONTENT_TYPE_JSON, self, 400)
        return required_obj

    def required_object_for_aggregation_operation(self, request, a_dictionary):
        required_obj =  RequiredObject(a_dictionary,self.content_type_or_default_content_type(request), a_dictionary, 200)
        return required_obj

    def required_object_for_simple_path(self, request):
        objects = self.model_class().objects.all()
        serializer = self.serializer_class(objects, many=True, context={'request': request})
        required_object = RequiredObject(serializer.data, self.content_type_or_default_content_type(request), objects, 200)
        self.temporary_content_type= required_object.content_type
        return required_object

    def required_object_for_only_attributes(self, request, attributes_functions_str):
        attrs_funcs_str = self.remove_projection_from_path(attributes_functions_str, remove_only_name=True)
        objects = self.get_objects_by_only_attributes(attrs_funcs_str)
        serialized_data = self.get_objects_serialized_by_only_attributes(attrs_funcs_str, objects)
        #content_type = self.temporary_content_type if self.temporary_content_type != None else self.content_type_or_default_content_type(request)
        content_type = self.content_type_or_default_content_type(request)
        return RequiredObject(serialized_data, content_type, objects, 200)

    def required_object_for_complex_request(self, request):
        response = self.execute_complex_request(request)
        required_object = RequiredObject(json.loads(response.json), self.content_type_or_default_content_type(request), self, 200)
        return required_object

    def generics_collection_operation_name(self):
       return self.operation_controller.feature_collection_operations_dict().keys()

    def q_object_for_filter_array_of_terms(self, array_of_terms):
        return FactoryComplexQuery().q_object_for_filter_expression(None, self.model_class(), array_of_terms)

    def q_object_for_filter_expression(self, attributes_functions_str):
        if attributes_functions_str[-1] == '*' or (attributes_functions_str[-1] == '/' and attributes_functions_str[-2] == '*'):
            arr = attributes_functions_str[:-1].split('/')
        else:
            arr = attributes_functions_str.split('/')

        if self.path_has_url(attributes_functions_str):
           #arr = self.transform_path_with_url_as_array(arr)
            arr = self.attribute_functions_str_with_url_splitted_by_slash(attributes_functions_str)

        return FactoryComplexQuery().q_object_for_filter_expression(None, self.model_class(), arr[1:])

    def get_objects_from_filter_operation_OLD(self, attributes_functions_str):
        q_object = self.q_object_for_filter_expression(attributes_functions_str)
        return self.model_class().objects.filter(q_object)

    def get_objects_from_filter_operation(self, attributes_functions_str):
        if self.path_has_projection(attributes_functions_str):
            attrs_funcs_str = self.remove_projection_from_path(attributes_functions_str)
            q_object = self.q_object_for_filter_expression(attrs_funcs_str)

            attrs_arr = self.extract_projection_attributes(attributes_functions_str)
            return self.model_class().objects.filter(q_object).values(*attrs_arr)
        else:
            q_object = self.q_object_for_filter_expression(attributes_functions_str)
            return self.model_class().objects.filter(q_object)

    def get_objects_from_collect_operation(self, attributes_functions_str, queryset=None):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split("/")
        objects = self.model_class().objects.all() if queryset is None else queryset

        collect_object_list = []
        attrs_from_object = attrs_funcs_arr[1].split('&')
        attrs_out_of_operation = attrs_from_object[:-1]
        operated_attr = attrs_from_object[-1]

        operation_name = attrs_funcs_arr[2]
        operation_params = attrs_funcs_arr[3:]

        for obj in objects:
            obj_attrs_dict = {}
            for attr in attrs_out_of_operation:
                obj_attrs_dict[attr] = getattr(obj, attr)

            value_to_operation = getattr(obj, operated_attr)
            operated_value = self._execute_attribute_or_method(value_to_operation, operation_name, operation_params)

            obj_attrs_dict[operated_attr] = operated_value
            collect_object_list.append(obj_attrs_dict)

        return collect_object_list

    def get_objects_from_filter_and_collect_operation(self, attributes_functions_str):
        filter_oper_snippet = attributes_functions_str[:attributes_functions_str.index("*")]
        collect_oper_snippet = attributes_functions_str[attributes_functions_str.index("*")+1:]
        filtered_collection = self.get_objects_from_filter_operation(filter_oper_snippet)
        collected_objects = self.get_objects_from_collect_operation(collect_oper_snippet, filtered_collection)
        return collected_objects

    def transform_queryset_in_object_model_list(self, queryset):
        if type(queryset[0]) == self.model_class():
            return queryset

        objs_list = []
        for object in queryset:
            model_object = self.model_class()()
            for attr in object:
                setattr(model_object, attr, object[attr])
            objs_list.append(model_object)

        return objs_list

    def get_objects_from_offset_limit_and_collect_operation(self, attributes_functions_str):
        offset_limit_snippet = attributes_functions_str[:attributes_functions_str.index('/*')]
        queryset_or_objects = self.get_objects_from_offset_limit_operation(offset_limit_snippet)
        collect_operation_snippet = attributes_functions_str[attributes_functions_str.index('/*')+2:]
        collected_objects = self.get_objects_from_collect_operation(collect_operation_snippet, queryset=queryset_or_objects)
        return collected_objects

    #Todo
    def get_objects_from_collect_and_filter_operation(self, attributes_functions_str):
        pass

    def get_objects_from_distinct_operation(self, attributes_functions_str):
        attrs_funcs_no_projection = self.remove_last_slash(attributes_functions_str)

        if self.path_has_projection(attributes_functions_str):
            projection_attrs = self.extract_projection_attributes(attributes_functions_str)
            attrs_funcs_no_projection = self.remove_projection_from_path(attrs_funcs_no_projection)

        attrs_funcs_list = attrs_funcs_no_projection.split('/')
        distinct_parameters = attrs_funcs_list[1].split('&')

        if self.path_has_projection(attributes_functions_str):
            return self.model_class().objects.distinct(*distinct_parameters).values(*projection_attrs)
        else:
            return self.model_class().objects.distinct(*distinct_parameters)

    def get_objects_from_group_by_operation(self, attributes_functions_str):
        attributes_functions_list = attributes_functions_str.split('/')
        attributes_functions_list = [attr_func for attr_func in attributes_functions_list if attr_func != '']
        parameters = attributes_functions_list[1:][0].split(',')
        return self.model_class().objects.values(*parameters)

    def get_objects_from_group_by_count_operation(self, attributes_functions_str):
        attributes_functions_list = attributes_functions_str.split('/')
        attributes_functions_list = [attr_func for attr_func in attributes_functions_list if attr_func != '']
        parameters = attributes_functions_list[1:][0].split(',')
        return self.model_class().objects.values(*parameters).annotate(count=Count(*parameters))

    def get_objects_from_offset_limit_operation(self, attributes_functions_str):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split('/')
        if self.path_has_projection(attributes_functions_str):
            num_params = attrs_funcs_arr[3].split('&')
            selected_attrs = self.extract_projection_attributes(attributes_functions_str)
        else:
            num_params = attrs_funcs_arr[1].split('&')
            selected_attrs = attrs_funcs_arr[2].split(',') if len(attrs_funcs_arr) > 2 else None

        offset = int(num_params[0])
        limit = int(num_params[1])
        # starting from 0 or 1 has the same effect
        offset = offset if offset == 0 else offset - 1

        if self.path_has_projection(attributes_functions_str):
            objects = self.model_class().objects.values(*selected_attrs)[offset:offset + limit]
        else:
            if len(attrs_funcs_arr) > 2:
                objects = self.model_class().objects.values(*selected_attrs)[offset:offset + limit]
            else:
                objects = self.model_class().objects.all()[offset:offset + limit]

        return objects

    # Have to be overrided
    def get_objects_from_specialized_operation(self, attributes_functions_str):
        pass

    # Have to be overrided
    def get_objects_serialized_by_only_attributes(self, attributes_functions_str, objects):
        pass

    def get_objects_serialized_by_collect_operation(self, attributes_functions_str, objects):
        collect_operatiion_snippet = self.remove_last_slash(attributes_functions_str)
        collect_operation_arr = collect_operatiion_snippet.split('/')
        operation_name = collect_operation_arr[2]
        operated_attr = collect_operation_arr[1].split('&')[-1]

        collected_attrs = self.extract_collect_operation_attributes(collect_operatiion_snippet)
        if operated_attr not in objects[0].keys():
            collected_attrs[-1] = operation_name
        collected_attrs_str = ",".join(collected_attrs)

        return self.get_objects_serialized_by_only_attributes(collected_attrs_str, objects)

    def converter_collection_operation_parameters(self, operation_name, parameters):
        """
        Receive a operation name for a collection resource and a list of parameters
        for this operation. If this operation name corresponds to an collection operations
        dict key, convert each element into the parameters list to the expected type for
        the respective collection operation. Return the parameters intact if the operation
        name isn't in the collection operations dict.
        :param operation_name:
        :param parameters:
        :return:
        """
        operation_name_lower = operation_name.lower()

        # gets the dict whit all operations for collections
        collection_operations_dict = self.operation_controller.collection_operations_dict()
        if operation_name_lower in collection_operations_dict:
            # if operation_name is a collection operations dict key, return the related Type_Called
            type_called = collection_operations_dict[operation_name_lower]
            # convert each element in 'parameter' to the respective parameter type in Type_Called.parameters
            converted_parameters = [ConverterType().value_converted(param, parameters[i]) for i, param in enumerate(type_called.parameters)]
            return converted_parameters

        # returning the parameters without convertion
        return parameters

    def operation_names_model(self):
        return self.operation_controller.collection_operations_dict()

    def get_generic_operation_name(self, attributes_functions_str):
        if attributes_functions_str[-1] != '/':
            att_func_str = attributes_functions_str + '/'
        else:
            att_func_str = attributes_functions_str

        first_op_name = att_func_str[:att_func_str.find('/')]
        if first_op_name not in self.generics_collection_operation_name():
            return None
        idx = -1
        if first_op_name == 'filter':
            idx = att_func_str.find('/*collect')
        elif first_op_name == 'collect':
            idx = att_func_str.find('/*filter')
        if idx == -1:
            return 'get_objects_from_' + first_op_name + '_operation'
        partial_str = att_func_str[(idx +2):]

        second_op_name = partial_str[:partial_str.find('/')]

        return 'get_objects_from_' + first_op_name + '_and_' + second_op_name + '_operation'

    #Responds a dictionary(key=operation_name, value=method_to_execute).Should be overrided
    def operation_name_method_dic(self):
        d = {}
        d[self.operation_controller.offset_limit_collection_operation_name] =   self.required_object_for_offset_limit_operation
        d[self.operation_controller.offset_limit_and_collect_collection_operation_name] = self.required_object_for_offset_limit_and_collect_collection_operation
        d[self.operation_controller.filter_and_collect_collection_operation_name] = self.required_object_for_filter_and_collect_collection_operation
        d[self.operation_controller.filter_and_count_resource_collection_operation_name] = self.required_object_for_filter_and_count_resource_collection_operation
        d[self.operation_controller.count_resource_collection_operation_name] = self.required_object_for_count_resource_operation
        d[self.operation_controller.distinct_collection_operation_name] = self.required_object_for_distinct_operation
        d[self.operation_controller.group_by_collection_operation_name] = self.required_object_for_group_by_operation
        d[self.operation_controller.group_by_count_collection_operation_name] = self.required_object_for_group_by_count_operation
        d[self.operation_controller.filter_collection_operation_name] = self.required_object_for_filter_operation
        d[self.operation_controller.collect_collection_operation_name] = self.required_object_for_collect_operation
        return d

    #Responds a method to be executed.
    def get_operation_to_execute(self, operation_name):
        d = self.operation_name_method_dic()
        if operation_name is None:
            return None
        return d[operation_name]

    #Responds a RequiredObject via execute operation thats depends on path(attributes_functions_str) of the IRI
    def get_requiredObject_from_method_to_execute(self, request, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        method_to_execute = self.get_operation_to_execute(operation_name)
        if method_to_execute is None:
            return None
        attr_functions_str =  attributes_functions_str.replace(operation_name, self.get_real_operation_name(operation_name))
        return method_to_execute(*[request, attr_functions_str])

    #Responds a dictionary(key=operation_name, value=method_to_execute).Should be overrided
    def operation_name_context_dic(self):
        d = {}
        d[self.operation_controller.offset_limit_collection_operation_name] =   self.context_resource.context()
        d[self.operation_controller.count_resource_collection_operation_name] = self.required_object_for_count_resource_operation
        d[self.operation_controller.distinct_collection_operation_name] = self.required_object_for_distinct_operation
        d[self.operation_controller.group_by_collection_operation_name] = self.required_object_for_group_by_operation
        d[self.operation_controller.group_by_count_collection_operation_name] = self.required_object_for_group_by_count_operation
        d[self.operation_controller.filter_collection_operation_name] = self.required_object_for_filter_operation
        d[self.operation_controller.collect_collection_operation_name] = self.required_object_for_collect_operation
        d[self.operation_controller.filter_and_collect_collection_operation_name] = self.required_object_for_filter_and_collect_collection_operation
        return d

    #Responds a context. Should be overrided
    def get_context_from_method_to_execute(self, request, attributes_functions_str):
        method_to_execute = self.get_operation_to_execute(request, attributes_functions_str)
        if method_to_execute is None:
            return self.context_resource.context()
        if method_to_execute == self.required_object_for_count_resource_operation:
            self._set_context_to_operation()

    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get("attributes_functions", None)
        self.inject_e_tag()

        if self.is_simple_path(attributes_functions_str):
            return self.required_object_for_simple_path(request)

        if self.path_has_only_attributes(attributes_functions_str):
            return self.required_object_for_only_attributes(request, attributes_functions_str)

        if self.is_complex_request(request):
            if ENABLE_COMPLEX_REQUESTS:
                return self.required_object_for_complex_request(request)
            else:
                return RequiredObject(representation_object={"This request has invalid attribute or operation: ": attributes_functions_str}, content_type=CONTENT_TYPE_JSON, origin_object=self,status_code=400)

        res = self.get_requiredObject_from_method_to_execute(request, attributes_functions_str)
        if res is None:
            return RequiredObject(representation_object={"This request has invalid attribute or operation: ": attributes_functions_str}, content_type=CONTENT_TYPE_JSON, origin_object=self,status_code=400)
        return res

    def basic_options(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get("attributes_functions", None)

        if self.is_simple_path(attributes_functions_str):
            return self.required_context_for_simple_path(request)
        elif self.path_has_only_attributes(attributes_functions_str):
            return self.required_context_for_only_attributes(request, attributes_functions_str)
        elif self.path_has_operations(attributes_functions_str):
            return self.required_context_for_operation(request, attributes_functions_str)
        else:
            return RequiredObject(representation_object={"This request has invalid attribute or operation: ":  attributes_functions_str},
                              content_type=CONTENT_TYPE_JSON, origin_object=self,status_code=400)

    def options(self, request, *args, **kwargs):
        required_object = self.basic_options(request, *args, **kwargs)
        response = Response(data=required_object.representation_object, content_type=required_object.content_type, status=required_object.status_code)
        if required_object.status_code == 200:
            self.add_base_headers(request, response)
        return response

    def basic_post(self, request):
        response =  Response(status=status.HTTP_201_CREATED, content_type=CONTENT_TYPE_JSON)
        response['Content-Location'] = request.path + str(self.object_model.pk)
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            obj =  serializer.save()
            self.object_model = obj
            return self.basic_post(request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def hashed_value(self, object):
        dt = datetime.now()
        local_hash = self.__class__.__name__ + str(dt.microsecond)
        return local_hash

    def get_objects_by_only_attributes(self, attribute_names_str):
        arr = []
        attribute_names_str_as_array = self.remove_last_slash(attribute_names_str).split(',')
        return self.model_class().objects.values(*attribute_names_str_as_array)

    # se for uma operação derivada de collect, definir supported operations de acordo com a lista de attributos
    def get_context_for_operation(self, request, attributes_functions_str):
        context = {}
        attrs_functs_arr = self.remove_last_slash(attributes_functions_str).split('/')
        operation_name = self.get_operation_name_from_path(attributes_functions_str)

        if operation_name in self.operation_controller.internal_collection_operations_dict().keys():
            last_oper_name = operation_name.split("_and_")[1]
        else:
            last_oper_name = operation_name
        oper_type_called = self._dict_all_operation_dict()[last_oper_name]

        if operation_name in [self.operation_controller.collect_collection_operation_name,
                              self.operation_controller.filter_and_collect_collection_operation_name,
                              self.operation_controller.offset_limit_and_collect_collection_operation_name]:
            context.update(self.get_context_for_collect_operation(request, attributes_functions_str))
        else:

            #if resource_type is None or resource_type == self.default_resource_type():
                # only uses default resource type if operation return type is too generic (like 'object')
            #    return_type = resource_type if oper_type_called.return_type == object else oper_type_called.return_type
            #else:
            #    return_type = resource_type

            #if operation_name in self.operation_controller.subcollection_operations_dict().keys():
            if Q in oper_type_called.parameters:
                context.update({"hydra:supportedProperties": self.context_resource.supportedProperties()})
            #    property_field = self.field_for(attrs_functs_arr[1])
            #    operators_type = type(property_field) if property_field is not None else 'object'
                #context.update({"hydra:supportedOperators": self.context_resource.supportedOperators()})

            resource_type = self.define_resource_type(request, attributes_functions_str)
            context.update({"hydra:supportedOperations": self.context_resource.supportedOperationsFor(self.object_model, resource_type)})
            context.update(self.context_resource.get_resource_type_context(resource_type))
            self.context_resource.set_context_to_operation(self.object_model, last_oper_name)
            context.update({"@context": self.context_resource.dict_context["@context"]})

        return context

    def get_context_for_collect_operation(self, request, attributes_functions_str):
        attrs_func_str = self.remove_last_slash(attributes_functions_str)
        operation_name = self.get_operation_name_from_path(attrs_func_str)

        if operation_name != self.operation_controller.collect_collection_operation_name:
            collect_oper_snippet = attrs_func_str[attrs_func_str.index('*')+1:]
            collect_operation_params = collect_oper_snippet.split('/')
        else:
            collect_operation_params = attrs_func_str.split('/')

        operation_in_collect = "/".join(collect_operation_params)
        context = self.get_context_for_operation_in_collect_operation(request, operation_in_collect)

        attrs = ",".join(collect_operation_params[1].split("&"))
        attrs_context = self.get_context_by_only_attributes(None, attrs)
        context['@context'].update(attrs_context["@context"].items())

        return context

    def get_context_for_operation_in_collect_operation(self, request, collect_operation_str):
        pass

    def set_resource_type_context_by_operation(self, request, attributes_functions_str):
        attrs_func_str = self.remove_last_slash(attributes_functions_str)
        operation_name = self.get_operation_name_from_path(attrs_func_str)

        type_called = self.operation_controller.dict_all_operation_dict()[operation_name]

        if operation_name in self.operation_controller.subcollection_operations_dict():
            self.context_resource.set_context_to_resource_type(request, self.object_model, 'Collection')
        else:
            self.context_resource.set_context_to_resource_type(request, self.object_model, type_called.return_type)

        return self.context_resource.get_resource_type_context()

class CollectionResource(AbstractCollectionResource):
    def __init__(self):
        super(CollectionResource, self).__init__()
        self.queryset = None
        self.operation_controller = CollectionResourceOperationController()

    def operations_with_parameters_type(self):
        return self.operation_controller.collection_operations_dict()

    def get_objects_serialized(self):
        objects = self.model_class().objects.all()
        return self.serializer_class(objects, many=True, context={'request': self.request}).data

    def get_objects_by_only_attributes(self, attribute_names_str):
        arr = []
        attribute_names_str_as_array = self.remove_last_slash(attribute_names_str).split(',')

        return self.model_class().objects.values(*attribute_names_str_as_array)

    def get_objects_serialized_by_only_attributes(self, attribute_names_str, query_set):
        arr = []
        attribute_names_str_as_array = self.remove_last_slash(attribute_names_str).split(',')
        for obj in query_set:
            a_dic = {}
            for att_name in attribute_names_str_as_array:
                a_dic[att_name] = obj[att_name]
            arr.append(a_dic)
        return arr

    def get_objects_from_specialized_operation(self, attributes_functions_str):
        return self.get_objects_from_filter_operation(attributes_functions_str)

    def get_objects_by_functions(self, attributes_functions_str):

        objects = []
        if self.path_has_filter_operation(attributes_functions_str):
            objects = self.get_objects_from_filter_operation(attributes_functions_str)
        return objects

    def get_context_by_only_attributes(self, request, attributes_functions_str):
        attrs_context = super(CollectionResource, self).get_context_by_only_attributes(request, attributes_functions_str)
        resource_type = self.resource_type_or_default_resource_type(request)
        self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)

        context = self.context_resource.dict_context
        return context

    def basic_get_OLD(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get("attributes_functions", None)
        self.inject_e_tag()
        if self.is_simple_path(attributes_functions_str):  # to get query parameters
            query_set = self.model_class().objects.all()
            serializer = self.serializer_class(query_set, many=True, context={"request" : request})
            required_object = RequiredObject(serializer.data, self.content_type_or_default_content_type(request), query_set, 200)
            return required_object

        elif self.path_has_only_attributes(attributes_functions_str):
            query_set = self.get_objects_by_only_attributes(attributes_functions_str)
            serialized_data = self.get_objects_serialized_by_only_attributes(attributes_functions_str, query_set)
            return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), query_set, 200)

        elif self.path_has_distinct_operation(attributes_functions_str):
            query_set =  self.get_objects_from_distinct_operation(attributes_functions_str)
            serializer = self.serializer_class(query_set, many=True, context={"request": request})
            return RequiredObject(serializer.data, self.content_type_or_default_content_type(request), query_set, 200)

        elif self.path_has_countresource_operation(attributes_functions_str):
            return RequiredObject({"countResource": self.model_class().objects.count()}, CONTENT_TYPE_JSON, self.object_model, 200)

        elif self.path_has_offsetlimit_operation(attributes_functions_str):
            query_set = self.get_objects_from_offset_limit_operation(attributes_functions_str)
            serializer = self.serializer_class(query_set, many=True, context={'request': request})
            return RequiredObject(serializer.data, self.content_type_or_default_content_type(request), query_set, 200)

        elif self.path_has_operations(attributes_functions_str) and self.path_request_is_ok(attributes_functions_str):
            query_set = self.get_objects_by_functions(attributes_functions_str)
            serialized_data = self.serializer_class(query_set, many=True, context={'request': request})
            return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), query_set, 200)

        else:
            return RequiredObject(representation_object={"This request has invalid attribute or operation"},
                                  content_type=CONTENT_TYPE_JSON,
                                  origin_object=self,
                                  status_code=400)

class SpatialCollectionResource(AbstractCollectionResource):
    def __init__(self):
        super(SpatialCollectionResource, self).__init__()
        self.queryset = None
        self.operation_controller = SpatialCollectionOperationController()
    #todo
    def path_request_is_ok(self, attributes_functions_str):
        return True

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def operation_names_model(self):
        return self.operation_controller.feature_collection_operations_dict().keys()

    def path_has_only_spatial_operation(self, attributes_functions_str):
        pass

class RasterCollectionResource(SpatialCollectionResource):
   field_names = []

   def fields_to_web(self):
       return self.field_names

   def spatial_field_name(self):
        return self.serializer_class.Meta.geo_field

   def initialize_object(self, request, *args, **kwargs):
        self.object_model = BaseModel().get_iris_raster(self, kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        self.is_entry_point = True

   #response = self.add_url_in_header(entry_pointURL, response, 'http://schema.org/EntryPoint')

class TiffCollectionResource(RasterCollectionResource):

    def default_content_type(self):
        return CONTENT_TYPE_JSON



    def basic_get(self, request, *args, **kwargs):

        self.initialize_object(request, *args, **kwargs)
        #self.e_tag = str(hash(self.object_model))
        # self.request.query_params.
        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())
        if self.is_simple_path(attributes_functions_str):

            required_object = RequiredObject(self.object_model, self.content_type_or_default_content_type(request), self.object_model, 200)

        elif self.path_has_only_attributes(attributes_functions_str):
            str_attribute = attributes_functions_str.replace(" ", "").replace("/","")
            required_object = self.response_resquest_with_attributes(str_attribute , request)

            att_names = attributes_functions_str.split(',')
            if len(att_names) > 1:
                self._set_context_to_attributes(att_names)
            else:
                self._set_context_to_only_one_attribute(attributes_functions_str)
        elif self.path_has_url(attributes_functions_str.lower()):
            required_object = self.response_request_attributes_functions_str_with_url(attributes_functions_str, request)
            self.context_resource.set_context_to_object(self.current_object_state, self.name_of_last_operation_executed)
        else:
            s = str(attributes_functions_str)
            if s[-1] == '/':
               s = s[:-1]
            required_object = self.response_of_request(s)
            self._set_context_to_operation(self.name_of_last_operation_executed)
        self.inject_e_tag()
        self.temporary_content_type= required_object.content_type
        return required_object

    def options(self, request, *args, **kwargs):
        self.initialize_object(request, *args, **kwargs)

        dic_attrib_key_iri_value = BaseModel().get_iris_raster(self, kwargs)
        self.field_names = list(dic_attrib_key_iri_value.keys())
        return super(TiffCollectionResource, self).options(request, *args, **kwargs)


class FeatureCollectionResource(SpatialCollectionResource):
    def __init__(self):
         super(FeatureCollectionResource, self).__init__()
         self.operation_controller = SpatialCollectionOperationController()
         #self.operation_controller.initialize()

    def default_resource_type(self):
        return 'FeatureCollection'

    def get_real_operation_name(self, operation_name_from_path):
        all_geometry_collection_operations = dict(self.operation_controller.feature_collection_operations_dict(),
                                                  **self.operation_controller.internal_collection_operations_dict())
        type_called = all_geometry_collection_operations[operation_name_from_path]
        return type_called.name

    def geometry_operations(self):
        return self.operation_controller.feature_collection_operations_dict()

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def is_spatial_attribute(self, attribute_name):
        return attribute_name == self.geometry_field_name()

    def is_spatial_operation(self, operation_name):
        return operation_name in self.geometry_operations()

    def dict_list_as_feature_collection(self, dict_list):
        return {"type": "FeatureCollection", "features": dict_list}

    def dict_list_as_geometry_collection(self, dict_list):
        return {'type': 'GeometryCollection', "geometries": dict_list}

    def default_content_type(self):
        return self.temporary_content_type if self.temporary_content_type is not None else CONTENT_TYPE_GEOJSON

    def dict_by_accept_resource_type(self):
        dict = {}
        dict[CONTENT_TYPE_OCTET_STREAM] = 'GeobufCollection'
        return dict

    def define_resource_type(self, request, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        res_type_or_default = self.resource_type_or_default_resource_type(request)
        attrs_funcs_str = self.remove_last_slash(attributes_functions_str)
        attrs_funcs_arr = attrs_funcs_str.split("/")

        if self.path_has_only_attributes(attributes_functions_str):
            attrs = attrs_funcs_arr[0].split(',')
            if self.geometry_field_name() in attrs:
                if len(attrs) == 1:
                    return res_type_or_default if res_type_or_default == 'GeobufCollection' else GeometryCollection
            else:
                return bytes if res_type_or_default == 'GeobufCollection' else 'Collection'

        elif operation_name in self.operation_controller.collect_operations_dict().keys():
            if operation_name != self.operation_controller.collect_collection_operation_name:
                collect_oper_snippet = attrs_funcs_str[attrs_funcs_str.index("*"):]
            else:
                collect_oper_snippet = attrs_funcs_str
            collect_oper_arr = collect_oper_snippet.split("/")
            attrs_in_collect = collect_oper_arr[1].split("&")

            if collect_oper_arr[2] in BaseOperationController().geometry_operations_dict().keys():
                if res_type_or_default == 'GeobufCollection':
                    return res_type_or_default
                else:
                    return res_type_or_default if len(attrs_in_collect) > 1 else GeometryCollection
            else:
                if self.geometry_field_name() not in attrs_in_collect:
                    return bytes if res_type_or_default == 'GeobufCollection' else "Collection"
                else:
                    return res_type_or_default

        elif self.path_has_operations(attributes_functions_str):
            type_called = self.get_operation_type_called(attributes_functions_str)
            if not issubclass(type_called.return_type, GEOSGeometry):
                if res_type_or_default == 'GeobufCollection':
                    return bytes
                else:
                    if res_type_or_default is None or res_type_or_default == self.default_resource_type():
                        return res_type_or_default if type_called.return_type == object else type_called.return_type

        return res_type_or_default

    #attributes_functions_str == spatial_collection_operations_dict/... Or attributes_functions_str == geom/spatial_collection_operations_dict/....

    #todo
    def path_request_is_ok(self, attributes_functions_str):
        return True

    def path_has_only_spatial_operation(self, attributes_functions_str):

        att_funcs = attributes_functions_str.split('/')
        spatial_operation_names = self.geometry_operations().keys()

        if (len(att_funcs) > 1 and (att_funcs[0].lower() in spatial_operation_names)):
           return True

        return  (att_funcs[0].lower() in spatial_operation_names)

    def get_operation_name_from_path(self, attributes_functions_str):
        first_part_name = super(FeatureCollectionResource, self).get_operation_name_from_path(attributes_functions_str)
        if first_part_name not in self.array_of_operation_name():
            return None
        if (first_part_name == self.operation_controller.filter_collection_operation_name or
            first_part_name == self.operation_controller.offset_limit_collection_operation_name) and '/*extent' in attributes_functions_str:
            return 'extent'
        if (first_part_name == self.operation_controller.filter_collection_operation_name or
            first_part_name == self.operation_controller.offset_limit_collection_operation_name) and '/*union' in attributes_functions_str:
            return 'union'
        if (first_part_name == self.operation_controller.filter_collection_operation_name or
            first_part_name == self.operation_controller.offset_limit_collection_operation_name) and '/*make_line' in attributes_functions_str:
            return 'make_line'
        return first_part_name

    def is_filter_with_spatial_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        return (len(att_funcs) > 1 and (att_funcs[0].lower() in self.geometry_operations().keys())) or self.attributes_functions_str_is_filter_with_spatial_operation(attributes_functions_str)

    def operations_with_parameters_type(self):
        return self.operation_controller.feature_collection_operations_dict()

    def get_objects_from_spatial_operation(self, array_of_terms):
        full_oper_snippet = "/".join(array_of_terms)
        first_oper_snippet, second_oper_snippet = self.split_combined_operation(full_oper_snippet)
        arr_to_q_object = array_of_terms

        #defining array to Q object
        if self.path_has_projection(full_oper_snippet):
            arr_to_q_object = array_of_terms[2:]

        if second_oper_snippet is not None:
            second_oper_init = [k for k, v in enumerate(arr_to_q_object) if v.startswith('*collect') or v.startswith('*count_resource')]
            arr_to_q_object = arr_to_q_object if len(second_oper_snippet) == 0 else arr_to_q_object[:second_oper_init[0]]

        q_object = self.q_object_for_filter_array_of_terms(arr_to_q_object)

        if second_oper_snippet is not None:
            if second_oper_snippet.startswith('collect'):
                collect_attrs = self.extract_collect_operation_attributes(second_oper_snippet)
                queryset = self.model_class().objects.filter(q_object).values(*collect_attrs)
                return self.get_objects_from_collect_operation(second_oper_snippet, queryset)
            else: # the only options is 'collect' or 'count_resource'
                return self.model_class().objects.filter(q_object).count()

        if self.path_has_projection(full_oper_snippet):
            projection_attrs = self.extract_projection_attributes(full_oper_snippet)
            return self.model_class().objects.filter(q_object).values(*projection_attrs)

        return self.model_class().objects.filter(q_object)

    def q_object_for_filter_array_of_terms(self, array_of_terms):
        fcq = FactoryComplexQuery()
        return fcq.q_object_for_spatial_expression(None, self.model_class(), array_of_terms)

    #Responds a path(string) normalized for spatial operation in IRI. Ex.: within/... => geom/within/...
    def inject_geometry_attribute_in_spatial_operation_for_path(self, arr_of_term):
        indexes = []
        for idx, term in enumerate(arr_of_term):
            array_django_name_operation = [type_called.name for type_called in self.operation_controller.feature_collection_operations_dict().values()]
            if term in array_django_name_operation:
                indexes.append(idx)
        count = 0
        for i in indexes:
            arr_of_term.insert(i + count, self.geometry_field_name())
            count+=1

        return arr_of_term

    def path_has_geometry_attribute(self, term_of_path):
        return term_of_path.lower() == self.geometry_field_name()

    def execute_complex_request(self, request):
        # using request.build_absolute_uri() will cause problems in the case use of GeoJson in request
        absolute_uri = request.scheme + '://' + request.get_host() + request.path
        absolute_uri = absolute_uri if absolute_uri[-1] != '/' else absolute_uri[:-1]
        request_list = self.split_complex_uri(absolute_uri)
        operation = request_list[1]
        ct = ConverterType()

        # requests for FeatureCollectionResource means that the first url request_list[0]
        # is an url that corresponds to an FreatureCollection/GeometryCollection
        geom_left = ct.get_geos_geometry_from_request(request_list[0])

        if self.path_has_url(request_list[2]):
            response = requests.get(request_list[2])
            response_right = json.dumps(response.json())
        else: # if request_list[2] is GeometryCollection (GeoJson) or WKT ...
            response_right = request_list[2]

        result = self._execute_attribute_or_method(geom_left, operation, [response_right])
        return result

    def operation_name_method_dic(self):
        dicti = super(FeatureCollectionResource, self).operation_name_method_dic()
        dicti[self.operation_controller.bbcontaining_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.contained_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.containing_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.containing_properly_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.covering_by_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.covering_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.crossing_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.disjointing_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.intersecting_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.isvalid_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.overlaping_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.relating_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.touching_operation_name ] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.within_operation_name ] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.on_left_operation_name ] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.on_right_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.overlaping_left_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.overlaping_right_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.overlaping_above_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.overlaping_below_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.strictly_above_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.strictly_below_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.distance_gt_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.distance_gte_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.distance_lt_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.distance_lte_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.dwithin_operation_name] = self.required_object_for_specialized_operation
        dicti[self.operation_controller.union_collection_operation_name] = self.required_object_for_union_operation
        dicti[self.operation_controller.extent_collection_operation_name] = self.required_object_for_extent_operation
        dicti[self.operation_controller.make_line_collection_operation_name] = self.required_object_for_make_line_operation
        return dicti

    #Responds an array of operations name.
    def array_of_operation_name(self):
        collection_operations_array = super(FeatureCollectionResource, self).array_of_operation_name()
        collection_operations_array.extend(self.operation_controller.feature_collection_operations_dict().keys())
        return collection_operations_array

    def required_object_for_specialized_operation(self, request, attributes_functions_str):
        first_oper_snippet, second_oper_snippet = self.split_combined_operation(attributes_functions_str)

        if second_oper_snippet is not None:
            if second_oper_snippet.startswith('collect'):
                if self.path_has_projection(first_oper_snippet) and not self.projection_attrs_equals_collect_attrs(attributes_functions_str):
                    message = "Projection attribute list must be the same as collect operation attribute list"
                    return self.required_object_for_invalid_sintax(attributes_functions_str, message)

                spatial_objects = self.get_objects_from_specialized_operation(attributes_functions_str)
                serialized_data = self.get_objects_serialized_by_collect_operation(second_oper_snippet, spatial_objects)
            #if second_oper_snippet.startswith('count_resource'):
            else:
                spatial_objects = self.get_objects_from_specialized_operation(attributes_functions_str)
                serialized_data = {'count_resource': spatial_objects}

            return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), spatial_objects, 200)

        spatial_objects = self.get_objects_from_specialized_operation(attributes_functions_str)
        if self.path_has_projection(attributes_functions_str):
            attrs_str = self.extract_projection_attributes(attributes_functions_str, as_string=True)
            serialized_data = self.get_objects_serialized_by_only_attributes(attrs_str, spatial_objects)
            return RequiredObject(serialized_data,self.content_type_or_default_content_type(request), spatial_objects, 200)
        else:
            return self.required_object(request, spatial_objects)

    def required_object_for_extent_operation(self,request, attributes_functions_str):
        extent_dict = self.get_objects_from_extent_spatial_operation(attributes_functions_str)
        extent_dict['extent'] = extent_dict.pop(self.geometry_field_name() + '__extent')
        return self.required_object_for_aggregation_operation( request, extent_dict)

    def required_object_for_union_operation(self,request, attributes_functions_str):
        object = self.get_object_from_union_spatial_operation(attributes_functions_str)
        a_dictionary = json.loads(object[self.geometry_field_name() + '__union'].geojson)
        return self.required_object_for_aggregation_operation(request, a_dictionary)

    def required_object_for_make_line_operation(self,request, attributes_functions_str):
        line = self.get_object_from_make_line_spatial_operation(attributes_functions_str)
        a_dictionary = json.loads(line[self.geometry_field_name() + '__makeline'].geojson)
        return self.required_object_for_aggregation_operation(request, a_dictionary)

    #todo: Define header Content-Type depending of wich type is returned (FeatureCollection, bufer, dict, etc)
    def required_object_for_collect_operation(self, request, attributes_functions_str):
        collect_operation_snippet = self.remove_last_slash(attributes_functions_str)
        if self.path_has_projection(collect_operation_snippet):
            if self.projection_attrs_equals_collect_attrs(collect_operation_snippet):
                collect_operation_snippet = self.remove_projection_from_path(attributes_functions_str)
            else:
                message = "Projection attributes list must be the same as collect operation attributes list"
                return self.required_object_for_invalid_sintax(attributes_functions_str, message)

        business_objects = self.get_objects_from_collect_operation(collect_operation_snippet)

        serialized_data = self.get_objects_serialized_by_collect_operation(collect_operation_snippet, business_objects)
        return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), business_objects, 200)

    def get_objects_from_specialized_operation(self, attributes_functions_str):
        if self.path_has_url(attributes_functions_str):
            #arr = self.transform_path_with_url_as_array(att_func_arr)
            arr = self.attribute_functions_str_with_url_splitted_by_slash(attributes_functions_str)
        else:
            arr = attributes_functions_str.split('/')

        if  not self.path_has_geometry_attribute(arr[0]):
            arr = self.inject_geometry_attribute_in_spatial_operation_for_path(arr) #ex.: within/... => geom/within/...

        return self.get_objects_from_spatial_operation(arr)

    def get_objects_from_extent_spatial_operation(self, attributes_functions_str):
        first_part_name = super(FeatureCollectionResource, self).get_operation_name_from_path(attributes_functions_str)
        if first_part_name == self.operation_controller.filter_collection_operation_name:
            filter_snippet = attributes_functions_str[:attributes_functions_str.index("/*")]
            queryset_or_model_class = self.get_objects_from_filter_operation(filter_snippet)

        elif first_part_name == self.operation_controller.offset_limit_collection_operation_name:
            offset_limit_snippet = attributes_functions_str[:attributes_functions_str.index("/*")]
            queryset_or_model_class = self.get_objects_from_offset_limit_operation(offset_limit_snippet)
        else:
            queryset_or_model_class = self.model_class().objects

        return queryset_or_model_class.aggregate(Extent(self.geometry_field_name()))

    def get_object_from_union_spatial_operation(self, attributes_functions_str):
        first_part_name = super(FeatureCollectionResource, self).get_operation_name_from_path(attributes_functions_str)
        if first_part_name == self.operation_controller.filter_collection_operation_name:
            filter_snippet = attributes_functions_str[:attributes_functions_str.index("/*")]
            queryset_or_model_class = self.get_objects_from_filter_operation(filter_snippet)

        elif first_part_name == self.operation_controller.offset_limit_collection_operation_name:
            offset_limit_snippet = attributes_functions_str[:attributes_functions_str.index("/*")]
            queryset_or_model_class = self.get_objects_from_offset_limit_operation(offset_limit_snippet)
        else:
            queryset_or_model_class = self.model_class().objects

        return queryset_or_model_class.aggregate(Union(self.geometry_field_name()))

    def get_object_from_make_line_spatial_operation(self, attributes_functions_str):
        first_part_name = super(FeatureCollectionResource, self).get_operation_name_from_path(attributes_functions_str)
        if first_part_name == self.operation_controller.filter_collection_operation_name:
            filter_snippet = attributes_functions_str[:attributes_functions_str.index("/*")]
            queryset_or_model_class = self.get_objects_from_filter_operation(filter_snippet)

        elif first_part_name == self.operation_controller.offset_limit_collection_operation_name:
            offset_limit_snippet = attributes_functions_str[:attributes_functions_str.index("/*")]
            queryset_or_model_class = self.get_objects_from_offset_limit_operation(offset_limit_snippet)
        else:
            queryset_or_model_class = self.model_class().objects

        return queryset_or_model_class.aggregate(MakeLine(self.geometry_field_name()))

    def get_objects_from_collect_operation(self, attributes_functions_str, queryset=None):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split("/")
        objects = self.model_class().objects.all() if queryset is None else queryset
        obj_model_list_or_queryset = self.transform_queryset_in_object_model_list(objects)

        collected_objects_list = []

        collected_attrs = self.extract_collect_operation_attributes(attributes_functions_str)
        attrs_out_of_operation = collected_attrs[:-1] # only the last one will be operated
        operated_attr = collected_attrs[-1]
        operation_name = attrs_funcs_arr[2]
        operation_params = attrs_funcs_arr[3:]

        for obj in obj_model_list_or_queryset:
            collected_object = {}
            for attr in attrs_out_of_operation:
                collected_object[attr] = getattr(obj, attr)

            # executing operation in selected attribute
            if operated_attr == self.geometry_field_name():
                operated_value = self._execute_attribute_or_method(obj, operation_name, operation_params)
            else:
                operated_attr_val = getattr(obj, operated_attr)
                if operated_attr_val is not None:
                    operated_value = self._execute_attribute_or_method(operated_attr_val, operation_name, operation_params)
                else:
                    operated_value = None

            if isinstance(operated_value, GEOSGeometry):
                collected_object[operated_attr] = operated_value
            else:
                collected_object[operation_name] = operated_value
            collected_objects_list.append(collected_object)

        return collected_objects_list

    def get_objects_serialized_by_only_attributes(self, attribute_names_str, objects):
        arr = []
        attribute_names_str_as_array = self.remove_last_slash(attribute_names_str).split(',')
        has_geo_field = self.geometry_field_name() in attribute_names_str_as_array

        for dic in objects:
            a_dic = {}
            for att_name in attribute_names_str_as_array:
                #a_dic[att_name] = dic[att_name] if not isinstance(dic[att_name], GEOSGeometry) else json.loads(dic[att_name].json)
                if has_geo_field and att_name == self.geometry_field_name():
                    a_dic[att_name] = json.loads(dic[att_name].json)
                else:
                    a_dic[att_name] = dic[att_name]

            # reference to each geometry
            if has_geo_field:
                if len(attribute_names_str_as_array) > 1:
                    a_dic = self.dict_as_geojson(a_dic)
                else:
                    a_dic = a_dic[self.geometry_field_name()]
            arr.append(a_dic)

        # reference to the entire collection
        if has_geo_field:
            if len(attribute_names_str_as_array) > 1:
                arr = self.dict_list_as_feature_collection(arr)
            else:
                arr = self.dict_list_as_geometry_collection(arr)
        else:
            self.temporary_content_type = CONTENT_TYPE_JSON
        return arr

    def get_objects_from_within_operation(self, attributes_functions_str):
        return self.get_objects_from_filter_operation(attributes_functions_str)

    def get_objects_by_functions(self, attributes_functions_str):

        objects = []
        #if self.path_has_filter_operation(attributes_functions_str) or self.path_has_spatial_operation(attributes_functions_str) or  self.is_filter_with_spatial_operation(attributes_functions_str):
        if self.path_has_filter_operation(attributes_functions_str):
            objects = self.get_objects_from_filter_operation(attributes_functions_str)

        return objects

    def get_context_by_only_attributes(self, request, attributes_functions_str):
        context = {}
        attrs_context = super(FeatureCollectionResource, self).get_context_by_only_attributes(request, attributes_functions_str)
        context.update(attrs_context)
        resource_type = self.define_resource_type(request, attributes_functions_str)

        self.resource_type = resource_type
        supported_operations_list = self.context_resource.supportedOperationsFor(self.object_model, resource_type)
        context.update({"hydra:supportedOperations": supported_operations_list})

        self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)
        resource_type_context = self.context_resource.get_resource_type_context(resource_type)
        context.update(resource_type_context)
        return context

    def get_context_for_operation_in_collect_operation(self, request, collect_operation_str):
        context = {}
        collect_operation_arr = collect_operation_str.split('/')
        oper_name_in_collect_arr = collect_operation_arr[2]
        attrs_from_collect = collect_operation_arr[1].split('&')
        #resource_type = self.resource_type_or_default_resource_type(request)
        resource_type = self.define_resource_type(request, collect_operation_str)

        base_oper_dict = BaseOperationController().dict_all_operation_dict()

        if oper_name_in_collect_arr in base_oper_dict.keys():
            oper_ret_type = base_oper_dict[oper_name_in_collect_arr].return_type

            if issubclass(GEOSGeometry, oper_ret_type):
                self.context_resource.set_context_to_operation(GeometryCollection(), oper_name_in_collect_arr)

                if len(attrs_from_collect) == 1:
                    # prioritizing operation return over default resource type
                    resource_type = GeometryCollection if resource_type == self.default_resource_type() else resource_type

                self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)
                context.update(self.context_resource.dict_context)
            else:
                #self.context_resource.set_context_to_operation(oper_ret_type(), oper_name_in_collect_arr)
                self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)
                context.update(self.context_resource.dict_context)

                #self.context_resource.dict_context.update({"hydra:supportedOperations": supp_opers_list})
                #a_context_dict = { "@id": vocabulary(oper_name_in_collect_arr),"@type": "@id" }

                supp_opers_list =  self.context_resource.supportedOperationsFor(self.object_model, resource_type)
                self.context_resource.set_context_to_operation(resource_type, oper_name_in_collect_arr)
                self.context_resource.dict_context["hydra:supportedOperations"] = supp_opers_list
                context.update(self.context_resource.dict_context)
                #self.context_resource.dict_context.update(a_context_dict)
        return context

    def set_resource_type_context_by_operation(self, request, oper_name):
        resource_type = self.resource_type_or_default_resource_type(request)

        if resource_type is None or resource_type == self.default_resource_type():
            all_operations_dict = self._dict_all_operation_dict()
            oper_ret_type = all_operations_dict[oper_name].return_type
            ret_type = resource_type if oper_ret_type == object else oper_ret_type
        else:
            ret_type = resource_type

        self.context_resource.set_context_to_resource_type(request, self.object_model, ret_type)
        return self.context_resource.get_resource_type_context()

    def get_png(self, queryset, request):
        style = self.get_style_file(request)
        geom_type = None
        wkt = "GEOMETRYCOLLECTION("
        for i, e in enumerate(queryset):
            if isinstance(e,FeatureModel):
                wkt += e.get_spatial_object().wkt  # it is need to fix the case that the attribute is not called by geom
            else:
                geome = GEOSGeometry(json.dumps(e['geometry']))
                wkt +=  geome.wkt
                geom_type = geome.geom_type
            if i != len(queryset) - 1:
                wkt += ","
            else:
                wkt += ")"
        if isinstance(queryset[0], FeatureModel):
            geom_type = queryset[0].get_spatial_object().geom_type


        config = {'wkt': wkt, 'type': geom_type}
        if style is not None:
            config["style"] = style
            config["deleteStyle"] = True
        builder_png = BuilderPNG(config)
        return builder_png.generate()

    def basic_response(self, request, objects):

        serialized_data =  self.serializer_class(objects, many=True, context={'request': request}).data
        resp =  Response(data= serialized_data,status=200, content_type=CONTENT_TYPE_JSON)
        dt = datetime.now()
        local_hash = self.hashed_value(None)
        self.add_key_value_in_header(resp, ETAG, local_hash)
        iri_with_content_type = request.build_absolute_uri() + request.META[HTTP_ACCEPT]
        cache.set(iri_with_content_type,(local_hash, serialized_data), 3600)
        return resp

    def get(self, request, *args, **kwargs):
        absolute_uri = request.build_absolute_uri()
        self.change_request_if_image_png_into_IRI(request)
        return super(FeatureCollectionResource,self).get(request, *args, **self.kwargs)
'''