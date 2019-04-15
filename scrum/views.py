from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from hyper_resource.views import *
from hyper_resource.contexts import *
from scrum.models import *
from scrum.serializers import *
from scrum.contexts import *

from hyper_resource.resources.EntryPointResource import *
from hyper_resource.resources.AbstractCollectionResource import AbstractCollectionResource
from hyper_resource.resources.AbstractResource import *
from hyper_resource.resources.CollectionResource import CollectionResource
from hyper_resource.resources.FeatureCollectionResource import FeatureCollectionResource
from hyper_resource.resources.FeatureResource import FeatureResource
from hyper_resource.resources.NonSpatialResource import NonSpatialResource
from hyper_resource.resources.RasterCollectionResource import RasterCollectionResource
from hyper_resource.resources.RasterResource import RasterResource
from hyper_resource.resources.SpatialCollectionResource import SpatialCollectionResource
from hyper_resource.resources.SpatialResource import SpatialResource
from hyper_resource.resources.StyleResource import StyleResource
from hyper_resource.resources.TiffCollectionResource import TiffCollectionResource
from hyper_resource.resources.TiffResource import TiffResource
from django.shortcuts import get_object_or_404, render
class APIRoot(NonSpatialEntryPointResource):
    serializer_class = EntryPointSerializer

    def get_root_response(self, request, format=None, *args, **kwargs):
        root_links = {
          'continuous-activity-list': reverse('scrum:ContinuousActivity_list', request=request, format=format),
          'impediment-list': reverse('scrum:Impediment_list', request=request, format=format),
          'project-list': reverse('scrum:Project_list', request=request, format=format),
          'scrum-user-list': reverse('scrum:ScrumUser_list', request=request, format=format),
          'sprint-list': reverse('scrum:Sprint_list', request=request, format=format),
          'task-list': reverse('scrum:Task_list', request=request, format=format),
          'type-continuous-activity-list': reverse('scrum:TypeContinuousActivity_list', request=request, format=format),
        }

        ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
        return ordered_dict_of_link

def index(request):
    #data = open("index.html", 'r').read()

    return HttpResponse(render(request, "scrum/index.html"), content_type="text/html")

class ContinuousActivityList(CollectionResource):
    queryset = ContinuousActivity.objects.all()
    serializer_class = ContinuousActivitySerializer
    contextclassname = 'continuous-activity-list'

    def initialize_context(self):
        self.context_resource = ContinuousActivityListContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True


class ContinuousActivityDetail(NonSpatialResource):
    serializer_class = ContinuousActivitySerializer
    contextclassname = 'continuous-activity-list'

    def initialize_context(self):
        self.context_resource = ContinuousActivityDetailContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True


class ImpedimentList(CollectionResource):
    queryset = Impediment.objects.all()
    serializer_class = ImpedimentSerializer
    contextclassname = 'impediment-list'

    def initialize_context(self):
        self.context_resource = ImpedimentListContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True

    def token_has_permission(self, request, a_token):
        is_safe_request_or_admin = super(ImpedimentList, self).token_has_permission(request, a_token)
        if is_safe_request_or_admin:
            return True

        if request.method in ['POST']:
            return True
            #return user.is_task_owner(request.data)

        return False


class ImpedimentDetail(NonSpatialResource):
    serializer_class = ImpedimentSerializer
    contextclassname = 'impediment-list'

    def initialize_context(self):
        self.context_resource = ImpedimentDetailContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True

    def token_has_permission(self, request, a_token):
        is_safe_request_or_admin = super(ImpedimentDetail, self).token_has_permission(request, a_token)
        if is_safe_request_or_admin:
            return True

        if request.method in ['DELETE']:
            return True
            #return user.is_task_owner(request.data)

        return False

    def delete(self, request, *args, **kwargs):
        data = request.data
        impediment = self.get_object(kwargs)
        user = self.get_user_from_request(request)

        if impediment.is_self_task_impediment(user):
            return super(ImpedimentDetail, self).delete(request, *args, **kwargs)

        return self.get_response_for_not_privileged_token()

class ProjectList(CollectionResource):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    contextclassname = 'project-list'

    def initialize_context(self):
        self.context_resource = ProjectListContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True

    def token_has_permission(self, request, a_token):
        is_safe_request_or_admin = super(ProjectList, self).token_has_permission(request, a_token)
        if is_safe_request_or_admin:
            return True

        if request.method in ['POST']:
            return True
            #return user.is_task_owner(request.data)

        return False


class ProjectDetail(NonSpatialResource):
    serializer_class = ProjectSerializer
    contextclassname = 'project-list'

    def initialize_context(self):
        self.context_resource = ProjectDetailContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True

    def token_has_permission(self, request, a_token):
        is_safe_request_or_admin = super(ProjectDetail, self).token_has_permission(request, a_token)
        if is_safe_request_or_admin:
            return True

        if request.method in ['PUT', 'DELETE']:
            return True
            #return user.is_task_owner(request.data)

        return False

    def get_project_by_id(self, id):
        return Project.objects.get(pk=id)

    def is_setting_project_to_admin(self, data):
        if "administrative_responsible" not in data and "technical_responsible" not in data:
            return False

        adm_responsible_id = int(self.remove_last_slash(data["administrative_responsible"]).split("/")[-1])
        adm_responsible = ScrumUser.objects.get(pk=adm_responsible_id)

        if adm_responsible.role == "admin":
            return True

        tec_responsible_id = int(self.remove_last_slash(data["technical_responsible"]).split("/")[-1])
        tec_responsible = ScrumUser.objects.get(pk=tec_responsible_id)
        if tec_responsible.role == "admin":
            return True

        return False

    def changing_project_responsible_for_another_admin(self, current_user, data):
        if current_user.is_project_owner(data):
            return False

        administrative_responsible_changing_id = int(self.remove_last_slash(data["administrative_responsible"]).split("/")[-1])
        changing_administrative_responsible = ScrumUser.objects.get(pk=administrative_responsible_changing_id)
        if changing_administrative_responsible.is_admin():
            return True

        technical_responsible_changing_id = int(self.remove_last_slash(data["technical_responsible"]).split("/")[-1])
        changing_technical_responsible = ScrumUser.objects.get(pk=technical_responsible_changing_id)

        return changing_technical_responsible.is_admin()

    def changing_project_responsable(self, data):
        request_project_administrative_rasponsable_id = int(self.remove_last_slash(data["administrative_responsible"]).split("/")[-1])
        project_from_db = self.get_project_by_id(data["id"])

        if request_project_administrative_rasponsable_id == project_from_db.administrative_responsible.id:
            return False

        request_project_technical_responsible_id = int(self.remove_last_slash(data["technical_responsible"]).split("/")[-1])
        return request_project_technical_responsible_id == project_from_db.technical_responsible.id

    def put(self, request, *args, **kwargs):
        project = self.get_object(kwargs)
        user = self.get_user_from_request(request)

        if user.is_admin():
            if self.changing_project_responsible_for_another_admin(user, request.data):
                return self.get_response_for_not_privileged_token()
            return super(ProjectDetail, self).put(request, *kwargs, **kwargs)

        if user.is_project_owner(project):
            if self.is_setting_project_to_admin(request.data):
                return self.get_response_for_not_privileged_token("You cannot set this project to admin")
            return super(ProjectDetail, self).put(request, *kwargs, **kwargs)

        return self.get_response_for_not_privileged_token()

    def delete(self, request, *args, **kwargs):
        project = self.get_object(kwargs)
        user = self.get_user_from_request(request)

        if user.is_project_owner(project):
            return super(ProjectDetail, self).delete(request, *kwargs, **kwargs)

        if project.is_admin_project():
            return self.get_response_for_not_privileged_token()

        if user.is_project_owner(project) or user.is_admin():
            return super(ProjectDetail, self).delete(request, *kwargs, **kwargs)

        return self.get_response_for_not_privileged_token()

class ScrumUserList(CollectionResource):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    contextclassname = 'user-list'

    def initialize_context(self):
        self.context_resource = ScrumUserListContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True

class ScrumUserDetail(NonSpatialResource):
    serializer_class = ScrumUserSerializer
    contextclassname = 'user-list'

    def initialize_context(self):
        self.context_resource = ScrumUserDetailContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True

    def changing_from_user_to_admin(self, data):
        if "role" not in data:
            return False

        #obj = self.get_object(kwargs)
        obj_from_db = ScrumUser.objects.get(pk=data["id"])

        if data["role"] == obj_from_db.role:
            return False

        if data["role"] == "admin":
            return True

    def put(self, request, *args, **kwargs):
        #data = request.data
        #if "password" in data:
        #    data.pop("password")

        #if "user_name" in data:
        #    data.pop("user_name")

        if not self.changing_from_user_to_admin(request.data):
            return super(ScrumUserDetail, self).put(request, *args, **kwargs)

        token = self.get_token_from_request(request)
        user = self.get_user_from_token(token)
        if not user.is_admin():
            return self.get_response_for_not_privileged_token(message="You cannot change user role")

        return super(ScrumUserDetail, self).put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user_from_db = self.get_object(kwargs)
        if user_from_db.is_admin():
            return self.get_response_for_not_privileged_token(message="You cannot delete admin users")

        return super(ScrumUserDetail, self).delete(request, *args, **kwargs)


class ScrumUserRegister(CollectionResource):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    contextclassname = 'user-list'

    def initialize_context(self):
        self.context_resource = ScrumUserDetailContext()
        self.context_resource.resource = self

    def user_role_is_admin(self, request_data):
        if not "role" in request_data:
            return False

        return request_data["role"] == "admin"

    def post(self, request, *args, **kwargs):
        if self.user_role_is_admin(request.data):
            a_token_or_none = self.get_token_from_request(request)

            if a_token_or_none is None:
                return self.get_response_for_not_privileged_token()

            user = self.get_user_from_token(a_token_or_none)
            if not user.is_admin():
                return self.get_response_for_not_privileged_token(message="You're not authorized to create admin users")

        resp = super(ScrumUserRegister, self).post(request, *args, **kwargs)
        if resp.status_code != 400:
            resp['x-access-token'] = self.object_model.getToken()
        return resp

    def get(self, request, format=None, *args, **kwargs):
        if format == 'jsonld':
            return self.options(request, *args, **kwargs)

        if request.build_absolute_uri().endswith('.jsonld'):
            kwargs = self.remove_suffix_from_kwargs(**kwargs)
            self.kwargs = kwargs
            return self.options(request, *args, **kwargs)

        response = Response(data={}, status=status.HTTP_204_NO_CONTENT, content_type=self.default_content_type())
        self.add_allowed_methods(["POST"])
        self.add_base_headers(request, response)
        self.add_cors_headers_in_header(response)
        return response

    def head(self, request, *args, **kwargs):
        self.add_allowed_methods(["post"])
        resp = Response(data={}, status=status.HTTP_200_OK, content_type=self.default_content_type())
        self.add_base_headers(request, resp)
        return resp

    def options(self, request, *args, **kwargs):
        self.add_allowed_methods(["post"])
        resp = Response(data={}, status=status.HTTP_204_NO_CONTENT, content_type=self.default_content_type())
        self.add_base_headers(request, resp)
        return resp


class ScrumUserLogin(CollectionResource):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    contextclassname = 'user-list'

    def initialize_context(self):
        self.context_resource = ScrumUserLoginContext()
        self.context_resource.resource = self

    def post(self, request, *args, **kwargs):
        res = ScrumUser.getOneOrNone(request.data['user_name'], request.data['password'])

        if res is None:
            res = Response(status=status.HTTP_401_UNAUTHORIZED, content_type='application/json')
            res['WWW-Authenticate'] = 'Bearer'
            return res

        response = Response(status=status.HTTP_201_CREATED, content_type='application/json')
        response['Content-Location'] = request.path + str(res.id) + '/'
        response['x-access-token'] = res.getToken()
        response['X-Frame-Options'] = 'SAMEORIGIN'
        self.add_cors_headers_in_header(response)

        return response

    def get(self, request, *args, **kwargs):
        if format == 'jsonld':
            return super(ScrumUserLogin, self).get(request, *args, *kwargs)

        if request.build_absolute_uri().endswith('.jsonld'):
            kwargs = self.remove_suffix_from_kwargs(**kwargs)
            self.kwargs = kwargs
            return self.options(request, *args, **kwargs)

        self.add_allowed_methods(["post"])
        resp = Response(status=status.HTTP_204_NO_CONTENT)
        self.add_base_headers(request, resp)
        return resp

    def head(self, request, *args, **kwargs):
        self.add_allowed_methods(["post"])
        resp = Response(data={}, status=status.HTTP_200_OK, content_type=self.default_content_type())
        self.add_base_headers(request, resp)
        return resp


class SprintList(CollectionResource):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    contextclassname = 'sprint-list'

    def initialize_context(self):
        self.context_resource = SprintListContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True

    def token_has_permission(self, request, a_token):
        if request.method in ['POST']:
            return True

        return super(SprintList, self).token_has_permission(request, a_token)


class SprintDetail(NonSpatialResource):
    serializer_class = SprintSerializer
    contextclassname = 'sprint-list'

    def initialize_context(self):
        self.context_resource = SprintDetailContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True


class TaskList(CollectionResource):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    contextclassname = 'task-list'

    def initialize_context(self):
        self.context_resource = TaskListContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True

    def token_has_permission(self, request, a_token):
        #payload = self.get_token_payload(a_token)
        #user = ScrumUser.objects.filter(**payload).first()

        if request.method in ['POST']:
            return True

        return super(TaskList, self).token_has_permission(request, a_token)

    def user_is_task_responsable(self, incoming_task_data, user):
        return user.id == int( self.remove_last_slash(incoming_task_data["responsible"]).split("/")[-1] )

    def post(self, request, *args, **kwargs):
        token = self.get_token_from_request(request)
        user = self.get_user_from_token(token)
        if self.user_is_task_responsable(request.data, user) or user.is_admin():
            return super(TaskList, self).post(request, *args, **kwargs)
        return Response(data={"Not enough privileges": "You don't have permission to assign task for other people"}, status=status.HTTP_401_UNAUTHORIZED)


class TaskDetail(NonSpatialResource):
    serializer_class = TaskSerializer
    contextclassname = 'task-list'

    def initialize_context(self):
        self.context_resource = TaskDetailContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True

    def is_task_owner(self, user):
        user_related_task_ids = [task.id for task in user.tasks.all()]
        return True

    def token_has_permission(self, request, a_token):
        is_safe_request_or_admin = super(TaskDetail, self).token_has_permission(request, a_token)
        if is_safe_request_or_admin:
            return True

        if request.method in ['PUT', 'DELETE']:
            return True
            #return user.is_task_owner(request.data)

        return False

    def get_task_by_id(self, id):
        return Task.objects.get(pk=id)

    def changing_responsable(self, data):
        request_task_rasponsable_id = int(self.remove_last_slash(data["responsible"]).split("/")[-1])
        task_from_db = self.get_task_by_id(data["id"])

        return not request_task_rasponsable_id == task_from_db.responsible.id

    def changing_for_another_admin(self, current_user, data):
        if current_user.is_task_owner(data):
            return False
        task_responsible_changing_id = int(self.remove_last_slash(data["responsible"]).split("/")[-1])

        changing_user = ScrumUser.objects.get(pk=task_responsible_changing_id)

        return changing_user.is_admin()

    def put(self, request, *args, **kwargs):
        request_data = request.data

        a_token = self.get_token_from_request(request)
        payload = self.get_token_payload(a_token)
        user = ScrumUser.objects.filter(**payload).first()

        if user.is_admin() and not self.changing_for_another_admin(user, request_data):
            return super(TaskDetail, self).put(request, *args, **kwargs)

        if self.changing_responsable(request_data):
            return self.get_response_for_not_privileged_token()

        if not user.is_task_owner(request_data):
            return self.get_response_for_not_privileged_token()

        return super(TaskDetail, self).put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        task = self.get_object(kwargs)
        user = self.get_user_from_request(request)

        if user.is_admin() and not task.task_from_admin():
            return super(TaskDetail, self).delete(request, *args, **kwargs)

        if user.is_task_owner(task):
            return super(TaskDetail, self).delete(request, *args, **kwargs)

        return self.get_response_for_not_privileged_token(message="You cannot delete this task")




class TaskListStatus(CollectionResource):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    contextclassname = 'task-list'

    def initialize_context(self):
        self.context_resource = TaskDetailContext()
        self.context_resource.resource = self

    def get(self, request, *args, **kwargs):
       a_data = Task.status_dic()
       return Response(data=a_data, content_type='application/json')

    def token_is_need(self):
        return True


class TypeContinuousActivityList(CollectionResource):
    queryset = TypeContinuousActivity.objects.all()
    serializer_class = TypeContinuousActivitySerializer
    contextclassname = 'type-continuous-activity-list'

    def initialize_context(self):
        self.context_resource = TypeContinuousActivityListContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True


class TypeContinuousActivityDetail(NonSpatialResource):
    serializer_class = TypeContinuousActivitySerializer
    contextclassname = 'type-continuous-activity-list'

    def initialize_context(self):
        self.context_resource = TypeContinuousActivityDetailContext()
        self.context_resource.resource = self

    def token_is_need(self):
        return True


class TypeContinuousActivityTypeList(CollectionResource):
    queryset = TypeContinuousActivity.objects.all()
    serializer_class = TypeContinuousActivitySerializer
    contextclassname = 'type-continuous-activity-list'

    def initialize_context(self):
        self.context_resource = TypeContinuousActivityDetailContext()
        self.context_resource.resource = self

    def get(self, request, *args, **kwargs):
       a_data = TypeContinuousActivity.type_dic()
       return Response(data=a_data, content_type='application/json')

    def token_is_need(self):
        return True

