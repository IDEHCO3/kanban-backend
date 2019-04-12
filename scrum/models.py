from __future__ import unicode_literals
from hyper_resource.models import FeatureModel, BusinessModel

from datetime import datetime
from django.contrib.gis.db import models

import base64

import jwt

from kanban.settings import SECRET_KEY

class ScrumUser(BusinessModel):
    #id = models.AutoField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100, default='')
    email = models.CharField(unique=True, max_length=100, null=True)
    password = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True, default='')
    role = models.CharField(max_length=100, blank=True, default='user')
    avatar = models.CharField(max_length=200, blank=True, default='')
    active = models.NullBooleanField()
    user_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'scrum_scrumuser'

    @classmethod
    def jwt_algorithm(cls):
        return 'HS256'

    @classmethod
    def getOneOrNone(cls, a_user_name, password):
        user = ScrumUser.objects.filter(user_name=a_user_name, password=password).first()
        return user

    def getToken(self):
        encoded = jwt.encode({'id': self.id, 'user_name': self.user_name, 'avatar': self.avatar}, SECRET_KEY,
                             algorithm=ScrumUser.jwt_algorithm())
        #print(jwt.decode(encoded, SECRET_KEY, algorithm='HS256'))
        return encoded

    @classmethod
    def login(cls, user_name, password):
        user = ScrumUser.getOneOrNone(user_name, password)
        if user is None:
            return None

        a_dict = {
            'id': user.id,
            'name': user.name,
            'user_name': user.user_name,
            'avatar': user.avatar,
            'token': user_name.getToken()
        }
        return a_dict

    @classmethod
    def token_is_ok(cls, a_token):
        try:
            payload = jwt.decode(a_token, SECRET_KEY, algorithm=ScrumUser.jwt_algorithm())
            return True

        except jwt.InvalidTokenError:
            return False

    #@classmethod
    def is_admin(self):
        return self.role == "admin"

    def is_task_owner(self, task):
        if type(task) == dict:
            uri_without_slash = task["responsible"] if task["responsible"][-1] != "/" else task["responsible"][:-1]
            return self.id == int(uri_without_slash.split("/")[-1])

        return  self.id == task.responsible_id

    def is_project_owner(self, project):
        return self.id == project.administrative_responsible_id or self.id == project.technical_responsible_id

    def encodeField(self, a_field):
        return base64.b64encode(a_field.encode())

    def decodeField(self, a_field):
        return base64.b64decode(a_field.encode())


class ContinuousActivity(BusinessModel):
    id = models.AutoField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    started = models.DateField(blank=True, null=True)
    ended = models.DateField(blank=True, null=True)

    responsible = models.ForeignKey(ScrumUser, related_name='continuous_activities', on_delete=models.SET_NULL, db_column='id_scrumuser', blank=True, null=True)
    typeContinuousActivity = models.ForeignKey(ScrumUser, on_delete=models.SET_NULL, db_column='id_typeContinuousActivity', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scrum_continuousactivity'


class Project(BusinessModel):
    id = models.AutoField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    start = models.DateField(blank=True, null=True)
    real_start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    real_end = models.DateField(blank=True, null=True)

    administrative_responsible = models.ForeignKey(ScrumUser, related_name='administrative_responsible', on_delete=models.SET_NULL, db_column='id_scrumuser_administrative', blank=True, null=True)
    technical_responsible = models.ForeignKey(ScrumUser, on_delete=models.SET_NULL, db_column='id_scrumuser_technical', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scrum_project'

    def is_admin_project(self):
        return self.administrative_responsible.role == "admin" or self.technical_responsible.role == "admin"


class Sprint(BusinessModel):
    id_sprint = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    project = models.ForeignKey(Project, related_name='sprints', on_delete=models.SET_NULL, db_column='id_project', blank=True, null=True)
    responsible = models.ForeignKey(ScrumUser, related_name='sprints', on_delete=models.SET_NULL, db_column='id_scrumuser', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scrum_sprint'


class TypeContinuousActivity(BusinessModel):
    id = models.AutoField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    type = models.IntegerField(blank=True, null=True)

    TYPE_COMMITTEE = 1
    TYPE_MEETING = 2
    TYPE_COLLABORATIVE_WORK = 3
    TYPE_WORKSHOP = 4
    TYPE_CONGRESS_SYMPOSIUM_COLLOQUIUM = 5
    TYPE_EVENT = 6
    TYPE_ABSENCE_FROM_WORK = 7
    TYPE_OTHER = 8

    TYPE_CHOICES = (
        (TYPE_COMMITTEE, 'Comitê'),
        (TYPE_MEETING, 'Reunião'),
        (TYPE_COLLABORATIVE_WORK, 'Trabalho colaborativo'),
        (TYPE_WORKSHOP, 'Workshop/Treinamento'),
        (TYPE_CONGRESS_SYMPOSIUM_COLLOQUIUM, 'Congresso/Simpósio/Colóquio'),
        (TYPE_EVENT, 'Evento'),
        (TYPE_ABSENCE_FROM_WORK, 'Ausência'),
        (TYPE_OTHER, 'Outros'),
    )

    class Meta:
        managed = False
        db_table = 'scrum_typecontinuousactivity'

    @classmethod
    def type_dic(cls):
        dic_values = []
        for tupla in cls.TYPE_CHOICES:
            dicti = {}
            dicti['id'] = tupla[0]
            dicti['dominio'] = tupla[1]
            dic_values.append(dicti)
        return dic_values


class Task(BusinessModel):
    contextclassname = 'tasks'

    STATUS_TODO = 1
    STATUS_IN_PROGRESS = 2
    STATUS_IN_PENDING = 3
    STATUS_DONE = 4
    STATUS_CHOICES = (
        (STATUS_TODO, 'A fazer'),
        (STATUS_IN_PROGRESS, 'Fazendo'),
        (STATUS_IN_PENDING, 'Pendente'),
        (STATUS_DONE, 'Feito'),
    )

    id= models.AutoField(primary_key=True, db_column='id_task' )
    name = models.CharField(max_length=300, blank=True, null=True, unique=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    started = models.DateField(blank=True, null=True)
    due = models.DateField(blank=True, null=True)
    completed = models.DateField(blank=True, null=True)

    sprint = models.ForeignKey(Sprint, related_name='tasks', on_delete=models.SET_NULL, db_column='id_sprint', blank=True, null=True)
    responsible = models.ForeignKey(ScrumUser, related_name='tasks', on_delete=models.CASCADE, db_column='id_scrumuser')
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.SET_NULL, db_column='id_project', blank=True, null=True)
    typeContinuousActivity = models.ForeignKey(TypeContinuousActivity, on_delete=models.SET_NULL, db_column='id_typeContinuousActivity', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scrum_task'

    def __str__(self):
        return self.name

    @classmethod
    def status_dic(cls):
        dic_values = []
        for tupla in cls.STATUS_CHOICES:
            dicti = {
                'id': tupla[0],
                'dominio': tupla[1]
            }
            dic_values.append(dicti)

        return dic_values

    def to_string(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.status is None:
           self.status = Task.STATUS_TODO

        return super(Task, self).save(*args, **kwargs)

    def task_from_admin(self):
        return self.responsible.role == "admin"


class Impediment(BusinessModel):
    contextclassname = 'impediments'
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    created_date = models.DateField(default=datetime.now)
    resolution_date = models.DateField(blank=True)

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='impediments', db_column='id_task')
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, db_column='id_sprint', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scrum_impediment'

    def to_string(self):
        return self.name


class EntryPoint(BusinessModel):
    scrum_user = models.CharField(max_length=200)
    continuous_activity = models.CharField(max_length=200)
    project = models.CharField(max_length=200)
    sprint = models.CharField(max_length=200)
    type_continuous_activity = models.CharField(max_length=200)
    task = models.CharField(max_length=200)
    impediment = models.CharField(max_length=200)