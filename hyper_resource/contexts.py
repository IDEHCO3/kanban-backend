# coding: utf-8
from django.contrib.gis.db import models
from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.db.models import LineStringField
from django.contrib.gis.db.models import MultiLineStringField
from django.contrib.gis.db.models import MultiPointField
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models import PolygonField
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import GEOSGeometry, Point, Polygon, MultiPolygon,LineString, MultiLineString, MultiPoint, GeometryCollection
from datetime import date, datetime
from time import *
from copy import deepcopy

from django.contrib.gis.geos.prepared import PreparedGeometry
from django.db.models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from hyper_resource.models import *
from hyper_resource.resources import FeatureResource
from hyper_resource.resources.AbstractResource import *
from hyper_resource.resources.AbstractCollectionResource import GROUP_BY_SUM_PROPERTY_NAME


class Reflection:
    def superclass(a_class):
        return a_class.__base__

    def superclasses(a_class):
        return a_class.__bases__

    def operation_names(a_class):
        return [method for method in dir(a_class) if
                callable(getattr(a_class, method)) and a_class.is_not_private(method)]

VOCABULARY ={
    BooleanField: 'http://schema.org/Boolean',
    bool: 'https://schema.org/Boolean',
    True: 'https://schema.org/Boolean',
    False: 'https://schema.org/Boolean',
    FloatField: 'https://schema.org/Float',
    float: 'https://schema.org/Float',
    ForeignKey: 'http://schema.org/URL',
    IntegerField: 'https://schema.org/Integer',
    DecimalField: 'https://schema.org/Float',
    AutoField: 'https://schema.org/identifier',
    int: 'https://schema.org/Integer',
    CharField: 'https://schema.org/Text',
    TextField: 'https://schema.org/Text',
    str: 'https://schema.org/Text',
    DateField: 'http://schema.org/Date',
    date: 'http://schema.org/Date',
    DateTimeField: 'http://schema.org/DateTime',
    datetime: 'http://schema.org/DateTime',
    TimeField: 'http://schema.org/Time',
    Model: 'https://purl.org/geojson/vocab#Feature',
    tuple: 'https://schema.org/ItemList',
    list: 'https://schema.org/ItemList',

    Q: 'http://extension.schema.org/expression',
    bytes: 'https://extension.schema.org/binary',
    object: 'https://schema.org/Thing',
    'Collection': 'http://www.w3.org/ns/hydra/core#Collection',
    'Link': "http://www.w3.org/ns/hydra/core#Link",
    GROUP_BY_SUM_PROPERTY_NAME: 'https://schema.org/Float',
    "hydra": "http://www.w3.org/ns/hydra/core#",

    'nome': 'https://schema.org/name',
    'name': 'https://schema.org/name',
    'nomeAbrev': 'https://schema.org/alternateName',
    'responsible': 'http://schema.org/accountablePerson',
    'usuario': 'http://schema.org/Person',
    'user': 'http://schema.org/Person',

    'FeatureCollection': 'https://purl.org/geojson/vocab#FeatureCollection',
    FeatureCollection: 'https://purl.org/geojson/vocab#FeatureCollection',
    'Feature': 'https://purl.org/geojson/vocab#Feature',
    FeatureResource: 'https://purl.org/geojson/vocab#Feature',
    GeometryField: 'https://purl.org/geojson/vocab#geometry',
    PointField: 'https://purl.org/geojson/vocab#Point',
    LineStringField: 'https://purl.org/geojson/vocab#LineString',
    PolygonField: 'https://purl.org/geojson/vocab#Polygon',
    MultiPolygonField: 'https://purl.org/geojson/vocab#MultiPolygon',
    MultiLineStringField: 'https://purl.org/geojson/vocab#MultiLineString',
    MultiPointField: 'https://purl.org/geojson/vocab#MultiPoint',

    MultiPolygon: 'https://purl.org/geojson/vocab#MultiPolygon',
    'MultiPolygon': 'https://purl.org/geojson/vocab#MultiPolygon',
    Polygon: 'https://purl.org/geojson/vocab#Polygon',
    'Polygon': 'https://purl.org/geojson/vocab#Polygon',
    LineString: 'https://purl.org/geojson/vocab#LineString',
    'LineString': 'https://purl.org/geojson/vocab#LineString',
    Point: 'https://purl.org/geojson/vocab#Point',
    'Point': 'https://purl.org/geojson/vocab#Point',
    GEOSGeometry: 'https://purl.org/geojson/vocab#geometry',
    'GEOSGeometry': 'https://purl.org/geojson/vocab#geometry',
    OGRGeometry: 'https://purl.org/geojson/vocab#geometry',
    'OGRGeometry': 'https://purl.org/geojson/vocab#geometry',
    MultiLineString: 'https://purl.org/geojson/vocab#MultiLineString',
    'MultiLineString': 'https://purl.org/geojson/vocab#MultiLineString',
    MultiPoint: 'https://purl.org/geojson/vocab#MultiPoint',
    'MultiPoint': 'https://purl.org/geojson/vocab#MultiPoint',
    GeometryCollection: 'https://purl.org/geojson/vocab#GeometryCollection',
    'GeometryCollection': 'https://purl.org/geojson/vocab#GeometryCollection',
    SpatialReference: 'https://purl.org/geojson/vocab#SpatialReference',
    'SpatialReference': 'https://purl.org/geojson/vocab#SpatialReference',

    # Collection
    'filter': 'http://172.30.10.86/api/operations-list/collection-operation-interface-list/1/',
    'map': 'http://opengis.org/operations/map',
    'annotate': 'http://opengis.org/operations/annotate',
    'group-by': "http://172.30.10.86/api/operations-list/collection-operation-interface-list/6/",
    'group-by-sum': 'http://172.30.10.86/api/operations-list/collection-operation-interface-list/10/',
    'group-by-count': 'http://172.30.10.86/api/operations-list/collection-operation-interface-list/7/',
    'distinct': 'http://172.30.10.86/api/operations-list/collection-operation-interface-list/5/',
    'count-resource': 'http://172.30.10.86/api/operations-list/collection-operation-interface-list/count-resource/',
    'resource-quantity': "https://schema.org/Integer",
    'collect': 'http://172.30.10.86/api/operations-list/collection-operation-interface-list/2/',
    'join': 'http://172.30.10.86/api/operations-list/object-operations-interface-list/1/',
    'projection': 'http://172.30.10.86/api/operations-list/object-operations-interface-list/2/',
    'make_line': 'http://172.30.10.86/api/operations-list/spatial-collection-operation-interface-list/30',
    'count_elements': 'http://opengis.org/operations/count_elements',
    'offset-limit': "http://172.30.10.86/api/operations-list/collection-operation-interface-list/4",
    'distance_lte': 'http://opengis.org/operations/distance_lte',
    'area': "http://172.30.10.86/api/operations-list/spatial-operation-interface-list/77",
    'boundary': 'http://172.30.10.86/api/operations-list/spatial-operation-interface-list/78',
    'buffer': 'http://172.30.10.86/api/operations-list/spatial-operation-interface-list/79',
    'centroid': 'http://opengis.org/operations/centroid', 'contains': 'http://opengis.org/operations/contains',
    'convex_hull': 'http://opengis.org/operations/convex_hull',
    'coord_seq': 'http://opengis.org/operations/coord_seq',
    'coords': 'https://purl.org/geojson/vocab#coordinates',
    'count': 'http://opengis.org/operations/count',
    'crosses': 'http://opengis.org/operations/crosses',
    'crs': 'http://opengis.org/operations/crs',
    'difference': 'http://opengis.org/operations/difference',
    'dims': 'http://opengis.org/operations/dims',
    'disjoint': 'http://opengis.org/operations/disjoint',
    'distance': 'http://opengis.org/operations/distance',
    'empty': 'http://opengis.org/operations/empty',
    'envelope': 'http://opengis.org/operations/envelope',
    'equals': 'http://opengis.org/operations/equals',
    'equals_exact': 'http://opengis.org/operations/equals_exact',
    'ewkb': 'http://opengis.org/operations/ewkb',
    'ewkt': 'http://opengis.org/operations/ewkt',
    'extend': 'http://opengis.org/operations/extend',
    'extent': 'http://opengis.org/operations/extent',
    'geojson': 'http://opengis.org/operations/geojson',
    'geom_type': 'http://opengis.org/operations/geom_type',
    'geom_typeid': 'http://opengis.org/operations/geom_typeid',
    'get_coords': 'http://opengis.org/operations/get_coords',
    'get_srid': 'http://opengis.org/operations/get_srid',
    'get_x': 'http://opengis.org/operations/get_x',
    'get_y': 'http://opengis.org/operations/get_y',
    'get_z': 'http://opengis.org/operations/get_z',
    'has_cs': 'http://opengis.org/operations/has_cs',
    'hasz': 'http://opengis.org/operations/hasz',
    'hex': 'http://opengis.org/operations/hex',
    'hexewkb': 'http://opengis.org/operations/hexewkb',
    'index': 'http://opengis.org/operations/index',
    'intersection': 'http://opengis.org/operations/intersection',
    'intersects': 'http://opengis.org/operations/intersects',
    'interpolate': 'http://opengis.org/operations/interpolate',
    'json': 'http://opengis.org/operations/json',
    'kml': 'http://opengis.org/operations/kml',
    'length': 'http://opengis.org/operations/length',
    'normalize': 'http://opengis.org/operations/normalize',
    'num_coords': 'http://opengis.org/operations/num_coords',
    'num_geom': 'http://opengis.org/operations/num_geom',
    'num_s': 'http://opengis.org/operations/num_s',
    'num_points': 'http://opengis.org/operations/num_points',
    'point_on_surface': 'http://opengis.org/operations/point_on_surface',
    'ogr': 'http://opengis.org/operations/ogr',
    'overlaps': 'http://opengis.org/operations/overlaps',
    '_on_surface': 'http://opengis.org/operations/_on_surface',
    'pop': 'http://opengis.org/operations/pop',
    'prepared': 'http://opengis.org/operations/prepared',
    'relate': 'http://opengis.org/operations/relate',
    'relate_pattern': 'http://opengis.org/operations/relate_pattern',
    'ring': 'http://opengis.org/operations/ring',
    'set_coords': 'http://opengis.org/operations/set_coords',
    'set_srid': 'http://opengis.org/operations/set_srid',
    'set_x': 'http://opengis.org/operations/set_x',
    'set_y': 'http://opengis.org/operations/set_y',
    'set_z': 'http://opengis.org/operations/set_z',
    'simple': 'http://opengis.org/operations/simple',
    'simplify': 'http://opengis.org/operations/simplify',
    'srid': 'http://opengis.org/operations/srid',
    'srs': 'http://opengis.org/operations/srs',
    'sym_difference': 'http://opengis.org/operations/sym_difference',
    'touches': 'http://opengis.org/operations/touches',
    'transform': 'http://opengis.org/operations/transform',
    'tuple': 'http://opengis.org/operations/tuple',
    'union': 'http://opengis.org/operations/union',
    'valid': 'http://opengis.org/operations/valid',
    'valid_reason': 'http://opengis.org/operations/valid_reason',
    'within': 'http://opengis.org/operations/within',
    'wkb': 'http://opengis.org/operations/wkb',
    'wkt': 'http://opengis.org/operations/wkt',
    'x': 'http://opengis.org/operations/x',
    'y': 'http://opengis.org/operations/y',
    'z': 'http://opengis.org/operations/z',

    'distance_gt': 'http://opengis.org/operations/distance_gt',
    'overlaps-right': 'http://opengis.org/operations/overlaps-right',
    'contained': 'http://opengis.org/operations/contained',
    'distance_lt': 'http://opengis.org/operations/distance_lt',
    'dwithin': 'http://opengis.org/operations/dwithin',
    'bboverlaps': 'http://opengis.org/operations/bboverlaps',
    'bbcontains': 'http://opengis.org/operations/bbcontains',
    'distance_gte': 'http://opengis.org/operations/distance_gte',
    'overlaps-below': 'http://opengis.org/operations/overlaps-below',
    'overlaps-above': 'http://opengis.org/operations/overlaps-above',
    'overlaps-left': 'http://opengis.org/operations/overlaps-left',
    'contains-properly': 'http://opengis.org/operations/contains-properly',
    'isvalid': 'http://opengis.org/operations/isvalid',
    'right': 'http://opengis.org/operations/right',
    'exact': 'http://opengis.org/operations/exact',
    'covers': 'http://opengis.org/operations/covers',
    'strictly_below': 'http://opengis.org/operations/strictly_below',
    'left': 'http://opengis.org/operations/left',
    'same_as': 'http://opengis.org/operations/same_as',
    'coveredby': 'http://opengis.org/operations/coveredby',
    'strictly_above': 'http://opengis.org/operations/strictly_above',
    'operation': 'http://www.w3.org/ns/hydra/core#operation',
    property: 'http://www.w3.org/ns/hydra/core#property',
    'EntryPoint': 'http://www.w3.org/ns/hydra/core#entrypoint',
    'Tiff': "https://schema.org/ImageObject",
    GDALRaster: "https://schema.org/ImageObject",
    RasterField: "https://schema.org/ImageObject"
}

OPERATION_VOCABULARY = {
    str: ["http://172.30.10.86/api/operations-list/string-operation-interface-list"],
    'str': ["http://172.30.10.86/api/operations-list/string-operation-interface-list"],
    CharField: ["http://172.30.10.86/api/operations-list/string-operation-interface-list"],
    date: ["http://172.30.10.86/api/operations-list/date-operation-interface-list"],
    GEOSGeometry: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    GeometryField: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    GeometryCollection: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    PointField: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    Point: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    MultiPointField: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    MultiPoint: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    LineStringField: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    LineString: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    MultiLineStringField: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    MultiLineString: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    PolygonField: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    Polygon: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    MultiPolygonField: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"],
    MultiPolygon: ["http://172.30.10.86/api/operations-list/spatial-operation-interface-list"]
}

def vocabulary(a_key):
    return VOCABULARY.get(a_key) or None

def operation_vocabulary(a_key):
    return OPERATION_VOCABULARY.get(a_key) or None


class SupportedProperty:
    def __init__(self, field):
        self.property_name = field.name
        self.required = field.null
        self.readable = True
        self.writeable = True
        self.is_unique = field.unique
        self.is_identifier = field.primary_key
        self.is_external = isinstance(field, ForeignKey)
        self.field = field

    def get_supported_operations(self):
        voc = operation_vocabulary(self.field.name) or operation_vocabulary(type(self.field))

        if voc is None:
            voc  = []

        oper_res_voc_dict_list = [{"hydra:Link": voc}]
        return oper_res_voc_dict_list

    def context(self):
        return {
            "@type": "hydra:SupportedProperty",
            "hydra:property": self.property_name,
            "hydra:writeable": self.writeable,
            "hydra:readable": self.readable,
            "hydra:required": self.required,
            "isUnique": self.is_unique,
            "isIdentifier": self.is_identifier,
            "isExternal": self.is_external,
            "hydra:supportedOperations": self.get_supported_operations()
        }

class SupportedOperation:
    def __init__(self, operation='', title='', method='', expects='', returns='', type='', link=''):
        self.method = method
        self.operation = operation
        self.title = title
        self.expects = expects
        self.returns = returns
        self.type = type
        self.link = link # the link to the explanation of what this operation is

    def context(self):
        return {
                "hydra:method": self.method,
                "hydra:operation": self.operation,
                "hydra:expects": self.expects,
                "hydra:returns": self.returns,
                "hydra:statusCode": '',
                "@id": self.link
        }

class SupportedOperator:
    def __init__(self, operator='', expects='', returns='', link=''):
        self.operator = operator
        self.expects = expects
        self.returns = returns
        self.link = link

    def context(self):
        return {
            "operator": self.operator,
            "expects": self.expects,
            "returns": self.returns,
            "@id": self.link
        }

def initialize_dict():
    dict = {}
    oc = BaseOperationController()
    dict[GeometryField] = oc.geometry_operations_dict()
    dict['Feature'] = oc.geometry_operations_dict()
    dict['Geobuf'] = oc.geometry_operations_dict()
    dict[GEOSGeometry] = oc.geometry_operations_dict()
    dict[Point] = oc.point_operations_dict()
    dict[PointField] = oc.point_operations_dict()
    dict[Polygon] = oc.polygon_operations_dict()
    dict[LineString] = oc.line_operations_dict()
    dict[MultiPoint] = oc.point_operations_dict()
    dict[MultiPolygon] = oc.polygon_operations_dict()
    dict[MultiLineString] = oc.line_operations_dict()
    dict[str] = oc.string_operations_dict()
    dict['Text'] = oc.string_operations_dict()
    dict[CharField] = oc.string_operations_dict()
    dict['Thing'] = oc.generic_object_operations_dict()
    dict[object] = oc.generic_object_operations_dict()

    ro = RasterOperationController()
    dict['Raster'] = ro.dict_all_operation_dict()
    dict['Tiff'] = ro.dict_all_operation_dict()
    dict[GDALRaster] = ro.dict_all_operation_dict()

    soc = SpatialCollectionOperationController()
    dict[GeometryCollection] = soc.feature_collection_operations_dict()
    dict['FeatureCollection'] = soc.feature_collection_operations_dict()
    dict[FeatureCollection] = soc.feature_collection_operations_dict()
    dict['GeobufCollection'] = soc.feature_collection_operations_dict()

    coc = CollectionResourceOperationController()
    dict['Collection'] = coc.collection_operations_dict()

    epoc = EntryPointResourceOperationController()
    dict['EntryPoint'] = epoc.collection_operations_dict()
    return dict


class ContextResource:
    def __init__(self):
        self.basic_path = None
        self.complement_path = None
        self.host = None
        self.dict_context = None
        self.resource = None

    def get_dict_context(self):
        '''use this method instead of reference self.dict_context directly'''
        return deepcopy(self.dict_context)

    #def attribute_name_list(self):
    #    return ( field.attname for field in self.model_class._meta.fields[:])

    #def attribute_type_list(self):
    #    return ( type(field) for field in self.model_class._meta.fields[:])

    def host_with_path(self):
        return self.host + self.basic_path + "/" + self.complement_path

    def operation_names(self):
        return [method for method in dir(self) if callable(getattr(self, method)) and self.is_not_private(method)]

    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        '''
        Used as resource identification and typing
        '''
        dic = {}
        return dic

    def attributes_term_definition_context_dict(self, attrs_list):
        dic_field = {}
        fields = self.resource.fields_to_web_for_attribute_names(attrs_list)

        for field_model in fields:
            dic_field[field_model.name] = self.attribute_contextualized_dict_for_field(field_model)

        dic_field.update(self.get_subClassOf_term_definition())
        return dic_field

    def operation_term_definition_context_dict(self):
        '''
        Used as term definition inside @context. it's important to remember that some operations
        don't have term definition because his name don'r appear in resource body
        '''
        return {}

    def resource_id_and_type_by_operation_context(self, a_key, operation_return_type):
        operation_dict = self.resource_id_and_type_by_operation_dict(operation_return_type)
        return operation_dict.get(a_key) or None

    def operation_term_definition_context(self, a_key, operation_return_type=None):
        term_definition_context = self.operation_term_definition_context_dict()
        return term_definition_context.get(a_key) or {"@id": vocabulary(object), "@type": vocabulary(object)}

    def attribute_contextualized_dict_for_field(self, field):
        voc = vocabulary(field.name)
        voc_type = vocabulary(type(field))

        res_voc = voc or voc_type

        if res_voc is None:
            res_voc = vocabulary(object)

        return {
            '@id': res_voc,
            '@type':  ("@id" if isinstance(field, ForeignKey) else voc_type)
        }

    def attribute_contextualized_dict_for_type(self, a_type):
        res_voc = vocabulary(a_type)
        return {
            '@id': res_voc,
            '@type':  ("@id" if a_type == ForeignKey else res_voc)
        }

    def get_vocabulary_for(self, key):
        return vocabulary(key)

    def get_subClassOf_term_definition(self):
        dic = {
            "subClassOf": {
                "@id": "rdfs:subClassOf",
                "@type": "@vocab"
            },
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
        }
        dic.update(self.get_hydra_term_definition())
        return dic

    def get_hydra_term_definition(self):
        return {"hydra": vocabulary("hydra")}

    def attributes_contextualized_dict(self):
        dic_field = {}
        fields = self.resource.fields_to_web()

        for field_model in fields:
            dic_field[field_model.name] = self.attribute_contextualized_dict_for_field(field_model)

        dic_field.update(self.get_subClassOf_term_definition())
        return dic_field

    def selectedAttributeContextualized_dict(self, attribute_name_array):
        return {k: v for k, v in list(self.attributes_contextualized_dict().items()) if k in attribute_name_array}

    def supportedPropertyFor(self, field):
        res_voc = vocabulary(field.name) or vocabulary(type(field))
        return { "@id": res_voc, "@type": "@id"}

    def identifier_field_or_None(self):
        fields = self.resource.fields_to_web()
        for field in fields:
             if field.primary_key is True:
                 return field

        return None

    def representationName(self):
        ide_field = self.identifier_field_or_None()
        if ide_field is not None:
            return  {"hydra:property":ide_field.name , "@type": "hydra:SupportedProperty"}

        return {}

    def supportedProperties(self, attribute_names=None):
        if self.resource is None:
            return []

        fields = self.resource.fields_to_web() if attribute_names is None else self.resource.fields_to_web_for_attribute_names(attribute_names)

        arr_dict = []
        for field in fields:
            prop = SupportedProperty(field)
            arr_dict.append(prop)

        return [supportedAttribute.context() for supportedAttribute in arr_dict]

    def supportedOperationsFor(self, object, object_type=None):
        dict = initialize_dict()
        a_type = object_type or type(object)
        dict_operations = dict[a_type] if a_type in dict else {}

        arr = []
        for k, v_typed_called in dict_operations.items():

            exps = []
            if v_typed_called.has_parameters:
                for parameter, representation_list in v_typed_called.get_parameters_and_representations():
                    representation_voc_list = [vocabulary(representation) for representation in representation_list]
                    exps.append({
                        "parameter": vocabulary(parameter),
                        "representations": representation_voc_list
                    })

            rets = vocabulary(v_typed_called.return_type) or "NOT FOUND"
            link_id = vocabulary(v_typed_called.name)
            arr.append(SupportedOperation(operation=k, title=v_typed_called.name, method='GET', expects=exps, returns=rets, type='', link=link_id))

        return [supportedOperation.context() for supportedOperation in arr]

    '''
    def supportedOperations(self):
        arr = []
        if self.resource is None:
            return []
        for k, v_typed_called in self.resource.operations_with_parameters_type().items():
            exps = [] if v_typed_called.parameters is None else [vocabulary(param) for param in v_typed_called.parameters]
            if v_typed_called.return_type in vocabularyDict():
                rets = vocabulary(v_typed_called.return_type)
            else:
                rets = "NOT FOUND"
            link_id = vocabulary(v_typed_called.name)
            arr.append( SupportedOperation(operation=k, title=v_typed_called.name, method='GET', expects=exps, returns=rets, type='', link=link_id))

        return [supportedOperation.context() for supportedOperation in arr]
    '''

    def iriTemplates(self):
        iri_templates = []
        dict = {
            "@type": "IriTemplate",
            "template": self.host_with_path() + "{list*}",
            "mapping": [
                {"@type": "iriTemplateMapping", "variable": "list*", "property": "hydra:property", "required": True}
            ]
        }

        iri_templates.append(dict)
        return {"iri_templates": iri_templates}

    def get_default_context_superclass(self):
        return {"subClassOf": "hydra:Resource"}

    def get_context_superclass_by_return_type(self, return_type):
        return {"subClassOf": "hydra:Resource"}

    def get_default_resource_type_identification(self):
        return {
            "@id": self.get_default_resource_id_vocabulary(),
            "@type": self.get_default_resource_type_vocabulary()
        }

    def get_default_resource_id_vocabulary(self):
        id_vocabulary = vocabulary(self.resource.default_resource_representation())
        return id_vocabulary or vocabulary(object)

    def get_default_resource_type_vocabulary(self):
        type_vocabulary = vocabulary(self.resource.default_resource_representation())
        return type_vocabulary or vocabulary(object)

    def get_resource_id_and_type_by_attributes_return_type(self, attr_list, return_type):
        dic = {
            "@id": self.get_resource_id_by_attributes_return_type(attr_list, return_type),
            "@type": vocabulary(return_type)
        }
        dic.update(self.get_context_superclass_by_attributes(attr_list))
        return dic

    def get_resource_id_by_attributes_return_type(self, attr_list, return_type):
        if len(attr_list) == 1:
            field_for_attribute = self.resource.field_for(attr_list[0])
            return vocabulary(field_for_attribute.name) or vocabulary(type(field_for_attribute))
        
        return vocabulary(object)

    def get_context_superclass_by_attributes(self, attr_list):
        return self.get_default_context_superclass()

    def get_operation_return_type_context_by_operation_name(self, operation_name):
        return self.get_operation_return_type_term_definition(operation_name)

    def get_resource_id_and_type_by_operation_return_type(self, operation_name, operation_return_type):
        dic = self.resource_id_and_type_by_operation_context(operation_name, operation_return_type)
        dic.update(self.get_default_context_superclass())
        return dic

    def get_operation_return_type_term_definition(self, operation_name, operation_return_type=None):
        return {operation_name: self.operation_term_definition_context(operation_name)}

    def set_context_to_attributes(self, attributes_name):
        self.dict_context = {
            "@context": self.selectedAttributeContextualized_dict(attributes_name)
        }
        self.dict_context["@context"].update(self.get_subClassOf_term_definition())
        #self.dict_context["@context"]["hydra"] = "http://www.w3.org/ns/hydra/core#"

    def set_context_to_operation(self, object, operation_name):
        self.dict_context = {}
        dict = {
            operation_name: {
                "@id": vocabulary(operation_name),
                "@type": "@id"
            }
        }

        self.dict_context["@context"] = dict

    def get_context_to_operation(self, operation_name):
        dict = {
            operation_name: {
                "@id": vocabulary(operation_name),
                "@type": "@id"
            }
        }
        return {"@context": dict}

    def initialize_context(self, resource_type):
        self.dict_context = {
            "@context": self.attributes_contextualized_dict(),
            "hydra:supportedProperties": self.supportedProperties(),
            "hydra:supportedOperations": self.supportedOperationsFor(self.resource.object_model, resource_type),
            "hydra:representationName": self.representationName(),
            "hydra:iriTemplate": self.iriTemplates()
        }
        #self.dict_context["@context"].update(self.get_hydra_term_definition())
        #self.dict_context["@context"].update(self.get_subClassOf_term_definition())
        self.dict_context.update(self.get_default_context_superclass())
        self.dict_context.update(self.get_default_resource_type_identification())

        return deepcopy(self.dict_context)

    def context(self, resource_type=None):
        if self.dict_context is None:
            resource_type = resource_type or self.resource.default_resource_representation()
            self.initialize_context(resource_type)
            
        return deepcopy(self.dict_context)


class FeatureResourceContext(ContextResource):
    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        oc = self.resource.operation_controller
        dic = super(FeatureResourceContext, self).resource_id_and_type_by_operation_dict(operation_return_type)
        dic.update({
            oc.area_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.contains_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.coord_seq_operation_name:        {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.coords_operation_name:           {"@id": vocabulary(oc.coords_operation_name), "@type": vocabulary(object)},
            oc.count_operation_name:            {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.crosses_operation_name:          {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.crs_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.difference_operation_name:       {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.dims_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.disjoint_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.distance_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.empty_operation_name:            {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.equals_exact_operation_name:     {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.equals_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.ewkb_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.ewkt_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(str)},
            oc.extent_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.geojson_operation_name:          {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.geom_type_operation_name:        {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.geom_typeid_operation_name:      {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.has_cs_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.hasz_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.hex_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            oc.hexewkb_operation_name:          {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.intersection_operation_name:     {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.intersects_operation_name:       {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.json_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.kml_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.length_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.num_coords_operation_name:       {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.num_geom_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.num_points_operation_name:       {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.ogr_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.overlaps_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.point_on_surface_operation_name: {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.relate_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.relate_pattern_operation_name:   {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.ring_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.simple_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.simplify_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.srid_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.srs_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.sym_difference_operation_name:   {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.touches_operation_name:          {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.transform_operation_name:        {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.union_operation_name:            {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.valid_operation_name:            {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.valid_reason_operation_name:     {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.within_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.wkb_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.wkt_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(str)},
            oc.x_operation_name:                {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.y_operation_name:                {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
            oc.z_operation_name:                {"@id": vocabulary(operation_return_type), "@type": vocabulary(object)},
        })
        return dic

    def operation_term_definition_context_dict(self):
        oc = self.resource.operation_controller
        dic = super(FeatureResourceContext, self).operation_term_definition_context_dict()
        dic.update({
            oc.area_operation_name:             {"@id": vocabulary(float), "@type": vocabulary(float)},
            oc.contains_operation_name:         {"@id": vocabulary(bool), "@type": vocabulary(bool)},
            oc.coords_operation_name:           {"@id": vocabulary(oc.coords_operation_name), "@type": vocabulary(oc.coords_operation_name)},
            oc.ewkt_operation_name:             {"@id": vocabulary(oc.ewkt_operation_name), "@type": vocabulary(str)},
            oc.geojson_operation_name:          {"@id": vocabulary(oc.geojson_operation_name), "@type": vocabulary(str)},
            oc.json_operation_name:             {"@id": vocabulary(oc.json_operation_name), "@type": vocabulary(str)},
            oc.ogr_operation_name:              {"@id": vocabulary(oc.ogr_operation_name), "@type": vocabulary(str)},
            oc.relate_pattern_operation_name:   {"@id": vocabulary(bool), "@type": vocabulary(bool)},
            oc.relate_operation_name:           {"@id": vocabulary(str), "@type": vocabulary(str)},
            oc.wkt_operation_name:              {"@id": vocabulary(oc.wkt_operation_name), "@type": vocabulary(str)},
        })
        return dic

    def get_resource_id_and_type_by_operation_return_type(self, operation_name, operation_return_type):
        if not issubclass(operation_return_type, GEOSGeometry):
            return super(FeatureResourceContext, self).get_resource_id_and_type_by_operation_return_type(operation_name, operation_return_type)
        
        dic = {
            "@id": vocabulary(operation_return_type),
            "@type": vocabulary(operation_return_type)
        }
        dic.update(self.get_default_context_superclass())
        return dic

    def get_resource_id_and_type_by_attributes_return_type(self, attr_list, return_type):
        id_and_type_voc = super(FeatureResourceContext, self).get_resource_id_and_type_by_attributes_return_type(attr_list, return_type)
        if self.resource.geometry_field_name() in attr_list:
            id_and_type_voc["@type"] = vocabulary(return_type)
        
        return id_and_type_voc

    def get_resource_id_by_attributes_return_type(self, attr_list, return_type):
        if self.resource.geometry_field_name() not in attr_list:
            return super(FeatureResourceContext, self).get_resource_id_by_attributes_return_type(attr_list, return_type)
        
        return vocabulary(return_type)

    def attributes_contextualized_dict(self):
        dict_field = super(FeatureResourceContext, self).attributes_contextualized_dict()
        dict_field.pop(self.resource.geometry_field_name())
        return dict_field


class AbstractCollectionResourceContext(ContextResource):
    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        oc = self.resource.operation_controller
        default_at_id = self.get_default_resource_id_vocabulary()
        
        dic = super(AbstractCollectionResourceContext, self).resource_id_and_type_by_operation_dict(operation_return_type)
        dic.update({
            oc.count_resource_collection_operation_name:    {"@id": "hydra:totalItems", "@type": "https://schema.org/Thing"},
            # For operations with subcollection return, @type is to much generic, therefore this @type must be based on operation return type defined in resource class (views)
            oc.distinct_collection_operation_name:          {"@id": default_at_id, "@type": vocabulary(operation_return_type)},
            oc.filter_collection_operation_name:            {"@id": default_at_id, "@type": vocabulary(operation_return_type)},
            oc.group_by_sum_collection_operation_name:      {"@id": default_at_id, "@type": vocabulary(operation_return_type)},
        })
        return dic

    def operation_term_definition_context_dict(self):
        oc = self.resource.operation_controller
        dic = super(AbstractCollectionResourceContext, self).operation_term_definition_context_dict()
        dic.update({
            oc.count_resource_collection_operation_name:    {"@id": "https://schema.org/Integer", "@type": "https://schema.org/Integer"},
            oc.group_by_sum_collection_operation_name:      {"@id": vocabulary(GROUP_BY_SUM_PROPERTY_NAME), "@type": vocabulary(GROUP_BY_SUM_PROPERTY_NAME)}
        })
        return dic

    def get_default_context_superclass(self):
        return {"subClassOf": "hydra:Resource"}

    def get_default_resource_id_vocabulary(self):
        return vocabulary(object)

    '''
    def get_resource_id_and_type_by_attributes_return_type(self, attr_list, return_type):
        dic = {}
        dic["@id"] = vocabulary(object)
        dic["@type"] = vocabulary(return_type)
        dic.update(self.get_context_superclass_by_attributes(attr_list))
        return dic
    '''

    def get_resource_id_and_type_by_operation_return_type(self, operation_name, operation_return_type):
        dic = self.get_context_superclass_by_return_type(operation_return_type)

        operation_id_type = self.resource_id_and_type_by_operation_context(operation_name, operation_return_type)
        if operation_id_type:
            dic.update(operation_id_type)
        else:
            dic.update(
                {"@id": vocabulary(object), "@type": vocabulary(operation_return_type)}
            )
        return dic

    def get_resource_id_by_attributes(self, attr_list):
        '''
        For Collection @id represents the identification of each element in collection and not the collection itself
        '''
        if len(attr_list) > 1:
            return vocabulary(object)

        field_for_attribute = self.resource.field_for(attr_list[0])
        return vocabulary(field_for_attribute.name) or vocabulary(type(field_for_attribute))


class FeatureCollectionResourceContext(AbstractCollectionResourceContext):
    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        oc = self.resource.operation_controller
        
        dic = super(FeatureCollectionResourceContext, self).resource_id_and_type_by_operation_dict(operation_return_type)
        dic.update({
            oc.extent_collection_operation_name:    {"@id": vocabulary(operation_return_type), "@type": "https://schema.org/Thing"},
            oc.make_line_collection_operation_name: {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            oc.union_collection_operation_name:     {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
        })
        return dic

    def operation_term_definition_context_dict(self):
        oc = self.resource.operation_controller

        dic = super(FeatureCollectionResourceContext, self).operation_term_definition_context_dict()
        dic.update({
            oc.extent_collection_operation_name: {"@id": vocabulary(list), "@type": vocabulary(list)}
        })
        return dic

    def get_default_context_superclass(self):
        return {"subClassOf": vocabulary("Collection")}

    def get_context_superclass_by_return_type(self, return_type):
        if return_type not in [GeometryCollection, FeatureCollection]:
            return super(FeatureCollectionResourceContext, self).get_context_superclass_by_return_type(return_type)

        return self.get_default_context_superclass()

    def get_default_resource_id_vocabulary(self):
        return vocabulary("Feature")

    def get_context_superclass_by_attributes(self, attr_list):
        if self.resource.geometry_field_name() not in attr_list:
            return super(FeatureCollectionResourceContext, self).get_default_context_superclass()

        return self.get_default_context_superclass()

    def get_resource_id_and_type_by_attributes_return_type(self, attr_list, return_type):
        dic = {
            "@id": self.get_resource_id_by_attributes(attr_list),
            "@type": vocabulary(return_type)
        }
        dic.update( self.get_context_superclass_by_attributes(attr_list) )
        return dic

    def attributes_contextualized_dict(self):
        dict_field = super(FeatureCollectionResourceContext, self).attributes_contextualized_dict()
        dict_field.pop(self.resource.geometry_field_name())
        return dict_field

    def get_resource_id_by_attributes(self, attr_list):
        if self.resource.geometry_field_name() not in attr_list:
            return super(FeatureCollectionResourceContext, self).get_resource_id_by_attributes(attr_list)

        if len(attr_list) > 1:
            return vocabulary("Feature")

        return vocabulary(type(self.resource.field_for(attr_list[0])))

    def get_resource_id_and_type_by_operation_return_type(self, operation_name, operation_return_type):
        dic = self.get_context_superclass_by_return_type(operation_return_type)
        operation_id_type = self.resource_id_and_type_by_operation_context(operation_name, operation_return_type)

        if operation_id_type:
            dic.update(operation_id_type)
        else:
            dic.update(
                {"@id": self.get_default_resource_id_vocabulary(), "@type": vocabulary(operation_return_type)}
            )
        return dic


class NonSpatialResourceContext(ContextResource):
    pass


class RasterResourceContext(ContextResource):
    def get_resource_id_by_attributes_return_type(self, attr_list, return_type):
        if len(attr_list) == 1:
            return super(RasterResourceContext, self).get_resource_id_by_attributes_return_type(attr_list, return_type)

        return vocabulary(return_type)

    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        oc = self.resource.operation_controller

        dic = super(RasterResourceContext, self).resource_id_and_type_by_operation_dict(operation_return_type)
        dic.update({
            oc.driver_operation_name: {"@id": "https://schema.org/Text", "@type": "https://schema.org/Thing"}
        })
        return dic

    def attributes_term_definition_context_dict(self, attrs_list):
        if self.resource.spatial_field_name() in attrs_list:
            return self.attributes_contextualized_dict()

        return super(RasterResourceContext, self).attributes_term_definition_context_dict(attrs_list)

    def operation_term_definition_context_dict(self):
        dic = super(RasterResourceContext, self).operation_term_definition_context_dict()
        dic.update({
            self.resource.operation_controller.driver_operation_name: {"@id": "https://schema.org/Text", "@type": "https://schema.org/Text"}
        })
        return dic

    def attributes_contextualized_dict(self):
        return self.get_subClassOf_term_definition()

    def get_resource_id_and_type_by_operation_return_type(self, operation_name, operation_return_type):
        if not issubclass(operation_return_type, GDALRaster):
            return super(RasterResourceContext, self).get_resource_id_and_type_by_operation_return_type(operation_name, operation_return_type)

        dic = self.get_default_context_superclass()
        dic["@id"] = vocabulary(operation_return_type)
        dic["@type"] = vocabulary(operation_return_type)
        return dic

    def get_resource_id_and_type_by_attributes_return_type(self, attr_list, return_type):
        dic = {
            "@id": self.get_resource_id_by_attributes_return_type(attr_list, return_type),
            "@type": vocabulary(return_type)
        }
        dic.update( self.get_context_superclass_by_attributes(attr_list) )
        return dic


class EntryPointResourceContext(AbstractCollectionResourceContext):
    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        oc = self.resource.operation_controller

        dic = super(AbstractCollectionResourceContext, self).resource_id_and_type_by_operation_dict(operation_return_type)
        dic.update({
            oc.count_resource_collection_operation_name: {"@id": "hydra:totalItems", "@type": "https://schema.org/Thing"},
        })
        return dic

    def operation_term_definition_context_dict(self):
        oc = self.resource.operation_controller

        dic = super(AbstractCollectionResourceContext, self).operation_term_definition_context_dict()
        dic.update({
            oc.count_resource_collection_operation_name: {"@id": "https://schema.org/Integer", "@type": "https://schema.org/Integer"}
        })
        return dic

    def get_default_resource_id_vocabulary(self):
        return vocabulary('Link')

    def attributes_contextualized_dict(self):
        default_attrs_context_dict = super(EntryPointResourceContext, self).attributes_contextualized_dict()
        for field in self.resource.fields_to_web():
            default_attrs_context_dict[field.name]["@id"] = "https://schema.org/Thing"
            default_attrs_context_dict[field.name]["@type"] = "@id"

        return default_attrs_context_dict

    def addContext(self, request, response):
        return self.createLinkOfContext(request, response)

    def createLinkOfContext(self, request, response, properties=None):
        # if properties is None:
        #     url = reverse('context:detail', args=[self.contextclassname], request=request)
        # else:
        #     url = reverse('context:detail-property', args=[self.contextclassname, ",".join(properties)], request=request)

        url = request.build_absolute_uri()
        url = url if not url.endswith('/') else url[:-1]
        url = url + ".jsonld"

        context_link = ' <'+url+'>; rel=\"http://www.w3.org/ns/json-ld#context\"; type=\"application/ld+json\" '
        if "Link" not in response:
            response['Link'] = context_link
        else:
            response['Link'] += "," + context_link

        return response

    def create_context_as_dict(self, dict_of_name_link):
        a_context = {}
        dic = {"@context": a_context}

        for key in dict_of_name_link.keys():
            a_context[key] = {"@id": "https://schema.org/Thing", "@type": "@id" }

        return dic


class FeatureEntryPointResourceContext(EntryPointResourceContext):
    def attributes_contextualized_dict(self):
        default_attrs_context_dict = super(FeatureEntryPointResourceContext, self).attributes_contextualized_dict()
        for field in self.resource.fields_to_web():
            default_attrs_context_dict[field.name]["@type"] = "@id"
            default_attrs_context_dict[field.name]["@id"] = vocabulary('FeatureCollection')

        return default_attrs_context_dict

    def create_context_as_dict(self, dict_of_name_link):
        a_context = {}
        dic = {"@context": a_context}
        for key in dict_of_name_link.keys():
            a_context[key] = {"@id": vocabulary('FeatureCollection'), "@type": "@id" }

        return dic


class RasterEntryPointResourceContext(EntryPointResourceContext):
    pass


class NonSpatialEntryPointResourceContext(EntryPointResourceContext):
    pass