from hyper_resource.models import RasterOperationController
from hyper_resource.resources.SpatialResource import SpatialResource


class RasterResource(SpatialResource):
    def __init__(self):
        super(RasterResource, self).__init__()
        self.operation_controller = RasterOperationController()

    def default_file_name(self):
        return self.object_model.model_class_name() + '_' + str(self.object_model.pk) + '.tiff'

    def default_resource_representation(self):
        return 'Raster'

    def get_object_model_raster(self, kwargs):
        pass