from django.contrib.gis.gdal import GDALRaster
from django.db import connection


class BaseModel(object):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def create_model_object_raster(self, view_resource, row):
        obj_model = view_resource.model_class()()
        setattr(obj_model,view_resource.pk_name(), row[0])
        rst = GDALRaster(row[1].tobytes())
        setattr(obj_model,view_resource.spatial_field_name(), rst)
        return obj_model

    '''
    def get_raster_bands(self, queryset):
        band_arr = []
        for band in queryset.rast.bands:
            band_arr.append({
                "nodata_value": band.nodata_value,
                "size": (queryset.rast.width, queryset.rast.height)
            })
        return band_arr


    def queryset_as_gdal_raster(self, queryset):
        gdal_raster = GDALRaster({
            "srid": queryset.rast.srid,
            "width": queryset.rast.width,
            "height": queryset.rast.height,
            "driver": queryset.rast.driver.name,
            "name": "/vsimem/",
            "origin": [queryset.rast.origin.x, queryset.rast.origin.y],
            "scale": [queryset.rast.scale.x, queryset.rast.scale.y],
            "skew": [queryset.rast.skew.x, queryset.rast.skew.y],
            "bands": self.get_raster_bands(queryset)
        })
        return gdal_raster
    '''

    def get_model_object_raster(self, view_resource, kwargs):
        #obj_model = view_resource.model_class()()
        #queryset = view_resource.model_class().objects.get(pk=61)
        #raster_resource = self.queryset_as_gdal_raster(queryset)
        #setattr(obj_model,view_resource.pk_name(), queryset.pk)
        #setattr(obj_model,view_resource.spatial_field_name(), raster_resource)
        #return obj_model

       pk_name = view_resource.pk_name()
       sql_string = "SELECT " + pk_name +  ", ST_AsGDALRaster(" + view_resource.spatial_field_name() +  ", 'GTiff') FROM " + view_resource.table_name() +  " WHERE " + pk_name + "  = " + kwargs['pk']
       with connection.cursor() as cursor:
            cursor.execute(sql_string)
            row = cursor.fetchone()
            return self.create_model_object_raster(view_resource, row)

    def get_model_objects_raster(self, view_resource, kwargs):
       pk_name = view_resource.pk_name()
       sql_string = "SELECT " + pk_name +  ", ST_AsGDALRaster(" + view_resource.spatial_field_name() +  ", 'GTiff') FROM " + view_resource.table_name()
       with connection.cursor() as cursor:
            cursor.execute(sql_string)
            rows = cursor.fetchall()
            model_raster_collection = []
            for row in rows:
                model_raster_collection.append(self.create_model_object_raster(view_resource, row))
            return model_raster_collection

    def get_iris_raster(self, view_resource, kwargs):
        pk_name = view_resource.pk_name()
        sql_string = "SELECT " + pk_name + " FROM " + view_resource.table_name()
        iri= view_resource.request.build_absolute_uri()
        iri = iri if iri[-1] == "/" else iri + "/"
        with connection.cursor() as cursor:
            cursor.execute(sql_string)
            rows = cursor.fetchall()
            iri_raster_dic = {}
            name = view_resource.table_name()
            for row in rows:
                str_pk = str(row[0])
                iri_raster_dic[name+ '-' + str_pk ] = (iri + str_pk + '/')
                #iri_raster_dic[str_pk ] = (iri + str_pk + '/')
            return iri_raster_dic