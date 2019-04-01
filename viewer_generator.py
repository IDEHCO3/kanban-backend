import os
import sys, inspect
import django
import re
from django.contrib.gis.db import models
from django.contrib.gis.db.models import GeometryField

from hyper_resource.models import FeatureModel

def generate_get_root_response(a_name_space, model_class_name):

    context_name = convert_camel_case_to_hifen(model_class_name) + '-list'

    return "'"+ context_name +"'"+': reverse(' + "'" +a_name_space +':'+ model_class_name+'_list'+"'"+' , request=request, format=format),\n'

def convert_camel_case_to_hifen(camel_case_string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', camel_case_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def get_unique_field_name_or_none(model_class):
    obj = model_class()
    unique_field_name_arr = [field.name for field in obj._meta.fields if field.unique and not field.primary_key]
    return unique_field_name_arr[0] if len(unique_field_name_arr) == 1 else None

def generate_snippets_to_view(model_class_name, model_class, is_spatial):
    super_class_collection_name = 'FeatureCollectionResource' if is_spatial else 'CollectionResource'
    super_class_name = 'FeatureResource' if is_spatial else 'NonSpatialResource'
    serializer_class_snippet = (' ' * 4) + 'serializer_class = ' + model_class_name + 'Serializer\n'
    context_name = convert_camel_case_to_hifen(model_class_name)
    context = convert_camel_case_to_hifen((' ' * 4) + 'contextclassname = ' + "'" + context_name + "-list'\n")
    unique_field_name = get_unique_field_name_or_none(model_class)
    arr = []
    arr.append('class ' + model_class_name + 'List('+ super_class_collection_name +'):\n')
    arr.append((' ' * 4) + 'queryset = ' + model_class_name + '.objects.all()' + '\n')
    arr.append(serializer_class_snippet)
    arr.append(context)
    arr.append((' ' * 4) + 'def initialize_context(self):\n')
    arr.append((' ' * 8) + 'self.context_resource = ' + model_class_name + 'ListContext()\n')
    arr.append((' ' * 8) + 'self.context_resource.resource = self\n')
    arr.append('\n')
    arr.append('class ' + model_class_name + 'Detail(' + super_class_name +'):\n')
    arr.append(serializer_class_snippet)
    arr.append(context)
    arr.append((' ' * 4) + 'def initialize_context(self):\n')
    arr.append((' ' * 8) + 'self.context_resource = ' + model_class_name + 'DetailContext()\n')
    arr.append((' ' * 8) + 'self.context_resource.resource = self\n')

    if unique_field_name:
        arr.append('\n')
        arr.append((' ' * 4) + 'def get(self, request, format=None, *args, **kwargs):\n')
        arr.append((' ' * 8) + "if kwargs.get('" + unique_field_name + "') is not None:\n")
        arr.append((' ' * 12) + "kwargs['" + unique_field_name + "'] = kwargs.get('" + unique_field_name + "')\n")
        arr.append((' ' * 12) + "self.kwargs['" + unique_field_name + "'] = kwargs.get('" + unique_field_name + "')\n")
        arr.append((' ' * 8) + 'return super(' + model_class_name + 'Detail, self).get(request, *args, **self.kwargs)\n')

        arr.append('\n')
        arr.append((' ' * 4) + 'def options(self, request, *args, **kwargs):\n')
        arr.append((' ' * 8) + "if kwargs.get('" + unique_field_name + "') is not None:\n")
        arr.append((' ' * 12) + "kwargs['" + unique_field_name + "'] = kwargs.get('" + unique_field_name + "')\n")
        arr.append((' ' * 12) + "self.kwargs['" + unique_field_name + "'] = kwargs.get('" + unique_field_name + "')\n")
        arr.append((' ' * 8) + 'return super(' + model_class_name + 'Detail, self).options(request, *args, **self.kwargs)\n')

    return arr

def is_spatial(model_class):
    for field in model_class._meta.get_fields():
      if isinstance(field, GeometryField):
         return True
    return False

def imports_str_as_array(a_name):
    arr = []
    arr.append("from collections import OrderedDict\n")

    arr.append("from rest_framework.response import Response\n")
    arr.append("from rest_framework.reverse import reverse\n")
    arr.append("from rest_framework.views import APIView\n")
    arr.append("from rest_framework import permissions\n")
    arr.append("from rest_framework import generics\n")
    arr.append("from rest_framework import status\n")
    arr.append("from hyper_resource.views import *\n")
    arr.append("from hyper_resource.contexts import *\n")
    arr.append("from " + a_name + ".models import *\n")
    arr.append("from " + a_name + ".serializers import *\n")
    arr.append("from " + a_name + ".contexts import *\n\n")
    #arr.append("from hyper_resource.contexts import BaseContext, NonSpatialAPIRoot, FeatureAPIRoot\n")
    arr.append("from hyper_resource.resources.EntryPointResource import *\n")
    arr.append("from hyper_resource.resources.AbstractCollectionResource import AbstractCollectionResource\n")
    arr.append("from hyper_resource.resources.AbstractResource import *\n")
    arr.append("from hyper_resource.resources.CollectionResource import CollectionResource\n")
    arr.append("from hyper_resource.resources.FeatureCollectionResource import FeatureCollectionResource\n")
    arr.append("from hyper_resource.resources.FeatureResource import FeatureResource\n")
    arr.append("from hyper_resource.resources.NonSpatialResource import NonSpatialResource\n")
    arr.append("from hyper_resource.resources.RasterCollectionResource import RasterCollectionResource\n")
    arr.append("from hyper_resource.resources.RasterResource import RasterResource\n")
    arr.append("from hyper_resource.resources.SpatialCollectionResource import SpatialCollectionResource\n")
    arr.append("from hyper_resource.resources.SpatialResource import SpatialResource\n")
    arr.append("from hyper_resource.resources.StyleResource import StyleResource\n")
    arr.append("from hyper_resource.resources.TiffCollectionResource import TiffCollectionResource\n")
    arr.append("from hyper_resource.resources.TiffResource import TiffResource\n\n")

    return arr


def generate_file(package_name, default_name='views.py'):
    arr_tuple_name_and_class = [(name, method) for name, method in  inspect.getmembers(sys.modules[package_name + '.models'],inspect.isclass)  if (name != 'BusinessModel' and name != 'FeatureModel' and isinstance(method, django.db.models.base.ModelBase)) ]
    with open(default_name, 'w+') as sr:
        for import_str in imports_str_as_array(package_name):
            sr.write(import_str)

        has_spatial_model = False
        for tuple_name_and_class in arr_tuple_name_and_class:
            if is_spatial(tuple_name_and_class[1]):
                has_spatial_model = True
                break

        if has_spatial_model:
            sr.write('class APIRoot(FeatureEntryPointResource):\n\n')
        else:
            sr.write('class APIRoot(NonSpatialEntryPointResource):\n\n')
        sr.write((' ' * 4) + 'serializer_class = EntryPointSerializer\n\n')
        sr.write((' ' * 4) + 'def get_root_response(self, request, format=None, *args, **kwargs):\n')
        sr.write((' ' * 8) + 'root_links = {\n\n')
        for tuple_name_and_class in arr_tuple_name_and_class:
            get_root_str = generate_get_root_response(package_name ,tuple_name_and_class[0])
            sr.write((' ' * 10) + get_root_str)
        sr.write((' ' * 8) + '}\n\n')
        sr.write((' ' * 8) + 'ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))\n')
        sr.write((' ' * 8) + 'return ordered_dict_of_link\n\n')
        for tuple_name_and_class in arr_tuple_name_and_class:

            for str in generate_snippets_to_view(tuple_name_and_class[0], tuple_name_and_class[1], is_spatial(tuple_name_and_class[1])):
                sr.write(str)
            sr.write('\n')
        sr.close()

if __name__ == "__main__":
    if (len( sys.argv))!= 3:
        print('Usage: python viewer_generator.py django_project_name django_app_name')
        exit()

    prj_name = sys.argv[1]
    app_name = sys.argv[2]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", prj_name + ".settings")
    django.setup()
    generate_file(app_name)
    print('views.py  has been generated')