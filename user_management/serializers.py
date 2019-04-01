from user_management.models import *
from hyper_resource.serializers import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework.serializers import HyperlinkedRelatedField

class APIResourceSerializer(BusinessSerializer):
    class Meta:
        model = APIResource
        fields = ['id','package_name','class_name','method_name','operation_name']
        identifier = 'id'
        identifiers = ['pk', 'id']

class HyperUserSerializer(BusinessSerializer):
    subordinates = HyperlinkedRelatedField(view_name='user_management:HyperUser_detail', many=True, read_only=True)
    boss = HyperlinkedRelatedField(view_name='user_management:HyperUser_detail', many=False, read_only=True)
    class Meta:
        model = HyperUser
        fields = ['subordinates','id','name','user_name','email','password','description','active','boss']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def field_relationship_to_validate_dict(self):
        a_dict = {}
        a_dict['boss_id'] = 'boss'
        return a_dict

class HyperUserGroupSerializer(BusinessSerializer):
    col_of_user_group_api = HyperlinkedRelatedField(view_name='user_management:HyperUserGroupAPIResource_detail', many=True, read_only=True)
    class Meta:
        model = HyperUserGroup
        fields = ['col_of_user_group_api','id','name','type']
        identifier = 'id'
        identifiers = ['pk', 'id']

class HyperUserGroupAPIResourceSerializer(BusinessSerializer):
    user_group = HyperlinkedRelatedField(view_name='user_management:HyperUserGroup_detail', many=False, read_only=True)
    api_resource = HyperlinkedRelatedField(view_name='user_management:HyperUserGroup_detail', many=False, read_only=True)
    class Meta:
        model = HyperUserGroupAPIResource
        fields = ['id','active','user_group','api_resource']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def field_relationship_to_validate_dict(self):
        a_dict = {}
        a_dict['user_group_id'] = 'user_group'
        a_dict['api_resource_id'] = 'api_resource'
        return a_dict



serializers_dict = {}