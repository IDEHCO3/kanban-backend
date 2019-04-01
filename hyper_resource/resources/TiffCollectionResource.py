from hyper_resource.resources.AbstractResource import *
from hyper_resource.resources.BaseModel import BaseModel
from hyper_resource.resources.RasterCollectionResource import RasterCollectionResource


class TiffCollectionResource(RasterCollectionResource):

    '''
    def default_content_type(self):
        return CONTENT_TYPE_JSON

    def basic_get(self, request, *args, **kwargs):
        self.initialize_object(request, *args, **kwargs)
        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if self.is_simple_path(attributes_functions_str):
            required_object = RequiredObject(self.object_model, self.content_type_or_default_content_type(request), self.object_model, 200)

        elif self.path_has_only_attributes(attributes_functions_str):
            str_attribute = attributes_functions_str.replace(' ', '').replace('/', '')
            required_object = self.response_request_with_attributes(str_attribute, request)

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

            if s.endswith('/'):
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
    '''

