
from hyper_resource.models import SpatialCollectionOperationController
from hyper_resource.resources.AbstractCollectionResource import AbstractCollectionResource


class SpatialCollectionResource(AbstractCollectionResource):
    def __init__(self):
        super(SpatialCollectionResource, self).__init__()
        self.queryset = None
        self.operation_controller = SpatialCollectionOperationController()

    def attribute_names_to_web(self):
        alpha_attrs_names = super(SpatialCollectionResource, self).attribute_names_to_web()
        alpha_attrs_names.append(self.serializer_class.Meta.geo_field)
        return alpha_attrs_names

    #todo
    def path_request_is_ok(self, attributes_functions_str):
        return True

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def operation_names_model(self):
        return self.operation_controller.feature_collection_operations_dict().keys()

    def path_has_only_spatial_operation(self, attributes_functions_str):
        pass
