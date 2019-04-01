# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
import base64
import jwt
import sys
from django.contrib.gis.db import models
from hyper_resource.models import BusinessModel
SECRET_KEY = '!ijb)p^wxprqdccf7*kxzu6l^&sf%_+w@!$6e#yl^^47i3j0f6asdfg'

class HyperUser(BusinessModel):
    contextclassname = 'user-list'
    name = models.CharField(max_length=100, blank=True, default='')
    user_name = models.CharField(max_length=100, unique=True )
    email = models.CharField(max_length=100, unique=True, null=True)
    password  = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, default='')
    avatar = models.CharField(max_length=200, blank=True, default='', null=True)
    active   = models.NullBooleanField()
    boss = models.ForeignKey('self', db_column='id_boss',on_delete=models.SET_NULL, related_name='subordinates', blank=True, null=True)

    @classmethod
    def jwt_algorithm(cls):
        return 'HS256'

    @classmethod
    def getOneOrNone(cls, a_user_name, password):
        return HyperUser.objects.filter(user_name=a_user_name, password=password).first()

    def getToken(self):
        encoded = jwt.encode({'id': self.id, 'user_name': self.user_name, 'avatar': self.avatar}, SECRET_KEY,
                             algorithm=HyperUser.jwt_algorithm())
        return encoded

    @classmethod
    def login(cls, user_name, password):
        user = HyperUser.getOneOrNone(user_name, password)
        if user is None:
            return None
        a_dict = {}
        a_dict['id'] = user.id
        a_dict['name'] = user.name
        a_dict['user_name'] = user.user_name
        a_dict['avatar'] = user.avatar
        a_dict['token'] = user_name.getToken()
        return a_dict

    @classmethod
    def token_is_ok(cls, a_token):
        try:
            payload = jwt.decode(a_token, SECRET_KEY, algorithm=HyperUser.jwt_algorithm())
            return True
        except jwt.InvalidTokenError:
            return False

    def encodeField(self, a_field):
        return base64.b64encode(a_field.encode())

    def decodeField(self, a_field):
        return base64.b64decode(a_field.encode())

class HyperUserGroup(BusinessModel):
    contextclassname = 'user-group-list'
    name = models.CharField(max_length=100, blank=True, default='')
    type = models.IntegerField(null=False)

    TYPE_ADMINISTRATOR = 1
    TYPE_DEVELOPER = 2
    TYPE_MANAGER = 3
    TYPE_STAFF = 4
    TYPE_USER_REGISTERED = 5
    TYPE_READONLY = 6

    TYPE_CHOICES = (
        (TYPE_ADMINISTRATOR, ('Adminstrador')),
        (TYPE_DEVELOPER, ('Desenvolvedor')),
        (TYPE_MANAGER, ('Gerente')),
        (TYPE_STAFF, ('Funcionário')),
        (TYPE_USER_REGISTERED, ('Usuário')),
        (TYPE_READONLY, ('Usuário de leitura')),
    )


class APIResource(BusinessModel):
    package_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    method_name = models.CharField(max_length=100)
    operation_name = models.CharField(max_length=100, null=True)

class HyperUserGroupAPIResource(BusinessModel):
    active   = models.NullBooleanField()
    user_group = models.ForeignKey(HyperUserGroup, db_column='id_user_group', on_delete=models.SET_NULL, related_name='col_of_user_group_api', blank=True, null=True)
    api_resource = models.ForeignKey(HyperUserGroup, db_column='id_api_resource', on_delete=models.SET_NULL, blank=True, null=True)