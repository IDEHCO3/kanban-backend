from hyper_resource.resources.AbstractResource import *
from hyper_resource.resources.SpatialResource import SpatialResource


class FeatureResource(SpatialResource):
    def __init__(self):
        super(FeatureResource, self).__init__()

    def default_resource_representation(self):
        return 'Feature'

    def dict_by_accept_resource_representation(self):
        dict = {
            CONTENT_TYPE_OCTET_STREAM: 'Geobuf'
        }

        return dict

    # Must be overridden
    def initialize_context(self):
        pass

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def is_spatial_attribute(self, attribute_name):
        return self.model.geo_field_name() == attribute_name.lower()

    def operations_with_parameters_type(self):
        return self.object_model.operations_with_parameters_type()

    def get_object_from_operation_attributes_functions_str_with_url(self, attributes_functions_str, request=None):
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
            attributes_functions_str = arr_of_two_url_and_param[0] + j + PARAM_SEPARATOR + arr_of_two_url_and_param[2]
        else:
            attributes_functions_str = arr_of_two_url_and_param[0] + j
        #external_etag = resp.headers['etag']
        #self.inject_e_tag(external_etag)
        return self.get_object_from_operation(attributes_functions_str)

    def get_object_from_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        a_value = self._execute_attribute_or_method(self.object_model, att_funcs[0], att_funcs[1:])

        if isinstance(a_value, GEOSGeometry):
            a_value = json.loads(a_value.geojson)
        elif isinstance(a_value, SpatialReference) or isinstance(a_value, OGRGeometry):
            a_value = { self.name_of_last_operation_executed: a_value.wkt.strip('\n')}
        elif isinstance(a_value, memoryview) or isinstance(a_value, buffer):
            a_value = a_value.hex()
        elif isinstance(a_value, bytes):
            a_value = a_value.decode()
        else:
            try:
                a_value = {self.name_of_last_operation_executed: str(json.loads(a_value))}
            except (json.decoder.JSONDecodeError, TypeError):
                a_value = {self.name_of_last_operation_executed: a_value}
        return a_value

    def operation_name_method_dic(self):
        dict = super(FeatureResource, self).operation_name_method_dic()
        dict.update({
            self.operation_controller.area_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.boundary_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.buffer_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.centroid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.contains_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.convex_hull_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.coord_seq_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.coords_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.count_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.crosses_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.crs_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.difference_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.dims_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.disjoint_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.distance_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.empty_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.envelope_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.equals_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.equals_exact_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.ewkb_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.ewkt_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.extend_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.extent_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.geojson_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.geom_type_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.geom_typeid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.get_coords_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.get_srid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.get_x_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.get_y_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.get_z_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.has_cs_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.hasz_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.hex_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.hexewkb_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.index_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.intersection_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.intersects_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.interpolate_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.json_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.kml_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.length_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.normalize_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.num_coords_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.num_geom_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.num_points_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.ogr_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.overlaps_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.point_on_surface_operation_name:  self.required_object_for_spatial_operation,
            self.operation_controller.relate_operation_name:            self.required_object_for_spatial_operation,
            self.operation_controller.relate_pattern_operation_name:    self.required_object_for_spatial_operation,
            self.operation_controller.ring_operation_name:              self.required_object_for_spatial_operation,
            self.operation_controller.simple_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.simplify_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.srid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.srs_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.sym_difference_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.touches_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.transform_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.union_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.valid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.valid_reason_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.within_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.wkb_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.wkt_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.x_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.y_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.z_operation_name: self.required_object_for_spatial_operation,
        })
        return dict

    def operation_name_context_dic(self):
        dict = super(FeatureResource, self).operation_name_context_dic()
        dict.update({
            self.operation_controller.area_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.boundary_operation_name:          self.required_context_for_operation,
            self.operation_controller.buffer_operation_name:            self.required_context_for_operation,
            self.operation_controller.centroid_operation_name:          self.required_context_for_operation,
            self.operation_controller.contains_operation_name:          self.required_context_for_non_spatial_return_operation,
            self.operation_controller.convex_hull_operation_name:       self.required_context_for_operation,
            self.operation_controller.coord_seq_operation_name:         self.required_context_for_non_spatial_return_operation,
            self.operation_controller.coords_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.count_operation_name:             self.required_context_for_non_spatial_return_operation,
            self.operation_controller.crosses_operation_name:           self.required_context_for_non_spatial_return_operation,
            self.operation_controller.crs_operation_name:               self.required_context_for_non_spatial_return_operation,
            self.operation_controller.difference_operation_name:        self.required_context_for_operation,
            self.operation_controller.dims_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.disjoint_operation_name:          self.required_context_for_non_spatial_return_operation,
            self.operation_controller.distance_operation_name:          self.required_context_for_non_spatial_return_operation,
            self.operation_controller.empty_operation_name:             self.required_context_for_non_spatial_return_operation,
            self.operation_controller.envelope_operation_name:          self.required_context_for_operation,
            self.operation_controller.equals_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.equals_exact_operation_name:      self.required_context_for_non_spatial_return_operation,
            self.operation_controller.ewkb_operation_name:              self.required_context_for_operation,
            self.operation_controller.ewkt_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.extent_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.geojson_operation_name:           self.required_context_for_non_spatial_return_operation,
            self.operation_controller.geom_type_operation_name:         self.required_context_for_non_spatial_return_operation,
            self.operation_controller.geom_typeid_operation_name:       self.required_context_for_non_spatial_return_operation,
            self.operation_controller.has_cs_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.hasz_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.hex_operation_name:               self.required_context_for_operation,
            self.operation_controller.hexewkb_operation_name:           self.required_context_for_operation,
            self.operation_controller.intersection_operation_name:      self.required_context_for_operation,
            self.operation_controller.intersects_operation_name:        self.required_context_for_non_spatial_return_operation,
            self.operation_controller.interpolate_operation_name:       self.required_context_for_operation,
            self.operation_controller.json_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.kml_operation_name:               self.required_context_for_non_spatial_return_operation,
            self.operation_controller.length_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.normalize_operation_name:         self.required_context_for_operation,
            self.operation_controller.num_coords_operation_name:        self.required_context_for_non_spatial_return_operation,
            self.operation_controller.num_geom_operation_name:          self.required_context_for_non_spatial_return_operation,
            self.operation_controller.num_points_operation_name:        self.required_context_for_non_spatial_return_operation,
            self.operation_controller.ogr_operation_name:               self.required_context_for_non_spatial_return_operation,
            self.operation_controller.overlaps_operation_name:          self.required_context_for_non_spatial_return_operation,
            self.operation_controller.point_on_surface_operation_name:  self.required_context_for_operation,
            self.operation_controller.relate_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.relate_pattern_operation_name:    self.required_context_for_non_spatial_return_operation,
            self.operation_controller.ring_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.simple_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.simplify_operation_name:          self.required_context_for_operation,
            self.operation_controller.srid_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.srs_operation_name:               self.required_context_for_non_spatial_return_operation,
            self.operation_controller.sym_difference_operation_name:    self.required_context_for_operation,
            self.operation_controller.touches_operation_name:           self.required_context_for_non_spatial_return_operation,
            self.operation_controller.transform_operation_name:         self.required_context_for_operation,
            self.operation_controller.union_operation_name:             self.required_context_for_operation,
            self.operation_controller.valid_operation_name:             self.required_context_for_non_spatial_return_operation,
            self.operation_controller.valid_reason_operation_name:      self.required_context_for_non_spatial_return_operation,
            self.operation_controller.within_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.wkb_operation_name:               self.required_context_for_operation,
            self.operation_controller.wkt_operation_name:               self.required_context_for_non_spatial_return_operation,
            self.operation_controller.x_operation_name:                 self.required_context_for_non_spatial_return_operation,
            self.operation_controller.y_operation_name:                 self.required_context_for_non_spatial_return_operation,
            self.operation_controller.z_operation_name:                 self.required_context_for_non_spatial_return_operation,
        })
        return dict

    def operation_name_return_type_dic(self):
        dicti = super(FeatureResource, self).operation_name_return_type_dic()
        dicti.update({
            self.operation_controller.area_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.boundary_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.buffer_operation_name:            self.return_type_for_specialized_operation,
            self.operation_controller.centroid_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.contains_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.convex_hull_operation_name:       self.return_type_for_generic_spatial_operation,
            self.operation_controller.coord_seq_operation_name:         self.return_type_for_generic_spatial_operation,
            self.operation_controller.coords_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.count_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.crosses_operation_name:           self.return_type_for_generic_spatial_operation,
            self.operation_controller.crs_operation_name:               self.return_type_for_generic_spatial_operation,
            self.operation_controller.difference_operation_name:        self.return_type_for_specialized_operation,
            self.operation_controller.dims_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.disjoint_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.distance_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.empty_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.envelope_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.equals_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.equals_exact_operation_name:      self.return_type_for_generic_spatial_operation,
            self.operation_controller.ewkb_operation_name:              self.return_type_for_geometric_representation_operation,
            self.operation_controller.ewkt_operation_name:              self.return_type_for_geometric_representation_operation,
            self.operation_controller.extend_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.extent_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.geojson_operation_name:           self.return_type_for_geometric_representation_operation,
            self.operation_controller.geom_type_operation_name:         self.return_type_for_generic_spatial_operation,
            self.operation_controller.geom_typeid_operation_name:       self.return_type_for_generic_spatial_operation,
            self.operation_controller.get_coords_operation_name:        self.return_type_for_generic_spatial_operation,
            self.operation_controller.get_srid_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.get_x_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.get_y_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.get_z_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.has_cs_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.hasz_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.hex_operation_name:               self.return_type_for_geometric_representation_operation,
            self.operation_controller.hexewkb_operation_name:           self.return_type_for_geometric_representation_operation,
            self.operation_controller.index_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.intersection_operation_name:      self.return_type_for_specialized_operation,
            self.operation_controller.intersects_operation_name:        self.return_type_for_generic_spatial_operation,
            self.operation_controller.interpolate_operation_name:       self.return_type_for_generic_spatial_operation,
            self.operation_controller.json_operation_name:              self.return_type_for_geometric_representation_operation,
            self.operation_controller.kml_operation_name:               self.return_type_for_generic_spatial_operation,
            self.operation_controller.length_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.normalize_operation_name:         self.return_type_for_generic_spatial_operation,
            self.operation_controller.num_coords_operation_name:        self.return_type_for_generic_spatial_operation,
            self.operation_controller.num_geom_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.num_points_operation_name:        self.return_type_for_generic_spatial_operation,
            self.operation_controller.ogr_operation_name:               self.return_type_for_geometric_representation_operation,
            self.operation_controller.overlaps_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.point_on_surface_operation_name:  self.return_type_for_generic_spatial_operation,
            self.operation_controller.relate_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.relate_pattern_operation_name:    self.return_type_for_generic_spatial_operation,
            self.operation_controller.ring_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.simple_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.simplify_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.srid_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.srs_operation_name:               self.return_type_for_generic_spatial_operation,
            self.operation_controller.sym_difference_operation_name:    self.return_type_for_specialized_operation,
            self.operation_controller.touches_operation_name:           self.return_type_for_generic_spatial_operation,
            self.operation_controller.transform_operation_name:         self.return_type_for_specialized_operation,
            self.operation_controller.union_operation_name:             self.return_type_for_specialized_operation,
            self.operation_controller.valid_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.valid_reason_operation_name:      self.return_type_for_generic_spatial_operation,
            self.operation_controller.within_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.wkb_operation_name:               self.return_type_for_geometric_representation_operation,
            self.operation_controller.wkt_operation_name:               self.return_type_for_geometric_representation_operation,
            self.operation_controller.x_operation_name:                 self.return_type_for_generic_spatial_operation,
            self.operation_controller.y_operation_name:                 self.return_type_for_generic_spatial_operation,
            self.operation_controller.z_operation_name:                 self.return_type_for_generic_spatial_operation,
        })
        return dicti

    def operation_name_resource_representation_dic(self):
        dicti = super(FeatureResource, self).operation_name_resource_representation_dic()
        dicti.update({
            self.operation_controller.area_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.boundary_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.buffer_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.centroid_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.contains_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.convex_hull_operation_name:       self.define_resource_representation_by_operation,
            self.operation_controller.coord_seq_operation_name:         self.define_resource_representation_by_operation,
            self.operation_controller.coords_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.count_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.crosses_operation_name:           self.define_resource_representation_by_operation,
            self.operation_controller.crs_operation_name:               self.define_resource_representation_by_operation,
            self.operation_controller.difference_operation_name:        self.define_resource_representation_by_operation,
            self.operation_controller.dims_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.disjoint_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.distance_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.empty_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.envelope_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.equals_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.equals_exact_operation_name:      self.define_resource_representation_by_operation,
            self.operation_controller.ewkb_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.ewkt_operation_name:              self.define_resource_representation_by_str_return_type_operation,
            self.operation_controller.extend_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.extent_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.geojson_operation_name:           self.define_resource_representation_by_str_return_type_operation,
            self.operation_controller.geom_type_operation_name:         self.define_resource_representation_by_operation,
            self.operation_controller.geom_typeid_operation_name:       self.define_resource_representation_by_operation,
            self.operation_controller.get_coords_operation_name:        self.define_resource_representation_by_operation,
            self.operation_controller.get_srid_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.get_x_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.get_y_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.get_z_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.has_cs_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.hasz_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.hex_operation_name:               self.define_resource_representation_by_hex_operation,
            self.operation_controller.hexewkb_operation_name:           self.define_resource_representation_by_operation,
            self.operation_controller.index_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.intersection_operation_name:      self.define_resource_representation_by_operation,
            self.operation_controller.intersects_operation_name:        self.define_resource_representation_by_operation,
            self.operation_controller.interpolate_operation_name:       self.define_resource_representation_by_operation,
            self.operation_controller.json_operation_name:              self.define_resource_representation_by_str_return_type_operation,
            self.operation_controller.kml_operation_name:               self.define_resource_representation_by_operation,
            self.operation_controller.length_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.normalize_operation_name:         self.define_resource_representation_by_operation,
            self.operation_controller.num_coords_operation_name:        self.define_resource_representation_by_operation,
            self.operation_controller.num_geom_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.num_points_operation_name:        self.define_resource_representation_by_operation,
            self.operation_controller.ogr_operation_name:               self.define_resource_representation_by_str_return_type_operation,
            self.operation_controller.overlaps_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.point_on_surface_operation_name:  self.define_resource_representation_by_operation,
            self.operation_controller.relate_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.relate_pattern_operation_name:    self.define_resource_representation_by_operation,
            self.operation_controller.ring_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.simple_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.simplify_operation_name:          self.define_resource_representation_by_operation,
            self.operation_controller.srid_operation_name:              self.define_resource_representation_by_operation,
            self.operation_controller.srs_operation_name:               self.define_resource_representation_by_operation,
            self.operation_controller.sym_difference_operation_name:    self.define_resource_representation_by_operation,
            self.operation_controller.touches_operation_name:           self.define_resource_representation_by_operation,
            self.operation_controller.transform_operation_name:         self.define_resource_representation_by_operation,
            self.operation_controller.union_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.valid_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.valid_reason_operation_name:      self.define_resource_representation_by_operation,
            self.operation_controller.within_operation_name:            self.define_resource_representation_by_operation,
            self.operation_controller.wkb_operation_name:               self.define_resource_representation_by_operation,
            self.operation_controller.wkt_operation_name:               self.define_resource_representation_by_str_return_type_operation,
            self.operation_controller.x_operation_name:                 self.define_resource_representation_by_operation,
            self.operation_controller.y_operation_name:                 self.define_resource_representation_by_operation,
            self.operation_controller.z_operation_name:                 self.define_resource_representation_by_operation,
        })
        return dicti

    def required_object_for_simple_path(self, request):
        serializer = self.serializer_class(self.object_model)
        return RequiredObject(serializer.data, self.content_type_or_default_content_type(request), self.object_model, 200)

    def required_object_for_only_attributes(self, request, attributes_functions_str):
        required_object = super(FeatureResource, self).required_object_for_only_attributes(request, attributes_functions_str)
        required_object.content_type = self.define_content_type_by_only_attributes(request, attributes_functions_str)
        return required_object
        #object = self.get_object_by_only_attributes(attributes_functions_str)
        #serialized_data = self.get_object_serialized_by_only_attributes(attributes_functions_str, object)
        #return RequiredObject(serialized_data, content_type, object,  200)

    def required_object_for_spatial_operation(self, request, attributes_functions_str):
        content_type = self.content_type_or_default_content_type(request)
        if self.path_has_url(attributes_functions_str.lower()):
            result = self.get_object_from_operation_attributes_functions_str_with_url(attributes_functions_str, request)
        else:
            result = self.get_object_from_operation(self.remove_last_slash(attributes_functions_str))

        if isinstance(result, memoryview) or isinstance(result, buffer) or isinstance(result, bytes):
            content_type = CONTENT_TYPE_OCTET_STREAM

        return RequiredObject(result, content_type, self.object_model, 200)

    def get_objects_from_join_operation(self, request, attributes_functions_str):
        join_operation = self.build_join_operation(request, attributes_functions_str)

        if type(join_operation.right_join_data) is list:
            return self.join_feature_on_list_response(join_operation)
        return self.join_feature_on_dict_response(join_operation)

    def join_feature_on_dict_response(self, join_operation):
        if  join_operation.left_join_data['properties'][ join_operation.left_join_attr ] != join_operation.right_join_data[ join_operation.right_join_attr ]:
            return None # the datas isn't 'joinable'

        join_operation.left_join_data["properties"]["__joined__"] = []
        join_operation.left_join_data["properties"]["__joined__"].append(join_operation.right_join_data)
        return deepcopy(join_operation.left_join_data)

    def join_feature_on_list_response(self, join_operation):
        join_operation.left_join_data['properties']['__joined__'] = []

        for dicti in join_operation.right_join_data:
            if join_operation.left_join_data['properties'][join_operation.left_join_attr] == dicti[join_operation.right_join_attr]:
                join_operation.left_join_data['properties']['__joined__'].append(dicti)

        if len(join_operation.left_join_data['properties']['__joined__']) == 0:
            return None
        return join_operation.left_join_data

    def get_context_for_join_operation(self, request, attributes_functions_str):
        geometric_uri, join_attr, alphanumeric_uri = self.split_join_uri(request, attributes_functions_str)
        return self.get_dict_from_response( requests.options(geometric_uri) )

        #todo: code for 'join' full context - DO NOT DELETE
        '''
        resource_type = self.resource_type_or_default_resource_type(request)
        context = self.context_resource.get_resource_type_identification(resource_type)
        context["hydra:supportedOperations"] = self.context_resource.supportedOperationsFor(self.object_model, resource_type)
        context["@context"] = self.context_resource.get_context_to_operation(self.operation_controller.join_operation_name)["@context"]
        context["@context"].update( self.get_merged_acontext_from_join_operation(request, attributes_functions_str) )

        return context
        '''

    #todo: code for 'join' full context - DO NOT DELETE
    def get_merged_acontext_from_join_operation(self, request, attributes_functions_str):
        geometric_uri, join_attr, alphanumeric_uri = self.split_join_uri(request, attributes_functions_str)

        geometric_acontext = self.get_dict_from_response( requests.options(geometric_uri) )["@context"]
        alphanumeric_acontext = self.get_dict_from_response( requests.options(alphanumeric_uri) )["@context"]

        alpha_acontext_renamed_keys = {}
        for k, v in alphanumeric_acontext.items():
            if k in geometric_acontext.keys():
                alpha_acontext_renamed_keys[alphanumeric_uri + "/" + k] = v
            else:
                alpha_acontext_renamed_keys[k] = v

        geometric_acontext.update(alpha_acontext_renamed_keys)

        return geometric_acontext
        #if set(geometric_context.keys()).intersection( set(alphanumeric_context.keys()) ):

    #todo: code for 'join' full context - DO NOT DELETE
    def add_context_to_joined_external_attributes(self, external_attributes_context):
        pass

    def required_context_for_non_spatial_return_operation(self, request, attributes_functions_str):
        context = self.get_context_for_non_spatial_return_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def get_context_by_only_attributes(self, request, attributes_functions_str):
        context = super(FeatureResource, self).get_context_by_only_attributes(request, attributes_functions_str)
        if self.geometry_field_name() in context["@context"].keys():
            context["@context"].pop(self.geometry_field_name())
        return context

    def get_context_for_non_spatial_return_operation(self, request, attributes_functions_str):
        context = self.get_context_for_operation(request, attributes_functions_str)
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        context["@context"].update(self.context_resource.get_operation_return_type_term_definition(operation_name))
        return context

    def return_type_by_only_attributes(self, attributes_functions_str):
        attrs = self.remove_last_slash(attributes_functions_str).split(",")
        if len(attrs) > 1:
            if self.geometry_field_name() in attrs:
                return "Feature"
            return object

        object_model = self.get_object(self.kwargs)
        attr_val = getattr(object_model, attrs[0])

        if attrs[0] == self.geometry_field_name():
            return attr_val.geom_type
        return type(attr_val)

    def return_type_for_specialized_operation(self, attributes_functions_str):
        '''
        Return type depends on specific geometry type
        '''
        model_object = self.get_object(self.kwargs)
        geom_val = getattr(model_object, self.geometry_field_name())
        operation_name = self.get_operation_name_from_path(attributes_functions_str)

        if self.path_has_url(attributes_functions_str):
            _ , url_external_resource, parameters_list = self.attributes_functions_splitted_by_url(attributes_functions_str)
            response = requests.get(url_external_resource)

            if response.status_code in[400, 401, 404, 500]:
                return None #operation_params = GEOSGeometry(Point([0, 0]))

            operation_params = [response.text]
            if parameters_list is not None:
                operation_params.append(parameters_list)

        else:
            operation_params = self.remove_last_slash(attributes_functions_str).split("/")[1:]
        return type( self._execute_attribute_or_method(geom_val, operation_name, operation_params) )

    def return_type_for_generic_spatial_operation(self, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        return self.operation_controller.dict_all_operation_dict()[operation_name].return_type

    # wkb, ewkb, hex, hexewkb, wkt, ogr, json, geojson, ogr operations returns an binary or text representation of an geometry
    def return_type_for_geometric_representation_operation(self, attributes_functions_str):
        model_object = self.get_object(self.kwargs)
        geom_val = getattr(model_object, self.geometry_field_name())
        return type(geom_val)

    def get_object_serialized_by_only_attributes(self, attributes_functions_str, object):
        attrs_arr = self.remove_last_slash(attributes_functions_str).split(',')
        serialized_object = {}

        for attr_name, attr_val in object.items():
            if attr_name == self.geometry_field_name():
                serialized_object[attr_name] = json.loads(object[attr_name].geojson)
            else:
                serialized_object[attr_name] = object[attr_name]

        if self.geometry_field_name() in attrs_arr:
            if len(attrs_arr) > 1:
                return self.dict_as_geojson(serialized_object)
            else:
                return serialized_object[self.geometry_field_name()]
        return serialized_object

    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.get_object(kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        self.inject_e_tag()
        #self.e_tag = str(hash(self.object_model))

        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if self.is_simple_path(attributes_functions_str):
            self.add_allowed_methods(['delete', 'put'])
            return self.required_object_for_simple_path(request)

        if self.path_has_only_attributes(attributes_functions_str):
            return self.required_object_for_only_attributes(request, attributes_functions_str)

        res = self.get_required_object_from_method_to_execute(request, attributes_functions_str)
        if res is None:
            return self.required_object_for_invalid_sintax(attributes_functions_str)
        return res

    def default_content_type(self):
        return CONTENT_TYPE_GEOJSON#self.temporary_content_type if self.temporary_content_type is not None else CONTENT_TYPE_GEOJSON

    def define_resource_representation_by_only_attributes(self, request, attributes_functions_str):
        attrs_functs_arr = self.remove_last_slash(attributes_functions_str).split(',')
        r_type = self.resource_representation_or_default_resource_representation(request)
        if r_type != self.default_resource_representation():
            return r_type if self.geometry_field_name() in attrs_functs_arr else bytes

        if len(attrs_functs_arr) == 1:
            # the field type has priority over default resource type
            return type(self.field_for(attrs_functs_arr[0]))

        return r_type if self.geometry_field_name() in attrs_functs_arr else 'Thing'

    def define_content_type_by_only_attributes(self, request, attributes_functions_str):
        if self.path_has_projection(attributes_functions_str):
            attrs_functs_arr = self.extract_projection_attributes(attributes_functions_str)
        else:
            attrs_functs_arr = self.remove_last_slash(attributes_functions_str).split(',')
        content_type_by_accept = self.content_type_or_default_content_type(request)

        # if 'Accept' is application/octet-stream, image/png, etc ...
        if content_type_by_accept != self.default_content_type():
            return content_type_by_accept

        if self.geometry_field_name() in attrs_functs_arr:
            return self.default_content_type()
        return CONTENT_TYPE_JSON

    def define_content_type_by_operation(self, request, operation_name):
        content_type_by_accept = self.content_type_or_default_content_type(request)
        oper_ret_type = self.operation_controller.dict_all_operation_dict()[operation_name].return_type

        if content_type_by_accept != self.default_content_type():
            return content_type_by_accept

        if issubclass(oper_ret_type, GEOSGeometry):
            return self.default_content_type()
        return CONTENT_TYPE_JSON

    def define_resource_representation_by_operation(self, request, attributes_functions_str):
        operation_return_type = self.execute_method_to_get_return_type_from_operation(attributes_functions_str)
        res_type_by_accept = self.resource_representation_or_default_resource_representation(request)

        if operation_return_type == GEOSGeometry:
            return res_type_by_accept
        elif type(operation_return_type) is not str and issubclass(operation_return_type, GEOSGeometry):
            return res_type_by_accept if res_type_by_accept != self.default_resource_representation() else operation_return_type
        else:
            res_type_by_accept = bytes if res_type_by_accept == 'Geobuf' else res_type_by_accept

        return operation_return_type if res_type_by_accept == self.default_resource_representation() else res_type_by_accept

    def define_resource_representation_by_wkt_operation(self, request, attributes_functions_str):
        '''
        WKT returns an string representation of a geometry
        '''
        resource_representation_by_accept = self.resource_representation_or_default_resource_representation(request)
        if resource_representation_by_accept == self.default_resource_representation():
            return str

    def define_resource_representation_by_ewkt_operation(self, request, attributes_functions_str):
        '''
        EWKT returns an string representation of a geometry
        '''
        resource_representation_by_accept = self.resource_representation_or_default_resource_representation(request)
        if resource_representation_by_accept == self.default_resource_representation():
            return str

    def define_resource_representation_by_hex_operation(self, request, attributes_functions_str):
        '''
        EWKT returns an string representation of a geometry
        '''
        resource_representation_by_accept = self.resource_representation_or_default_resource_representation(request)
        if resource_representation_by_accept == self.default_resource_representation():
            return bytes

    def define_resource_representation_by_str_return_type_operation(self, request, attributes_functions_str):
        '''
        WKT, ORG, EWKT, GEOJSON, JSON operations returns an string representation of a geometry
        '''
        resource_representation_by_accept = self.resource_representation_or_default_resource_representation(request)
        if resource_representation_by_accept == self.default_resource_representation():
            return str

    def get(self, request, format=None, *args, **kwargs):
        self.change_request_if_image_png_into_IRI(request)
        return super(FeatureResource,self).get(request, *args, **self.kwargs)
