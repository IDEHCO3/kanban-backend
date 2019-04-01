# coding: utf-8
from collections import OrderedDict

from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.db import models

class BusinessSerializer(ModelSerializer):
    #todo: isn't same as original hyper resource code
    def get_id_relationship_from_request(self, field_name_relationship):
        if field_name_relationship not in self.initial_data:
            return None

        field_iri = self.initial_data[field_name_relationship]
        if isinstance(field_iri, models.Model):
            return field_iri

        if type(field_iri) == int:
            return field_iri

        if field_iri != None and field_iri != '':
            arr = field_iri.split('/')
            return arr[-1] if arr[-1] != '' else arr[-2]
        return None

    def field_relationship_to_validate_dict(self):
        return {}

    def transform_relationship_from_request(self, validated_data):
        for key, value in self.field_relationship_to_validate_dict().items():
             validated_data[key] = self.get_id_relationship_from_request(value)

    def create_or_update(self, instance, validated_data):
        an_instance = instance
        self.transform_relationship_from_request(validated_data)
        if an_instance is None:
            an_instance = super(BusinessSerializer, self).create(validated_data)
        else:
            an_instance = super(BusinessSerializer, self).update(instance, validated_data)

        for key, value in self.field_relationship_to_validate_dict().items():
            setattr(an_instance, key, validated_data[key])

        return an_instance

    def create(self, validated_data):
        return self.create_or_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_or_update(instance, validated_data)

class GeoBusinessSerializer(GeoFeatureModelSerializer):
    def get_id_relationship_from_request(self, field_name_relationship):
        if field_name_relationship not in self.initial_data:
            return None
        field_iri = self.initial_data[field_name_relationship]
        if field_iri != None and field_iri != '':
            arr = field_iri.split('/')
            return  arr[-1] if arr[-1] != '' else arr[-2]
        return None

    def field_relationship_to_validate_dict(self):
        return {}

    def transform_relationship_from_request(self, validated_data):
        for key, value in self.field_relationship_to_validate_dict().items():
             validated_data[key] = self.get_id_relationship_from_request(value)

    def create_or_update(self, instance, validated_data):
        an_instance = instance
        self.transform_relationship_from_request(validated_data)
        if an_instance is None:
            an_instance = super(GeoBusinessSerializer, self).create(validated_data)
        else:
            an_instance = super(GeoBusinessSerializer, self).update(instance, validated_data)

        for key, value in self.field_relationship_to_validate_dict().items():
            setattr(an_instance, key, validated_data[key])

        return an_instance

    def create(self, validated_data):
        return self.create_or_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_or_update(instance, validated_data)

    def to_representation(self, instance):
        """
        Serialize objects -> primitives.
        """
        # prepare OrderedDict geojson structure
        feature = OrderedDict()
        # the list of fields that will be processed by get_properties
        # we will remove fields that have been already processed
        # to increase performance on large numbers
        fields = list(self.fields.values())

        # optional id attribute
        if self.Meta.id_field:
            field = self.fields[self.Meta.id_field]
            value = field.get_attribute(instance)
            feature[self.Meta.identifier] = field.to_representation(value)
            fields.remove(field)

        # required type attribute
        # must be "Feature" according to GeoJSON spec
        feature["type"] = "Feature"

        # required geometry attribute
        # MUST be present in output according to GeoJSON spec
        field = self.fields[self.Meta.geo_field]
        geo_value = field.get_attribute(instance)
        feature["geometry"] = field.to_representation(geo_value)
        fields.remove(field)
        # Bounding Box
        # if auto_bbox feature is enabled
        # bbox will be determined automatically automatically
        if self.Meta.auto_bbox and geo_value:
            feature["bbox"] = geo_value.extent
        # otherwise it can be determined via another field
        elif self.Meta.bbox_geo_field:
            field = self.fields[self.Meta.bbox_geo_field]
            value = field.get_attribute(instance)
            feature["bbox"] = value.extent if hasattr(value, 'extent') else None
            fields.remove(field)

        # GeoJSON properties
        feature["properties"] = self.get_properties(instance, fields)

        return feature