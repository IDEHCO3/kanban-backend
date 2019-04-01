
import json
from operator import itemgetter

import requests

from django.core import cache
from django.contrib.gis.db.models import Extent, Union, MakeLine
from django.contrib.gis.geos import GeometryCollection, GEOSGeometry

from rest_framework.response import Response

from hyper_resource.resources.AbstractResource import *
from hyper_resource.resources.AbstractResource import RequiredObject
from hyper_resource.resources.FeatureResource import FeatureResource
from hyper_resource.resources.SpatialCollectionResource import SpatialCollectionResource
from hyper_resource.resources.AbstractCollectionResource import AbstractCollectionResource, COLLECTION_TYPE
from hyper_resource.models import SpatialCollectionOperationController, BaseOperationController, FactoryComplexQuery, \
    ConverterType, FeatureModel, FeatureCollection
from copy import deepcopy
from image_generator.img_generator import BuilderPNG


class FeatureCollectionResource(SpatialCollectionResource):
    def __init__(self):
         super(FeatureCollectionResource, self).__init__()
         self.operation_controller = SpatialCollectionOperationController()
         #self.operation_controller.initialize()

    def default_resource_representation(self):
        return FeatureCollection

    def geometry_operations(self):
        return self.operation_controller.feature_collection_operations_dict()

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def is_spatial_attribute(self, attribute_name):
        return attribute_name == self.geometry_field_name()

    def is_spatial_operation(self, operation_name):
        return operation_name in self.geometry_operations()

    def dict_list_as_feature_collection(self, dict_list):
        return {'type': 'FeatureCollection', 'features': dict_list}

    def dict_list_as_geometry_collection(self, dict_list):
        return {'type': 'GeometryCollection', 'geometries': dict_list}

    def default_content_type(self):
        return self.temporary_content_type if self.temporary_content_type is not None else CONTENT_TYPE_GEOJSON

    def define_content_type_by_only_attributes(self, request, attributes_functions_str):
        content_type_by_accept = self.content_type_or_default_content_type(request)
        attrs_arr = self.remove_last_slash(attributes_functions_str).split(',')

        if self.geometry_field_name() in attrs_arr:
            return content_type_by_accept

        if content_type_by_accept != self.default_content_type():
            return content_type_by_accept
        return CONTENT_TYPE_JSON

    def define_content_type_by_operation(self, request, operation_name):
        content_type_by_accept = self.content_type_or_default_content_type(request)
        oper_ret_type = self._dict_all_operation_dict()[operation_name].return_type

        if content_type_by_accept != self.default_content_type():
            return content_type_by_accept

        if issubclass(oper_ret_type, GEOSGeometry):
            return self.default_content_type()
        return CONTENT_TYPE_JSON

    def dict_by_accept_resource_representation(self):
        dict = {
            CONTENT_TYPE_OCTET_STREAM: 'GeobufCollection'
        }

        return dict

    def define_resource_representation_by_operation(self, request, attributes_functions_str):
        resource_representation_by_accept = self.resource_representation_or_default_resource_representation(request)
        resource_representation_by_return_type = self.execute_method_to_get_return_type_from_operation(attributes_functions_str)
        accept_is_binary = resource_representation_by_accept == self.dict_by_accept_resource_representation()[CONTENT_TYPE_OCTET_STREAM]

        if not issubclass(resource_representation_by_return_type, GEOSGeometry):
            if accept_is_binary:
                return bytes

        if resource_representation_by_accept != self.default_resource_representation():
            if accept_is_binary:
                if resource_representation_by_return_type not in [FeatureCollection, GeometryCollection]:
                    return "Geobuf"
            return resource_representation_by_accept
        return resource_representation_by_return_type

    #todo: need prioritize in unity tests
    def define_resource_representation_from_collect_operation(self, request, attributes_functions_str):
        collected_attrs = self.extract_collect_operation_attributes(attributes_functions_str)
        res_type_by_accept = self.resource_representation_or_default_resource_representation(request)
        oper_in_collect_ret_type = self.get_operation_in_collect_return_type(attributes_functions_str)

        if res_type_by_accept != self.default_resource_representation():
            if self.geometry_field_name() not in collected_attrs:
                return bytes

            # the operated attribute isn't the geometric attribute
            if self.geometry_field_name() != collected_attrs[-1]:
                return res_type_by_accept

            if issubclass(oper_in_collect_ret_type, GEOSGeometry):
                return res_type_by_accept
            return bytes

        # at this point 'res_type_by_accept' current value is 'FeatureCollection'
        if self.geometry_field_name() not in collected_attrs:
            return COLLECTION_TYPE

        # at this point collect operation has geometric attribute
        if len(collected_attrs) == 1:
            if issubclass(oper_in_collect_ret_type, GEOSGeometry):
                return GeometryCollection
            return COLLECTION_TYPE

        return res_type_by_accept

    def define_resource_representation_by_only_attributes(self, request, attributes_functions_str):
        attr_arr = self.remove_last_slash(attributes_functions_str).split(",")
        resource_type_by_accept = self.resource_representation_or_default_resource_representation(request)
        accept_content_type = request.META.get(HTTP_ACCEPT, '')

        alpha_dict_by_accept = super(FeatureCollectionResource, self).dict_by_accept_resource_representation()

        if resource_type_by_accept != self.default_resource_representation():
            if self.geometry_field_name() in attr_arr:
                return resource_type_by_accept
            return alpha_dict_by_accept[ accept_content_type ] if accept_content_type in alpha_dict_by_accept else "Thing"

        if self.geometry_field_name() in attr_arr:
            if len(attr_arr) > 1:
                return self.default_resource_representation()
            return GeometryCollection

        return COLLECTION_TYPE

    #todo
    def path_request_is_ok(self, attributes_functions_str):
        return True

    def path_has_only_spatial_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        spatial_operation_names = self.geometry_operations().keys()

        if len(att_funcs) > 1 and (att_funcs[0].lower() in spatial_operation_names):
            return True

        return att_funcs[0].lower() in spatial_operation_names

    def get_operation_name_from_path(self, attributes_functions_str):
        first_part_name = super(FeatureCollectionResource, self).get_operation_name_from_path(attributes_functions_str)

        # join operation has priority
        if self.path_has_join_operation(attributes_functions_str):
            return self.operation_controller.join_operation_name

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
            return 'make-line'

        return first_part_name

    def is_filter_with_spatial_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')

        return (len(att_funcs) > 1 and (att_funcs[0].lower() in self.geometry_operations().keys())) \
               or self.attributes_functions_str_is_filter_with_spatial_operation(attributes_functions_str)

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
            second_oper_init = [k for k, v in enumerate(arr_to_q_object) if v.startswith('*collect') or v.startswith('*' + self.operation_controller.count_resource_collection_operation_name)]
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

    # Responds a path(string) normalized for spatial operation in IRI. Ex.: within/... => geom/within/...
    def inject_geometry_attribute_in_spatial_operation_for_path(self, arr_of_term):
        indexes = []
        projection_snippet_arr = None

        if arr_of_term[0] == self.operation_controller.projection_operation_name:
            projection_snippet_arr, arr_of_term_without_projection = arr_of_term[:2], arr_of_term[2:]
        else:
            arr_of_term_without_projection = arr_of_term

        for idx, term in enumerate(arr_of_term_without_projection):
            array_django_name_operation = [type_called.name for type_called in self.operation_controller.feature_collection_operations_dict().values()]
            if term in array_django_name_operation:
                indexes.append(idx)
        count = 0
        for i in indexes:
            arr_of_term_without_projection.insert(i + count, self.geometry_field_name())
            count += 1

        if projection_snippet_arr is not None and arr_of_term_without_projection is not None:
            projection_snippet_arr.extend(arr_of_term_without_projection)
            return projection_snippet_arr

        return arr_of_term_without_projection

    def path_has_geometry_attribute(self, term_of_path):
        return term_of_path.lower() == self.geometry_field_name()

    def execute_complex_request(self, request):
        # using request.build_absolute_uri() will cause problems in the case use of GeoJson in request
        absolute_uri = request.scheme + '://' + request.get_host() + request.path
        absolute_uri = self.remove_last_slash(absolute_uri)
        request_tuple = self.split_complex_uri(absolute_uri)
        operation = request_tuple[1]
        ct = ConverterType()

        # requests for FeatureCollectionResource means that the first url request_list[0]
        # is an url that corresponds to an FeatureCollection/GeometryCollection
        geom_left = ct.get_geos_geometry_from_request(request_tuple[0])

        if self.path_has_url(request_tuple[2]):
            response = requests.get(request_tuple[2])
            response_right = json.dumps(response.json())

        else: # if request_list[2] is GeometryCollection (GeoJson) or WKT ...
            response_right = request_tuple[2]

        result = self._execute_attribute_or_method(geom_left, operation, [response_right])
        return result

    def operation_name_method_dic(self):
        dicti = super(FeatureCollectionResource, self).operation_name_method_dic()
        dicti.update({
             self.operation_controller.bbcontaining_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.contained_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.containing_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.containing_properly_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.covering_by_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.covering_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.crossing_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.disjointing_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.intersecting_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.isvalid_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.overlaping_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.relating_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.touching_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.within_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.on_left_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.on_right_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.overlaping_left_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.overlaping_right_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.overlaping_above_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.overlaping_below_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.strictly_above_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.strictly_below_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.distance_gt_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.distance_gte_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.distance_lt_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.distance_lte_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.dwithin_operation_name: self.required_object_for_specialized_operation,
             self.operation_controller.union_collection_operation_name: self.required_object_for_union_operation,
             self.operation_controller.extent_collection_operation_name: self.required_object_for_extent_operation,
             self.operation_controller.make_line_collection_operation_name: self.required_object_for_make_line_operation,
        })

        return dicti

    def operation_name_context_dic(self):
        dicti = super(FeatureCollectionResource, self).operation_name_context_dic()
        dicti.update({
             self.operation_controller.bbcontaining_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.contained_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.containing_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.containing_properly_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.covering_by_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.covering_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.crossing_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.disjointing_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.intersecting_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.isvalid_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.overlaping_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.relating_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.touching_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.within_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.on_left_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.on_right_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.overlaping_left_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.overlaping_right_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.overlaping_above_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.overlaping_below_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.strictly_above_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.strictly_below_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.distance_gt_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.distance_gte_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.distance_lt_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.distance_lte_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.dwithin_operation_name: self.required_context_for_specialized_operation,
             self.operation_controller.union_collection_operation_name: self.required_context_for_union_operation,
             self.operation_controller.extent_collection_operation_name: self.required_context_for_extent_operation,
             self.operation_controller.make_line_collection_operation_name: self.required_context_for_make_line_operation,
             self.operation_controller.join_operation_name: self.required_context_for_specialized_operation,
        })
        return dicti

    def operation_name_return_type_dic(self):
        dicti = super(FeatureCollectionResource, self).operation_name_return_type_dic()
        dicti.update({
            self.operation_controller.bbcontaining_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.bboverlaping_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.contained_operation_name:             self.return_type_for_specialized_operation,
            self.operation_controller.containing_operation_name:            self.return_type_for_specialized_operation,
            self.operation_controller.containing_properly_operation_name:   self.return_type_for_specialized_operation,
            self.operation_controller.covering_by_operation_name:           self.return_type_for_specialized_operation,
            self.operation_controller.covering_operation_name:              self.return_type_for_specialized_operation,
            self.operation_controller.crossing_operation_name:              self.return_type_for_specialized_operation,
            self.operation_controller.disjointing_operation_name:           self.return_type_for_specialized_operation,
            self.operation_controller.intersecting_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.isvalid_operation_name:               self.return_type_for_specialized_operation,
            self.operation_controller.overlaping_operation_name:            self.return_type_for_specialized_operation,
            self.operation_controller.relating_operation_name:              self.return_type_for_specialized_operation,
            self.operation_controller.touching_operation_name:              self.return_type_for_specialized_operation,
            self.operation_controller.within_operation_name:                self.return_type_for_specialized_operation,
            self.operation_controller.on_left_operation_name:               self.return_type_for_specialized_operation,
            self.operation_controller.on_right_operation_name:              self.return_type_for_specialized_operation,
            self.operation_controller.overlaping_left_operation_name:       self.return_type_for_specialized_operation,
            self.operation_controller.overlaping_right_operation_name:      self.return_type_for_specialized_operation,
            self.operation_controller.overlaping_above_operation_name:      self.return_type_for_specialized_operation,
            self.operation_controller.overlaping_below_operation_name:      self.return_type_for_specialized_operation,
            self.operation_controller.strictly_above_operation_name:        self.return_type_for_specialized_operation,
            self.operation_controller.strictly_below_operation_name:        self.return_type_for_specialized_operation,
            self.operation_controller.distance_gt_operation_name:           self.return_type_for_specialized_operation,
            self.operation_controller.distance_gte_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.distance_lt_operation_name:           self.return_type_for_specialized_operation,
            self.operation_controller.distance_lte_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.dwithin_operation_name:               self.return_type_for_specialized_operation,
            self.operation_controller.union_collection_operation_name:      self.return_type_for_union_operation,
            self.operation_controller.extent_collection_operation_name:     self.return_type_for_extent_operation,
            self.operation_controller.make_line_collection_operation_name:  self.return_type_for_make_line_operation
        })
        return dicti

    def operation_name_resource_representation_dic(self):
        dicti = super(FeatureCollectionResource, self).operation_name_resource_representation_dic()
        dicti.update({
            self.operation_controller.bbcontaining_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.bboverlaping_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.contained_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.containing_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.containing_properly_operation_name:   self.define_resource_representation_by_operation,
            self.operation_controller.covering_by_operation_name:           self.define_resource_representation_by_operation,
            self.operation_controller.covering_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.crossing_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.disjointing_operation_name:           self.define_resource_representation_by_operation,
            self.operation_controller.intersecting_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.isvalid_operation_name:               self.define_resource_representation_by_operation,
            self.operation_controller.overlaping_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.relating_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.touching_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.within_operation_name:                self.define_resource_representation_by_operation,
            self.operation_controller.on_left_operation_name:               self.define_resource_representation_by_operation,
            self.operation_controller.on_right_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.overlaping_left_operation_name:       self.define_resource_representation_by_operation,
            self.operation_controller.overlaping_right_operation_name:      self.define_resource_representation_by_operation,
            self.operation_controller.overlaping_above_operation_name:      self.define_resource_representation_by_operation,
            self.operation_controller.overlaping_below_operation_name:      self.define_resource_representation_by_operation,
            self.operation_controller.strictly_above_operation_name:        self.define_resource_representation_by_operation,
            self.operation_controller.strictly_below_operation_name:        self.define_resource_representation_by_operation,
            self.operation_controller.distance_gt_operation_name:           self.define_resource_representation_by_operation,
            self.operation_controller.distance_gte_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.distance_lt_operation_name:           self.define_resource_representation_by_operation,
            self.operation_controller.distance_lte_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.dwithin_operation_name:               self.define_resource_representation_by_operation,
            self.operation_controller.union_collection_operation_name:      self.define_resource_representation_by_operation,
            self.operation_controller.extent_collection_operation_name:     self.define_resource_representation_by_operation,
            self.operation_controller.make_line_collection_operation_name:  self.define_resource_representation_by_operation
        })
        return dicti

    # Responds an array of operations name.
    def array_of_operation_name(self):
        collection_operations_array = super(FeatureCollectionResource, self).array_of_operation_name()
        collection_operations_array.extend(self.operation_controller.feature_collection_operations_dict().keys())
        return collection_operations_array

    def return_type_by_only_attributes(self, attributes_functions_str):
        attrs = self.remove_last_slash(attributes_functions_str).split(",")
        if self.geometry_field_name() not in attrs:
            return super(FeatureCollectionResource, self).return_type_by_only_attributes(attributes_functions_str)

        if len(attrs) > 1:
            return FeatureCollection
        return GeometryCollection

    def return_type_for_filter_operation(self, attributes_functions_str):
        return FeatureCollection

    def return_type_for_offset_limit_operation(self, attributes_functions_str):
        return FeatureCollection

    def return_type_for_distinct_operation(self, attributes_functions_str):
        return FeatureCollection

    def return_type_for_group_by_count_operation(self, attributes_functions_str):
        grouped_attribute = self.remove_last_slash(attributes_functions_str).split("/")[-1]
        if grouped_attribute != self.geometry_field_name():
            return super(FeatureCollectionResource, self).return_type_for_group_by_count_operation(attributes_functions_str)
        return FeatureCollection

    def return_type_for_collect_operation(self, attributes_functions_str):
        attributes_in_collect_arr = self.extract_collect_operation_attributes(attributes_functions_str)

        if self.geometry_field_name() not in attributes_in_collect_arr:
            return super(FeatureCollectionResource, self).return_type_for_collect_operation(attributes_functions_str)

        operated_attribute = attributes_in_collect_arr[-1]
        if not self.geometry_field_name() == operated_attribute:
            return FeatureCollection

        operation_in_collect_return_type = self.get_operation_in_collect_return_type(attributes_functions_str)
        if not issubclass(operation_in_collect_return_type, GEOSGeometry):
            return COLLECTION_TYPE

        if len(attributes_in_collect_arr) > 1:
            return FeatureCollection
        return GeometryCollection

    def return_type_for_specialized_operation(self, attributes_functions_str):
        return self.default_resource_representation()

    def return_type_for_union_operation(self, attributes_functions_str):
        geometry_field_type = type(self.field_for(self.geometry_field_name()))
        multi_object_class_for_geom_type = {
            PointField: MultiPoint,
            LineStringField: MultiLineString,
            PolygonField: MultiPolygon,
            MultiPointField: MultiPoint,
            MultiLineString: MultiLineString,
            MultiPolygonField: MultiPolygon,
            GEOSGeometry: MultiPolygon
        }
        return multi_object_class_for_geom_type[geometry_field_type]

    def return_type_for_make_line_operation(self, attributes_functions_str):
        return LineString

    def return_type_for_extent_operation(self, attributes_functions_str):
        return list

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
            serialized_data = self.get_object_serialized_by_only_attributes(attrs_str, spatial_objects)
            return RequiredObject(serialized_data,self.content_type_or_default_content_type(request), spatial_objects, 200)
        else:
            return self.required_object(request, spatial_objects)

    def required_context_for_specialized_operation(self, request, attributes_functions_str):
        context = self.get_context_for_specialized_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_union_operation(self, request, attributes_functions_str):
        context = self.get_context_for_union_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_extent_operation(self, request, attributes_functions_str):
        context = self.get_context_for_extent_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_make_line_operation(self, request, attributes_functions_str):
        context = self.get_context_for_make_line_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_object_for_extent_operation(self, request, attributes_functions_str):
        extent_dict = self.get_objects_from_extent_spatial_operation(attributes_functions_str)
        extent_dict['extent'] = extent_dict.pop(self.geometry_field_name() + '__extent')
        return self.required_object_for_aggregation_operation( request, extent_dict)

    def required_object_for_union_operation(self,request, attributes_functions_str):
        object_ = self.get_object_from_union_spatial_operation(attributes_functions_str)
        a_dictionary = json.loads(object_[self.geometry_field_name() + '__union'].geojson)

        return self.required_object_for_aggregation_operation(request, a_dictionary)

    def required_object_for_make_line_operation(self,request, attributes_functions_str):
        line = self.get_object_from_make_line_spatial_operation(attributes_functions_str)
        a_dictionary = json.loads(line[self.geometry_field_name() + '__makeline'].geojson)

        return self.required_object_for_aggregation_operation(request, a_dictionary)

    #todo: Define header Content-Type depending of which type is returned (FeatureCollection, buffer, dict, etc)
    def required_object_for_collect_operation(self, request, attributes_functions_str):
        collect_operation_snippet = self.remove_last_slash(attributes_functions_str)

        if self.path_has_projection(collect_operation_snippet):
            if self.projection_attrs_equals_collect_attrs(collect_operation_snippet):
                collect_operation_snippet = self.remove_projection_from_path(attributes_functions_str)

            else:
                message = 'Projection attributes list must be the same as collect operation attributes list'

                return self.required_object_for_invalid_sintax(attributes_functions_str, message)

        business_objects = self.get_objects_from_collect_operation(collect_operation_snippet)
        serialized_data = self.get_objects_serialized_by_collect_operation(collect_operation_snippet, business_objects)
        return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), business_objects, 200)

    def get_objects_from_join_operation(self, request, attributes_functions_str):
        join_operation = self.build_join_operation(request, attributes_functions_str)
        return self.join_feature_collection_on_dict_list(join_operation)

    def join_feature_collection_on_dict_list(self, join_operation):
        joined_data_list = []
        for original_feature in join_operation.left_join_data['features']:
            updated_feature = deepcopy(original_feature)
            updated_feature['properties']['__joined__'] = []

            for dict_to_join in join_operation.right_join_data:
                if updated_feature['properties'][join_operation.left_join_attr] == dict_to_join[join_operation.right_join_attr]:
                    updated_feature['properties']['__joined__'].append( deepcopy(dict_to_join) )

            # verify if the current feature was updated
            #if sorted(list(updated_feature['properties'].keys())) != sorted(list(original_feature['properties'].keys())):
            if len(updated_feature['properties']['__joined__']) > 0:
                joined_data_list.append(updated_feature)

        return {'type': 'FeatureCollection', 'features': joined_data_list}

    def get_objects_from_specialized_operation(self, attributes_functions_str):

        if self.path_has_url(attributes_functions_str):
            arr = self.attribute_functions_str_with_url_splitted_by_slash(attributes_functions_str)
        else:
            arr = attributes_functions_str.split('/')

        if  not self.path_has_geometry_attribute(arr[0]):
            arr = self.inject_geometry_attribute_in_spatial_operation_for_path(arr)

        return self.get_objects_from_spatial_operation(arr)

    def get_objects_from_extent_spatial_operation(self, attributes_functions_str):
        first_part_name = super(FeatureCollectionResource, self).get_operation_name_from_path(attributes_functions_str)

        if first_part_name == self.operation_controller.filter_collection_operation_name:
            filter_snippet = attributes_functions_str[:attributes_functions_str.index('/*')]
            queryset_or_model_class = self.get_objects_from_filter_operation(filter_snippet)

        elif first_part_name == self.operation_controller.offset_limit_collection_operation_name:
            offset_limit_snippet = attributes_functions_str[:attributes_functions_str.index('/*')]
            queryset_or_model_class = self.get_objects_from_offset_limit_operation(offset_limit_snippet)

        else:
            queryset_or_model_class = self.model_class().objects

        return queryset_or_model_class.aggregate(Extent(self.geometry_field_name()))

    def get_object_from_union_spatial_operation(self, attributes_functions_str):
        first_part_name = super(FeatureCollectionResource, self).get_operation_name_from_path(attributes_functions_str)

        if first_part_name == self.operation_controller.filter_collection_operation_name:
            filter_snippet = attributes_functions_str[:attributes_functions_str.index('/*')]
            queryset_or_model_class = self.get_objects_from_filter_operation(filter_snippet)

        elif first_part_name == self.operation_controller.offset_limit_collection_operation_name:
            offset_limit_snippet = attributes_functions_str[:attributes_functions_str.index('/*')]
            queryset_or_model_class = self.get_objects_from_offset_limit_operation(offset_limit_snippet)
        else:
            queryset_or_model_class = self.model_class().objects

        return queryset_or_model_class.aggregate(Union(self.geometry_field_name()))

    def get_object_from_make_line_spatial_operation(self, attributes_functions_str):
        first_part_name = super(FeatureCollectionResource, self).get_operation_name_from_path(attributes_functions_str)

        if first_part_name == self.operation_controller.filter_collection_operation_name:
            filter_snippet = attributes_functions_str[:attributes_functions_str.index('/*')]
            queryset_or_model_class = self.get_objects_from_filter_operation(filter_snippet)

        elif first_part_name == self.operation_controller.offset_limit_collection_operation_name:
            offset_limit_snippet = attributes_functions_str[:attributes_functions_str.index('/*')]
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

    def get_object_serialized_by_only_attributes(self, attribute_names_str, object):
        arr = []
        attribute_names_str_as_array = self.remove_last_slash(attribute_names_str).split(',')
        has_geo_field = self.geometry_field_name() in attribute_names_str_as_array

        for dic in object:
            a_dic = {}
            for att_name in attribute_names_str_as_array:
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
        if self.path_has_filter_operation(attributes_functions_str):
            objects = self.get_objects_from_filter_operation(attributes_functions_str)

        return objects

    def get_context_by_only_attributes(self, request, attributes_functions_str):
        context = super(FeatureCollectionResource, self).get_context_by_only_attributes(request, attributes_functions_str)
        if self.geometry_field_name() in context["@context"].keys():
            context["@context"].pop(self.geometry_field_name())
        return context

    def get_context_for_specialized_operation(self, request, attributes_functions_str):
        return self.get_context_for_filter_operation(request, attributes_functions_str)
        #operation_name = self.get_operation_name_from_path(attributes_functions_str)
        #resource_type = self.define_resource_representation_by_operation(request, operation_name)
        #context = self.get_context_for_operation_resource_type(attributes_functions_str, resource_type)
        #context["@context"].update(self.context_resource.attributes_contextualized_dict())
        #return context

    def get_context_for_union_operation(self, request, attributes_functions_str):
        return self.get_context_for_operation(request, attributes_functions_str)
        #resource_type_by_accept = self.resource_representation_or_default_resource_representation(request)
        #resource_type = resource_type_by_accept if resource_type_by_accept != self.default_resource_representation() else 'Feature'
        #return self.get_context_for_operation_resource_type(attributes_functions_str, resource_type)

    def get_context_for_extent_operation(self, request, attributes_functions_str):
        context = self.get_context_for_operation(request, attributes_functions_str)
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        context["@context"].update(self.context_resource.get_operation_return_type_term_definition(operation_name))
        return context

    def get_context_for_make_line_operation(self, request, attributes_functions_str):
        return self.get_context_for_operation(request, attributes_functions_str)
        #resource_type_by_accept = self.resource_representation_or_default_resource_representation(request)
        #resource_type = resource_type_by_accept if resource_type_by_accept != self.default_resource_representation() else LineString
        #return self.get_context_for_operation_resource_type(attributes_functions_str, resource_type)

    def get_context_for_collect_operation(self, request, attributes_functions_str):
        context = super(FeatureCollectionResource, self).get_context_for_collect_operation(request, attributes_functions_str)

        attrs = self.extract_collect_operation_attributes(attributes_functions_str)
        if self.geometry_field_name() not in attrs:
            return context

        operated_attribute = attrs[-1]
        if self.geometry_field_name() != operated_attribute:
            context["@context"].pop(self.geometry_field_name())
            context["@id"] = self.context_resource.get_vocabulary_for("Feature")
            return context

        oper_in_collect_return_type = self.get_operation_in_collect_return_type(attributes_functions_str)
        if not issubclass(oper_in_collect_return_type, GEOSGeometry):
            return context

        if len(attrs) > 1:
            context["@id"] = self.context_resource.get_vocabulary_for("Feature")
        else:
            context["@id"] = self.context_resource.get_vocabulary_for(GEOSGeometry)

        return context

    def get_context_for_attributes_in_collect_operation(self, request, attributes_functions_str):
        context = super(FeatureCollectionResource, self).get_context_for_attributes_in_collect_operation(request, attributes_functions_str)
        operation_in_collect_name = self.extract_collect_operation_snippet(attributes_functions_str).split('/')[2]
        oper_return_type = BaseOperationController().dict_all_operation_dict()[operation_in_collect_name].return_type
        if issubclass(oper_return_type, GEOSGeometry):
            context.pop(operation_in_collect_name)
        return context

    def get_png(self, queryset, request):
        geom_type = None
        wkt = 'GEOMETRYCOLLECTION('

        for i, e in enumerate(queryset):
            if isinstance(e, FeatureModel):
                wkt += e.get_spatial_object().wkt  # it is need to fix the case that the attribute is not called by geom

            else:
                geome = GEOSGeometry(json.dumps(e['geometry']))
                wkt +=  geome.wkt
                geom_type = geome.geom_type

            wkt += ',' if i != len(queryset) - 1 else ')'

        if len(queryset):
            if isinstance(queryset[0], FeatureModel):
                geom_type = queryset[0].get_spatial_object().geom_type
        else:
            geom_type = ''

        config = {'wkt': wkt, 'type': geom_type}
        style = self.get_style_file(request)

        if style is not None:
            config.update({
                'style': style,
                'deleteStyle': True
            })

        builder_png = BuilderPNG(config)

        return builder_png.generate()

    def get(self, request, format=None, *args, **kwargs):
        self.change_request_if_image_png_into_IRI(request)
        return super(FeatureCollectionResource,self).get(request, *args, **self.kwargs)