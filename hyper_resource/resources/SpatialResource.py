
import json

from django.contrib.gis.geos import GEOSGeometry, GeometryCollection

from rest_framework.response import Response

from hyper_resource.resources.AbstractResource import AbstractResource


class SpatialResource(AbstractResource):
    def __init__(self):
        super(SpatialResource, self).__init__()
        self.iri_style = ''

    def spatial_field_name(self):
        return self.serializer_class.Meta.geo_field

    def attribute_names_to_web(self):
        alpha_attrs_names = super(SpatialResource, self).attribute_names_to_web()
        alpha_attrs_names.append(self.serializer_class.Meta.geo_field)
        return alpha_attrs_names

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
            parameters_type = self.operations_with_parameters_type()[attribute_or_function_name].get_parameters()

            for i in range(len(parameters)):
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

    def options(self, request, *args, **kwargs):
        required_object = self.basic_options(request, *args, **kwargs)
        if required_object.status_code == 200:
            response = Response(required_object.representation_object, content_type=required_object.content_type,
                                status=200)
            self.add_options_headers(request, response)
        else:
            response = Response(data={"This request is not supported": self.kwargs.get("attributes_functions", None)},
                                status=required_object.status_code)
        return response

    def head(self, request, *args, **kwargs):
        if self.is_simple_path(self.kwargs.get('attributes_functions')):
            self.add_allowed_methods(['delete', 'put'])
        return super(SpatialResource, self).head(request, *args, **kwargs)
