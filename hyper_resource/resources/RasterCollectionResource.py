from hyper_resource.resources.BaseModel import BaseModel
from hyper_resource.resources.EntryPointResource import RasterEntryPointResource
from hyper_resource.resources.SpatialCollectionResource import SpatialCollectionResource


class RasterCollectionResource(RasterEntryPointResource):
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

    def get_root_response(self, request, format=None, *args, **kwargs):
        self.initialize_object(request, *args, **kwargs)
        return self.object_model
