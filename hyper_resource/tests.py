import django
import rest_framework
#from rest_framework import generics
#from rest_framework.response import Response
#from rest_framework.views import APIView
#from rest_framework import permissions
#from rest_framework import permissions

from django.contrib.gis.geos import Point
from django.test import TestCase
# Create your tests here.
from django.contrib.gis.db import models

from hyper_resource.models import FeatureModel, FactoryComplexQuery
from hyper_resource.contexts import *
from hyper_resource.resources.AbstractResource import AbstractResource
from hyper_resource.resources.FeatureCollectionResource import FeatureCollectionResource
from hyper_resource.resources.AbstractCollectionResource import AbstractCollectionResource
from hyper_resource.resources.CollectionResource import CollectionResource
from django.contrib.gis.geos import GEOSGeometry
from django.test import SimpleTestCase
from controle.views import UsuarioList, UsuarioDetail
from controle.models import Usuario

import json
import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


from django.test.runner import DiscoverRunner
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'bc_edgv.settings'
#django.setup()
#python manage.py test bcim.test_utils  --testrunner=bcim.test_utils.NoDbTestRunner
#python manage.py test hyper_resource.tests --testrunner=hyper_resource.tests.NoDbTestRunner
from django.contrib.gis.db.models import Q

HOST = 'luc00557196:8000/'

class NoDbTestRunner(DiscoverRunner):
   """ A test runner to test without database creation/deletion """

   def setup_databases(self, **kwargs):
     pass

   def teardown_databases(self, old_config, **kwargs):
     pass

class Ponto(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.PointField(blank=True, null=True)
class Linha(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.LineStringField(blank=True, null=True)
class Poligono(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.PolygonField(blank=True, null=True)
class Geometria(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.GeometryField(blank=True, null=True)

## ativando virtual environment em: source ~/desenv/env/env_bc_edgv/bin/activate
## Testando
# python manage.py test hyper_resource.tests  --testrunner=hyper_resource.tests.NoDbTestRunner
##
#python manage.py test bcim.test_utils  --testrunner=bcim.test_utils.NoDbTestRunner
#python manage.py test hyper_resource.tests --testrunner=hyper_resource.tests.NoDbTestRunner
from django.test import SimpleTestCase
#from bcim.utils import APIViewHypermedia
#python manage.py test app --testrunner=app.filename.NoDbTestRunner
#python manage.py test bcim.tests  --testrunner=bcim.tests.NoDbTestRunner
#python manage.py test hyper_resource.tests --testrunner=hyper_resource.tests.NoDbTestRunner
from bcim.models import ModeloTeste

class ModelTest(models.Model):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    tipopostofisc = models.CharField(max_length=22, blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)
    polygon = models.PolygonField(blank=True, null=True)
    lineString = models.LineStringField(blank=True, null=True)
    point = models.PointField(blank=True, null=True)
    multipolygon = models.MultiPolygonField(blank=True, null=True)

class TesteResource(AbstractResource):
    def __init__(self, a_name, params, answer):
        self.name = a_name
        self.parameters = params
        self.return_type = answer

class FeatureModelTestCase(SimpleTestCase):
    def setUp(self):
        self.ponto = Ponto()
        self.linha = Linha()
        self.poligono = Poligono()
        self.geometria = Geometria()

    def url_feature(self):
        return ''

    def test_get_geometry_type(self):
        self.assertEquals(self.ponto.get_geometry_type(), Point)

    def test_fields(self):
        self.assertEquals(self.ponto.fields()[0].name, 'id_objeto')

class AbstractResourceTestCase(SimpleTestCase):

    def setUp(self):
        self.tr = TesteResource('name', 'parameters', 'answer')
        self.ar = AbstractCollectionResource()

    def test_attributes(self):
        pass
    def test_operations(self):
        pass
    def test_remove_last_slash(self):

        self.assertEquals(self.ar.remove_last_slash('within/__tokenurl__1/collect/geom/buffer/0.2/'), 'within/__tokenurl__1/collect/geom/buffer/0.2')
        self.assertEquals(self.ar.remove_last_slash('within/__tokenurl__1/collect/geom/buffer/0.2'), 'within/__tokenurl__1/collect/geom/buffer/0.2')
        self.assertEquals(self.ar.remove_last_slash('within/__tokenurl__1/collect/geom/buffer/0.2 '), 'within/__tokenurl__1/collect/geom/buffer/0.2')

    def test_attribute_functions_str_splitted_by_slash(self):
        res = self.ar.attribute_functions_str_splitted_by_slash('within/http://172.30.10.86:8000/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2/intersects/https://172.30.10.86:8000/instituicoes/bcim/estado/rj/*')
        self.assertEquals(res[0], 'within')
        self.assertEquals(res[1], 'http://172.30.10.86:8000/ibge/bcim/municipios/3159407/')
        self.assertEquals(res[2], '*collect')
        self.assertEquals(res[3], 'geom')
        self.assertEquals(res[4], 'buffer')
        self.assertEquals(res[5], '0.2')
        self.assertEquals(res[6], 'intersects')
        self.assertEquals(res[7], 'https://172.30.10.86:8000/instituicoes/bcim/estado/rj/')

class SpatialResourceTest(SimpleTestCase):

    def test_attributeContextualized(self):
        pass

'''
class FeatureResourceTest(SimpleTestCase):

    def test_basic_get(self):
        pass
    def test_options_url_without_parameters(self):
        pass
    def test_options_url_with_only_attributes(self):
        pass
    def test_options_url_with_only_one_attribute(self):
        pass
    def test_options_url_with_spatia_functions(self):
        pass
'''

class FactoryComplexQueryTest(SimpleTestCase):
    def setUp(self):
        self.fcq = FactoryComplexQuery()
    def test_q_object_for_in(self):

        q = self.fcq.q_object_for_in(str,'sigla', ['ES,RJ'])
        self.assertEquals(Q(sigla__in=['ES,RJ']).__repr__(), q.__repr__())

    def test_q_object_for_eq(self):

        q = self.fcq.q_object_for_eq(str,'sigla', 'ES')
        self.assertEquals(Q(sigla='ES').__repr__(), q.__repr__())

    def test_q_object_for_neq(self):

        q = self.fcq.q_object_for_neq(str, 'sigla', 'ES')
        self.assertEquals((~Q(sigla='ES')).__repr__(), q.__repr__())

    def test_q_object_by_filter_operation(self):
        attribute_operation_str ='filter/sigla/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/'
        import datetime
        start_date = datetime.date(2017, 2, 1)
        end_date = datetime.date(2017, 6, 30)
        q = Q(sigla__in=['rj','es','go']) & Q(data__range=(start_date, end_date))
        model_class = ModeloTeste
        self.fcq.q_object_serialized_by_filter_operation(attribute_operation_str, model_class)

class AbstractCollectionResourceTestCase(SimpleTestCase):
    def setUp(self):
        self.attributes_functions = ['filter/sigla/in/rj,es,go/', 'filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/', 'filter/sigla/in/rj,es,go/and/geom/within/{"type":"Polygon","coordinates":[[[-41.881710164667396,-21.297482165015307],[-28.840495695785098,-21.297482165015307],[-28.840495695785098,-17.886950999070834],[-41.881710164667396,-17.886950999070834],[-41.881710164667396,-21.297482165015307]]]}']
        self.acr = AbstractCollectionResource()

    def test_get_operation_name_from_path(self):
        self.assertEquals(self.acr.get_operation_name_from_path('collect/geom/buffer/0.2'), 'collect')
        self.assertEquals(self.acr.get_operation_name_from_path('filter/geom/buffer/0.2'), 'filter')
        self.assertEquals(self.acr.get_operation_name_from_path('filter/geom/containing/http://host/aldeias-indigenas/821/*collect/nome.geom/buffer/0.2'), 'filter_collect')
        self.assertEquals(self.acr.get_operation_name_from_path('collect/nome&geom/buffer/0.2/containing/http://host/aldeias-indigenas/821/*filter/nome/startswith/rio'), 'collect_filter')
        self.assertEquals(self.acr.get_operation_name_from_path('count-resource'), 'count-resource')
        self.assertEquals(self.acr.get_operation_name_from_path('group-by/nome'), 'group-by')
        self.assertEquals(self.acr.get_operation_name_from_path('group-by-count/nome'), 'group-by-count')
        self.assertEquals(self.acr.get_operation_name_from_path('distinct'), 'distinct')
        self.assertEquals(self.acr.get_operation_name_from_path('offset-limit/1&10'), 'offset-limit')
        self.assertEquals(self.acr.get_operation_name_from_path('nadahaver'), None)
    def test_attributes_functions_str_is_filter_with_spatial_operation(self):
        pass
        """
        self.assertTrue(self.acr.attributes_functions_str_is_filter_with_spatial_operation('filter/sigla/in/rj,es,go/and/geom/within/Point(1,2)'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/filter'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/ast/eq/ass/geom/within/asd'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/within/eq/asd'))
        self.assertTrue(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/within/eq/geom/and/geom/within/asd'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/operacao/eq/within'))
        self.assertTrue(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/eq/within/abxgeom'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/within/eq/abxx'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/within/geom'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/within/filter'))
        """
    def test_attributes_functions_str_splitted_by_slash(self):
        self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2') == ['collect','geom', 'buffer', '0.2']
        self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2/') == ['collect','geom', 'buffer', '0.2']
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2'), ['collect','geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2/transform/3005&True/area'), ['collect', 'geom', 'buffer', '0.2', 'transform', '3005&True', 'area'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('offsetLimit/1&10/collect/geom/buffer/0.2'), ['offsetLimit', '1&10', 'collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}/collect/geom/buffer/0.2'), ['within', '{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}', 'collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2/'), ['within', 'http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/', '*collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/https://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2'), ['within', 'https://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/', '*collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2/within/http://ibge/unidades-federativas/RJ/*'), ['within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/', '*collect', 'geom', 'buffer', '0.2', 'within','http://ibge/unidades-federativas/RJ/'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/*'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/*and/sigla/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/*'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/', '*and', 'sigla', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/*collect/collect/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/*'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/', '*collect', 'collect', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/'])
 #       self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom*/and/geocodigo/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/*/collect/collect/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo*'),
#['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom','and','geocodigo','eq','http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/and/geocodigo', 'collect', 'collect', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo'])
        #self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/WWw.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407*/collect/geom/buffer/0.2'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom', 'and', 'sigla', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/collect/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/*collect/collect/transform/3005&True/area'),[
            'filter','collect','within','http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/','*collect','collect','transform', '3005&True','area'] )

    def test_get_generic_operation_name(self):

        prefix = 'get_objects_from_'
        suffix = '_operation'

        operation_name = self.acr.get_generic_operation_name('filter/geom/within/http://luc00557347.ibge.gov.br/ibge/bcim/unidades-federativas/ES/geom/buffer/0.2*/and/fclass/eq/school/*collect/geom/buffer/0.2')
        self.assertEquals(operation_name, prefix + 'filter_and_collect' + suffix)

        operation_name = self.acr.get_generic_operation_name('filter/sigla/in/RJ,ES/*collect/geom/transform/3005&True/area')
        self.assertEquals(operation_name, prefix + 'filter_and_collect' + suffix)

        operation_name = self.acr.get_generic_operation_name('collect/geom/buffer/0.2/*filter/geom/within/http://luc00557347.ibge.gov.br/ibge/bcim/unidades-federativas/ES/geom/buffer/0.2/and/fclass/eq/school*/')
        self.assertEquals(operation_name, prefix + 'collect_and_filter' + suffix)

        operation_name = self.acr.get_generic_operation_name('filter/geom/within/http://luc00557347.ibge.gov.br/ibge/bcim/unidades-federativas/ES/geom/buffer/0.2')
        self.assertEquals(operation_name, prefix + 'filter' + suffix)

        operation_name = self.acr.get_generic_operation_name('collect/geom/buffer/0.2')
        self.assertEquals(operation_name, prefix + 'collect' + suffix)

        operation_name = self.acr.get_generic_operation_name('groupby/geom/')
        self.assertEquals(operation_name, prefix + 'groupby' + suffix)

        operation_name = self.acr.get_generic_operation_name('groupbycount/geom/')
        self.assertEquals(operation_name, prefix + 'groupbycount' + suffix)

        operation_name = self.acr.get_generic_operation_name('offsetlimit/1:10/')
        self.assertEquals(operation_name, prefix + 'offsetlimit' + suffix)

        operation_name = self.acr.get_generic_operation_name('distinct')
        self.assertEquals(operation_name, prefix + 'distinct' + suffix)

        operation_name = self.acr.get_generic_operation_name('countresource')
        self.assertEquals(operation_name, prefix + 'countresource' + suffix)

        operation_name = self.acr.get_generic_operation_name('annotate/')
        self.assertEquals(operation_name, prefix + 'annotate' + suffix)

#python manage.py test hyper_resource.tests.FeatureCollectionResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner
class FeatureCollectionResourceTest(SimpleTestCase):
    def setUp(self):
        self.attributes_functions = [
            'filter/sigla/in/rj,es,go/',
            'filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/',
            'filter/sigla/in/rj,es,go/and/geom/within/{"type":"Polygon","coordinates":[[[-41.881710164667396,-21.297482165015307],[-28.840495695785098,-21.297482165015307],[-28.840495695785098,-17.886950999070834],[-41.881710164667396,-17.886950999070834],[-41.881710164667396,-21.297482165015307]]]}',
        ]
        self.fc = FeatureCollectionResource()

    def test_is_filter_operation(self):
        self.assertTrue(self.fc.path_has_filter_operation('filter/sigla/in/rj,es,go/and/geom'))
        self.assertFalse( self.fc.path_has_filter_operation('/filter'))
        self.assertTrue('filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/')

    """
    def test_q_objects_from_filter_operation(self):
        result = self.fc.q_object_for_filter_expression('filter/sigla/eq/ES')
        self.assertEquals(result.__repr__(), Q(sigla='ES').__repr__())
        result = self.fc.q_object_for_filter_expression('filter/sigla/eq/ES/')[0]
        self.assertEquals(result.__repr__(), Q(sigla='ES').__repr__())
        result = self.fc.q_object_for_filter_expression('filter/sigla/in/ES,RJ')[0]
        self.assertEquals(result.__repr__(), Q(sigla__in=['ES,RJ']).__repr__())
        result = self.fc.q_object_for_filter_expression('filter/sigla/in/ES,RJ/')[0]
        self.assertEquals(result, Q(sigla__in=['ES,RJ']))
        result1 = self.fc.q_object_for_filter_expression('filter/sigla/in/ES,RJ/and/data/between/2017-02-01,2017-06-30')[0]
        result2 = self.fc.q_object_for_filter_expression('filter/sigla/in/ES,RJ/and/data/between/2017-02-01,2017-06-30')[1]
        self.assertEquals(result1, Q(sigla__in=['ES,RJ']))
        self.assertEquals(result2, Q(data='ES,RJ'))
    """

    def test_transform_path_with_spatial_operation_str_and_url_as_array(self):
        self.maxDiff = None
        s = 'geom/contains/http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/*or/geom/contains/http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159406'
        arr = ['geom', 'contains', 'http:','172.30.10.86:8000','instituicoes','ibge','bcim','municipios','3159407', '*or', 'geom', 'contains', 'http:','172.30.10.86:8000','instituicoes','ibge','bcim','municipios','3159406']
        arr1 = ['geom', 'contains', 'http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/', '*or', 'geom', 'contains', 'http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159406/']

        self.assertEquals(len(self.fc.transform_path_with_url_as_array(arr)), len(arr1))

class CollectionResourceTest(SimpleTestCase):
    def setUp(self):
        self.host = 'luc00557196.ibge.gov.br:8000/'
        self.base_uri = "http://" + self.host + "controle-list/"

    def test_simple_collection_request(self):
        # requests.get(uri, headers={key: value, key: value})
        res = requests.get(self.base_uri + "gasto-list/")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')

    def test_collection_request_by_attributes(self):
        res = requests.get(self.base_uri + "gasto-list/id,data,valor")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')

    def test_distinct_operation_for_collection_resource(self):
        res = requests.get(self.base_uri + "gasto-list/distinct/data")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')

    def test_offset_limit_operation_for_collection_resource(self):
        res = requests.get(self.base_uri + "gasto-list/offsetLimit/2&3")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')
    """
    def test_groupBy_operation_for_collection_resource(self):
        res = requests.get(self.base_uri + "gasto-list/groupBy/data,valor")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')
    """


class AbstractRequestTest(SimpleTestCase):
    def setUp(self):
        self.bcim_base_uri = "http://" + HOST + "api/bcim/"
        self.controle_base_uri = "http://" + HOST + "controle-list/"
        self.raster_base_uri = "http://" + HOST + "raster/"

    def aux_get_dict_from_response(self, response):
        return dict( json.loads(response.text) )

    def aux_get_keys_from_response(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        return sorted( list(response_dict.keys()) )

    # todo: this methods below must be moved for "AbstractOptionsRequestTest" class
    def aux_get_keys_from_response_context(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        return sorted( list(response_dict["@context"].keys()) )

    def aux_get_keys_from_acontext_attrs(self, response, attr_name):
        response_dict = self.aux_get_dict_from_response(response)
        context_dict = response_dict["@context"]
        return sorted( list( context_dict[attr_name].keys() ) )

class AbstractGetRequestTest(AbstractRequestTest):
    def setUp(self):
        super(AbstractGetRequestTest, self).setUp()
        self.feature_collection_keys = ["features", "type"]
        self.geometry_collection_keys = ["geometries", "type"]
        self.feature_keys = ["geometry", "properties", "type"]
        self.geometry_keys = ["coordinates", "type"]

    def aux_get_list_from_response(self, response):
        return list( json.loads(response.text) )

    def aux_get_first_feature(self, response):
        response_dict = self.aux_get_dict_from_response(response)

        if "features" not in response_dict.keys():
            return response_dict
        return response_dict["features"][0]

    def aux_get_first_feature_keys(self, response):
        first_feature = self.aux_get_first_feature(response)
        return sorted( list(first_feature.keys()) )

    def aux_get_first_feature_properties_keys(self, response):
        first_feature = self.aux_get_first_feature(response)
        return sorted( list(first_feature['properties'].keys()) )

    def aux_get_first_element_from_response_list(self, response):
        return self.aux_get_list_from_response(response)[0]

    def aux_get_first_element_keys_from_response_list(self, response):
        first_element = self.aux_get_first_element_from_response_list(response)
        return sorted( list(first_element.keys()) )

    def aux_get_first_element_joined_length(self, response):
        first_element = self.aux_get_first_element_from_response_list(response)
        return len(first_element["__joined__"])

    def aux_get_single_element_from_response(self, response):
        response_text = json.loads(response.text)
        return dict( response_text )

    def aux_get_sigle_element_keys_from_response(self, response):
        first_element = self.aux_get_single_element_from_response(response)
        return sorted( list(first_element.keys()) )

    def aux_get_first_geometry_keys_from_response_list(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        first_geometry = response_dict["geometries"][0]
        return sorted( list(first_geometry.keys()) )

    def aux_get_single_feature_properties_keys_from_response(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        return sorted( list(response_dict['properties'].keys()) )

class AbstractOptionsRequestTest(AbstractRequestTest):
    def setUp(self):
        super(AbstractOptionsRequestTest, self).setUp()
        self.supported_operation_key = 'hydra:supportedOperations'
        self.supported_property_key = 'hydra:supportedProperties'
        self.term_definition_default_keys = ['hydra', 'rdfs', 'subClassOf']

        self.simple_path_options_dict_keys = ['@context', '@id', '@type', 'hydra:iriTemplate', 'hydra:representationName',
                                              self.supported_operation_key, self.supported_property_key, 'subClassOf']

        self.non_simple_path_dict_keys = ["@context", '@id', '@type', self.supported_operation_key, 'subClassOf']

        self.keys_from_attrs_context = ["@id", "@type"]
        self.keys_from_oper_context = ["@id", "@type"]

        self.expected_supported_property_keys = ["@type", "hydra:property", "hydra:readable", "hydra:required",
                                                 self.supported_operation_key, "hydra:writeable", "isExternal", "isIdentifier", "isUnique"]

        self.spatial_operation_names = ['area', 'boundary', 'buffer', 'centroid', 'contains', 'convex_hull', 'coord_seq', 'coords', 'count', 'crosses',
                                        'crs', 'difference', 'dims', 'disjoint', 'distance', 'empty', 'envelope', 'equals', 'equals_exact', 'ewkb',
                                        'ewkt', 'extend', 'extent', 'geojson', 'geom_type', 'geom_typeid', 'get_coords', 'get_srid', 'get_x', 'get_y',
                                        'get_z', 'has_cs', 'hasz', 'hex', 'hexewkb', 'index', 'interpolate', 'intersection', 'intersects', 'join', 'json', 'kml',
                                        'length', 'normalize', 'num_coords', 'num_geom', 'num_points', 'ogr', 'overlaps', 'point_on_surface', 'projection',
                                        'relate', 'relate_pattern', 'ring', 'simple', 'simplify', 'srid',
                                        'srs', 'sym_difference', 'touches', 'transform', 'union', 'valid', 'valid_reason', 'within', 'wkb', 'wkt', 'x', 'y', 'z']

        self.string_operations_names = ['capitalize', 'center', 'count', 'endswith', 'find', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isupper',
                                        'join', 'lower', 'split', 'startswith', 'upper']

        self.basic_operations_names = ['join', 'projection']

        self.spatial_collection_operation_names = ['bbcontains', 'bboverlaps', 'collect', 'contained', 'contains', 'contains-properly', 'count-resource',
                                                    'covers', 'covers-by', 'crosses', 'disjoint', 'distance-gt', 'distance-gte', 'distance-lt', 'distance-lte',
                                                    'distinct', 'dwithin', 'extent', 'filter', 'group-by-count', 'group-by-sum', 'intersects', 'isvalid', 'join', 'left',
                                                    'make-line', 'offset-limit', 'overlaps', 'overlaps-above', 'overlaps-below', 'overlaps-left', 'overlaps-right', 'projection',
                                                   'relate', 'right', 'strictly-above', 'strictly-below', 'touches', 'union', 'within']

        self.collection_operation_names = ['collect', 'count-resource', 'distinct', 'filter', 'group-by-count', 'group-by-sum', 'join', 'offset-limit', 'projection']

        self.raster_operation_names = ['bands', 'destructor', 'driver', 'extent', 'geotransform', 'height', 'info',
                                       'metadata', 'name', 'origin', 'projection', 'ptr', 'ptr_type', 'scale', 'skew',
                                       'srid', 'srs', 'transform', 'vsi_buffer', 'warp', 'width']

        self.entrypoint_operation_names = ["collect", "count-resource", "filter", "offset-limit", "projection"]
        
        self.collection_vocab = "http://www.w3.org/ns/hydra/core#Collection"
        self.link_vocab = "http://www.w3.org/ns/hydra/core#Link"
        self.entrypoint_vocab = "http://www.w3.org/ns/hydra/core#entrypoint"

    def aux_get_context_keys_merged_with_default_keys(self, expected_context_keys):
        expected_keys = deepcopy(expected_context_keys)
        expected_keys.extend(self.term_definition_default_keys)
        return sorted(expected_keys)

    def aux_get_supported_property_keys(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        supported_properties_keys = response_dict[self.supported_property_key][0].keys()
        return sorted(supported_properties_keys)

    def aux_get_supported_property_names(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        supported_properties = response_dict[self.supported_property_key]
        property_names = []
        for sp in supported_properties:
            property_names.append( sp['hydra:property'] )
        return sorted(property_names)

    def aux_get_supported_operations_names(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        operations_names = [operation_dict['hydra:operation'] for operation_dict in response_dict[self.supported_operation_key]]
        return sorted(operations_names)

    def aux_get_supported_properties_names(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        supp_props_names = [ supp_props["hydra:property"] for supp_props in response_dict[self.supported_property_key] ]
        return sorted(supp_props_names)

class AbstractHeadRequestTest(AbstractRequestTest):

    def aux_get_headers_list_from_response(self, response):
        return sorted( list(response.headers.keys()) )

    def aux_get_allowed_methods(self, response, allow_header):
        allowed_methods = []
        for method in response.headers[allow_header].split(','):
            if method != '':
                allowed_methods.append(method.strip())
        return sorted(allowed_methods)

    def aux_get_hypermidia_control_dict_from_link_header(self, response):
        link_header_content = response.headers['link']
        hypermidia_control_list = [hypermidia_control.strip() for hypermidia_control in link_header_content.split(',')]

        hypermidia_control_dict = {}
        for hypermidia_control in hypermidia_control_list:
            hypermidia_control_splited = hypermidia_control.split(";")
            key = hypermidia_control_splited.pop(1).strip()[5:-1] # removing rel=""
            val = ";".join(hypermidia_control_splited)
            hypermidia_control_dict[key] = val
        return hypermidia_control_dict

    def aux_get_hypermidia_control_from_link_header(self, response, hypermidia_control_rel):
        return self.aux_get_hypermidia_control_dict_from_link_header(response)[hypermidia_control_rel]


#                               OPERATIONS SINTAX TEST
#python manage.py test hyper_resource.tests.GenericOperationsSintaxTest --testrunner=hyper_resource.tests.NoDbTestRunner
class GenericOperationsSintaxTest(SimpleTestCase):
    def setUp(self):
        self.generic_object = UsuarioDetail()
        self.generic_object.object_model = Usuario()

    def test_projection_operation_sintax(self):
        self.assertTrue( self.generic_object.projection_operation_sintax_is_ok("projection/nome,email") )
        self.assertTrue( self.generic_object.projection_operation_sintax_is_ok("projection/nome") )
        self.assertFalse( self.generic_object.projection_operation_sintax_is_ok("projection/this_attribute_doesnt_exists") )
        self.assertFalse( self.generic_object.projection_operation_sintax_is_ok("projection/") )
        self.assertFalse( self.generic_object.projection_operation_sintax_is_ok("projection/this_operation_doesnt_exists") )

#python manage.py test hyper_resource.tests.CollectionOperationsSintaxTest --testrunner=hyper_resource.tests.NoDbTestRunner
class CollectionOperationsSintaxTest(SimpleTestCase):
    def setUp(self):
        self.collection_object = UsuarioList()
        self.collection_object.object_model = Usuario()
        """gastos (referencia),        id,        nome,        nome_usuario,        data_nascimento,        email,        senha"""

    def test_filter_operation_sintax(self):
        # testing arr[0]
        self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filtering/nome/isnull")) # wrong name
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/isnull")) # right version
        # testing arr[1]
        self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filter/abc/isnull")) # inexistent attribute
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/isnull")) # right version
        # testing arr[2]
        self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filter/nome/xyz")) # not an boolean operator
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/isnull")) # right version
        # testing arr[3]
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/isnull"))  # arr[3] can be empty
        self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filter/nome/eq/"))  # 'eq' needs an value
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/eq/rio"))  # right version (literal value)
        #self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filter/geom/within/http://gabriel:8001/api/bcim/unidades-federativas/FF"))  # reference to nowhere
        #self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/geom/within/http://gabriel:8001/api/bcim/unidades-federativas/ES")))
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/eq/" + HOST + "/controle-list/usuario-list/1/abc")) # reference to nowhere
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/eq/" + HOST + "/controle-list/usuario-list/1/nome"))  # right version (external value)
        # testing arr[4]
        self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filter/nome/eq/rio/xyz/email/isnotnull")) # if arr[2] is an expression operator that expects a value, arr[4] must be AND or OR
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/eq/rio/and/email/isnotnull")) # right version
        self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filter/data_nascimento/between/2000-01-01/or/2010-01-01/")) # if arr[2] is 'between', arr[4] must be AND
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/data_nascimento/between/2000-01-01/and/2010-01-01/")) # right version
        # testing arr[-1] (without boolean operators AND or OR)
        self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filter/data_nascimento/eq/not_an_operation")) # final index is not an operation nor a value that can be converted to Date type
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/data_nascimento/eq/2000-01-01")) # final index can be converted to Date type
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/isnull/count-resource")) # right version (has operation in the ending)

        # another tests
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/isnull"))
        self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filter/nome/isnull/and"))
        self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filter/nome")) # inssuficient arguments (at least 3)
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/data_nascimento/between/2000-01-01/and/2010-01-01/and/nome/isnotnull"))

        '''
        # 1ยบ step test - testing array[:3]
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/data_nascimento/isnull")) # filter/local_attribute/boolean_operator
        # 2ยบ step test - testing array[3]
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/eq/Rio")) # filter/local_attribute/boolean_operator/literal_value
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/eq/http://172.30.10.86/api/bcim/unidades-federativas/ES/nome")) # filter/local_attribute/boolean_operator/external_value
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/data_nascimento/isnull/and/nome/eq/r")) # filter/local_attribute/boolean_operator/literal_value/logical_operator
        # 3ยบ step test - testing array[4]
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/eq/r/and/data_nascimento/isnull")) # filter/local_attribute/boolean_operator/literal_value/logical_operator/...
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/data_nascimento/isnull/and/nome/eq/r")) # filter/local_attribute/boolean_operator/logical_operator/local_attribute/...
        # 4ยบ step test - testing array[5]
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/nome/eq/Rio/or/data_nascimento/isnull")) # filter/local_attribute/boolean_operator/literal_value/logical_operator/local_attribute...
        self.assertTrue(self.collection_object.filter_operation_sintax_is_ok("filter/data_nascimento/isnull/or/nome/eq/Rio")) # filter/local_attribute/boolean_operator/logical_operator/local_attribute/boolean_operator...

        self.assertFalse(self.collection_object.filter_operation_sintax_is_ok("filter/nome")) # less than 3 indexes
        '''

    def test_offset_limit_operation_sintax(self):
        self.assertTrue( self.collection_object.offset_limit_operation_sintax_is_ok("offset-limit/0&2") )
        self.assertFalse( self.collection_object.offset_limit_operation_sintax_is_ok("offset-limit/0&-2") )
        self.assertFalse( self.collection_object.offset_limit_operation_sintax_is_ok("offset-limit/-1&5") )
        self.assertFalse( self.collection_object.offset_limit_operation_sintax_is_ok("offset-limit/0&2/nome") )
        self.assertFalse( self.collection_object.offset_limit_operation_sintax_is_ok("offset-limit/0&2/nome,email") )
        self.assertTrue( self.collection_object.offset_limit_operation_sintax_is_ok("offset-limit/0&2/collect") )
        self.assertFalse( self.collection_object.offset_limit_operation_sintax_is_ok("offset-limit/0") )


#                               SPECIFIC OPERATIONS TEST
#python manage.py test hyper_resource.tests.CollectOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class CollectOperationTest(AbstractGetRequestTest):

    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    # FeatureCollection return
    def test_collect_operation_with_feature_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/buffer/0.2/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertEquals(first_feature_keys, self.feature_keys)

        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(first_feature_properties_keys, ['nome'])

    def test_collect_operation_with_feature_collection_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/buffer/0.2/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_non_spatial_operation_and_feature_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom&nome/upper")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertEquals(first_feature_keys, self.feature_keys)

        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(first_feature_properties_keys, ['upper']) # possible conceitual error

        #response_dict = self.aux_get_dict_from_response(response)
        #self.assertEquals(list(response_dict["features"][0]["properties"].keys()), ["upper"])

    def test_collect_operation_with_non_spatial_operation_and_feature_collection_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom&nome/upper",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # GeometryCollection return
    def test_collect_operation_with_geometry_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom/buffer/0.2/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.geometry_collection_keys)

        first_geometry_keys = self.aux_get_first_geometry_keys_from_response_list(response)
        self.assertEquals(first_geometry_keys, self.geometry_keys)

    def test_collect_operation_with_geometry_collection_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom/buffer/0.2/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # list return
    def test_collect_operation_with_spatial_operation_and_float_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/area")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ["area", "nome"])

    def test_collect_operation_with_spatial_operation_and_float_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/area",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_alphanumeric_operation(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome/upper")
        self.assertEquals(response.status_code, 200)

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ["upper"])

    def test_collect_operation_with_alphanumeric_operation_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome/upper",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # with projection
    def test_collect_operation_with_projection(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/nome,geom/collect/nome&geom/buffer/0.5")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertListEqual(first_feature_keys, self.feature_keys)

        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(list(first_feature_properties_keys), ["nome"])

    def test_collect_operation_with_projection_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome/upper",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_projection_different_from_collect_attrs(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/geom/collect/nome&geom/buffer/0.5")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.headers['content-type'], 'application/json')


    # ------------------- TESTS FOR COLLECTION -------------------------------------
    # list return
    def test_collect_operation_with_collection_return(self):
        response = requests.get(self.controle_base_uri + "usuario-list/collect/email&nome/upper/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ["email", "upper"])

    def test_collect_operation_with_collection_return_with_accept_header(self):
        response = requests.get(self.controle_base_uri + "usuario-list/collect/email&nome/upper/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_collection_return_only_one_attribute(self):
        response = requests.get(self.controle_base_uri + "usuario-list/collect/nome/upper/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ["upper"])

    def test_collect_operation_with_collection_return_only_one_attribute_with_accept_header(self):
        response = requests.get(self.controle_base_uri + "usuario-list/collect/nome/upper/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # with projection
    def test_collect_operation_with_projection_and_collection_return(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/collect/email&nome/upper/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ["email", "upper"])

    def test_collect_operation_with_projection_collection_return_and_accept_header(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/collect/email&nome/upper/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_for_collection_with_projection_diferent_from_collect_attrs(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/email/collect/email&nome/upper/")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.headers['content-type'], 'application/json')

#python manage.py test hyper_resource.tests.OptionsForCollectOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsForCollectOperationTest(AbstractOptionsRequestTest):
    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    # FeatureCollection return
    def test_options_collect_operation_for_feature_collection_buffer_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/sigla&geom/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "sigla", "subClassOf"])

        #geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_oper_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_collect_operation_for_feature_collection_buffer_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/sigla&geom/buffer/0.2",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "sigla", "subClassOf"])

        #geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_oper_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_collect_operation_for_feature_collection_lower_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom&sigla/lower/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "lower", "rdfs", "subClassOf"])

        #geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_oper_context)
        lower_context_keys = self.aux_get_keys_from_acontext_attrs(response, "lower")
        self.assertEquals(lower_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_collect_operation_for_feature_collection_lower_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom&sigla/lower",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "lower", "rdfs", "subClassOf"])

        #geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        lower_context_keys = self.aux_get_keys_from_acontext_attrs(response, "lower")
        self.assertEquals(lower_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#FeatureCollection')
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    # GeometryCollection return
    def test_options_collect_operation_for_feature_collection_only_geometry_attribute_and_buffer_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "subClassOf"])

        #geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_oper_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#geometry")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_collect_operation_for_feature_collection_only_geometry_attribute_and_buffer_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom/buffer/0.2",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "subClassOf"])

        #geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#geometry")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    # Collection return
    def test_options_collect_operation_for_feature_collection_area_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom/area")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["area", "hydra", "rdfs", "subClassOf"])

        area_context_keys = self.aux_get_keys_from_acontext_attrs(response, "area")  # context for the float value, not the operation
        self.assertEquals(area_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")  # context for the float value, not the operation
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collect_operation_for_feature_collection_area_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom/area",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["area", "hydra", "rdfs", "subClassOf"])

        area_context_keys = self.aux_get_keys_from_acontext_attrs(response, "area") # context for the float value, not the operation
        self.assertEquals(area_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf") # context for the float value, not the operation
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collect_operation_for_feature_collection_only_alphanumeric_attribute_and_lower_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/sigla/lower")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "lower", "rdfs", "subClassOf"])

        lower_context_keys = self.aux_get_keys_from_acontext_attrs(response, "lower")
        self.assertEquals(lower_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Text")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_collect_operation_for_feature_collection_only_alphanumeric_attribute_and_lower_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/sigla/lower",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "lower", "rdfs", "subClassOf"])

        lower_context_keys = self.aux_get_keys_from_acontext_attrs(response, "lower")
        self.assertEquals(lower_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Text")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    # with projection
    def test_options_collect_operation_for_feature_collection_with_projection(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/sigla,geom/collect/sigla&geom/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", 'rdfs', "sigla", 'subClassOf'])

        #geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_collect_operation_for_feature_collection_with_projection_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/sigla,geom/collect/sigla&geom/buffer/0.2",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", 'rdfs', "sigla", 'subClassOf'])

        #geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_collect_operation_for_feature_collection_with_projection_attributes_different_from_collect_attributes(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/geom/collect/sigla&geom/buffer/0.2")
        self.assertEquals(response.status_code, 400)

    # ------------------- TESTS FOR COLLECTION -------------------------------------
    # list return
    # tests for collection collect operation
    def test_options_collect_for_collection_with_lower_operation(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/collect/nome/upper')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'upper'])

        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Text")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_collect_for_collection_with_lower_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/collect/nome/upper',
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'upper'])

        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Text")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collect_for_collection_with_lower_operation_two_attributes(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/collect/nome&email/upper')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf', 'upper'])

        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_attrs_context)
        nome_upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_upper_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collect_for_collection_with_lower_operation_two_attributes_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/collect/nome&email/upper',
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf', 'upper'])

        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_attrs_context)
        nome_upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_upper_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # with projection
    def test_options_collect_for_collection_with_lower_operation_two_attributes_and_projection(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/projection/nome,email/collect/nome&email/upper')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf', 'upper'])

        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_attrs_context)
        nome_upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_upper_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collect_for_collection_with_lower_operation_two_attributes_and_projection_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/projection/nome,email/collect/nome&email/upper',
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf', 'upper'])

        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_attrs_context)
        nome_upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_upper_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collect_for_collection_with_projection_diferent_from_collect_attrs(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/email/collect/email&nome/upper/")
        self.assertEquals(response.status_code, 400)

#python manage.py test hyper_resource.tests.GroupBySumOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class GroupBySumOperationTest(AbstractRequestTest):
    def setUp(self):
        super(GroupBySumOperationTest, self).setUp()

    def test_group_by_sum_operation(self):
        response = requests.get(self.controle_base_uri + "gasto-list/group-by-sum/data&valor")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

#python manage.py test hyper_resource.tests.ProjectionOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class ProjectionOperationTest(AbstractGetRequestTest):

    # --------------- TESTS FOR NONSPATIAL RESOURCE ---------------------------------
    def test_projection_for_non_spatial_resource(self):
        implicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/1/nome,email") # implicit projection
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/json')

        f_response_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_response_keys, ["email", "nome"])

        explicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/1/projection/nome,email") # explicit projection
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/json')

        s_response_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_response_keys, ["email", "nome"])

    def test_projection_for_non_spatial_resource_accept_octet_stream(self):
        implicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/1/nome,email", headers={"Accept": "application/octet-stream"}) # implicit projection
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/1/projection/nome,email", headers={"Accept": "application/octet-stream"}) # explicit projection
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    # --------------- TESTS FOR TIFF RESOURCE ---------------------------------
    def test_projection_for_tiff_resource_all_attributes(self):
        implicit_projection_resp = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rid,rast')
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers["content-type"], 'image/tiff')

        explicit_projection_resp = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/projection/rid,rast')
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers["content-type"], 'image/tiff')

    def test_projection_for_tiff_resource_without_raster_attribute(self):
        implicit_projection_resp = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rid')
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers["content-type"], 'application/json')

        f_response_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_response_keys, ["rid"])

        explicit_projection_resp = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/projection/rid')
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers["content-type"], 'application/json')

        s_response_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_response_keys, ["rid"])

    def test_projection_for_tiff_resource_only_raster_attribute(self):
        implicit_projection_resp = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rast')
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers["content-type"], 'image/tiff')

        explicit_projection_resp = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/projection/rast')
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers["content-type"], 'image/tiff')

    def test_projection_for_tiff_resource_all_attributes_accept_octet_stream(self):
        pass

    def test_projection_for_tiff_resource_without_raster_attribute_accept_octet_stream(self):
        implicit_projection_resp = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rid',
                                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers["content-type"], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/projection/rid',
                                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers["content-type"], 'application/octet-stream')

    def test_projection_for_tiff_resource_only_raster_attribute_accept_octet_stream(self):
        pass

    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    def test_projection_for_feature_resource(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/nome,geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        f_response_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_response_keys, self.feature_keys)

        f_feature_properties_keys = self.aux_get_single_feature_properties_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_feature_properties_keys, ["nome"])

        # explicit projection
        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/nome,geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        s_response_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_response_keys, self.feature_keys)

        s_feature_properties_keys = self.aux_get_single_feature_properties_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_feature_properties_keys, ["nome"])

    def test_projection_for_feature_resource_without_geometric_attribute(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/nome,sigla")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/json')

        f_feature_properties_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_feature_properties_keys, ["nome", "sigla"])

        # explicit projection
        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/nome,sigla")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/json')

        s_feature_properties_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_feature_properties_keys, ["nome", "sigla"])

    def test_projection_for_feature_resource_only_geometric_attribute(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        f_response_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_response_keys, self.geometry_keys)

        # explicit projection
        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        s_response_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_response_keys, self.geometry_keys)

    def test_projection_for_feature_resource_accept_octet_stream(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/nome,geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/nome,geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    def test_projection_for_feature_resource_without_geometric_attribute_accept_octet_stream(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/nome,sigla", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/nome,sigla", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    def test_projection_for_feature_resource_only_geometric_attribute_accept_octet_stream(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        # explicit projection
        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    # --------------- TESTS FOR COLLECTION ---------------------------------
    def test_projection_for_collection_resource(self):
        implicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/nome,email/")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/json')

        f_keys_from_first_element = self.aux_get_first_element_keys_from_response_list(implicit_projection_resp)
        self.assertEquals(f_keys_from_first_element, ['email', 'nome'])

        explicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/json')

        s_keys_from_first_element = self.aux_get_first_element_keys_from_response_list(explicit_projection_resp)
        self.assertEquals(s_keys_from_first_element, ['email', 'nome'])

    def test_projection_for_collection_resource_with_collect_operation(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/collect/email&nome/upper")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        keys_from_frist_element = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(keys_from_frist_element, ['email', 'upper'])

    def test_projection_for_collection_resource_with_collect_operation_projection_list_different_from_collect_list(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/collect/nome/upper")
        self.assertEquals(response.status_code, 400)

    def test_projection_for_collection_resource_accept_octet_stream(self):
        response = requests.get(self.controle_base_uri + "usuario-list/nome,email/", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_projection_for_collection_resource_with_collect_operation_accept_octet_stream(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/collect/email&nome/upper", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    def test_projection_for_feature_collection(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/nome,geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        f_first_feature_keys = self.aux_get_first_feature_keys(implicit_projection_resp)
        self.assertEquals(f_first_feature_keys, self.feature_keys)
        f_first_feature_properties_keys = self.aux_get_first_feature_properties_keys(implicit_projection_resp)
        self.assertEquals(f_first_feature_properties_keys, ['nome'])

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/nome,geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        s_first_feature_keys = self.aux_get_first_feature_keys(explicit_projection_resp)
        self.assertEquals(s_first_feature_keys, self.feature_keys)
        s_first_feature_properties_keys = self.aux_get_first_feature_properties_keys(explicit_projection_resp)
        self.assertEquals(s_first_feature_properties_keys, ['nome'])

    def test_projection_for_feature_collection_without_geometric_attribute(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/nome")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/json')

        f_first_element_keys = self.aux_get_first_element_keys_from_response_list(implicit_projection_resp)
        self.assertEquals(f_first_element_keys, ['nome'])

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/nome")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/json')

        s_first_element_keys = self.aux_get_first_element_keys_from_response_list(explicit_projection_resp)
        self.assertEquals(s_first_element_keys, ['nome'])

    def test_projection_for_feature_collection_only_geometric_attribute(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        f_first_geometry_keys = self.aux_get_first_geometry_keys_from_response_list(implicit_projection_resp)
        self.assertEquals(f_first_geometry_keys, self.geometry_keys)

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        s_first_geometry_keys = self.aux_get_first_geometry_keys_from_response_list(explicit_projection_resp)
        self.assertEquals(s_first_geometry_keys, self.geometry_keys)

    # tests just to know if projection works with collect operation (tests for collect operation must be in his specific test class)
    def test_projection_for_feature_collection_with_collect_operation(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/nome,geom/collect/nome&geom/buffer/0.2")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertEquals(first_feature_keys, self.feature_keys)
        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(first_feature_properties_keys, ['nome'])

    def test_projection_for_feature_collection_with_collect_operation_projection_attributes_different_from_collect_attibutes(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/nome,geom/collect/geom/buffer/0.2")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.headers['content-type'], 'application/json')

    # binary response
    def test_projection_for_feature_collection_accept_octet_stream(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/nome,geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/nome,geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    def test_projection_for_feature_collection_without_geometric_attribute_accept_octet_stream(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/nome", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/nome", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    def test_projection_for_feature_collection_only_geometric_attribute_accept_octet_stream(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    def test_projection_for_feature_collection_with_collect_operation_accept_octet_stream(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/nome,geom/collect/nome&geom/buffer/0.2",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

#python manage.py test hyper_resource.tests.OptionsForProjectionOperation --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsForProjectionOperation(AbstractOptionsRequestTest):

    # --------------- TESTS FOR NONSPATIAL RESOURCE ---------------------------------
    def test_options_for_non_spatial_resource_projection_operation(self):
        # implicit projection
        implicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/1/nome,email")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.basic_operations_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        f_email_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'email')
        self.assertEquals(f_email_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'subClassOf')
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_resp_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(f_resp_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(f_resp_dict['subClassOf'], "hydra:Resource")

        # explicit projection
        explicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/1/projection/nome,email")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.basic_operations_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        s_email_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'email')
        self.assertEquals(s_email_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_subClassOd_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'subClassOf')
        self.assertEquals(s_subClassOd_context_keys, self.keys_from_oper_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_resp_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(s_resp_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(s_resp_dict['subClassOf'], "hydra:Resource")

    def test_options_for_non_spatial_resource_projection_operation_accept_octet_stream(self):
        # implicit projection
        implicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/1/nome,email",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, [])

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        f_email_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'email')
        self.assertEquals(f_email_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'subClassOf')
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@id'], 'https://schema.org/Thing')
        self.assertEqual(f_resp_dict['@type'], 'https://schema.org/Thing')
        self.assertEqual(f_resp_dict['subClassOf'], 'hydra:Resource')

        # explicit projection
        explicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/1/projection/nome,email",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, [])

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        s_email_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'email')
        self.assertEquals(s_email_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'subClassOf')
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_attrs_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@id'], 'https://schema.org/Thing')
        self.assertEqual(s_resp_dict['@type'], 'https://schema.org/Thing')
        self.assertEqual(s_resp_dict['subClassOf'], 'hydra:Resource')

    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    def test_options_for_feature_resource_projection_operation(self):
        # implicit project
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/nome,geom/")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        #f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'geom')
        #self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'subClassOf')
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@id'], 'https://purl.org/geojson/vocab#Feature')
        self.assertEqual(f_resp_dict['@type'], 'https://purl.org/geojson/vocab#Feature')
        self.assertEqual(f_resp_dict['subClassOf'], 'hydra:Resource')

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/projection/nome,geom/")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        #s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'geom')
        #self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'subClassOf')
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_attrs_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@id'], 'https://purl.org/geojson/vocab#Feature')
        self.assertEqual(s_resp_dict['@type'], 'https://purl.org/geojson/vocab#Feature')
        self.assertEqual(s_resp_dict['subClassOf'], 'hydra:Resource')

    def test_options_for_feature_resource_projection_operation_only_geometric_attribute(self):
        # implicit project
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/geom/")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        #f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'geom')
        #self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'subClassOf')
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@id'], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEqual(f_resp_dict['@type'], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEqual(f_resp_dict['subClassOf'], 'hydra:Resource')

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/projection/geom/")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        #s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'geom')
        #self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'subClassOf')
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_attrs_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@id'], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEqual(s_resp_dict['@type'], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEqual(s_resp_dict['subClassOf'], 'hydra:Resource')

    def test_options_for_feature_resource_projection_operation_only_alphanumeric_attribute(self):
        # implicit project
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/nome/")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.string_operations_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'subClassOf')
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@id'], 'https://schema.org/name')
        self.assertEqual(f_resp_dict['@type'], 'https://schema.org/Text')
        self.assertEqual(f_resp_dict['subClassOf'], 'hydra:Resource')

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/projection/nome/")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.string_operations_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'subClassOf')
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_attrs_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@id'], 'https://schema.org/name')
        self.assertEqual(s_resp_dict['@type'], 'https://schema.org/Text')
        self.assertEqual(s_resp_dict['subClassOf'], 'hydra:Resource')

    # --------------- TESTS FOR COLLECTION ---------------------------------
    def test_options_for_collection_resource_projection_operation(self):
        implicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/nome,email")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        f_email_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'email')
        self.assertEquals(f_email_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'subClassOf')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@id'], 'https://schema.org/Thing')
        self.assertEqual(f_resp_dict['@type'], self.collection_vocab)
        self.assertEqual(f_resp_dict['subClassOf'], 'hydra:Resource')

        # explicit projection
        explicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/projection/nome,email")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        s_email_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'email')
        self.assertEquals(s_email_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'subClassOf')
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_oper_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@id'], 'https://schema.org/Thing')
        self.assertEqual(s_resp_dict['@type'], self.collection_vocab)
        self.assertEqual(s_resp_dict['subClassOf'], 'hydra:Resource')

    def test_options_for_collection_resource_projection_operation_with_collect_operation(self):
        response = requests.options(self.controle_base_uri + "usuario-list/projection/nome,email/collect/nome&email/upper")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf', 'upper'])

        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_attrs_context)
        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_context_keys, self.keys_from_oper_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEqual(response_dict['@id'], 'https://schema.org/Thing')
        self.assertEqual(response_dict['@type'], self.collection_vocab)
        self.assertEqual(response_dict['subClassOf'], 'hydra:Resource')

    def test_options_for_collection_resource_projection_operation_with_collect_operation_projection_list_different_from_collect_list(self):
        response = requests.options(self.controle_base_uri + "usuario-list/projection/nome/collect/nome&email/upper")
        self.assertEquals(response.status_code, 400)

    def test_options_for_collection_resource_projection_operation_accept_octet_stream(self):
        implicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/nome,email",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, [])

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        f_email_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'email')
        self.assertEquals(f_email_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'subClassOf')
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@id'], 'https://schema.org/Thing')
        self.assertEqual(f_resp_dict['@type'], self.collection_vocab)
        self.assertEqual(f_resp_dict['subClassOf'], 'hydra:Resource')

        # explicit projection
        explicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/projection/nome,email",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, [])

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        s_email_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'email')
        self.assertEquals(s_email_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'subClassOf')
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_oper_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@id'], 'https://schema.org/Thing')
        self.assertEqual(s_resp_dict['@type'], self.collection_vocab)
        self.assertEqual(s_resp_dict['subClassOf'], 'hydra:Resource')

    def test_options_for_collection_resource_projection_operation_with_collect_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/projection/nome,email/collect/nome&email/upper",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf', 'upper'])

        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_attrs_context)
        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_context_keys, self.keys_from_oper_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEqual(response_dict['@id'], 'https://schema.org/Thing')
        self.assertEqual(response_dict['@type'], self.collection_vocab)
        self.assertEqual(response_dict['subClassOf'], 'hydra:Resource')

    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    def test_options_for_feature_collection_projection_operation(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/nome,geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        #f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "geom")
        #self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "nome")
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "subClassOf")
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(f_response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(f_response_dict["subClassOf"], self.collection_vocab)

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome,geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        #s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "geom")
        #self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "nome")
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "subClassOf")
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_oper_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(s_response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(s_response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_projection_operation_only_geometric_attribute(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        #f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "geom")
        #self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "subClassOf")
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_response_dict["@id"], "https://purl.org/geojson/vocab#geometry")
        self.assertEquals(f_response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(f_response_dict["subClassOf"], self.collection_vocab)

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        #s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "geom")
        #self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "subClassOf")
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_oper_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_response_dict["@id"], "https://purl.org/geojson/vocab#geometry")
        self.assertEquals(s_response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(s_response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_projection_operation_only_alphanumeric_attributes(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/nome")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "nome")
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "subClassOf")
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_response_dict['@id'], 'https://schema.org/name')
        self.assertEqual(f_response_dict['@type'], self.collection_vocab)
        self.assertEqual(f_response_dict['subClassOf'], 'hydra:Resource')

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "nome")
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "subClassOf")
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_oper_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_response_dict['@id'], 'https://schema.org/name')
        self.assertEqual(s_response_dict['@type'], self.collection_vocab)
        self.assertEqual(s_response_dict['subClassOf'], 'hydra:Resource')

    def test_options_for_feature_collection_projection_operation_with_collect_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome,geom/collect/nome&geom/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_collection_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        #geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_oper_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_projection_operation_with_collect_operation_projection_list_different_from_collect_list(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome,geom/collect/geom/buffer/0.2")
        self.assertEquals(response.status_code, 400)

    # Accept: application/octet-stream
    def test_options_for_feature_collection_projection_operation_accept_octet_stream(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/nome,geom",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        #f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "geom")
        #self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "nome")
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "subClassOf")
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(f_response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(f_response_dict["subClassOf"], self.collection_vocab)

        #explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome,geom",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        #s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "geom")
        #self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "nome")
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "subClassOf")
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_attrs_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(s_response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(s_response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_projection_operation_only_geometric_attribute_accept_octet_stream(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/geom",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        #f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "geom")
        #self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "subClassOf")
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_response_dict["@id"], "https://purl.org/geojson/vocab#geometry")
        self.assertEquals(f_response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(f_response_dict["subClassOf"], self.collection_vocab)

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/geom",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        #s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "geom")
        #self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "subClassOf")
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_oper_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_response_dict["@id"], "https://purl.org/geojson/vocab#geometry")
        self.assertEquals(s_response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(s_response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_projection_operation_only_alphanumeric_attributes_accept_octet_stream(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/nome",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, [])

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "nome")
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)
        f_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "subClassOf")
        self.assertEquals(f_subClassOf_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_response_dict['@id'], 'https://schema.org/name')
        self.assertEqual(f_response_dict['@type'], self.collection_vocab)
        self.assertEqual(f_response_dict['subClassOf'], 'hydra:Resource')

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, [])

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "nome")
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "subClassOf")
        self.assertEquals(s_subClassOf_context_keys, self.keys_from_attrs_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_response_dict['@id'], 'https://schema.org/name')
        self.assertEqual(s_response_dict['@type'], self.collection_vocab)
        self.assertEqual(s_response_dict['subClassOf'], 'hydra:Resource')

    def test_options_for_feature_collection_projection_operation_with_collect_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome,geom/collect/nome&geom/buffer/0.2",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_collection_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        #geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        subClassOf_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_context_keys, self.keys_from_oper_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

#python manage.py test hyper_resource.tests.FilterOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class FilterOperationTest(AbstractRequestTest):

    def aux_get_attributes_from_features(self, response, attribute_name):
        response_dict = self.aux_get_dict_from_response(response)
        attrs_arr = [feature['properties'][attribute_name] for feature in response_dict['features'] ]
        return sorted(attrs_arr)

    def test_simple_filter(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/geocodigo/eq/22/")
        self.assertEquals(response.status_code, 200)

        names_list = self.aux_get_attributes_from_features(response, "nome")
        self.assertEquals(names_list, ["Piauí"])

    def test_filter_with_or_operator(self):
        # Maranhão = 21
        # Piauí = 22
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/geocodigo/eq/22/or/nome/eq/Maranhão/")
        self.assertEquals(response.status_code, 200)

        names_list = self.aux_get_attributes_from_features(response, "nome")
        self.assertEquals(names_list, ["Maranhão", "Piauí"])

    def test_filter_with_and_operator(self):
        # Maranhão = 21
        # Piauí = 22
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/geocodigo/eq/22/and/nome/eq/Maranhão/")
        self.assertEquals(response.status_code, 200)

        names_list = self.aux_get_attributes_from_features(response, "nome")
        self.assertEquals(names_list, [])

    # WARNING: This test don't pass and this problem must be solved by the url interpretor
    def test_precedence_between_AND_operator_and_OR_operator(self):
        '''
        Independent of which order you put AND or OR operator, the result must be the same
        (AND operator is always be the first to be considered)
        # Maranhão = 21
        # Piauí = 22
        '''
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/geocodigo/eq/22/or/nome/eq/Maranhão/and/geocodigo/eq/21/")
        self.assertEquals(response.status_code, 200)

        names_list = self.aux_get_attributes_from_features(response, "nome")
        self.assertEquals(names_list, ["Maranhão", "Piauí"])

        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/nome/eq/Maranhão/and/geocodigo/eq/21/or/geocodigo/eq/22/")
        self.assertEquals(response.status_code, 200)

        names_list = self.aux_get_attributes_from_features(response, "nome")
        self.assertEquals(names_list, ["Maranhão", "Piauí"])

#python manage.py test hyper_resource.tests.JoinOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class JoinOperationTest(AbstractGetRequestTest):
    def setUp(self):
        super(JoinOperationTest, self).setUp()
        self.pesquisa_esporte_base_url = "http://172.30.10.86/esporte-list/"
        self.munic_2015_base_uri = "http://172.30.10.86/api/munic-2015/"
        self.pib_municipio_base_uri = "http://172.30.10.86/api/pib-municipio/"
        self.feature_keys = ["geometry", "id", "properties", "type"]

    def aux_get_first_joined_dict_attributes_from_first_feature(self, response):
        first_feature = self.aux_get_first_feature(response)
        first_joined_alfa_dict = first_feature['properties']['__joined__'][0]
        return sorted( list(first_joined_alfa_dict.keys()) )

    def aux_get_first_feature_joined_length(self, response):
        first_feature = self.aux_get_first_feature(response)
        return len(first_feature['properties']['__joined__'])

    def aux_get_first_joined_dict_attributes_from_single_element_response(self, response):
        first_element = self.aux_get_single_element_from_response(response)
        return sorted( first_element["__joined__"][0].keys() )

    def aux_get_first_joined_dict_attributes_from_first_element_response(self, response):
        first_element = self.aux_get_first_element_from_response_list(response)
        return sorted( list(first_element["__joined__"][0].keys()) )

    def aux_get_single_element_joined_length(self, response):
        first_element = self.aux_get_single_element_from_response(response)
        return len(first_element['__joined__'])

    # --------------- TESTS FOR NON SPATIAL RESOURCE ---------------------------------
    def test_join_operation_for_non_spatial_resource_one_to_one_rel(self):
        response = requests.get(self.controle_base_uri + "gasto-list/7/join/cod_municipio&geocodigo/" + self.munic_2015_base_uri + "variaveis-externas-list/3243")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_sigle_element_keys_from_response(response)
        self.assertEquals(first_element_keys, ['__joined__', 'cod_municipio', 'data', 'id', 'tipo_gasto', 'usuario', 'valor'])

        joined_dicts_len = self.aux_get_single_element_joined_length(response)
        self.assertEquals(joined_dicts_len, 1)

        joined_attrs_list = self.aux_get_first_joined_dict_attributes_from_single_element_response(response)
        self.assertEquals(joined_attrs_list, ['classe_tama_populacao_estimada_2015', 'codfigo_uf', 'geocodigo',
                                              'id_variaveis_externas', 'nome_municipio', 'populacao_estimada_2015',
                                              'regiao', 'sigla_unidade_federacao'])

    def test_join_operation_for_non_spatial_resource_one_to_one_rel_accept_octet_stream(self):
        response = requests.get(self.controle_base_uri + "gasto-list/7/join/cod_municipio&geocodigo/" + self.munic_2015_base_uri + "variaveis-externas-list/3243",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_join_operation_for_non_spatial_resource_one_to_many_rel(self):
        response = requests.get(self.controle_base_uri + "gasto-list/7/join/cod_municipio&cod_municipio/" + self.pib_municipio_base_uri + "faturamento-list/filter/cod_municipio/eq/3304557/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_sigle_element_keys_from_response(response)
        self.assertEquals(first_element_keys, ['__joined__', 'cod_municipio', 'data', 'id', 'tipo_gasto', 'usuario', 'valor'])

        joined_dicts_len = self.aux_get_single_element_joined_length(response)
        self.assertEquals(joined_dicts_len, 6)

        joined_attrs_list = self.aux_get_first_joined_dict_attributes_from_single_element_response(response)
        self.assertEquals(joined_attrs_list, ['ano', 'cod_municipio', 'id', 'id_municipio', 'impostos_produtos',
                                              'num_habitantes', 'valor_bruto_adm', 'valor_bruto_agro', 'valor_bruto_ind',
                                              'valor_bruto_serv'])

    def test_join_operation_for_non_spatial_resource_one_to_many_rel_accept_octet_stream(self):
        response = requests.get(self.controle_base_uri + "gasto-list/7/join/cod_municipio&cod_municipio/" + self.pib_municipio_base_uri + "faturamento-list/filter/cod_municipio/eq/3304557/",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')


    # --------------- TESTS FOR COLLECTION RESOURCE ---------------------------------
    def test_join_operations_for_collection_resource_one_to_one_rel(self):
        response = requests.get(self.controle_base_uri + "gasto-list/join/cod_municipio&geocodigo/" + self.munic_2015_base_uri + "variaveis-externas-list/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ['__joined__', 'cod_municipio', 'data', 'id', 'tipo_gasto', 'usuario', 'valor'])

        joined_dicts_len = self.aux_get_first_element_joined_length(response)
        self.assertEquals(joined_dicts_len, 1)

        joined_attrs_list = self.aux_get_first_joined_dict_attributes_from_first_element_response(response)
        self.assertEquals(joined_attrs_list, ['classe_tama_populacao_estimada_2015', 'codfigo_uf', 'geocodigo',
                                              'id_variaveis_externas', 'nome_municipio', 'populacao_estimada_2015',
                                              'regiao', 'sigla_unidade_federacao'])

    def test_join_operations_for_collection_resource_one_to_one_rel_accept_octet_stream(self):
        response = requests.get(self.controle_base_uri + "gasto-list/join/cod_municipio&geocodigo/" + self.munic_2015_base_uri + "variaveis-externas-list/",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_join_operations_for_collection_resource_one_to_many_rel(self):
        response = requests.get(self.controle_base_uri + "gasto-list/join/cod_municipio&cod_municipio/" + self.pib_municipio_base_uri + "faturamento-list/filter/cod_municipio/in/3550308&3304557")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ['__joined__', 'cod_municipio', 'data', 'id', 'tipo_gasto', 'usuario', 'valor'])

        joined_dicts_len = self.aux_get_first_element_joined_length(response)
        self.assertEquals(joined_dicts_len, 6)

        joined_attrs_list = self.aux_get_first_joined_dict_attributes_from_first_element_response(response)
        self.assertEquals(joined_attrs_list, ['ano', 'cod_municipio', 'id', 'id_municipio', 'impostos_produtos',
                                              'num_habitantes', 'valor_bruto_adm', 'valor_bruto_agro', 'valor_bruto_ind',
                                              'valor_bruto_serv'])

    def test_join_operations_for_collection_resource_one_to_many_rel_accept_octet_stream(self):
        response = requests.get(self.controle_base_uri + "gasto-list/join/cod_municipio&cod_municipio/" + self.pib_municipio_base_uri + "faturamento-list/filter/cod_municipio/in/3550308&3304557",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')


    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    def test_join_operation_for_feature_resource_one_to_one_rel(self):
        response = requests.get(self.bcim_base_uri + "municipios/3304557/join/geocodigo&geocodigo/" + self.munic_2015_base_uri + "planejamento-urbano-list/3243/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.feature_keys)

        feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(feature_properties_keys, ["__joined__", "anodereferencia", "geocodigo", "geometriaaproximada", "nome", "nomeabrev"])

        joined_dicts_len = self.aux_get_first_feature_joined_length(response)
        self.assertEquals(joined_dicts_len, 1)

        joined_alfanumeric_attrs = self.aux_get_first_joined_dict_attributes_from_first_feature(response)
        self.assertEquals(joined_alfanumeric_attrs, ['ano_lei_codigo_obras', 'ano_lei_criacao',
                                                     'ano_lei_legis_sob_area_zona_espe_inte_social',
                                                     'ano_lei_legis_sob_zona_area_espe_inter',
                                                     'ano_lei_legis_sobre_parc_solo',
                                                     'ano_lei_legis_sobre_zone_uso_ocupa_solo',
                                                     'ano_lei_legislacao_sobre_contri_melhoria',
                                                     'ano_lei_legislacao_sobre_dire_superficie',
                                                     'ano_lei_legislacao_sobre_estu_impa_vizinhanca',
                                                     'ano_lei_legislacao_sobre_estu_pre_impa_ambiental',
                                                     'ano_lei_legislacao_sobre_legitimacao_posse',
                                                     'ano_lei_legislacao_sobre_ope_urba_consorciada',
                                                     'ano_lei_legislacao_sobre_regula_fundiaria',
                                                     'ano_lei_legislacao_sobre_servi_administrativa',
                                                     'ano_lei_legislacao_sobre_solo_cria_outorga_onerosa_dir_construi',
                                                     'ano_lei_legislacao_sobre_tombamento',
                                                     'ano_lei_legislacao_sobre_uni_conservacao',
                                                     'ano_lei_legislacao_sobre_usuca_espe_imovel_urbano',
                                                     'ano_lei_legislacao_sobre_zonea_ambi_zonea_ecologico_economico',
                                                     'ano_lei_lei_perimetro_urba',
                                                     'ano_leilegislacao_sobre_conce_uso_espe_fins_moradia',
                                                     'ano_ultima_atualizacao', 'caract_orgao_gestor_plane_urba_munic',
                                                     'codigo_municipio', 'codigo_obras_existencia', 'codigo_uf',
                                                     'geocodigo', 'id_planejamento_urbano',
                                                     'informacoes_sob_gestor_escolaridade',
                                                     'legis_sobre_parc_solo_existencia',
                                                     'legislacao_sobre_area_zona_espec_inter_social_existencia',
                                                     'legislacao_sobre_conce_uso_espe_fins_moradia',
                                                     'legislacao_sobre_contri_melhoria_existencia',
                                                     'legislacao_sobre_dire_superficie',
                                                     'legislacao_sobre_estu_impa_vizinhanca_existencia',
                                                     'legislacao_sobre_estu_pre_impa_ambiental',
                                                     'legislacao_sobre_legitimacao_posse',
                                                     'legislacao_sobre_ope_urba_consorciada_existencia',
                                                     'legislacao_sobre_regula_fundiaria',
                                                     'legislacao_sobre_servi_administrativa',
                                                     'legislacao_sobre_solo_cria_outorga_onerosa_dir_construir_exist',
                                                     'legislacao_sobre_tombamento',
                                                     'legislacao_sobre_uni_conservacao',
                                                     'legislacao_sobre_usuca_espe_imovel_urbano',
                                                     'legislacao_sobre_zona_area_espe_inter_existencia',
                                                     'legislacao_sobre_zone_uso_ocupa_solo_existencia',
                                                     'legislacao_sobre_zonea_ambi_zonea_ecologico_economico',
                                                     'lei_perimetro_urba_existencia', 'nome',
                                                     'o_municipio_elabo_plano_diretor', 'plano_diretor_existencia'] )

    def test_join_operation_for_feature_resource_one_to_one_rel_accept_octet_stream(self):
        response = requests.get(self.bcim_base_uri + "municipios/3304557/join/geocodigo&geocodigo/" + self.munic_2015_base_uri + "planejamento-urbano-list/3243/",
                                headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_join_operation_for_feature_resource_one_to_many_rel(self):
        response = requests.get(self.bcim_base_uri + "municipios/3304557/join/geocodigo&cod_municipio/" + self.pib_municipio_base_uri + "faturamento-list/filter/cod_municipio/eq/3304557")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.feature_keys)

        feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(feature_properties_keys, ['__joined__', 'anodereferencia', 'geocodigo', 'geometriaaproximada', 'nome', 'nomeabrev'])

        joined_dicts_len = self.aux_get_first_feature_joined_length(response)
        self.assertEquals(joined_dicts_len, 6)

        joined_dict_attrs = self.aux_get_first_joined_dict_attributes_from_first_feature(response)
        self.assertEquals(joined_dict_attrs, ['ano', 'cod_municipio', 'id', 'id_municipio', 'impostos_produtos',
                                              'num_habitantes', 'valor_bruto_adm', 'valor_bruto_agro',
                                              'valor_bruto_ind', 'valor_bruto_serv'])

    def test_join_operation_for_feature_resource_one_to_many_rel_accept_octet_stream(self):
        response = requests.get(self.bcim_base_uri + "municipios/3304557/join/geocodigo&cod_municipio/" + self.pib_municipio_base_uri + "faturamento-list/filter/cod_municipio/eq/3304557",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')


    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    def test_join_operation_for_feature_collection_one_to_one_rel(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/sigla/in/RJ&ES&MG/join/geocodigo&cod_estado/" + self.pesquisa_esporte_base_url + "cond-funcionamento-list/filter/cod_estado/in/31&32&33&35/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertEquals(first_feature_keys, self.feature_keys)

        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(first_feature_properties_keys, ["__joined__", "geocodigo", "geometriaaproximada", "nome", "nomeabrev", "sigla"])

        joined_alfanumeric_attrs = self.aux_get_first_joined_dict_attributes_from_first_feature(response)
        self.assertEquals(joined_alfanumeric_attrs, ['ano', 'autodromo_func', 'autodromo_parado', 'cod_estado',
                                                     'compl_aqua_func', 'compl_aqua_parado', 'compl_esp_func',
                                                     'compl_esp_parado', 'est_func', 'est_parado', 'gin_func',
                                                     'gin_parado', 'id', 'id_estado', 'kartodromo_func',
                                                     'kartodromo_parado'] )

    def test_join_operation_for_feature_collection_one_to_one_rel_accept_octet_stream(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/sigla/in/RJ&ES&MG/join/geocodigo&cod_estado/" + self.pesquisa_esporte_base_url + "cond-funcionamento-list/filter/cod_estado/in/31&32&33&35/",
                                headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_join_operation_for_feature_collection_one_to_many_rel(self):
        response = requests.get(self.bcim_base_uri + "municipios/filter/nome/in/Rio de Janeiro&Belo Horizonte&Sรฃo Paulo/join/geocodigo&cod_municipio/" + self.pib_municipio_base_uri + "faturamento-list/filter/cod_municipio/in/3304557&3106200&3550308&4106902")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'application/vnd.geo+json')

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertEquals(first_feature_keys, self.feature_keys)

        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(first_feature_properties_keys, ["__joined__", "anodereferencia", "geocodigo", "geometriaaproximada", "nome", "nomeabrev"])

        joined_dicts_len = self.aux_get_first_feature_joined_length(response)
        self.assertEquals(joined_dicts_len, 6)

        joined_dict_attrs = self.aux_get_first_joined_dict_attributes_from_first_feature(response)
        self.assertEquals(joined_dict_attrs, ['ano', 'cod_municipio', 'id', 'id_municipio', 'impostos_produtos',
                                              'num_habitantes', 'valor_bruto_adm', 'valor_bruto_agro',
                                              'valor_bruto_ind', 'valor_bruto_serv'])

    def test_join_operation_for_feature_collection_one_to_many_rel_accept_octet_stream(self):
        response = requests.get(self.bcim_base_uri + "municipios/filter/nome/in/Rio de Janeiro&Belo Horizonte&Sรฃo Paulo/join/geocodigo&cod_municipio/" + self.pib_municipio_base_uri + "faturamento-list/filter/cod_municipio/in/3304557&3106200&3550308&4106902",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'application/octet-stream')

#python manage.py test hyper_resource.tests.OptionsForJoinOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsForJoinOperationTest(AbstractOptionsRequestTest):
    def setUp(self):
        super(OptionsForJoinOperationTest, self).setUp()
        self.pesquisa_esporte_base_url = "http://172.30.10.86/esporte-list/"
        self.munic_2015_base_uri = "http://172.30.10.86/api/munic-2015/"
        self.pib_municipio_base_uri = "http://172.30.10.86/api/pib-municipio/"
        self.keys_from_external_attr_context = ['@id', '@type', self.link_vocab, 'hydra:method']

    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    # todo: provisory test, full context must be implemented
    def test_options_for_feature_resource_join_operation_one_to_one_rel(self):

        response = requests.options(self.bcim_base_uri + "municipios/3304557/join/geocodigo&geocodigo/" + self.munic_2015_base_uri + "planejamento-urbano-list/3243/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.simple_path_options_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['anodereferencia', 'geocodigo', 'geom', 'geometriaaproximada', 'hydra', 'id_objeto', 'nome', 'nomeabrev'])

        geocodigo_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertEquals(geocodigo_acontext_keys, self.keys_from_attrs_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")


        # todo: test for join full context
        '''
        response = requests.options(self.bcim_base_uri + "municipios/3304557/join/geocodigo&geocodigo/" + self.munic_2015_base_uri + "planejamento-urbano-list/3243/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['ano_lei_codigo_obras', 'ano_lei_criacao', 'ano_lei_legis_sob_area_zona_espe_inte_social',
                                          'ano_lei_legis_sob_zona_area_espe_inter', 'ano_lei_legis_sobre_parc_solo',
                                          'ano_lei_legis_sobre_zone_uso_ocupa_solo', 'ano_lei_legislacao_sobre_contri_melhoria',
                                          'ano_lei_legislacao_sobre_dire_superficie', 'ano_lei_legislacao_sobre_estu_impa_vizinhanca',
                                          'ano_lei_legislacao_sobre_estu_pre_impa_ambiental', 'ano_lei_legislacao_sobre_legitimacao_posse',
                                          'ano_lei_legislacao_sobre_ope_urba_consorciada', 'ano_lei_legislacao_sobre_regula_fundiaria',
                                          'ano_lei_legislacao_sobre_servi_administrativa', 'ano_lei_legislacao_sobre_solo_cria_outorga_onerosa_dir_construi',
                                          'ano_lei_legislacao_sobre_tombamento', 'ano_lei_legislacao_sobre_uni_conservacao',
                                          'ano_lei_legislacao_sobre_usuca_espe_imovel_urbano', 'ano_lei_legislacao_sobre_zonea_ambi_zonea_ecologico_economico',
                                          'ano_lei_lei_perimetro_urba', 'ano_leilegislacao_sobre_conce_uso_espe_fins_moradia',
                                          'ano_ultima_atualizacao', 'anodereferencia', 'caract_orgao_gestor_plane_urba_munic',
                                          'codigo_municipio', 'codigo_obras_existencia', 'codigo_uf', 'geocodigo', 'geom',
                                          'geometriaaproximada', 'http://172.30.10.86/api/munic-2015/planejamento-urbano-list/3243/:geocodigo',
                                          'http://172.30.10.86/api/munic-2015/planejamento-urbano-list/3243/:nome', 'id_objeto',
                                          'id_planejamento_urbano', 'informacoes_sob_gestor_escolaridade', 'iri_metadata',
                                          'iri_style', 'legis_sobre_parc_solo_existencia', 'legislacao_sobre_area_zona_espec_inter_social_existencia',
                                          'legislacao_sobre_conce_uso_espe_fins_moradia', 'legislacao_sobre_contri_melhoria_existencia',
                                          'legislacao_sobre_dire_superficie', 'legislacao_sobre_estu_impa_vizinhanca_existencia',
                                          'legislacao_sobre_estu_pre_impa_ambiental', 'legislacao_sobre_legitimacao_posse',
                                          'legislacao_sobre_ope_urba_consorciada_existencia', 'legislacao_sobre_regula_fundiaria',
                                          'legislacao_sobre_servi_administrativa', 'legislacao_sobre_solo_cria_outorga_onerosa_dir_construir_exist',
                                          'legislacao_sobre_tombamento', 'legislacao_sobre_uni_conservacao', 'legislacao_sobre_usuca_espe_imovel_urbano',
                                          'legislacao_sobre_zona_area_espe_inter_existencia', 'legislacao_sobre_zone_uso_ocupa_solo_existencia',
                                          'legislacao_sobre_zonea_ambi_zonea_ecologico_economico', 'lei_perimetro_urba_existencia', 'nome',
                                          'nomeabrev', 'o_municipio_elabo_plano_diretor', 'plano_diretor_existencia'])

        # 'geocodigo' is present in the feature and in the external resourse, hence 'geocodigo' in the external resource must be preffixed
        external_geocodigo_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "http://172.30.10.86/api/munic-2015/planejamento-urbano-list/3243/:geocodigo")
        self.assertEquals(external_geocodigo_acontext_keys, self.keys_from_external_attr_context)
        external_codigo_municipio_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "codigo_municipio")
        self.assertEquals(external_codigo_municipio_acontext_keys, self.keys_from_external_attr_context)
        # 'geocodigo' (without preffix) comes from the feature
        geocodigo_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertEquals(geocodigo_acontext_keys, self.keys_from_attrs_context)
        join_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "join")
        self.assertEquals(join_acontext_keys, self.keys_from_oper_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "Feature")
        '''

    """
    def test_options_for_feature_resource_join_operation_one_to_many_rel(self):
        response = requests.options(self.bcim_base_uri + "municipios/3304557/join/geocodigo&cod_municipio/" +
                                    self.pib_municipio_base_uri + "faturamento-list/filter/cod_municipio/eq/3304557")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['ano_lei_codigo_obras', 'ano_lei_criacao', 'ano_lei_legis_sob_area_zona_espe_inte_social',
                                          'ano_lei_legis_sob_zona_area_espe_inter', 'ano_lei_legis_sobre_parc_solo',
                                          'ano_lei_legis_sobre_zone_uso_ocupa_solo', 'ano_lei_legislacao_sobre_contri_melhoria',
                                          'ano_lei_legislacao_sobre_dire_superficie', 'ano_lei_legislacao_sobre_estu_impa_vizinhanca',
                                          'ano_lei_legislacao_sobre_estu_pre_impa_ambiental', 'ano_lei_legislacao_sobre_legitimacao_posse',
                                          'ano_lei_legislacao_sobre_ope_urba_consorciada', 'ano_lei_legislacao_sobre_regula_fundiaria',
                                          'ano_lei_legislacao_sobre_servi_administrativa', 'ano_lei_legislacao_sobre_solo_cria_outorga_onerosa_dir_construi',
                                          'ano_lei_legislacao_sobre_tombamento', 'ano_lei_legislacao_sobre_uni_conservacao',
                                          'ano_lei_legislacao_sobre_usuca_espe_imovel_urbano', 'ano_lei_legislacao_sobre_zonea_ambi_zonea_ecologico_economico',
                                          'ano_lei_lei_perimetro_urba', 'ano_leilegislacao_sobre_conce_uso_espe_fins_moradia', 'ano_ultima_atualizacao',
                                          'caract_orgao_gestor_plane_urba_munic', 'codigo_municipio', 'codigo_obras_existencia',
                                          'codigo_uf', 'http://172.30.10.86/api/pib-municipio/faturamento-list:geocodigo', 'id_planejamento_urbano',
                                          'informacoes_sob_gestor_escolaridade', 'legis_sobre_parc_solo_existencia',
                                          'legislacao_sobre_area_zona_espec_inter_social_existencia', 'legislacao_sobre_conce_uso_espe_fins_moradia',
                                          'legislacao_sobre_contri_melhoria_existencia', 'legislacao_sobre_dire_superficie',
                                          'legislacao_sobre_estu_impa_vizinhanca_existencia', 'legislacao_sobre_estu_pre_impa_ambiental',
                                          'legislacao_sobre_legitimacao_posse', 'legislacao_sobre_ope_urba_consorciada_existencia',
                                          'legislacao_sobre_regula_fundiaria', 'legislacao_sobre_servi_administrativa',
                                          'legislacao_sobre_solo_cria_outorga_onerosa_dir_construir_exist', 'legislacao_sobre_tombamento',
                                          'legislacao_sobre_uni_conservacao', 'legislacao_sobre_usuca_espe_imovel_urbano',
                                          'legislacao_sobre_zona_area_espe_inter_existencia', 'legislacao_sobre_zone_uso_ocupa_solo_existencia',
                                          'legislacao_sobre_zonea_ambi_zonea_ecologico_economico', 'lei_perimetro_urba_existencia', '(joined) nome', # same attribute name on different resources
                                          'o_municipio_elabo_plano_diretor', 'plano_diretor_existencia',
                                          'anodereferencia', 'geocodigo', 'geom', 'geometriaaproximada', 'id_objeto', 'iri_metadata', 'iri_style', 'nome', 'nomeabrev', 'spatialize'])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "Feature")

    def test_options_for_feature_resource_join_operation__one_to_one_rel_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "municipios/3304557/join/geocodigo&geocodigo/" + self.munic_2015_base_uri + "planejamento-urbano-list/3243/",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['(joined) ano_lei_codigo_obras', '(joined) ano_lei_criacao', '(joined) ano_lei_legis_sob_area_zona_espe_inte_social',
                                          '(joined) ano_lei_legis_sob_zona_area_espe_inter', '(joined) ano_lei_legis_sobre_parc_solo',
                                          '(joined) ano_lei_legis_sobre_zone_uso_ocupa_solo', '(joined) ano_lei_legislacao_sobre_contri_melhoria',
                                          '(joined) ano_lei_legislacao_sobre_dire_superficie', '(joined) ano_lei_legislacao_sobre_estu_impa_vizinhanca',
                                          '(joined) ano_lei_legislacao_sobre_estu_pre_impa_ambiental', '(joined) ano_lei_legislacao_sobre_legitimacao_posse',
                                          '(joined) ano_lei_legislacao_sobre_ope_urba_consorciada', '(joined) ano_lei_legislacao_sobre_regula_fundiaria',
                                          '(joined) ano_lei_legislacao_sobre_servi_administrativa', '(joined) ano_lei_legislacao_sobre_solo_cria_outorga_onerosa_dir_construi',
                                          '(joined) ano_lei_legislacao_sobre_tombamento', '(joined) ano_lei_legislacao_sobre_uni_conservacao',
                                          '(joined) ano_lei_legislacao_sobre_usuca_espe_imovel_urbano', '(joined) ano_lei_legislacao_sobre_zonea_ambi_zonea_ecologico_economico',
                                          '(joined) ano_lei_lei_perimetro_urba', '(joined) ano_leilegislacao_sobre_conce_uso_espe_fins_moradia', '(joined) ano_ultima_atualizacao',
                                          '(joined) caract_orgao_gestor_plane_urba_munic', '(joined) codigo_municipio', '(joined) codigo_obras_existencia',
                                          '(joined) codigo_uf', '(joined) geocodigo', '(joined) id_planejamento_urbano',
                                          '(joined) informacoes_sob_gestor_escolaridade', '(joined) legis_sobre_parc_solo_existencia',
                                          '(joined) legislacao_sobre_area_zona_espec_inter_social_existencia', '(joined) legislacao_sobre_conce_uso_espe_fins_moradia',
                                          '(joined) legislacao_sobre_contri_melhoria_existencia', '(joined) legislacao_sobre_dire_superficie',
                                          '(joined) legislacao_sobre_estu_impa_vizinhanca_existencia', '(joined) legislacao_sobre_estu_pre_impa_ambiental',
                                          '(joined) legislacao_sobre_legitimacao_posse', '(joined) legislacao_sobre_ope_urba_consorciada_existencia',
                                          '(joined) legislacao_sobre_regula_fundiaria', '(joined) legislacao_sobre_servi_administrativa',
                                          '(joined) legislacao_sobre_solo_cria_outorga_onerosa_dir_construir_exist', '(joined) legislacao_sobre_tombamento',
                                          '(joined) legislacao_sobre_uni_conservacao', '(joined) legislacao_sobre_usuca_espe_imovel_urbano',
                                          '(joined) legislacao_sobre_zona_area_espe_inter_existencia', '(joined) legislacao_sobre_zone_uso_ocupa_solo_existencia',
                                          '(joined) legislacao_sobre_zonea_ambi_zonea_ecologico_economico', '(joined) lei_perimetro_urba_existencia', '(joined) nome', # same attribute name on different resources
                                          '(joined) o_municipio_elabo_plano_diretor', '(joined) plano_diretor_existencia',
                                          'anodereferencia', 'geocodigo', 'geom', 'geometriaaproximada', 'id_objeto', 'iri_metadata', 'iri_style', 'nome', 'nomeabrev', 'spatialize'])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "Geobuf")

    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    def test_join_operation_with_filter(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/filter/sigla/in/RJ&ES&MG/join/geocodigo&cod_estado/" +
                                    self.pesquisa_esporte_base_url + "cond-funcionamento-list/filter/cod_estado/in/31&32&33&35/")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["join"])

        join_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'join')
        self.assertListEqual(join_context_keys_list, ["@id", "@type"])

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')
    """


#                               RESOURCE TYPES TEST (GET, HEAD and OPTIONS requests)
# EntryPointResource
#python manage.py test hyper_resource.tests.EntryPointTest --testrunner=hyper_resource.tests.NoDbTestRunner
class EntryPointTest(AbstractGetRequestTest):

    # simple path
    def test_entry_point_resource_simple_path(self):
        response = requests.get(self.controle_base_uri)
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, ['gasto-list', 'tipo-gasto-list', 'usuario-list'])

    def test_entry_point_resource_simple_path_accept_octet_stream(self):
        response = requests.get(self.controle_base_uri, headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

    def test_entry_point_resource_simple_path_accept_image_png(self):
        pass

    # operations
    def test_entry_point_resource_count_resource_operation(self):
        response = requests.get(self.controle_base_uri + 'count-resource')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, ['count-resource'])

    def test_entry_point_resource_count_resource_operation_accept_octet_stream(self):
        response = requests.get(self.controle_base_uri + 'count-resource')
        self.assertEquals(response.status_code, 200)

    def test_entry_point_resource_count_resource_operation_accept_image_png(self):
        pass

#python manage.py test hyper_resource.tests.OptionsEntryPointTest --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsEntryPointTest(AbstractOptionsRequestTest):
    '''
    Class for tests every possible OPTIONS request for EntryPointResource
    '''

    # simple path
    def test_options_for_entry_point_resource_simple_path(self):
        response = requests.options(self.controle_base_uri)
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['gasto-list', 'hydra', 'rdfs', 'subClassOf', 'tipo-gasto-list', 'usuario-list'])

        gasto_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'gasto-list') # for each key of the entrypoint {@type: hydra:link}
        self.assertEquals(gasto_acontext_keys, self.keys_from_attrs_context)
        tipo_gasto_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'tipo-gasto-list')
        self.assertEquals(tipo_gasto_acontext_keys, self.keys_from_attrs_context)
        usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'usuario-list')
        self.assertEquals(usuario_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        suppoorted_property_keys = self.aux_get_supported_property_keys(response)
        self.assertListEqual(suppoorted_property_keys, self.expected_supported_property_keys)

        suppoerted_properties_names = self.aux_get_supported_properties_names(response)
        self.assertListEqual(suppoerted_properties_names, ['gasto-list', 'tipo-gasto-list', 'usuario-list'])

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.entrypoint_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], self.link_vocab)
        self.assertEquals(response_dict["@type"], self.entrypoint_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # operations
    def test_options_for_entry_point_resource_count_resource_operation(self):
        response = requests.options(self.controle_base_uri + "count-resource")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count-resource', 'hydra', 'rdfs', 'subClassOf'])

        count_resource_resource_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'count-resource')
        self.assertEquals(count_resource_resource_acontext_keys, self.keys_from_oper_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_oper_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "hydra:totalItems")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # simple path (binary)
    def test_options_for_entry_point_resource_simple_path_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri, headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['gasto-list', 'hydra', 'rdfs', 'subClassOf', 'tipo-gasto-list', 'usuario-list'])

        gasto_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'gasto-list')
        self.assertEquals(gasto_acontext_keys, self.keys_from_attrs_context)
        tipo_gasto_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'tipo-gasto-list')
        self.assertEquals(tipo_gasto_acontext_keys, self.keys_from_attrs_context)
        usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'usuario-list')
        self.assertEquals(usuario_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        suppoorted_property_keys = self.aux_get_supported_property_keys(response)
        self.assertListEqual(suppoorted_property_keys, self.expected_supported_property_keys)

        suppoerted_properties_names = self.aux_get_supported_properties_names(response)
        self.assertListEqual(suppoerted_properties_names, ['gasto-list', 'tipo-gasto-list', 'usuario-list'])

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], self.link_vocab)
        self.assertEquals(response_dict["@type"], self.entrypoint_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # operations (binary)
    def test_options_for_entry_point_resource_count_resource_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "count-resource", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count-resource', 'hydra', 'rdfs', 'subClassOf'])

        count_resource_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'count-resource')
        self.assertEquals(count_resource_acontext_keys, self.keys_from_oper_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "hydra:totalItems")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # simple path (image)
    def test_options_for_entry_point_resource_simple_path_accept_image_png(self):
        pass

    # operations (image)
    def test_options_for_entry_point_resource_count_resource_operation_accept_image_png(self):
        pass

#python manage.py test hyper_resource.tests.HeadEntryPointTest --testrunner=hyper_resource.tests.NoDbTestRunner
class HeadEntryPointTest(AbstractHeadRequestTest):

    # simple path
    def test_head_for_entry_point_resource_simple_path(self):
        response_head = requests.head(self.controle_base_uri)
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.controle_base_uri)
        self.assertEquals(response_get.status_code, 200)
        response_options = requests.options(self.controle_base_uri)
        self.assertEquals(response_options.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        options_headers = self.aux_get_headers_list_from_response(response_options)
        self.assertListEqual(head_headers, get_headers)
        self.assertListEqual(head_headers, options_headers)

        # compare HEAD with GET headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)

        # compare HEAD with OPTIONS headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_options.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_options.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_options.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_options.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_options.headers["allow"])
        self.assertEquals(response_head.headers["link"],                            response_options.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_options.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_options.headers["vary"])
        self.assertIn("Date", options_headers)
        self.assertIn("Content-Type", options_headers)

    def test_head_for_entry_point_resource_simple_path_accept_octet_stream(self):
        response_head = requests.head(self.controle_base_uri, headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.controle_base_uri, headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_get.status_code, 200)
        response_options = requests.options(self.controle_base_uri, headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_options.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        options_headers = self.aux_get_headers_list_from_response(response_options)
        self.assertListEqual(head_headers, get_headers)
        self.assertListEqual(head_headers, options_headers)

        # compare HEAD with GET headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)

        # compare HEAD with OPTIONS headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_options.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_options.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_options.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_options.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_options.headers["allow"])
        self.assertEquals(response_head.headers["link"],                            response_options.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_options.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_options.headers["vary"])
        self.assertIn("Date", options_headers)
        self.assertIn("Content-Type", options_headers)

    def test_head_for_entry_point_resource_simple_path_accept_image_png(self):
        pass

    #operations
    def test_head_for_entry_point_resource_count_resource_operation(self):
        response_head = requests.head(self.controle_base_uri + "count-resource")
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.controle_base_uri + "count-resource")
        self.assertEquals(response_get.status_code, 200)
        response_options = requests.options(self.controle_base_uri + "count-resource")
        self.assertEquals(response_options.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        options_headers = self.aux_get_headers_list_from_response(response_options)
        self.assertListEqual(head_headers, get_headers)
        self.assertListEqual(head_headers, options_headers)

        # compare HEAD with GET headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)

        # compare HEAD with OPTIONS headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_options.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_options.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_options.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_options.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_options.headers["allow"])
        self.assertEquals(response_head.headers["link"],                            response_options.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_options.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_options.headers["vary"])
        self.assertIn("Date", options_headers)
        self.assertIn("Content-Type", options_headers)

    def test_head_for_entry_point_resource_count_resource_operation_accept_octet_stream(self):
        response_head = requests.head(self.controle_base_uri + "count-resource", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.controle_base_uri + "count-resource", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_get.status_code, 200)
        response_options = requests.options(self.controle_base_uri + "count-resource", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_options.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        options_headers = self.aux_get_headers_list_from_response(response_options)
        self.assertListEqual(head_headers, get_headers)
        self.assertListEqual(head_headers, options_headers)

        # compare HEAD with GET headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)

        # compare HEAD with OPTIONS headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_options.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_options.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_options.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_options.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_options.headers["allow"])
        self.assertEquals(response_head.headers["link"],                            response_options.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_options.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_options.headers["vary"])
        self.assertIn("Date", options_headers)
        self.assertIn("Content-Type", options_headers)

    def test_head_for_entry_point_resource_count_resource_operation_accept_image_png(self):
        pass

# RasterResource
#python manage.py test hyper_resource.tests.RasterTest --testrunner=hyper_resource.tests.NoDbTestRunner
class RasterTest(AbstractRequestTest):
    '''
    Class for tests every possible GET request for RasterResources
    '''

    # simple path
    def test_tiff_resource_simple_path(self):
        response = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'image/tiff')

    # only attributes
    def test_tiff_resource_all_attributes(self):
        response = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rid,rast')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'image/tiff')

    def test_tiff_resource_only_raster_attribute(self):
        response = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rast')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'image/tiff')

    def test_tiff_resource_only_alphanumeric_attributes(self):
        response = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rid')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'application/json')

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, ["rid"])

    def test_tiff_resource_only_alphanumeric_attributes_accept_octet_stream(self):
        response = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rid',
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'application/octet-stream')

    # operations
    def test_tiff_resource_driver_operation(self):
        response = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/driver')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'application/json')

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, ["driver"])

    def test_tiff_resource_transform_operation(self):
        response = requests.get(self.raster_base_uri + "imagem-exemplo-tile1-list/61/transform/3086")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'image/tiff')

    def test_tiff_resource_driver_operation_accept_octet_stream(self):
        response = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/driver',
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'application/octet-stream')

    def test_tiff_resource_transform_operation_accept_octet_stream(self):
        response = requests.get(self.raster_base_uri + "imagem-exemplo-tile1-list/61/transform/3086",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'application/octet-stream')

#python manage.py test hyper_resource.tests.OptionsForRasterTest --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsForRasterTest(AbstractOptionsRequestTest):
    '''
    Class for tests every possible OPTIONS request for RasterResources
    '''

    # simple path
    def test_options_raster_resource_simple_path(self):
        response = requests.options(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "subClassOf"])

        #rast_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "rast")
        #self.assertEquals(rast_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.raster_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["@type"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # only attributes
    def test_options_tiff_resource_all_attributes(self):
        response = requests.options(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rid,rast')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "subClassOf"])

        #rast_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "rast")
        #self.assertEquals(rast_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.raster_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["@type"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_tiff_resource_only_raster_attribute(self):
        response = requests.options(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rast')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", 'rdfs', 'subClassOf'])

        #rast_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "rast")
        #self.assertEquals(rast_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.raster_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["@type"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_tiff_resource_only_alphanumeric_attributes(self):
        response = requests.options(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rid')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "rid", "subClassOf"])

        rid_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "rid")
        self.assertEquals(rid_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/identifier")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # operations
    def test_options_tiff_resource_driver_operation(self):
        response = requests.options(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/driver')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["driver", "hydra", "rdfs", "subClassOf"])

        driver_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "driver")
        self.assertEquals(driver_acontext_keys, self.keys_from_oper_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_oper_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Text")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_tiff_resource_transform_operation(self):
        response = requests.options(self.raster_base_uri + "imagem-exemplo-tile1-list/61/transform/3086")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "subClassOf"])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_oper_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.raster_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["@type"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # simple path (binary)
    def test_options_raster_resource_simple_path_accept_octet_stream(self):
        response = requests.options(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/',
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "subClassOf"])

        #rast_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "rast")
        #self.assertEquals(rast_acontext_keys, self.keys_from_attrs_context)
        #rid_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "rid")
        #self.assertEquals(rid_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["@type"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # only attributes
    def test_options_tiff_resource_all_attributes_accept_octet_stream(self):
        response = requests.options(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rid,rast',
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "subClassOf"])

        #rast_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "rast")
        #self.assertEquals(rast_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["@type"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_tiff_resource_only_raster_attribute_accept_octet_stream(self):
        response = requests.options(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rast',
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", 'rdfs', 'subClassOf'])

        #rast_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "rast")
        #self.assertEquals(rast_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["@type"], "https://schema.org/ImageObject")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_tiff_resource_only_alphanumeric_attributes_accept_octet_stream(self):
        response = requests.options(self.raster_base_uri + 'imagem-exemplo-tile1-list/61/rid',
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["hydra", "rdfs", "rid", "subClassOf"])

        rid_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "rid")
        self.assertEquals(rid_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/identifier")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

# FeatureCollectionResource
#python manage.py test hyper_resource.tests.FeatureCollectionTest --testrunner=hyper_resource.tests.NoDbTestRunner
class FeatureCollectionTest(AbstractGetRequestTest):
    '''
    Class for tests every possible GET request for FeatureCollectionResource
    '''

    pass

#python manage.py test hyper_resource.tests.OptionsFeatureCollectionTest --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsFeatureCollectionTest(AbstractOptionsRequestTest):
    '''
    Class for tests every possible OPTIONS request for FeatureCollectionResource
    '''

    # simple path
    def test_options_feature_collection_simple_path(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['geocodigo', 'geometriaaproximada', 'hydra', 'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'sigla', 'subClassOf'])

        geocodigo_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geocodigo')
        self.assertEquals(geocodigo_acontext_keys, self.keys_from_attrs_context)
        geometriaaproximada_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geometriaaproximada')
        self.assertEquals(geometriaaproximada_acontext_keys, self.keys_from_attrs_context)
        id_objeto_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id_objeto')
        self.assertEquals(id_objeto_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nomeabrev_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nomeabrev')
        self.assertEquals(nomeabrev_acontext_keys, self.keys_from_attrs_context)
        sigla_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'sigla')
        self.assertEquals(sigla_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_property_keys = self.aux_get_supported_property_keys(response)
        self.assertEquals(supported_property_keys, self.expected_supported_property_keys)

        supported_properties_names = self.aux_get_supported_properties_names(response)
        self.assertEquals(supported_properties_names, ['geocodigo', 'geom', 'geometriaaproximada',
                                                       'id_objeto', 'nome', 'nomeabrev', 'sigla'])

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/State")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    # only attributes
    def test_options_feature_collection_with_geometry_attribute(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/geom,nome")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_feature_collection_only_geometry_attribute(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/geom")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#geometry")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_feature_collection_without_geometry_attribute(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/nome,sigla")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'sigla', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        sigla_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'sigla')
        self.assertEquals(sigla_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    def test_options_feature_collection_only_one_alphanumeric_attribute(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/nome")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/name")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    # operations
    def test_options_feature_collection_within_operation(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + "unidades-federativas/ES")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['codigofunai', 'etnia', 'geometriaaproximada', 'hydra', 'id_objeto', 'nome', 'nomeabrev',
                           'rdfs', 'subClassOf', 'terraindigena'])

        codigofunai_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'codigofunai')
        self.assertEquals(codigofunai_acontext_keys, self.keys_from_attrs_context)
        geometriaaproximada_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geometriaaproximada')
        self.assertEquals(geometriaaproximada_acontext_keys, self.keys_from_attrs_context)
        id_objeto_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id_objeto')
        self.assertEquals(id_objeto_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nomeabrev_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nomeabrev')
        self.assertEquals(nomeabrev_acontext_keys, self.keys_from_attrs_context)
        etnia_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'etnia')
        self.assertEquals(etnia_acontext_keys, self.keys_from_attrs_context)
        terraindigena_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'terraindigena')
        self.assertEquals(terraindigena_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_feature_collection_union_operation(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/union")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra','rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPoint")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPoint")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_collection_make_line_operation(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/make-line")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra','rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#LineString")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#LineString")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_collection_extent_operation(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/extent")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['extent', 'hydra','rdfs', 'subClassOf'])

        extent_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'extent')
        self.assertEquals(extent_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ItemList")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # simple path (binary)
    def test_options_feature_collection_simple_path_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['geocodigo', 'geometriaaproximada', 'hydra', 'id_objeto', 'nome', 'nomeabrev', 'rdfs',
                           'sigla', 'subClassOf'])

        geocodigo_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geocodigo')
        self.assertEquals(geocodigo_acontext_keys, self.keys_from_attrs_context)
        geometriaaproximada_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geometriaaproximada')
        self.assertEquals(geometriaaproximada_acontext_keys, self.keys_from_attrs_context)
        id_objeto_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id_objeto')
        self.assertEquals(id_objeto_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nomeabrev_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nomeabrev')
        self.assertEquals(nomeabrev_acontext_keys, self.keys_from_attrs_context)
        sigla_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'sigla')
        self.assertEquals(sigla_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_property_keys = self.aux_get_supported_property_keys(response)
        self.assertEquals(supported_property_keys, self.expected_supported_property_keys)

        supported_properties_names = self.aux_get_supported_properties_names(response)
        self.assertEquals(supported_properties_names, ['geocodigo', 'geom', 'geometriaaproximada', 'id_objeto', 'nome',
                                                       'nomeabrev', 'sigla'])

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/State")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    # only attributes (binary)
    def test_options_feature_collection_with_geometry_attribute_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/geom,nome",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_feature_collection_only_geometry_attribute_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/geom",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#geometry")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_feature_collection_without_geometry_attribute_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/nome,sigla",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'sigla', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        sigla_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'sigla')
        self.assertEquals(sigla_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    def test_options_feature_collection_only_one_alphanumeric_attribute_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/nome",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/name")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    # operations (binary)
    def test_options_feature_collection_within_operation_accept_octet_stream(self):
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + "unidades-federativas/ES",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['codigofunai', 'etnia', 'geometriaaproximada', 'hydra', 'id_objeto', 'nome', 'nomeabrev',
                           'rdfs', 'subClassOf', 'terraindigena'])

        codigofunai_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'codigofunai')
        self.assertEquals(codigofunai_acontext_keys, self.keys_from_attrs_context)
        geometriaaproximada_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geometriaaproximada')
        self.assertEquals(geometriaaproximada_acontext_keys, self.keys_from_attrs_context)
        id_objeto_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id_objeto')
        self.assertEquals(id_objeto_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nomeabrev_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nomeabrev')
        self.assertEquals(nomeabrev_acontext_keys, self.keys_from_attrs_context)
        etnia_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'etnia')
        self.assertEquals(etnia_acontext_keys, self.keys_from_attrs_context)
        terraindigena_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'terraindigena')
        self.assertEquals(terraindigena_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_feature_collection_union_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/union", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPoint")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPoint")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_collection_make_line_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/make-line", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra','rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#LineString")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#LineString")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_collection_extent_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/extent", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['extent', 'hydra','rdfs', 'subClassOf'])

        extent_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'extent')
        self.assertEquals(extent_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ItemList")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # simple path (image)
    def test_options_feature_collection_simple_path_accept_image_png(self):
        pass

    # only attributes (image)
    def test_options_feature_collection_with_geometry_attribute_accept_image_png(self):
        pass

    def test_options_feature_collection_only_geometry_attribute_accept_image_png(self):
        pass

    def test_options_feature_collection_without_geometry_attribute_accept_image_png(self):
        pass

    # operations (image)
    def test_options_feature_collection_within_operation_accept_image_png(self):
        pass

    def test_options_feature_collection_union_operation_accept_image_png(self):
        pass

    def test_options_feature_collection_make_line_operation_accept_image_png(self):
        pass

    def test_options_feature_collection_extent_operation_accept_image_png(self):
        pass


#python manage.py test hyper_resource.tests.HeadFeatureCollectionTest --testrunner=hyper_resource.tests.NoDbTestRunner
class HeadFeatureCollectionTest(AbstractHeadRequestTest):
    '''
    Tests if GET response headers is the same as HEAD response headers and OPTIONS response headers. Requests for FeatureCollectionResource
    '''

    # feature entry point
    def test_head_entry_point(self):
        response_head = requests.head(self.bcim_base_uri)
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri)
        self.assertEquals(response_get.status_code, 200)
        response_options = requests.options(self.bcim_base_uri)
        self.assertEquals(response_options.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        options_headers = self.aux_get_headers_list_from_response(response_options)
        self.assertListEqual(head_headers, get_headers)
        self.assertListEqual(head_headers, options_headers)

        # compare HEAD with GET headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)

        # compare HEAD with OPTIONS headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_options.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_options.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_options.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_options.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_options.headers["allow"])
        #self.assertEquals(response_head.headers["content-type"],                    response_options.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_options.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_options.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_options.headers["vary"])
        self.assertIn("Date", options_headers)
        self.assertIn("Content-Type", options_headers)

    # features entry point (binary) todo
    def test_head_feature_entry_point_accept_octet_stream(self):
        response_head = requests.head(self.bcim_base_uri,
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_head.status_code, 200)

    # features entry point (image)
    def test_head_feature_entry_point_accept_image_png(self):
        pass

    '''
    # raster entry point
    def test_head_raster_entry_point(self):
        response_head = requests.head(self.raster_base_uri)
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.raster_base_uri)
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertEquals(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        #self.assertEquals(response_head.headers["connection"],                      response_get.headers["connection"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)

    def test_head_raster_entry_point_accept_octet_stream(self):
        response_head = requests.head(self.raster_base_uri,
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_head.status_code, 406)

    def test_head_raster_entry_point_accept_image_png(self):
        pass

    '''

    # simple path
    def test_head_feature_collection_simple_path(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/")
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/")
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertListEqual(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    # simple path (binary)
    def test_head_feature_collection_simple_path_accept_octet_stream(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/",
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/",
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertEquals(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    # simple path (image)
    def test_head_feature_collection_simple_path_accept_image_png(self):
        pass


    # only attributes (default)
    def test_head_feature_collection_with_geometry_attribute(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/nome,geom")
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/nome,geom")
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertListEqual(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    def test_head_feature_collection_only_geometry_attribute(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/geom")
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/geom")
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertListEqual(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    def test_head_feature_collection_without_geometry_attribute(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/nome")
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/nome")
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertListEqual(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    # only attributes (binary)
    def test_head_feature_collection_with_geometry_attribute_accept_octet_stream(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/nome,geom",
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/nome,geom",
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertListEqual(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    def test_head_feature_collection_only_geometry_attribute_accept_octet_stream(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/geom",
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/geom",
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertEquals(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    def test_head_feature_collection_without_geometry_attribute_accept_octet_stream(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/nome",
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/nome",
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertListEqual(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    # only attributes (image)
    def test_head_feature_collection_with_geometry_attribute_accept_image_png(self):
        pass

    def test_head_feature_collection_only_geometry_attribute_accept_image_png(self):
        pass

    def test_head_feature_collection_without_geometry_attribute_accept_image_png(self):
        pass


    # operations (default)
    def test_head_feature_collection_within_operation(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertListEqual(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    def test_head_feature_collection_count_resource_operations(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/count-resource")
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/count-resource")
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertListEqual(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    # operations (binary)
    def test_head_feature_collection_within_operation_accept_octet_stream(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + 'unidades-federativas/ES',
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + 'unidades-federativas/ES',
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertListEqual(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    def test_head_feature_collection_count_resource_operations_accept_octet_stream(self):
        response_head = requests.head(self.bcim_base_uri + "aldeias-indigenas/count-resource",
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_head.status_code, 200)
        response_get = requests.get(self.bcim_base_uri + "aldeias-indigenas/count-resource",
                                      headers={"Accept": "application/octet-stream"})
        self.assertEquals(response_get.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        self.assertListEqual(head_headers, get_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)
        self.assertIn("Etag", head_headers)
        self.assertIn("Etag", get_headers)

    # operations (image)
    def test_head_feature_collection_within_operation_accept_image_png(self):
        pass

    def test_head_feature_collection_count_resource_operations_accept_image_png(self):
        pass

# CollectionResource
#python manage.py test hyper_resource.tests.OptionsCollectionResource --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsCollectionResource(AbstractOptionsRequestTest):

    # simple path
    def test_options_collection_simple_path(self):
        response = requests.options(self.controle_base_uri + "usuario-list")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs',
                           'senha', 'subClassOf'])

        data_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data_nascimento')
        self.assertEquals(data_nascimento_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        id_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id')
        self.assertEquals(id_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nome_usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome_usuario')
        self.assertEquals(nome_usuario_acontext_keys, self.keys_from_attrs_context)
        senha_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'senha')
        self.assertEquals(senha_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_property_keys = self.aux_get_supported_property_keys(response)
        self.assertListEqual(supported_property_keys, self.expected_supported_property_keys)

        supported_properties_names = self.aux_get_supported_properties_names(response)
        self.assertListEqual(supported_properties_names, ['data_nascimento', 'email', 'id', 'nome', 'nome_usuario', 'senha'])

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # only attributes
    def test_options_collection_only_attributes(self):
        response = requests.options(self.controle_base_uri + "usuario-list/nome,email")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_only_one_attribute(self):
        response = requests.options(self.controle_base_uri + "usuario-list/nome")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/name")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # operations
    def test_options_collection_filter_operation(self):
        response = requests.options(self.controle_base_uri + "usuario-list/filter/eq/Rio")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs',
                           'senha', 'subClassOf'])

        data_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data_nascimento')
        self.assertEquals(data_nascimento_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        id_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id')
        self.assertEquals(id_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nome_usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome_usuario')
        self.assertEquals(nome_usuario_acontext_keys, self.keys_from_attrs_context)
        senha_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'senha')
        self.assertEquals(senha_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_collect_operation(self):
        response = requests.options(self.controle_base_uri + "usuario-list/collect/email&nome/upper")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['email', 'hydra', 'rdfs', 'subClassOf', 'upper'])

        upper_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_count_resource_operation(self):
        response = requests.options(self.controle_base_uri + "usuario-list/count-resource")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count-resource', 'hydra', 'rdfs', 'subClassOf'])

        count_resource_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'count-resource')
        self.assertEquals(count_resource_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "hydra:totalItems")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_offset_limit_operation(self):
        response = requests.options(self.controle_base_uri + "usuario-list/offset-limit/0&2")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs',
                           'senha', 'subClassOf'])

        data_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data_nascimento')
        self.assertEquals(data_nascimento_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        id_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id')
        self.assertEquals(id_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nome_usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome_usuario')
        self.assertEquals(nome_usuario_acontext_keys, self.keys_from_attrs_context)
        senha_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'senha')
        self.assertEquals(senha_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_distinct_operation(self):
        response = requests.options(self.controle_base_uri + "usuario-list/distinct/nome")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs',
                           'senha', 'subClassOf'])

        data_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data_nascimento')
        self.assertEquals(data_nascimento_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        id_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id')
        self.assertEquals(id_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nome_usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome_usuario')
        self.assertEquals(nome_usuario_acontext_keys, self.keys_from_attrs_context)
        senha_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'senha')
        self.assertEquals(senha_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_group_by_count_operation(self):
        response = requests.options(self.controle_base_uri + "usuario-list/group-by-count/nome")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        count_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'count')
        self.assertEquals(count_nascimento_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_group_by_sum_operation(self):
        response = requests.options(self.controle_base_uri + "gasto-list/group-by-sum/data&valor")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['data', 'hydra', 'rdfs', 'subClassOf', 'sum'])

        data_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data')
        self.assertEquals(data_acontext_keys, self.keys_from_attrs_context)
        sum_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'sum')
        self.assertEquals(sum_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_projection_operation(self):
        response = requests.options(self.controle_base_uri + "usuario-list/projection/nome,email")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # simple path (binary)
    def test_options_collection_simple_path_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs',
                           'senha', 'subClassOf'])

        data_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data_nascimento')
        self.assertEquals(data_nascimento_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        id_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id')
        self.assertEquals(id_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nome_usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome_usuario')
        self.assertEquals(nome_usuario_acontext_keys, self.keys_from_attrs_context)
        senha_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'senha')
        self.assertEquals(senha_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_property_keys = self.aux_get_supported_property_keys(response)
        self.assertListEqual(supported_property_keys, self.expected_supported_property_keys)

        supported_properties_names = self.aux_get_supported_properties_names(response)
        self.assertListEqual(supported_properties_names,
                             ['data_nascimento', 'email', 'id', 'nome', 'nome_usuario', 'senha'])

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # only attributes (binary)
    def test_options_collection_only_attributes_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/nome,email",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_only_one_attribute_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/nome",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/name")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # operations (binary)
    def test_options_collection_filter_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/filter/eq/Rio",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs',
                           'senha', 'subClassOf'])

        data_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data_nascimento')
        self.assertEquals(data_nascimento_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        id_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id')
        self.assertEquals(id_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nome_usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome_usuario')
        self.assertEquals(nome_usuario_acontext_keys, self.keys_from_attrs_context)
        senha_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'senha')
        self.assertEquals(senha_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_collect_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/collect/email&nome/upper",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['email', 'hydra', 'rdfs', 'subClassOf', 'upper'])

        upper_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_count_resource_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/count-resource",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count-resource', 'hydra', 'rdfs', 'subClassOf'])

        count_resource_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'count-resource')
        self.assertEquals(count_resource_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "hydra:totalItems")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_offset_limit_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/offset-limit/0&2",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs',
                           'senha', 'subClassOf'])

        data_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data_nascimento')
        self.assertEquals(data_nascimento_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        id_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id')
        self.assertEquals(id_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nome_usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome_usuario')
        self.assertEquals(nome_usuario_acontext_keys, self.keys_from_attrs_context)
        senha_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'senha')
        self.assertEquals(senha_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_distinct_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/distinct/nome",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys,
                          ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs',
                           'senha', 'subClassOf'])

        data_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data_nascimento')
        self.assertEquals(data_nascimento_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        id_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id')
        self.assertEquals(id_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        nome_usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome_usuario')
        self.assertEquals(nome_usuario_acontext_keys, self.keys_from_attrs_context)
        senha_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'senha')
        self.assertEquals(senha_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_group_by_count_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/group-by-count/nome",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        count_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'count')
        self.assertEquals(count_nascimento_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_group_by_sum_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "gasto-list/group-by-sum/data&valor",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['data', 'hydra', 'rdfs', 'subClassOf', 'sum'])

        data_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data')
        self.assertEquals(data_acontext_keys, self.keys_from_attrs_context)
        sum_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'sum')
        self.assertEquals(sum_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_collection_projection_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/projection/nome,email",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "http://www.w3.org/ns/hydra/core#Collection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

# NonSpatialResource
#python manage.py test hyper_resource.tests.OptionsNonSpatialResource --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsNonSpatialResource(AbstractOptionsRequestTest):

    # simple path
    def options_non_spatial_resource_simple_path(self):
        response = requests.options(self.controle_base_uri + "controle-list/usuario-list/1")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['data_nascimento', 'email', 'gastos', 'hydra', 'id', 'nome',
                                          'nome_usuario', 'rdfs', 'senha', 'subClassOf'])

        data_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data_nascimento')
        self.assertListEqual(data_nascimento_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertListEqual(email_acontext_keys, self.keys_from_attrs_context)
        gastos_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'gastos')
        self.assertListEqual(gastos_acontext_keys, self.keys_from_attrs_context)
        id_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id')
        self.assertListEqual(id_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        nome_usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome_usuario')
        self.assertListEqual(nome_usuario_acontext_keys, self.keys_from_attrs_context)
        senha_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'senha')
        self.assertListEqual(senha_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_property_keys = self.aux_get_supported_property_keys(response)
        self.assertListEqual(supported_property_keys, self.expected_supported_property_keys)

        suppoerted_properties_names = self.aux_get_supported_properties_names(response)
        self.assertListEqual(suppoerted_properties_names, ['data_nascimento', 'email', 'gastos', 'id', 'nome',
                                                           'nome_usuario', 'senha'])

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # only attributes
    def options_non_spatial_resource_only_attributes(self):
        response = requests.options(self.controle_base_uri + "controle-list/usuario-list/1/nome,email")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertListEqual(email_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def options_non_spatial_resource_only_one_attribute(self):
        response = requests.options(self.controle_base_uri + "controle-list/usuario-list/1/nome")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/name")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # operations
    def options_non_spatial_resource_projection_operation(self):
        response = requests.options(self.controle_base_uri + "controle-list/usuario-list/1/projection/nome,email")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertListEqual(email_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # simple path (binary)
    def options_non_spatial_resource_simple_path_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "controle-list/usuario-list/1", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['data_nascimento', 'email', 'gastos', 'hydra', 'id', 'nome',
                                             'nome_usuario', 'rdfs', 'senha', 'subClassOf'])

        data_nascimento_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'data_nascimento')
        self.assertListEqual(data_nascimento_acontext_keys, self.keys_from_attrs_context)
        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertListEqual(email_acontext_keys, self.keys_from_attrs_context)
        gastos_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'gastos')
        self.assertListEqual(gastos_acontext_keys, self.keys_from_attrs_context)
        id_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id')
        self.assertListEqual(id_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        nome_usuario_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome_usuario')
        self.assertListEqual(nome_usuario_acontext_keys, self.keys_from_attrs_context)
        senha_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'senha')
        self.assertListEqual(senha_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_property_keys = self.aux_get_supported_property_keys(response)
        self.assertListEqual(supported_property_keys, self.expected_supported_property_keys)

        suppoerted_properties_names = self.aux_get_supported_properties_names(response)
        self.assertListEqual(suppoerted_properties_names, ['data_nascimento', 'email', 'gastos', 'id', 'nome',
                                                           'nome_usuario', 'senha'])

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # only attributes (binary)
    def options_non_spatial_resource_only_attributes_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "controle-list/usuario-list/1/nome,email",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertListEqual(email_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def options_non_spatial_resource_only_one_attribute_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "controle-list/usuario-list/1/nome",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/name")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # operations (binary)
    def options_non_spatial_resource_projection_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "controle-list/usuario-list/1/projection/nome,email")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        email_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertListEqual(email_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # simple path (image)
    def options_non_spatial_resource_simple_path_accept_image_png(self):
        pass

    # only attributes (image)
    def options_non_spatial_resource_only_attributes_accept_image_png(self):
        pass

    def options_non_spatial_resource_only_one_attribute_accept_image_png(self):
        pass

    # operations (image)
    def options_non_spatial_resource_projection_operation_accept_image_png(self):
        pass

# FeatureResource
#python manage.py test hyper_resource.tests.FeatureResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner
class FeatureResourceTest(AbstractGetRequestTest):

    def test_feature_resource_simple_path(self):
        response = requests.get(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers["content-type"], 'application/vnd.geo+json')

        feature_keys = self.aux_get_first_feature_keys(response)
        self.assertListEqual(feature_keys, ['geometry', 'id_objeto', 'properties', 'type'])

        feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertListEqual(feature_properties_keys, ['geocodigo', 'geometriaaproximada', 'nome', 'nomeabrev', 'sigla'])

#python manage.py test hyper_resource.tests.OptionsFeatureResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsFeatureResourceTest(AbstractOptionsRequestTest):

    # simple path
    def test_options_feature_resource_simple_path(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'geometriaaproximada', 'hydra',
                                             'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'sigla', 'subClassOf'])

        geocodigo_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geocodigo')
        self.assertListEqual(geocodigo_acontext_keys, self.keys_from_attrs_context)
        geometriaaproximada_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geometriaaproximada')
        self.assertListEqual(geometriaaproximada_acontext_keys, self.keys_from_attrs_context)
        id_objeto_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id_objeto')
        self.assertListEqual(id_objeto_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        nomeabrev_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nomeabrev')
        self.assertListEqual(nomeabrev_acontext_keys, self.keys_from_attrs_context)
        sigla_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'sigla')
        self.assertListEqual(sigla_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        response_supported_property_keys = self.aux_get_supported_property_keys(response)
        self.assertListEqual(response_supported_property_keys, self.expected_supported_property_keys)

        supported_properties_names = self.aux_get_supported_property_names(response)
        self.assertListEqual(supported_properties_names, ['geocodigo', 'geom', 'geometriaaproximada', 'id_objeto',
                                                        'nome', 'nomeabrev', 'sigla'])

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/State")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # only attributes
    def test_options_feature_resource_only_attributes(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/geom,nome')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_only_geometry_attributes(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/geom')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_only__alphanumeric_attributes(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/sigla,nome')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'sigla', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        sigla_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'sigla')
        self.assertListEqual(sigla_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_only_one_alphanumeric_attributes(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/nome')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/name")
        self.assertEquals(response_dict["@type"], "https://schema.org/Text")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # operations
    def test_options_feature_resource_area_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/area")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['area', 'hydra', 'rdfs', 'subClassOf'])

        area_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'area')
        self.assertListEqual(area_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_boundary_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/boundary")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiLineString")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiLineString")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_buffer_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/buffer/1.2")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_centroid_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/centroid")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_contains_operation(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/contains/' + self.bcim_base_uri + 'aldeias-indigenas/623')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['contains', 'hydra', 'rdfs', 'subClassOf'])

        contains_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(contains_acontext_keys, self.keys_from_attrs_context)

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_convex_hull_operation(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/convex_hull')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Polygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Polygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    #todo: coord_seq doesn't return a respose (this operation must be deleted or altered)
    def test_options_feature_resource_coord_seq_operation(self):
        pass

    def test_options_feature_resource_coords_operation(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/coords')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['coords', 'hydra', 'rdfs', 'subClassOf'])

        coords_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'coords')
        self.assertListEqual(coords_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#coordinates")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_count_operation(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/count')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['count', 'hydra', 'rdfs', 'subClassOf'])

        count_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'count')
        self.assertListEqual(count_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_crosses_operation(self):
        response = requests.options(self.bcim_base_uri + 'trechos-rodoviarios/2625832/crosses/' + self.bcim_base_uri + 'municipios/45823')  # 48623 = itaguai, 2625832 = belo jardim
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['crosses', 'hydra', 'rdfs', 'subClassOf'])

        crosses_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'crosses')
        self.assertListEqual(crosses_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_crs_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/crs")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['crs', 'hydra', 'rdfs', 'subClassOf'])

        crs_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'crs')
        self.assertListEqual(crs_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#SpatialReference")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_difference_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/difference/" + self.bcim_base_uri + "unidades-federativas/RJ")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_dims_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/dims")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['dims', 'hydra', 'rdfs', 'subClassOf'])

        dims_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'dims')
        self.assertListEqual(dims_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_disjoint_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/disjoint/" + self.bcim_base_uri + "unidades-federativas/RJ")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['disjoint', 'hydra', 'rdfs', 'subClassOf'])

        disjoint_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'disjoint')
        self.assertListEqual(disjoint_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_distance_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/distance/" + self.bcim_base_uri + "aldeias-indigenas/623")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['distance', 'hydra', 'rdfs', 'subClassOf'])

        distance_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'distance')
        self.assertListEqual(distance_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_empty_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/empty")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['empty', 'hydra', 'rdfs', 'subClassOf'])

        empty_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'empty')
        self.assertListEqual(empty_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_envelope_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/envelope")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Polygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Polygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_equals_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/equals/" + self.bcim_base_uri + "unidades-federativas/RJ")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['equals', 'hydra', 'rdfs', 'subClassOf'])

        equals_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'equals')
        self.assertListEqual(equals_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_equals_exact_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/equals_exact/" + self.bcim_base_uri + "unidades-federativas/RJ")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['equals_exact', 'hydra', 'rdfs', 'subClassOf'])

        equals_exact_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'equals_exact')
        self.assertListEqual(equals_exact_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_ewkb_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/ewkb")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_ewkt_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/ewkt")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['ewkt', 'hydra', 'rdfs', 'subClassOf'])

        ewkt_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'ewkt')
        self.assertListEqual(ewkt_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: extend is not a FeatureResource operation
    def test_options_feature_resource_extend_operation(self):
        pass

    def test_options_feature_resource_extent_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/extent")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['extent', 'hydra', 'rdfs', 'subClassOf'])

        extent_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'extent')
        self.assertListEqual(extent_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ItemList")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: GET for geojson operation should return a default response
    def test_options_feature_resource_geojson_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/geojson")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geojson', 'hydra', 'rdfs', 'subClassOf'])

        geojson_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geojson')
        self.assertListEqual(geojson_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_geom_type_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/geom_type")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geom_type', 'hydra', 'rdfs', 'subClassOf'])

        geom_type_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geom_type')
        self.assertListEqual(geom_type_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Text")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_geom_typeid_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/geom_typeid")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geom_typeid', 'hydra', 'rdfs', 'subClassOf'])

        geom_typeid_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geom_typeid')
        self.assertListEqual(geom_typeid_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: get_coords is not a FeatureResource operation
    def test_options_feature_resource_get_coords_operation(self):
        pass

    # todo: get_srid is not a FeatureResource operation
    def test_options_feature_resource_get_srid_operation(self):
        pass

    # todo: get_x is not a FeatureResource operation
    def test_options_feature_resource_get_x_operation(self):
        pass

    # todo: get_y is not a FeatureResource operation
    def test_options_feature_resource_get_y_operation(self):
        pass

    # todo: get_z is not a FeatureResource operation
    def test_options_feature_resource_get_z_operation(self):
        pass

    def test_options_feature_resource_has_cs_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/has_cs")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['has_cs', 'hydra', 'rdfs', 'subClassOf'])

        has_cs_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'has_cs')
        self.assertListEqual(has_cs_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_hasz_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/hasz")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hasz', 'hydra', 'rdfs', 'subClassOf'])

        hasz_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'hasz')
        self.assertListEqual(hasz_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_hex_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/hex")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_hexewkb_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/hexewkb")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: GET request for index not working
    def test_options_feature_resource_index_operation(self):
        pass

    def test_options_feature_resource_intersection_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/intersection/" + self.bcim_base_uri + "aldeias-indigenas/623")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        # if there is no intersection between to geometries, intersection operation return a empty GeometryCollection
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_intersects_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/intersects/" + self.bcim_base_uri + "aldeias-indigenas/623")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'intersects', 'rdfs', 'subClassOf'])

        intersects_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'intersects')
        self.assertListEqual(intersects_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: interpolate is not a FeatureResource operation
    def test_options_feature_resource_interpolate_operation(self):
        pass

    # todo: GET for json operation should return a default response
    def test_options_feature_resource_json_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/json")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'json', 'rdfs', 'subClassOf'])

        json_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'json')
        self.assertListEqual(json_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_kml_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/kml")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'kml', 'rdfs', 'subClassOf'])

        kml_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'kml')
        self.assertListEqual(kml_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Text")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_length_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/length")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'length', 'rdfs', 'subClassOf'])

        length_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'length')
        self.assertListEqual(length_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: normalize doesn't return a respose (this operation must be deleted or altered)
    def test_options_feature_resource_normalize_operation(self):
        pass

    def test_options_feature_resource_num_coords_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/num_coords")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'num_coords', 'rdfs', 'subClassOf'])

        num_coords_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'num_coords')
        self.assertListEqual(num_coords_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_num_geom_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/num_geom")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'num_geom', 'rdfs', 'subClassOf'])

        num_geom_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'num_geom')
        self.assertListEqual(num_geom_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_num_points_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/num_points")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'num_points', 'rdfs', 'subClassOf'])

        num_points_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'num_points')
        self.assertListEqual(num_points_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: GET for ogr operation should return a default response
    def test_options_feature_resource_ogr_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/ogr")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'ogr', 'rdfs', 'subClassOf'])

        ogr_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'ogr')
        self.assertListEqual(ogr_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_overlaps_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/overlaps/" + self.bcim_base_uri + 'unidades-federativas/RJ')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'overlaps', 'rdfs', 'subClassOf'])

        overlaps_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'overlaps')
        self.assertListEqual(overlaps_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_point_on_surface_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/point_on_surface")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_relate_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/relate/" + self.bcim_base_uri + "unidades-federativas/RJ")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'relate', 'subClassOf'])

        relate_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'relate')
        self.assertListEqual(relate_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Text")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_relate_pattern_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/relate_pattern/" + self.bcim_base_uri + "unidades-federativas/RJ&FF2F11212")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'relate_pattern', 'subClassOf'])

        relate_pattern_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'relate_pattern')
        self.assertListEqual(relate_pattern_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_ring_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/ring")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'ring', 'subClassOf'])

        ring_pattern_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'ring')
        self.assertListEqual(ring_pattern_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_simple_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/simple")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'simple', 'subClassOf'])

        simple_pattern_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'simple')
        self.assertListEqual(simple_pattern_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_simplify_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/simplify")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_srid_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/srid")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'srid', 'subClassOf'])

        srid_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'srid')
        self.assertListEqual(srid_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_srs_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/srs")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'srs', 'subClassOf'])

        srs_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'srs')
        self.assertListEqual(srs_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#SpatialReference")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_sym_difference_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/sym_difference/" + self.bcim_base_uri + 'unidades-federativas/ES/')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_touches_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/touches/" + self.bcim_base_uri + "unidades-federativas/RJ/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'touches'])

        touches_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'touches')
        self.assertListEqual(touches_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_transform_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/transform/2805&False")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_union_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/union/" + self.bcim_base_uri + "unidades-federativas/RJ")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_valid_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/valid")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'valid'])

        valid_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'valid')
        self.assertListEqual(valid_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_valid_reason_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/valid_reason")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'valid_reason'])

        valid_reason_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'valid_reason')
        self.assertListEqual(valid_reason_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Text")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_within_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/within/" + self.bcim_base_uri + "unidades-federativas/ES")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'within'])

        within_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'within')
        self.assertListEqual(within_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_wkb_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/wkb")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_wkt_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/wkt")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'wkt'])

        wkt_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'wkt')
        self.assertListEqual(wkt_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.string_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: x is an operation that works only for Point objects
    def test_options_feature_resource_x_operation(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/623/x")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'x'])

        x_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'x')
        self.assertListEqual(x_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: y is an operation that works only for Point objects
    def test_options_feature_resource_y_operation(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/623/y")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'y'])

        y_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'y')
        self.assertListEqual(y_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: z is an operation that works only for Point objects
    def test_options_feature_resource_z_operation(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/623/z")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'z'])

        z_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'z')
        self.assertListEqual(z_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_projection_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/projection/geom,nome")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # simple path (binary)
    def test_options_feature_resource_simple_path_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'geometriaaproximada', 'hydra',
                                             'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'sigla', 'subClassOf'])

        geocodigo_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geocodigo')
        self.assertListEqual(geocodigo_acontext_keys, self.keys_from_attrs_context)
        geometriaaproximada_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geometriaaproximada')
        self.assertListEqual(geometriaaproximada_acontext_keys, self.keys_from_attrs_context)
        id_objeto_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'id_objeto')
        self.assertListEqual(id_objeto_acontext_keys, self.keys_from_attrs_context)
        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        nomeabrev_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nomeabrev')
        self.assertListEqual(nomeabrev_acontext_keys, self.keys_from_attrs_context)
        sigla_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'sigla')
        self.assertListEqual(sigla_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        response_supported_property_keys = self.aux_get_supported_property_keys(response)
        self.assertListEqual(response_supported_property_keys, self.expected_supported_property_keys)

        supported_properties_names = self.aux_get_supported_property_names(response)
        self.assertListEqual(supported_properties_names,
                             ['geocodigo', 'geom', 'geometriaaproximada', 'id_objeto',
                              'nome', 'nomeabrev', 'sigla'])

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/State")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # only attributes (binary)
    def test_options_feature_resource_only_attributes_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/geom,nome', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_only_geometry_attributes_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/geom', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_only__alphanumeric_attributes_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/sigla,nome', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'sigla', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        sigla_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'sigla')
        self.assertListEqual(sigla_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_only_one_alphanumeric_attributes_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/nome', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/name")
        self.assertEquals(response_dict["@type"], "https://schema.org/Text")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # operations (binary)
    def test_options_feature_resource_area_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/area", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['area', 'hydra', 'rdfs', 'subClassOf'])

        area_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'area')
        self.assertListEqual(area_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_boundary_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/boundary", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiLineString")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiLineString")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_buffer_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/buffer/1.2", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_centroid_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/centroid", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_contains_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/contains/' + self.bcim_base_uri + 'aldeias-indigenas/623', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['contains', 'hydra', 'rdfs', 'subClassOf'])

        contains_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(contains_acontext_keys, self.keys_from_attrs_context)

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_convex_hull_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/convex_hull', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Polygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Polygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    #todo: coord_seq doesn't return a respose (this operation must be deleted or altered)
    def test_options_feature_resource_coord_seq_operation_accept_octet_stream(self):
        pass

    def test_options_feature_resource_coords_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/coords', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['coords', 'hydra', 'rdfs', 'subClassOf'])

        coords_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'coords')
        self.assertListEqual(coords_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#coordinates")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_count_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/count', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['count', 'hydra', 'rdfs', 'subClassOf'])

        count_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'count')
        self.assertListEqual(count_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_crosses_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'trechos-rodoviarios/2625832/crosses/' + self.bcim_base_uri + 'municipios/45823', headers={"Accept": "application/octet-stream"})  # 48623 = itaguai, 2625832 = belo jardim
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['crosses', 'hydra', 'rdfs', 'subClassOf'])

        crosses_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'crosses')
        self.assertListEqual(crosses_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_crs_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/crs", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['crs', 'hydra', 'rdfs', 'subClassOf'])

        crs_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'crs')
        self.assertListEqual(crs_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#SpatialReference")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_difference_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/difference/" + self.bcim_base_uri + "unidades-federativas/RJ", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_dims_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/dims", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['dims', 'hydra', 'rdfs', 'subClassOf'])

        dims_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'dims')
        self.assertListEqual(dims_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_disjoint_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/disjoint/" + self.bcim_base_uri + "unidades-federativas/RJ", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['disjoint', 'hydra', 'rdfs', 'subClassOf'])

        disjoint_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'disjoint')
        self.assertListEqual(disjoint_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_distance_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/distance/" + self.bcim_base_uri + "aldeias-indigenas/623", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['distance', 'hydra', 'rdfs', 'subClassOf'])

        distance_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'distance')
        self.assertListEqual(distance_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_empty_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/empty", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['empty', 'hydra', 'rdfs', 'subClassOf'])

        empty_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'empty')
        self.assertListEqual(empty_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_envelope_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/envelope", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Polygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Polygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_equals_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/equals/" + self.bcim_base_uri + "unidades-federativas/RJ", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['equals', 'hydra', 'rdfs', 'subClassOf'])

        equals_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'equals')
        self.assertListEqual(equals_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_equals_exact_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/equals_exact/" + self.bcim_base_uri + "unidades-federativas/RJ", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['equals_exact', 'hydra', 'rdfs', 'subClassOf'])

        equals_exact_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'equals_exact')
        self.assertListEqual(equals_exact_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_ewkb_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/ewkb", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_ewkt_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/ewkt", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['ewkt', 'hydra', 'rdfs', 'subClassOf'])

        ewkt_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'ewkt')
        self.assertListEqual(ewkt_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: extend is not a FeatureResource operation
    def test_options_feature_resource_extend_operation_accept_octet_stream(self):
        pass

    def test_options_feature_resource_extent_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/extent", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['extent', 'hydra', 'rdfs', 'subClassOf'])

        extent_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'extent')
        self.assertListEqual(extent_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/ItemList")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_geojson_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/geojson", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geojson', 'hydra', 'rdfs', 'subClassOf'])

        geojson_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geojson')
        self.assertListEqual(geojson_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_geom_type_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/geom_type", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geom_type', 'hydra', 'rdfs', 'subClassOf'])

        geom_type_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geom_type')
        self.assertListEqual(geom_type_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Text")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_geom_typeid_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/geom_typeid", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geom_typeid', 'hydra', 'rdfs', 'subClassOf'])

        geom_typeid_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'geom_typeid')
        self.assertListEqual(geom_typeid_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: get_coords is not a FeatureResource operation
    def test_options_feature_resource_get_coords_operation_accept_octet_stream(self):
        pass

    # todo: get_srid is not a FeatureResource operation
    def test_options_feature_resource_get_srid_operation_accept_octet_stream(self):
        pass

    # todo: get_x is not a FeatureResource operation
    def test_options_feature_resource_get_x_operation_accept_octet_stream(self):
        pass

    # todo: get_y is not a FeatureResource operation
    def test_options_feature_resource_get_y_operation_accept_octet_stream(self):
        pass

    # todo: get_z is not a FeatureResource operation
    def test_options_feature_resource_get_z_operation_accept_octet_stream(self):
        pass

    def test_options_feature_resource_has_cs_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/has_cs", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['has_cs', 'hydra', 'rdfs', 'subClassOf'])

        has_cs_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'has_cs')
        self.assertListEqual(has_cs_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_hasz_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/hasz", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hasz', 'hydra', 'rdfs', 'subClassOf'])

        hasz_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'hasz')
        self.assertListEqual(hasz_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_hex_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/hex", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_hexewkb_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/hexewkb", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: GET request for index not working
    def test_options_feature_resource_index_operation_accept_octet_stream(self):
        pass

    def test_options_feature_resource_intersection_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/intersection/" + self.bcim_base_uri + "aldeias-indigenas/623", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        # if there is no intersection between to geometries, intersection operation return a empty GeometryCollection
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_intersects_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/intersects/" + self.bcim_base_uri + "aldeias-indigenas/623", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'intersects', 'rdfs', 'subClassOf'])

        intersects_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'intersects')
        self.assertListEqual(intersects_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: interpolate is not a FeatureResource operation
    def test_options_feature_resource_interpolate_operation_accept_octet_stream(self):
        pass

    def test_options_feature_resource_json_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/json", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'json', 'rdfs', 'subClassOf'])

        json_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'json')
        self.assertListEqual(json_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_kml_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/kml", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'kml', 'rdfs', 'subClassOf'])

        kml_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'kml')
        self.assertListEqual(kml_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Text")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_length_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/length", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'length', 'rdfs', 'subClassOf'])

        length_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'length')
        self.assertListEqual(length_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: normalize doesn't return a respose (this operation must be deleted or altered)
    def test_options_feature_resource_normalize_operation_accept_octet_stream(self):
        pass

    def test_options_feature_resource_num_coords_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/num_coords", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'num_coords', 'rdfs', 'subClassOf'])

        num_coords_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'num_coords')
        self.assertListEqual(num_coords_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_num_geom_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/num_geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'num_geom', 'rdfs', 'subClassOf'])

        num_geom_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'num_geom')
        self.assertListEqual(num_geom_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_num_points_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/num_points", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'num_points', 'rdfs', 'subClassOf'])

        num_points_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'num_points')
        self.assertListEqual(num_points_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: GET for ogr operation should return a default response
    def test_options_feature_resource_ogr_operation_accept_octet_stream(self):
        pass

    def test_options_feature_resource_overlaps_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/overlaps/" + self.bcim_base_uri + 'unidades-federativas/RJ', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'overlaps', 'rdfs', 'subClassOf'])

        overlaps_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'overlaps')
        self.assertListEqual(overlaps_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_point_on_surface_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/point_on_surface", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_relate_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/relate/" + self.bcim_base_uri + "unidades-federativas/RJ", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'relate', 'subClassOf'])

        relate_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'relate')
        self.assertListEqual(relate_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Text")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_relate_pattern_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/relate_pattern/" + self.bcim_base_uri + "unidades-federativas/RJ&FF2F11212", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'relate_pattern', 'subClassOf'])

        relate_pattern_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'relate_pattern')
        self.assertListEqual(relate_pattern_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_ring_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/ring", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'ring', 'subClassOf'])

        ring_pattern_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'ring')
        self.assertListEqual(ring_pattern_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_simple_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/simple", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'simple', 'subClassOf'])

        simple_pattern_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'simple')
        self.assertListEqual(simple_pattern_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_simplify_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/simplify", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_srid_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/srid", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'srid', 'subClassOf'])

        srid_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'srid')
        self.assertListEqual(srid_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Integer")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_srs_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/srs", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'srs', 'subClassOf'])

        srs_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'srs')
        self.assertListEqual(srs_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#SpatialReference")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_sym_difference_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/sym_difference/" + self.bcim_base_uri + 'unidades-federativas/ES/', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_touches_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/touches/" + self.bcim_base_uri + "unidades-federativas/RJ/", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'touches'])

        touches_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'touches')
        self.assertListEqual(touches_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_transform_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/transform/2805&False", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_union_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/union/" + self.bcim_base_uri + "unidades-federativas/RJ", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_valid_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/valid", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'valid'])

        valid_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'valid')
        self.assertListEqual(valid_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_valid_reason_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/valid_reason", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'valid_reason'])

        valid_reason_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'valid_reason')
        self.assertListEqual(valid_reason_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Text")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_within_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/within/" + self.bcim_base_uri + "unidades-federativas/ES", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'within'])

        within_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'within')
        self.assertListEqual(within_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Boolean")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_wkb_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/wkb", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_wkt_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/wkt", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'wkt'])

        wkt_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'wkt')
        self.assertListEqual(wkt_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names,[])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#MultiPolygon")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: x is an operation that works only for Point objects
    def test_options_feature_resource_x_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/623/x", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'x'])

        x_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'x')
        self.assertListEqual(x_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: y is an operation that works only for Point objects
    def test_options_feature_resource_y_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/623/y", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'y'])

        y_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'y')
        self.assertListEqual(y_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # todo: z is an operation that works only for Point objects
    def test_options_feature_resource_z_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/623/z", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf', 'z'])

        z_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'z')
        self.assertListEqual(z_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Float")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_feature_resource_projection_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/ES/projection/geom,nome", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertListEqual(nome_acontext_keys, self.keys_from_attrs_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_acontext_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

#python manage.py test hyper_resource.tests.HeadFeatureResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner
class HeadFeatureResourceTest(AbstractHeadRequestTest):

    def test_head_feature_resource_simple_path(self):
        response_get = requests.get(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response_get.status_code, 200)
        response_head = requests.head(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response_head.status_code, 200)
        response_options = requests.options(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response_options.status_code, 200)

        head_headers = self.aux_get_headers_list_from_response(response_head)
        get_headers = self.aux_get_headers_list_from_response(response_get)
        options_headers = self.aux_get_headers_list_from_response(response_options)
        self.assertListEqual(head_headers, get_headers)
        #self.assertListEqual(head_headers, options_headers)

        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_get.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_get.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_get.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_get.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_get.headers["allow"])
        self.assertEquals(response_head.headers["content-type"],                    response_get.headers["content-type"])
        self.assertEquals(response_head.headers["link"],                            response_get.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_get.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_get.headers["vary"])
        self.assertIn("Date", head_headers)
        self.assertIn("Date", get_headers)

        # compare HEAD with OPTIONS headers
        self.assertEquals(response_head.headers["access-control-allow-headers"],    response_options.headers["access-control-allow-headers"])
        self.assertEquals(response_head.headers["access-control-allow-methods"],    response_options.headers["access-control-allow-methods"])
        self.assertEquals(response_head.headers["access-control-allow-origin"],     response_options.headers["access-control-allow-origin"])
        self.assertEquals(response_head.headers["access-control-expose-headers"],   response_options.headers["access-control-expose-headers"])
        self.assertEquals(response_head.headers["allow"],                           response_options.headers["allow"])
        #self.assertEquals(response_head.headers["link"],                            response_options.headers["link"])
        self.assertEquals(response_head.headers["server"],                          response_options.headers["server"])
        self.assertEquals(response_head.headers["vary"],                            response_options.headers["vary"])
        self.assertIn("Date", options_headers)
        self.assertIn("Content-Type", options_headers)# OPTIONS content-type is aways JSON-LD


#                               ALLOWED METHODS TEST
#python manage.py test hyper_resource.tests.AllowedMethodsForEntryPoint --testrunner=hyper_resource.tests.NoDbTestRunner
class AllowedMethodsForEntryPoint(AbstractHeadRequestTest):
    def test_head_generic_entry_point(self):
        response = requests.head(self.controle_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )

    def test_head_feature_entry_point(self):
        response = requests.head(self.bcim_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )

    def test_head_raster_entry_point(self):
        response = requests.head(self.raster_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS', 'POST'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS', 'POST'] )
        #self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        #self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )

#python manage.py test hyper_resource.tests.AllowedMethodsForNonSpatialResource --testrunner=hyper_resource.tests.NoDbTestRunner
class AllowedMethodsForNonSpatialResource(AbstractHeadRequestTest):
    def test_head_non_spatial_resource_simple_path(self):
        response = requests.head(self.controle_base_uri + 'usuario-list/1')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT'] )

    def test_head_non_spatial_resource_only_attributes(self):
        response = requests.head(self.controle_base_uri + 'usuario-list/1/nome,email')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )

    def test_head_non_spatial_resource_operation(self):
        response = requests.head(self.controle_base_uri + 'usuario-list/1/projection/nome')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )

#python manage.py test hyper_resource.tests.AllowedMethodsForCollectionResource --testrunner=hyper_resource.tests.NoDbTestRunner
class AllowedMethodsForCollectionResource(AbstractHeadRequestTest):
    def test_head_collection_resource_simple_path(self):
        response = requests.head(self.controle_base_uri + 'usuario-list')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST'] )

    def test_head_collection_resource_only_attributes(self):
        response = requests.head(self.controle_base_uri + 'usuario-list/nome,email')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )

    def test_head_collection_resource_operation(self):
        response = requests.head(self.controle_base_uri + 'usuario-list/count-resource')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )

#python manage.py test hyper_resource.tests.AllowedMethodsForTiffCollectionResource --testrunner=hyper_resource.tests.NoDbTestRunner
class AllowedMethodsForTiffCollectionResource(AbstractHeadRequestTest):
    def test_head_tiff_collection_resource_simple_path(self):
        response = requests.head(self.raster_base_uri + 'imagem-exemplo-tile1-list')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS', 'POST'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS', 'POST'] )

    '''
    def test_head_tiff_collection_resource_only_attributes(self):
        response = requests.head(self.raster_base_uri + 'imagem-exemplo-tile1-list/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )
    '''

    def test_head_tiff_collection_resource_operation(self):
        response = requests.head(self.raster_base_uri + 'imagem-exemplo-tile1-list/count-resource')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )

#python manage.py test hyper_resource.tests.AllowedMethodsForTiffResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner
class AllowedMethodsForTiffResourceTest(AbstractHeadRequestTest):
    def test_head_tiff_resource_simple_path(self):
        response = requests.head(self.raster_base_uri + 'imagem-exemplo-tile1-list/181')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT'] )

    def test_head_tiff_resource_only_attributes(self):
        response = requests.head(self.raster_base_uri + 'imagem-exemplo-tile1-list/181/rid')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )

    def test_head_tiff_resource_operation(self):
        response = requests.head(self.raster_base_uri + 'imagem-exemplo-tile1-list/181/transform/3086')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'] )
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'] )

#python manage.py test hyper_resource.tests.AllowedMethodsForFeatureResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner
class AllowedMethodsForFeatureResourceTest(AbstractHeadRequestTest):
    '''
    Class to test every possible allowed methods for differents requests for FeatureResource
    '''

    def test_head_for_feature_resource_simple_path(self):
        response = requests.head(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT'])
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT'])

    def test_head_for_feature_resource_only_attributes(self):
        response = requests.head(self.bcim_base_uri + 'unidades-federativas/ES/nome,geom')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'])
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'])

    def test_head_for_feature_resource_operation(self):
        response = requests.head(self.bcim_base_uri + 'unidades-federativas/ES/buffer/0.8')
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'])
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'])

#python manage.py test hyper_resource.tests.AllowedMethodsForFeatureCollectionResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner
class AllowedMethodsForFeatureCollectionResourceTest(AbstractHeadRequestTest):
    '''
    Class to test every possible allowed methods for differents requests for FeatureCollectionResource
    '''

    # simple path
    def test_head_for_feature_collection_simple_path(self):
        response = requests.head(self.bcim_base_uri + "unidades-federativas")
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST'])
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST'])

    # attributes
    def test_head_for_feature_collection_only_attributes(self):
        response = requests.head(self.bcim_base_uri + "unidades-federativas/nome,geom")
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'])
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'])

    # operations
    def test_head_for_feature_collection_operation(self):
        response = requests.head(self.bcim_base_uri + "unidades-federativas/union")
        self.assertEquals(response.status_code, 200)
        self.assertEquals( self.aux_get_allowed_methods(response, 'allow'), ['GET', 'HEAD', 'OPTIONS'])
        self.assertEquals( self.aux_get_allowed_methods(response, 'access-control-allow-methods'), ['GET', 'HEAD', 'OPTIONS'])


#                               OTHER TEST
#python manage.py test hyper_resource.tests.LinkHeaderTest --testrunner=hyper_resource.tests.NoDbTestRunner
class LinkHeaderTest(AbstractHeadRequestTest):

    # --- EntryPoints ---
    # --- GET ---
    def test_get_for_generic_entry_point(self):
        response = requests.get(self.controle_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # has <EntryPoint>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertNotIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="stylesheet', response.headers['link'])

    def test_get_for_feature_entry_point(self):
        response = requests.get(self.bcim_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # has <EntryPoint>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertNotIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="stylesheet', response.headers['link'])

    def test_get_for_raster_entry_point(self):
        response = requests.get(self.raster_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # has <EntryPoint>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertNotIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="stylesheet', response.headers['link'])

    # --- HEAD ---
    def test_head_for_generic_entry_point(self):
        response = requests.head(self.controle_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # has <EntryPoint>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertNotIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="stylesheet', response.headers['link'])

    def test_head_for_feature_entry_point(self):
        response = requests.head(self.bcim_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # has <EntryPoint>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertNotIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="stylesheet', response.headers['link'])

    def test_head_for_raster_entry_point(self):
        response = requests.head(self.raster_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # has <EntryPoint>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertNotIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="stylesheet', response.headers['link'])

    # --- OPTIONS ---
    def test_options_for_generic_entry_point(self):
        response = requests.options(self.controle_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # has <EntryPoint>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertNotIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="stylesheet', response.headers['link'])

    def test_options_for_feature_entry_point(self):
        response = requests.options(self.bcim_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # has <EntryPoint>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertNotIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="stylesheet', response.headers['link'])

    def test_options_for_raster_entry_point(self):
        response = requests.options(self.raster_base_uri)
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # has <EntryPoint>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertNotIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="stylesheet', response.headers['link'])

    # --- POST ---
    def test_post_for_raster_entry_point(self):
        pass

    # --- FeatureResource ---
    def test_get_for_feature_resource(self):
        response = requests.get(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertIn('rel="up"', response.headers['link']) # has <Up>
        self.assertIn('rel="stylesheet', response.headers['link']) # has <Style>
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # <EntryPoint> cannot be on the 'Link' header
        self.assertNotIn('rel="describedBy"', response.headers['link'])

    def test_head_for_feature_resource(self):
        response = requests.head(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertIn('rel="up"', response.headers['link']) # has <Up>
        self.assertIn('rel="stylesheet', response.headers['link']) # has <Style>
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # <EntryPoint> cannot be on the 'Link' header
        self.assertNotIn('rel="describedBy"', response.headers['link'])

    '''
    def test_options_for_feature_resource(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link']) # has <Context>
        self.assertIn('rel="metadata"', response.headers['link']) # has <Metadata>
        self.assertIn('rel="up"', response.headers['link']) # has <Up>
        self.assertIn('rel="stylesheet', response.headers['link']) # has <Style>
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link']) # <EntryPoint> cannot be on the 'Link' header
        self.assertNotIn('rel="describedBy"', response.headers['link'])
    '''

    # --- TiffResource ---
    def test_get_for_raster_resource(self):
        response = requests.get(self.raster_base_uri + 'imagem-exemplo-tile1-list/181')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertIn('rel="describedBy"', response.headers['link']) # has <describedBy>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])

    def test_head_for_raster_resource(self):
        response = requests.head(self.raster_base_uri + 'imagem-exemplo-tile1-list/181')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertIn('rel="describedBy"', response.headers['link']) # has <describedBy>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])

    '''
    def test_options_for_raster_resource(self):
        response = requests.options(self.raster_base_uri + 'imagem-exemplo-tile1-list/181')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertIn('rel="describedBy"', response.headers['link']) # has <describedBy>
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])
    '''

    # --- FeatureCollection
    def test_get_for_feature_collection_resource(self):
        response = requests.get(self.bcim_base_uri + 'unidades-federativas')
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])

    def test_head_for_feature_collection_resource(self):
        response = requests.head(self.bcim_base_uri + 'unidades-federativas')
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])

    '''
    def test_options_for_feature_collection_resource(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas')
        self.assertEquals(response.status_code, 200)
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])
    '''

    def test_post_for_feature_collection_resource(self):
        pass

    # --- NonSpatialCollection
    def test_get_for_non_spatial_resource(self):
        response = requests.get(self.controle_base_uri + 'usuario-list/1')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])

    def test_head_for_non_spatial_resource(self):
        response = requests.head(self.controle_base_uri + 'usuario-list/1')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])

    '''
    def test_options_for_non_spatial_resource(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/1')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])
    '''

    # --- CollectionResource
    def test_get_for_collection_resource(self):
        response = requests.get(self.controle_base_uri + 'usuario-list')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])

    def test_head_for_collection_resource(self):
        response = requests.head(self.controle_base_uri + 'usuario-list')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])

    '''
    def test_options_for_collection_resource(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/1')
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])
        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])
    '''

#python manage.py test hyper_resource.tests.RequestOptionsTest --testrunner=hyper_resource.tests.NoDbTestRunner
class RequestOptionsTest(AbstractOptionsRequestTest):

    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    # tests for feature/geometry collection simple path
    def test_options_for_feature_collection_simple_path(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['codigofunai', 'etnia', 'geometriaaproximada', 'hydra',
                                             'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'subClassOf', 'terraindigena'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        codigofunai_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "codigofunai")
        self.assertListEqual(codigofunai_context_keys_list, self.keys_from_attrs_context)
        terraindigena_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "terraindigena")
        self.assertListEqual(terraindigena_context_keys_list, self.keys_from_attrs_context)
        etnia_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "etnia")
        self.assertListEqual(etnia_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        #rdfs_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'rdfs')
        #self.assertListEqual(rdfs_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_simple_path_with_accept_header(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/", headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['codigofunai', 'etnia', 'geometriaaproximada', 'hydra',
                                             'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'subClassOf', 'terraindigena'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        codigofunai_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "codigofunai")
        self.assertListEqual(codigofunai_context_keys_list, self.keys_from_attrs_context)
        terraindigena_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "terraindigena")
        self.assertListEqual(terraindigena_context_keys_list, self.keys_from_attrs_context)
        etnia_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "etnia")
        self.assertListEqual(etnia_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        #rdfs_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'rdfs')
        #self.assertListEqual(rdfs_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)


    # tests for feature/geometry collection attributes
    def test_options_for_feature_collection_only_attributes(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/geom,nome")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ["hydra", "nome", "rdfs", "subClassOf"])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_only_attributes_with_accept_header(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/geom,nome",
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ["hydra", "nome", "rdfs", "subClassOf"])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_only_geometric_attribute(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/geom")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ["hydra", "rdfs", "subClassOf"])

        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_only_geometric_attribute_accept_header(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/geom",
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ["hydra", "rdfs", "subClassOf"])

        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_only_alphanumeric_attributes(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/nome,nomeabrev")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ["hydra", "nome", "nomeabrev", "rdfs", "subClassOf"])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_for_feature_collection_only_alphanumeric_attributes_with_accept_header(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/nome,nomeabrev",
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ["hydra", "nome", "nomeabrev", "rdfs", "subClassOf"])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # tests for feature/geometry collection operation
    def test_options_for_feature_collection_operation_with_geometry_collection_return(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + "unidades-federativas/ES")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['codigofunai', 'etnia', 'geometriaaproximada', 'hydra',
                                             'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'subClassOf', 'terraindigena'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        codigofunai_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "codigofunai")
        self.assertListEqual(codigofunai_context_keys_list, self.keys_from_attrs_context)
        terraindigena_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "terraindigena")
        self.assertListEqual(terraindigena_context_keys_list, self.keys_from_attrs_context)
        etnia_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "etnia")
        self.assertListEqual(etnia_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        #rdfs_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'rdfs')
        #self.assertListEqual(rdfs_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_operation_with_geometry_collection_return_and_accept_header(self):
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + "unidades-federativas/ES",
            headers={'accept': 'application/octet-stream'}
        )
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['codigofunai', 'etnia', 'geometriaaproximada', 'hydra',
                                             'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'subClassOf', 'terraindigena'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        codigofunai_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "codigofunai")
        self.assertListEqual(codigofunai_context_keys_list, self.keys_from_attrs_context)
        terraindigena_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "terraindigena")
        self.assertListEqual(terraindigena_context_keys_list, self.keys_from_attrs_context)
        etnia_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "etnia")
        self.assertListEqual(etnia_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        #rdfs_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'rdfs')
        #self.assertListEqual(rdfs_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_options_for_feature_collection_count_resource(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/count-resource")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ["count-resource", "hydra", "rdfs", "subClassOf"])

        count_resource_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "count-resource")
        self.assertListEqual(count_resource_context_keys_list, self.keys_from_attrs_context)
        subClassOf_resource_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_resource_context_keys_list, self.keys_from_attrs_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "hydra:totalItems")
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_feature_collection_count_resource_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/count-resource",
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ["count-resource", "hydra", "rdfs", "subClassOf"])

        count_resource_resource_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "count-resource")
        self.assertListEqual(count_resource_resource_context_keys_list, self.keys_from_attrs_context)
        subClassOf_resource_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_resource_context_keys_list, self.keys_from_attrs_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "hydra:totalItems")
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")


    # --------------- TESTS FOR COLLECTION ---------------------------------
    # tests for collection simple path
    def test_options_for_collection_simple_path(self):
        response = requests.options(self.controle_base_uri + 'gasto-list/')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['data', "hydra", "id", "rdfs", "subClassOf", "tipo_gasto", "usuario", "valor"])

        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        data_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data")
        self.assertListEqual(data_keys_list, self.keys_from_attrs_context)
        tipo_gasto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "tipo_gasto")
        self.assertListEqual(tipo_gasto_context_keys_list, self.keys_from_attrs_context)
        usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "usuario")
        self.assertListEqual(usuario_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operation_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_name, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_collection_simple_path_with_accept_header(self):
        response = requests.options(self.controle_base_uri + 'gasto-list/', headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys,
                             ['data', "hydra", "id", "rdfs", "subClassOf", "tipo_gasto", "usuario", "valor"])

        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        data_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data")
        self.assertListEqual(data_keys_list, self.keys_from_attrs_context)
        tipo_gasto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "tipo_gasto")
        self.assertListEqual(tipo_gasto_context_keys_list, self.keys_from_attrs_context)
        usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "usuario")
        self.assertListEqual(usuario_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operation_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_name, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    # tests for collection attributes
    def test_options_for_collection_only_attributes(self):
        response = requests.options(self.controle_base_uri + 'gasto-list/data,valor')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ['data', 'hydra', 'rdfs', 'subClassOf', 'valor'])

        data_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data")
        self.assertListEqual(data_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_for_collection_only_attributes_with_accept_header(self):
        response = requests.options(self.controle_base_uri + 'gasto-list/data,valor',
                                    headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ["data", "hydra", "rdfs", "subClassOf", "valor"])

        data_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data")
        self.assertListEqual(data_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    # tests for collection operation
    def test_options_for_collection_operation_with_collection_return(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/group-by-count/nome')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        count_context_keys = self.aux_get_keys_from_acontext_attrs(response, "count")
        self.assertEquals(count_context_keys, self.keys_from_attrs_context)
        group_by_count_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(group_by_count_context_keys, self.keys_from_oper_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_for_collection_operation_with_collection_return_and_accept_header(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/group-by-count/nome',
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        count_context_keys = self.aux_get_keys_from_acontext_attrs(response, "count")
        self.assertEquals(count_context_keys, self.keys_from_attrs_context)
        group_by_count_context_keys = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertEquals(group_by_count_context_keys, self.keys_from_oper_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_for_collection_operation_with_integer_return(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/count-resource')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count-resource', 'hydra', 'rdfs', 'subClassOf'])

        count_resource_resource_context_keys = self.aux_get_keys_from_acontext_attrs(response, "count-resource")
        self.assertEquals(count_resource_resource_context_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "hydra:totalItems")
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_collection_operation_with_integer_return_and_accept_header(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/count-resource',
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count-resource', 'hydra', 'rdfs', 'subClassOf'])

        count_resource_resource_context_keys = self.aux_get_keys_from_acontext_attrs(response, "count-resource")
        self.assertEquals(count_resource_resource_context_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "hydra:totalItems")
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")


    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    # tests for feature simple path
    def test_options_for_feature_resource_simple_path(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'geometriaaproximada', 'hydra', 'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'sigla', 'subClassOf'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)
        #iri_metadata_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "iri_metadata")
        #self.assertListEqual(iri_metadata_context_keys_list, self.keys_from_attrs_context)
        #iri_style_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "iri_style")
        #self.assertListEqual(iri_style_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/State")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_for_feature_resource_simple_path_with_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES',
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys,
                            ['geocodigo', 'geometriaaproximada', 'hydra', 'id_objeto', 'nome', 'nomeabrev',
                             'rdfs', 'sigla', 'subClassOf'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)
        # iri_metadata_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "iri_metadata")
        # self.assertListEqual(iri_metadata_context_keys_list, self.keys_from_attrs_context)
        # iri_style_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "iri_style")
        # self.assertListEqual(iri_style_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/State")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # tests for feature attributes
    def test_options_for_feature_resource_only_attributes(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/geom,nome')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ["hydra", "nome", "rdfs", "subClassOf"])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_for_feature_resource_only_attributes_with_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/geom,nome',
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ["hydra", "nome", "rdfs", "subClassOf"])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_for_feature_resource_only_alphanumeric_attributes(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/geocodigo,nome')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ["geocodigo", "hydra", "nome", "rdfs", "subClassOf"])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_feature_resource_only_alphanumeric_attributes_with_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/geocodigo,nome',
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ["geocodigo", "hydra", "nome", "rdfs", "subClassOf"])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_feature_resource_only_geometric_attribute(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/geom')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ["hydra", "rdfs", "subClassOf"])

        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    def test_options_for_feature_resource_only_geometric_attribute_with_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/geom',
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ["hydra", "rdfs", "subClassOf"])

        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    def test_options_for_feature_resource_pointfield_attribute(self):
        response = requests.options(self.bcim_base_uri + 'aldeias-indigenas/623/geom')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ['hydra', 'rdfs', 'subClassOf'])

        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#Point')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#Point')
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_feature_resource_pointfield_attribute_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'aldeias-indigenas/623/geom', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ['hydra', 'rdfs', 'subClassOf'])

        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#Point')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#Point')
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")


    # tests for feature operations
    def test_options_for_feature_resource_operation_with_geometry_return(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/buffer/1.2')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_feature_resource_operation_with_geometry_return_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/buffer/1.2',
                                    headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_feature_resource_area_operation(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/area')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['area', 'hydra', 'rdfs', 'subClassOf'])

        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)
        area_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "area")
        self.assertListEqual(area_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://schema.org/Float')
        self.assertEquals(response_dict["@type"], 'https://schema.org/Thing')
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_feature_resource_area_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/area',
                                    headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['area', 'hydra', 'rdfs', 'subClassOf'])

        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)
        area_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "area")
        self.assertListEqual(area_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://schema.org/Float')
        self.assertEquals(response_dict["@type"], 'https://schema.org/Thing')
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_feature_resource_operation_with_point_return(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/point_on_surface')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_on_surface_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_on_surface_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#Point')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#Point')
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_feature_resource_operation_with_point_return_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/point_on_surface',
                                    headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_on_surface_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_on_surface_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#Point')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#Point')
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")


    # --------------- TESTS FOR NON SPATIAL RESOURCE ---------------------------------
    # tests for NonSpatialResource simple path
    def test_options_for_non_spatial_resource_simple_path(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs', 'senha', 'subClassOf'])

        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nome_usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome_usuario")
        self.assertListEqual(nome_usuario_context_keys_list, self.keys_from_attrs_context)
        senha_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "senha")
        self.assertListEqual(senha_context_keys_list, self.keys_from_attrs_context)
        data_nascimento_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data_nascimento")
        self.assertListEqual(data_nascimento_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)
        #avatar_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "avatar")
        #self.assertListEqual(avatar_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_non_spatial_resource_simple_path_with_accept_header(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/",
                                    headers={'Accept': "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys,
                             ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs', 'senha',
                              'subClassOf'])

        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nome_usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome_usuario")
        self.assertListEqual(nome_usuario_context_keys_list, self.keys_from_attrs_context)
        senha_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "senha")
        self.assertListEqual(senha_context_keys_list, self.keys_from_attrs_context)
        data_nascimento_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data_nascimento")
        self.assertListEqual(data_nascimento_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)
        # avatar_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "avatar")
        # self.assertListEqual(avatar_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    # tests for NonSpatialResource only attributes
    def test_options_for_non_spatial_resource_only_attributes(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/nome,email")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    def test_options_for_non_spatial_resource_only_attributes_with_accept_header(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/nome,email",
                                    headers={'Accept': "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")


    # ------------------- TESTS FOR ENTRY POINTS -------------------------------------
    def test_options_for_feature_entrypoint(self):
        response = requests.options(self.bcim_base_uri)
        self.assertEquals(response.status_code, 200)

        #self.assertEqual(response.headers['Link'],
        #'<http://luc00557196:8000/api/bcim/>; rel="https://schema.org/EntryPoint" , <http://luc00557196:8000/api/bcim.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"')

        a_context_keys = self.aux_get_keys_from_response_context(response)
        '''
        self.assertListEqual(a_context_keys, ['aglomerados rurais de extensao urbana', 'aglomerados rurais isolado',
                                              'aldeias indigenas', 'areas de desenvolvimento de controle', 'areas edificadas',
                                              'bancos de areia', 'barragens', 'brejos e pantanos', 'capitais', 'cidades',
                                              'corredeiras', 'curvas batimetricas', 'curvas de nivel', 'dunas', 'eclusas',
                                              'edificacoes agropecuarias de extracao vegetal e pesca',
                                              'edificacoes de construcao aeroportuaria', 'edificacoes de construcao portuaria',
                                              'edificacoes de metro ferroviaria', 'edificacoes industrial', 'edificacoes publica militar',
                                              'edificacoes religiosa', 'elementos fisiografico natural',
                                              'estacoes geradoras de energia eletrica', 'extracoes minerais', 'fozes maritima',
                                              'fundeadouros', 'hidreletricas', 'ilhas', 'mangues', 'marcos de limite', 'massas dagua',
                                              'municipios', 'outros limites oficiais', 'paises', 'picos', 'pistas de ponto pouso',
                                              'pontes', 'pontos cotados altimetricos', 'pontos cotados batimetricos', 'postos fiscais',
                                              'quedas dagua', 'recifes', 'rochas em agua', 'sinalizacoes', 'sumidouros vertedouros',
                                              'termeletricas', 'terras indigenas', 'terrenos sujeito a inundacao',
                                              'torres de energia', 'travessias', 'trechos de drenagem', 'trechos de massa dagua',
                                              'trechos dutos', 'trechos ferroviarios', 'trechos hidroviarios', 'trechos rodoviarios',
                                              'tuneis', 'unidades de conservacao nao snuc', 'unidades de protecao integral',
                                              'unidades de uso sustentavel', 'unidades federativas', 'vegetacoes de restinga', 'vilas'])
        '''
        self.assertListEqual(a_context_keys, ['aglomerados-rurais-de-extensao-urbana', 'aglomerados-rurais-isolado',
                                              'aldeias-indigenas', 'areas-de-desenvolvimento-de-controle', 'areas-edificadas',
                                              'bancos-de-areia', 'barragens', 'brejos-e-pantanos', 'capitais', 'cidades',
                                              'corredeiras', 'curvas-batimetricas', 'curvas-de-nivel', 'dunas', 'eclusas',
                                              'edificacoes-agropecuarias-de-extracao-vegetal-e-pesca',
                                              'edificacoes-de-construcao-aeroportuaria', 'edificacoes-de-construcao-portuaria',
                                              'edificacoes-de-metro-ferroviaria', 'edificacoes-industrial', 'edificacoes-publica-militar',
                                              'edificacoes-religiosa', 'elementos-fisiografico-natural',
                                              'estacoes-geradoras-de-energia-eletrica', 'extracoes-minerais',
                                              'fozes-maritima', 'fundeadouros', 'hidreletricas', 'hydra', 'ilhas',
                                              'mangues', 'marcos-de-limite', 'massas-dagua', 'municipios', 'outros-limites-oficiais', 'paises',
                                              'picos', 'pistas-de-ponto-pouso', 'pontes', 'pontos-cotados-altimetricos',
                                              'pontos-cotados-batimetricos', 'postos-fiscais', 'quedas-dagua', 'rdfs', 'recifes', 'rochas-em-agua',
                                              'sinalizacoes', 'subClassOf', 'sumidouros-vertedouros', 'termeletricas',
                                              'terras-indigenas', 'terrenos-sujeito-a-inundacao', 'torres-de-energia',
                                              'travessias', 'trechos-de-drenagem', 'trechos-de-massa-dagua',
                                              'trechos-dutos', 'trechos-ferroviarios', 'trechos-hidroviarios',
                                              'trechos-rodoviarios', 'tuneis', 'unidades-de-conservacao-nao-snuc',
                                              'unidades-de-protecao-integral', 'unidades-de-uso-sustentavel',
                                              'unidades-federativas', 'vegetacoes-de-restinga', 'vilas'])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], self.link_vocab)
        self.assertEquals(response_dict["@type"], self.entrypoint_vocab)
        self.assertEquals(response_dict["@context"]['aglomerados-rurais-de-extensao-urbana']["@id"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["@context"]['aglomerados-rurais-de-extensao-urbana']["@type"], "@id")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_for_raster_entrypoint(self):
        response = requests.options(self.raster_base_uri)
        self.assertEquals(response.status_code, 200)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(a_context_keys, ['hydra',
                                           'imagem-exemplo-tile1-list',
                                           'imagem-exemplo1-list',
                                           'imagem-exemplo2-list',
                                           'imagem-exemplo4-tile2-list',
                                           'rdfs', 'subClassOf'])

        response_dict = self.aux_get_dict_from_response(response)

        self.assertEquals(response_dict["@id"], self.link_vocab)
        self.assertEquals(response_dict["@type"], self.entrypoint_vocab)
        self.assertEquals(response_dict["@context"]['imagem-exemplo-tile1-list']["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@context"]['imagem-exemplo-tile1-list']["@type"], "@id")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

    def test_options_for_non_spatial_entrypoint(self):
        response = requests.options(self.controle_base_uri)
        self.assertEquals(response.status_code, 200)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['gasto-list', 'hydra', 'rdfs', 'subClassOf', 'tipo-gasto-list', 'usuario-list'])

        response_dict = self.aux_get_dict_from_response(response)

        self.assertEquals(response_dict["@id"], self.link_vocab)
        self.assertEquals(response_dict["@type"], self.entrypoint_vocab)
        self.assertEquals(response_dict["@context"]['gasto-list']["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@context"]['gasto-list']["@type"], "@id")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")

#python manage.py test hyper_resource.tests.GetRequestContextTest --testrunner=hyper_resource.tests.NoDbTestRunner
class GetRequestContextTest(AbstractOptionsRequestTest):

    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    # tests for feature resource simple path
    def test_suffixed_request_to_feature_resource_simple_path(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/ES.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'geometriaaproximada', 'hydra', 'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'sigla', 'subClassOf'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://schema.org/State')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#Feature')
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    # tests for feature resource attributes
    def test_suffixed_request_to_feature_resource_only_attributes(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/ES/geom,geocodigo,sigla.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'hydra', 'rdfs', 'sigla', 'subClassOf'])

        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    def test_suffixed_request_to_feature_resource_only_alphanumeric_attributes(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/ES/geocodigo,sigla.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'hydra', 'rdfs', 'sigla', 'subClassOf'])

        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://schema.org/Thing')
        self.assertEquals(response_dict["@type"], 'https://schema.org/Thing')
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    def test_suffixed_request_to_feature_resource_only_geometric_attribute(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/ES/geom.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    # tests for feature resource operations
    def test_suffixed_request_to_feature_resource_operation_with_float_return(self):
        response = requests.get(self.bcim_base_uri + 'unidades-federativas/ES/area.jsonld')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['area', 'hydra', 'rdfs', 'subClassOf'])

        area_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "area")
        self.assertListEqual(area_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://schema.org/Float')
        self.assertEquals(response_dict["@type"], 'https://schema.org/Thing')
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    def test_suffixed_request_to_feature_resource_operation_with_geometry_return(self):
        response = requests.get(self.bcim_base_uri + 'unidades-federativas/ES/buffer/1.2.jsonld')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#MultiPolygon')
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    def test_suffixed_request_to_feature_resource_point_on_surface_operation(self):
        response = requests.get(self.bcim_base_uri + 'unidades-federativas/ES/point_on_surface.jsonld')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['hydra', 'rdfs', 'subClassOf'])

        subClassOf_on_surface_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_on_surface_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://purl.org/geojson/vocab#Point')
        self.assertEquals(response_dict["@type"], 'https://purl.org/geojson/vocab#Point')
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')


    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    # tests for feature collection simple path
    def test_suffixed_request_to_feature_collection_resource_simple_path(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'geometriaaproximada', 'hydra', 'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'sigla', 'subClassOf'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/State")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    # tests for feature collection attributes
    def test_suffixed_request_to_feature_collection_resource_only_attributes(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/nome,geom.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_suffixed_request_feature_collection_only_geometric_attribute(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/geom.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['hydra', 'rdfs', 'subClassOf'])

        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Point")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#GeometryCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_suffixed_request_feature_collection_only_alphanumeric_attributes(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/nome,nomeabrev.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['hydra', 'nome', 'nomeabrev', 'rdfs', 'subClassOf'])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], 'https://schema.org/Thing')
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    # tests for feature collection operations
    def test_suffixed_request_feature_collection_operation_with_geometry_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + "unidades-federativas/ES.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['codigofunai', 'etnia', 'geometriaaproximada', 'hydra',
                                             'id_objeto', 'nome', 'nomeabrev', 'rdfs', 'subClassOf', 'terraindigena'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        codigofunai_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "codigofunai")
        self.assertListEqual(codigofunai_context_keys_list, self.keys_from_attrs_context)
        terraindigena_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "terraindigena")
        self.assertListEqual(terraindigena_context_keys_list, self.keys_from_attrs_context)
        etnia_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "etnia")
        self.assertListEqual(etnia_context_keys_list, self.keys_from_attrs_context)
        #geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        #self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        # rdfs_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'rdfs')
        # self.assertListEqual(rdfs_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://purl.org/geojson/vocab#Feature")
        self.assertEquals(response_dict["@type"], "https://purl.org/geojson/vocab#FeatureCollection")
        self.assertEquals(response_dict["subClassOf"], self.collection_vocab)

    def test_suffixed_request_feature_collection_operation_with_integer_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/count-resource.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(context_dict_keys, ["count-resource", 'hydra', 'rdfs', 'subClassOf'])

        count_resource_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'count-resource')
        self.assertEquals(count_resource_acontext_keys, self.keys_from_oper_context)
        subClassOf_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, 'subClassOf')
        self.assertEquals(subClassOf_acontext_keys, self.keys_from_oper_context)

        supported_operations = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "hydra:totalItems")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # --------------- TESTS FOR NON SPATIAL RESOURCE ---------------------------------
    # tests for nonspatialresource simple path
    def test_suffixed_request_to_non_spatial_resource_simple_path(self):
        response = requests.get(self.controle_base_uri + "usuario-list/1.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs', 'senha', 'subClassOf'])

        #avatar_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "avatar")
        #self.assertListEqual(avatar_context_keys_list, self.keys_from_attrs_context)
        data_nascimento_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data_nascimento")
        self.assertListEqual(data_nascimento_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nome_usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome_usuario")
        self.assertListEqual(nome_usuario_context_keys_list, self.keys_from_attrs_context)
        senha_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "senha")
        self.assertListEqual(senha_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    # tests for nonspatialresource attributes
    def test_suffixed_request_to_non_spatial_resource_only_attributes(self):
        response = requests.get(self.controle_base_uri + "usuario-list/1/nome,email.jsonld")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['email', 'hydra', 'nome', 'rdfs', 'subClassOf'])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@id"], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], "https://schema.org/Thing")
        self.assertEquals(response_dict["subClassOf"], "hydra:Resource")


    # --------------- TESTS FOR COLLECTION ---------------------------------
    # tests for collection simple path
    def test_suffixed_request_to_collection_resource_simple_path(self):
        response = requests.get(self.controle_base_uri + "usuario-list.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['data_nascimento', 'email', 'hydra', 'id', 'nome', 'nome_usuario', 'rdfs', 'senha', 'subClassOf'])

        #avatar_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "avatar")
        #self.assertListEqual(avatar_context_keys_list, self.keys_from_attrs_context)
        data_nascimento_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data_nascimento")
        self.assertListEqual(data_nascimento_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nome_usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome_usuario")
        self.assertListEqual(nome_usuario_context_keys_list, self.keys_from_attrs_context)
        senha_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "senha")
        self.assertListEqual(senha_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict['@type'], self.collection_vocab)
        self.assertEquals(response_dict['subClassOf'], "hydra:Resource")

    # tests for collection attributes
    def test_suffixed_request_to_collection_resource_only_attributes(self):
        response = requests.get(self.controle_base_uri + 'gasto-list/data,valor.jsonld')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ['data', 'hydra', 'rdfs', 'subClassOf', 'valor'])

        data_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data")
        self.assertListEqual(data_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)
        subClassOf_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "subClassOf")
        self.assertListEqual(subClassOf_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@id'], "https://schema.org/Thing")
        self.assertEquals(response_dict["@type"], self.collection_vocab)
        self.assertEquals(response_dict["subClassOf"], 'hydra:Resource')

    # tests for collection operation

    # tests for collection collect operation


    # ------------------- TESTS FOR ENTRY POINTS -------------------------------------

#python manage.py test hyper_resource.tests.PaginationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class PaginationTest(AbstractHeadRequestTest):
    '''
    def test_collection_simple_path_pagination(self):
        response = requests.get(self.controle_base_uri + "gasto-list/")
        self.assertEquals(response.status_code, 200)
        # the string must be hardcoded, if not, the test fails
        expected_link = '<http://luc00557196:8000/controle-list/>; rel="up" , <http://luc00557196:8000/controle-list/gasto-list.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" , <http://luc00557196:8000/controle-list/gasto-list/offset-limit/101&100>; rel="next" '
        #expected_link = '<' + HOST + 'api/bcim/>; rel="up" , <' + HOST + 'api/bcim/aldeias-indigenas.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" , <' + HOST + 'api/bcim/aldeias-indigenas/offset-limit/101&100>; rel="next" '
        self.assertEquals(response.headers["link"], expected_link)
    '''

    '''
    def test_feature_collection_simle_path_ordering_by_geometry_longitude(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/order_by/geom")
        self.assertEquals(response.status_code, 200)

        response_dict = self.aux_get_dict_from_response(response)
        features_names_ordered_by_longitude = [ uf['properties']['nome'] for uf in response_dict['features'] ]
        expected_names_ordered_by_longitude = ['Acre', 'Amazonas', 'Rondรดnia', 'Roraima', 'Mato Grosso', 'Parรก',
                                               'Mato Grosso do Sul', 'Rio Grande do Sul', 'Amapรก', 'Paranรก',
                                               'Santa Catarina', 'Goiรกs', 'Sรฃo Paulo', 'Minas Gerais', 'Tocantins',
                                               'Maranhรฃo', 'Distrito Federal', 'Bahia', 'Piauรญ', 'Rio de Janeiro',
                                               'Espรญrito Santo', 'Cearรก', 'Pernambuco', 'Paraรญba', 'Rio Grande do Norte',
                                               'Sergipe', 'Alagoas']
        self.assertListEqual(features_names_ordered_by_longitude, expected_names_ordered_by_longitude)
    '''

    def test_head_collection_simple_path_pagination(self):
        response = requests.head(self.controle_base_uri + "gasto-list/")
        self.assertEquals(response.status_code, 200)

        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])

        up_hypermidia_control = self.aux_get_hypermidia_control_from_link_header(response, 'up')
        self.assertEquals(up_hypermidia_control, "<" + self.controle_base_uri + ">")
        context_hypermidia_control = self.aux_get_hypermidia_control_from_link_header(response, 'http://www.w3.org/ns/json-ld#context')
        self.assertEquals(context_hypermidia_control, "<" + self.controle_base_uri + "gasto-list.jsonld>; type=\"application/ld+json\"")
        next_hypermidia_control = self.aux_get_hypermidia_control_from_link_header(response, 'next')
        self.assertEquals(next_hypermidia_control, "<" + self.controle_base_uri + "gasto-list/offset-limit/1001/1000>")

    def test_head_collection_pagination_with_offset_limit_operation(self):
        response = requests.head(self.controle_base_uri + "gasto-list/offset-limit/1001&1000")
        self.assertEquals(response.status_code, 200)

        self.assertIn('rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" ', response.headers['link'])
        self.assertIn('rel="metadata"', response.headers['link'])
        self.assertIn('rel="stylesheet', response.headers['link'])
        self.assertIn('rel="up"', response.headers['link'])
        self.assertNotIn('rel="https://schema.org/EntryPoint"', response.headers['link'])
        self.assertNotIn('rel="describedBy"', response.headers['link'])

        up_hypermidia_control = self.aux_get_hypermidia_control_from_link_header(response, 'up')
        self.assertEquals(up_hypermidia_control, "<" + self.controle_base_uri + ">")
        context_hypermidia_control = self.aux_get_hypermidia_control_from_link_header(response, 'http://www.w3.org/ns/json-ld#context')
        self.assertEquals(context_hypermidia_control, "<" + self.controle_base_uri + "gasto-list/offset-limit/1001&1000.jsonld>; type=\"application/ld+json\"")
        next_hypermidia_control = self.aux_get_hypermidia_control_from_link_header(response, 'next')
        self.assertEquals(next_hypermidia_control, "<" + self.controle_base_uri + "gasto-list/offset-limit/2001&1000>")

    """
    # Pagination for feature collection must be specific for each case
    # In this specific "aldeias-indigenas" case we are dealing with Poits and don't make sense paginate about 200 Points
    def test_feature_collection_simple_path_pagination(self):
        response = requests.head(self.bcim_base_uri + "aldeias-indigenas/")
        self.assertEquals(response.status_code, 200)
        expected_link = '<http://luc00557196:8000/api/bcim/aldeias-indigenas/offset-limit/1001/100>; rel="next" '
        self.assertNotIn(expected_link, response.headers["link"])
    """
