from copy import deepcopy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hyper_resource.contexts import EntryPointResourceContext, FeatureEntryPointResourceContext, RasterEntryPointResourceContext, NonSpatialEntryPointResourceContext
from hyper_resource.models import EntryPointResourceOperationController
from hyper_resource.resources.AbstractCollectionResource import AbstractCollectionResource
from hyper_resource.resources.AbstractResource import CORS_ALLOW_HEADERS, CORS_EXPOSE_HEADERS, AbstractResource, RequiredObject

class AbstractEntryPointResource(AbstractCollectionResource):

    def __init__(self):
        super(AbstractCollectionResource, self).__init__()
        self.operation_controller = EntryPointResourceOperationController()

    def default_resource_representation(self):
        return 'EntryPoint'
        #return 'https://www.hydra-cg.com/spec/latest/core/#hydra:entrypoint'

    def initialize_context(self):
        self.context_resource = EntryPointResourceContext()
        self.context_resource.resource = self

    def fields_to_web_for_attribute_names(self, attribute_names):
        # from client, comes with dash
        attribute_names_with_underscore = [attr_name.replace("-", "_") for attr_name in attribute_names]
        fields_model = super(AbstractCollectionResource, self).fields_to_web_for_attribute_names(attribute_names_with_underscore)

        # to client, goes with dash
        fields_models_with_dash = []
        for field in fields_model:
            new_field = deepcopy(field)
            new_field.name = new_field.name.replace("_", "-")
            fields_models_with_dash.append(new_field)
        return fields_models_with_dash

    def add_entry_point_links_in_header(self, request, response):
        entry_pointURL = request.build_absolute_uri() #reverse('bcim_v1:api_root', request=request)
        response = self.add_url_in_header(entry_pointURL, response, 'https://schema.org/EntryPoint')
        response = self.add_url_in_header(self.iri_metadata, response, 'metadata')
        return self.context_resource.addContext(request, response)

    def path_has_only_attributes(self, attributes_functions_name):
        attrs_functs = self.remove_last_slash(attributes_functions_name).split('/')

        if len(attrs_functs) > 1:
            return False

        attrs_arr = attrs_functs[0].split(",")
        for attr in attrs_arr:
            if attr not in self.attribute_names_to_web():
                return False
        return True

    def operation_name_method_dic(self):
        d = {
            self.operation_controller.filter_collection_operation_name:         self.required_object_for_filter_operation,
            self.operation_controller.collect_collection_operation_name:        self.required_object_for_collect_operation,
            self.operation_controller.count_resource_collection_operation_name: self.required_object_for_count_resource_operation,
            self.operation_controller.offset_limit_collection_operation_name:   self.required_object_for_offset_limit_operation,
            self.operation_controller.projection_operation_name:                self.required_object_for_projection_operation
        }
        return d

    def operation_name_context_dic(self):
        return {
            self.operation_controller.filter_collection_operation_name:         self.required_context_for_filter_operation,
            self.operation_controller.collect_collection_operation_name:        self.required_context_for_collect_operation,
            self.operation_controller.count_resource_collection_operation_name: self.required_context_for_count_resource_operation,
            self.operation_controller.offset_limit_collection_operation_name:   self.required_context_for_offset_limit_operation,
            self.operation_controller.projection_operation_name:                self.required_context_for_projection_operation
        }

    def operation_name_return_type_dic(self):
        dicti = {
            self.operation_controller.projection_operation_name: self.return_type_for_projection_operation,
            self.operation_controller.filter_collection_operation_name: self.return_type_for_filter_operation,
            self.operation_controller.collect_collection_operation_name: self.return_type_for_collect_operation,
            self.operation_controller.count_resource_collection_operation_name: self.return_type_for_count_resource_operation,
            self.operation_controller.offset_limit_collection_operation_name: self.return_type_for_offset_limit_operation,
        }
        return dicti

    def array_of_operation_name(self):
        collection_operations_array = list(self.operation_controller.collection_operations_dict().keys())
        return collection_operations_array

    def get_operation_name_from_path(self, attributes_functions_str):
        arr_att_funcs = self.remove_last_slash(attributes_functions_str).lower().split('/')

        if self.path_has_projection(attributes_functions_str):
            path_without_projection = self.remove_projection_from_path(attributes_functions_str)
            first_part_name = self.operation_controller.projection_operation_name if path_without_projection == '' else arr_att_funcs[2]
        else:
            first_part_name = arr_att_funcs[0]

        if first_part_name not in self.array_of_operation_name():
            return None
        return first_part_name

    def get_operation_type_called(self, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        return self.operation_controller.collection_operations_dict()[operation_name]

    def get_object_by_only_attributes(self, attribute_names_str):
        response_dict = {}
        attr_name_arr = self.remove_last_slash(attribute_names_str).split(",")
        for attr_name in attr_name_arr:
            response_dict[attr_name] = self.object_model[attr_name]
        return response_dict

    def get_root_response(self, request, format=None, *args, **kwargs):
        raise NotImplementedError("'get_root_response' must be implemented in subclasses")

    def options(self, request, *args, **kwargs):
        required_object = self.basic_options(request, *args, **kwargs)
        response = Response(required_object.representation_object, status=status.HTTP_200_OK, content_type="application/ld+json")
        self.add_cors_headers_in_header(response)
        return self.add_entry_point_links_in_header(request, response)

    def basic_options(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get('attributes_functions')
        if self.is_simple_path(attributes_functions_str):
            return self.required_context_for_simple_path(request)

        res = self.get_required_context_from_method_to_execute(request, attributes_functions_str)
        if res is None:
            return self.required_object_for_invalid_sintax(attributes_functions_str)
        return res

    def required_object_for_simple_path(self, request):
        return RequiredObject(self.object_model, self.content_type_or_default_content_type(request), self.object_model, 200)

    def required_object_for_count_resource_operation(self,request, attributes_functions_str):
        c_type_by_operation = self.define_content_type_by_operation(request, self.get_operation_name_from_path(attributes_functions_str))
        data = {self.operation_controller.count_resource_collection_operation_name: len(self.object_model)}
        return RequiredObject(data, c_type_by_operation, self.object_model, 200)

    def get(self, request, format=None, *args, **kwargs):
        required_object = self.basic_get(request, *args, **kwargs)
        response = Response(data=required_object.representation_object, status=200, content_type=required_object.content_type)
        self.add_cors_headers_in_header(response)
        entry_pointURL = request.build_absolute_uri() #reverse('bcim_v1:api_root', request=request)
        response = self.add_url_in_header(entry_pointURL, response, 'https://schema.org/EntryPoint')
        response = self.add_url_in_header(self.iri_metadata, response, 'metadata')
        return self.context_resource.addContext(request, response)

    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.get_root_response(request, *args, **kwargs)
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get('attributes_functions')

        if self.is_simple_path(attributes_functions_str):
            #self.add_allowed_methods(['delete', 'post'])
            return self.required_object_for_simple_path(request)

        # FOR ENTRYPOINTRESORCE IS NOT POSSIBLE SELECT ONLY ATTRIBUTES WITHOUT PROJECTION OPERATION
        # EXPLANATION: IF AN TABLE NAME IN DATABASE (A TABLE NAME IS AN ENTRYPOINT ATTRIBUTE NAME TO) HAS THE SAME NAME AS AN HYPER RESOURCE OPERATION
        # WON'T BE POSSIBLE TO DETERMINE IN http://server/entrypoint/projection if 'projection' IS AN ENTRYPOINT ATTRIBUTE NAME OR THE HYPER RESOURCE OPERATION 'projection'
        #if self.path_has_only_attributes(attributes_functions_str):
        #    return self.required_object_for_only_attributes(request, attributes_functions_str)

        res = self.get_required_object_from_method_to_execute(request, attributes_functions_str)
        if res is None:
            return self.required_object_for_invalid_sintax(attributes_functions_str)
        return res

    def head(self, request, *args, **kwargs):
        content_type = self.content_type_or_default_content_type(request)
        response = Response(data={}, status=status.HTTP_200_OK, content_type=content_type)
        self.add_cors_headers_in_header(response)
        return self.add_entry_point_links_in_header(request, response)


class FeatureEntryPointResource(AbstractEntryPointResource):

    def initialize_context(self):
        self.context_resource = FeatureEntryPointResourceContext()
        self.context_resource.resource = self


class NonSpatialEntryPointResource(AbstractEntryPointResource):

    def initialize_context(self):
        self.context_resource = NonSpatialEntryPointResourceContext()
        self.context_resource.resource = self


class RasterEntryPointResource(AbstractEntryPointResource):

    def initialize_context(self):
        self.context_resource = NonSpatialEntryPointResourceContext()
        self.context_resource.resource = self

    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.get_root_response(request, *args, **kwargs)
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get('attributes_functions')

        if self.is_simple_path(attributes_functions_str):
            self.add_allowed_methods(['post'])
            return self.required_object_for_simple_path(request)

        res = self.get_required_object_from_method_to_execute(request, attributes_functions_str)
        if res is None:
            return self.required_object_for_invalid_sintax(attributes_functions_str)
        return res

    def head(self, request, *args, **kwargs):
        if self.is_simple_path(self.kwargs.get('attributes_functions')):
            self.add_allowed_methods(['post'])
        return super(RasterEntryPointResource, self).head(request, *args, **kwargs)
