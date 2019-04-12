
from rest_framework import serializers

from scrum.models import *
from hyper_resource.serializers import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework.serializers import HyperlinkedRelatedField


class ContinuousActivitySerializer(BusinessSerializer):
    responsible = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)
    typeContinuousActivity = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)

    class Meta:
        model = ContinuousActivity
        fields = ['id', 'name', 'description', 'started', 'ended', 'responsible', 'typeContinuousActivity']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def field_relationship_to_validate_dict(self):
        a_dict = {
            'responsible_id': 'responsible',
            'typeContinuousActivity_id': 'typeContinuousActivity'
        }
        return a_dict

class EntryPointSerializer(BusinessSerializer):
    class Meta:
        model = EntryPoint
        fields = ['scrum_user','continuous_activity','project','sprint','type_continuous_activity','task','impediment']
        identifier = None
        identifiers = []

class ImpedimentSerializer(BusinessSerializer):
    task = HyperlinkedRelatedField(view_name='scrum:Task_detail', many=False, read_only=True)
    sprint = HyperlinkedRelatedField(view_name='scrum:Sprint_detail', many=False, read_only=True)

    class Meta:
        model = Impediment
        fields = ['id', 'name', 'description', 'created_date', 'resolution_date', 'task', 'sprint']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def field_relationship_to_validate_dict(self):
        a_dict = {
            'task_id': 'task',
            'sprint_id': 'sprint'
        }
        return a_dict

    def get_id_relationship_from_request(self, field_name_relationship):
        if field_name_relationship not in self.initial_data:
            return None

        field_iri = self.initial_data[field_name_relationship]
        if field_iri is not None and field_iri != '':
            arr = field_iri.split('/')
            return arr[-1] if arr[-1] != '' else arr[-2]

        return None

    def transform_relationship_from_request(self, validated_data):
        for key, value in self.field_relationship_to_validate_dict().items():
             validated_data[key] = self.get_id_relationship_from_request(value)

    def create_or_update(self, instance, validated_data):
        an_instance = instance
        self.transform_relationship_from_request(validated_data)

        if an_instance is None:
            an_instance = super(ImpedimentSerializer, self).create(validated_data)
        else:
            an_instance = super(ImpedimentSerializer, self).update(instance, validated_data)

        return an_instance

    def create(self, validated_data):
        return self.create_or_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_or_update(instance, validated_data)

class ProjectSerializer(BusinessSerializer):
    sprints = HyperlinkedRelatedField(view_name='scrum:Sprint_detail', many=True, read_only=True)
    tasks = HyperlinkedRelatedField(view_name='scrum:Task_detail', many=True, read_only=True)
    administrative_responsible = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)
    technical_responsible = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start', 'end', 'administrative_responsible', 'technical_responsible',
                  'tasks', 'sprints']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def field_relationship_to_validate_dict(self):
        a_dict = {
            'administrative_responsible_id': 'administrative_responsible',
            'technical_responsible_id': 'technical_responsible'
        }
        return a_dict

    def get_id_relationship_from_request(self, field_name_relationship):
        if field_name_relationship not in self.initial_data:
            return None

        field_iri = self.initial_data[field_name_relationship]
        if field_iri != None and field_iri != '':
            field_iri = field_iri if field_iri[-1] != '/' else field_iri[:-1]
            return field_iri.split("/")[-1]

        return None

    def transform_relationship_from_request(self, validated_data):
        validated_data['technical_responsible_id'] = self.get_id_relationship_from_request('technical_responsible')
        validated_data['administrative_responsible_id'] = self.get_id_relationship_from_request( 'administrative_responsible')

    '''
    def create_or_update(self, instance, validated_data):
        an_instance = instance
        self.transform_relationship_from_request(validated_data)

        if an_instance is None:
            an_instance = super(ProjectSerializer, self).create(validated_data)
        else:
            an_instance = super(ProjectSerializer, self).update(instance, validated_data)

        an_instance.technical_responsible_id = validated_data['technical_responsible_id']
        an_instance.administrative_responsible_id = validated_data['administrative_responsible_id']
        return an_instance
    '''

    '''
    def create(self, validated_data):
        return self.create_or_update(None, validated_data)
    '''

    def update(self, instance, validated_data):
        return self.create_or_update(instance, validated_data)

class ScrumUserSerializer(BusinessSerializer):
    continuous_activities = HyperlinkedRelatedField(view_name='scrum:ContinuousActivity_detail', many=True, read_only=True)
    sprints = HyperlinkedRelatedField(view_name='scrum:Sprint_detail', many=True, read_only=True)
    tasks = HyperlinkedRelatedField(view_name='scrum:Task_detail', many=True, read_only=True)

    class Meta:
        model = ScrumUser
        fields = ['id', 'name', 'email', 'password', 'description', 'role', 'avatar', 'active', 'user_name', 'tasks', 'sprints', 'continuous_activities']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def update(self, instance, validated_data):
        #self.validated_data.pop("user_name")
        #self.validated_data.pop("password")
        validated_data.pop("user_name")
        validated_data.pop("password")
        return super(ScrumUserSerializer, self).update(instance, validated_data)

class SprintSerializer(BusinessSerializer):
    #task = HyperlinkedRelatedField(view_name='scrum:Task_detail', many=True, read_only=True)
    #impediment = HyperlinkedRelatedField(view_name='scrum:Impediment_detail', many=True, read_only=True)
    project = HyperlinkedRelatedField(view_name='scrum:Project_detail', many=False, read_only=True)
    responsible = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)

    class Meta:
        model = Sprint
        fields = ['id_sprint','code','start','end','project','responsible']
        identifier = 'id_sprint'
        identifiers = ['pk', 'id_sprint']

    def field_relationship_to_validate_dict(self):
        a_dict = {
            'project_id': 'project',
            'responsible_id': 'responsible'}
        return a_dict

class TaskSerializer(BusinessSerializer):
    impediments = HyperlinkedRelatedField(view_name='scrum:Impediment_detail', many=True, read_only=True)
    sprint = HyperlinkedRelatedField(view_name='scrum:Sprint_detail', many=False, read_only=True)
    responsible = HyperlinkedRelatedField(view_name='scrum:ScrumUser_detail', many=False, read_only=True)
    project = HyperlinkedRelatedField(view_name='scrum:Project_detail', many=False, read_only=True)
    typeContinuousActivity = HyperlinkedRelatedField(view_name='scrum:TypeContinuousActivity_detail', many=False, read_only=True)

    to_string = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'status', 'order', 'started', 'due', 'completed', 'sprint',
                  'responsible', 'project', 'typeContinuousActivity', 'impediments', 'to_string']
        identifier = 'id'
        identifiers = ['pk', 'id']

    def field_relationship_to_validate_dict(self):
        a_dict = {
            'sprint_id': 'sprint',
            'responsible_id': 'responsible',
            'project_id': 'project',
            'typeContinuousActivity_id': 'typeContinuousActivity'
        }
        return a_dict

    def to_string(self, obj):
        return obj.to_string()

    def get_user_id(self, url_or_pk):
        if type(url_or_pk) == int:
            return url_or_pk
        url_or_pk = url_or_pk if url_or_pk[-1] != "/" else url_or_pk[:-1]
        return int(url_or_pk.split("/")[-1])

    # todo: Este metodo foi sobrescrito porque o metodo is_valid default estava ignorando as foreign keys
    def is_valid(self, raise_exception=False):
        super(TaskSerializer, self).is_valid(raise_exception=raise_exception)

        names_from_db = [dicti["name"] for dicti in Task.objects.values(*["name"])]
        # invalidade POST for task with same name
        if self.initial_data["name"] in names_from_db and not "id" in self.initial_data:
            return False

        responsible = self.initial_data["responsible"]
        id = self.get_user_id(responsible)
        try:
            ScrumUser.objects.get(pk=id)
            return True
        except ScrumUser.DoesNotExist:
            self._errors = {"responsible": "This field must be a valid user"}
            return False

class TypeContinuousActivitySerializer(BusinessSerializer):
    class Meta:
        model = TypeContinuousActivity
        fields = ['id', 'name', 'type']
        identifier = 'id'
        identifiers = ['pk', 'id']



serializers_dict = {}