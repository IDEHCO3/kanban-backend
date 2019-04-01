import json
from unittest import skip

import requests
from django.test import TestCase, SimpleTestCase
import datetime
from django.test.runner import DiscoverRunner


from kanban.settings import DATABASES

if not DATABASES['default']['NAME'].endswith("db_test.sqlite3"):
    print("Cerity yourself that you're using the test database")
    exit()

HOST = "http://localhost:8001"

class NoDbTestRunner(DiscoverRunner):
   """ A test runner to test without database creation/deletion """

   def setup_databases(self, **kwargs):
     pass

   def teardown_databases(self, old_config, **kwargs):
     pass

ADMIN_AUTH = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhZG1pbiIsImF2YXRhciI6IiIsImlkIjozMX0.YSoZxCMa-JNnxFi_sxTYe0B5asfYutsuG3X_qgePd5M"
DEFAULT_USER_AUTH = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDQsInVzZXJfbmFtZSI6InVzZXJfdGVzdCIsImF2YXRhciI6IiJ9.WkRj5ZO8crRHOmO8Z8-fT9SOzZ8wRIRJxtGijCkSFvU"
INVALID_AUTH = "Bearer eyJ0eXAiOiJKV1QiLCJhbGcOiJIUzI1NiJ9.eyJpZCI6NDQsInVzZXJfbmFtZSI6InVzZXJfdGVzdCIsImF2YXRhciI6IiJ9.WkRj5ZO8crRHOmO8Z8-fT9SOzZ8wRIRJxtGijCkSFvU"


#python manage.py test scrum.tests.ScrumUserDetailTest --testrunner=scrum.tests.NoDbTestRunner
class ScrumUserDetailTest(SimpleTestCase):
    def setUp(self):
        self.uri_sctum_user_list = HOST + "/scrum-list/user-list/"

        self.uri_user_for_edit = HOST + "/scrum-list/user-list/45"
        self.user_for_edit_auth = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDUsInVzZXJfbmFtZSI6InVzZXJfZWRpdF90ZXN0IiwiYXZhdGFyIjoiIn0.s__SQf1OxKcHxOCDdW7LwX0a2rEW-v2zwgU9QtjfdsU"

        self.uri_admin_for_edit = HOST + "/scrum-list/user-list/46"

        self.uri_user_for_delete = HOST + "/scrum-list/user-list/filter/user_name/eq/user_delete_test"
        self.uri_admin_for_delete = HOST + "/scrum-list/user-list/filter/user_name/eq/admin_delete_test"

    def aux_get_edit_user_setted_to_admin(self):
        return json.dumps(
            {
                #"user_name": "user_" + str(datetime.datetime.now().microsecond),
                #"password": str(datetime.datetime.now().microsecond)
                "id": 45,
                "role": "admin",
                "password": "ae",
                "user_name": "adfase"
            }
        )

    def aux_get_edit_admin_setted_to_default_user(self):
        return json.dumps(
            {
                #"user_name": "user_" + str(datetime.datetime.now().microsecond),
                #"password": str(datetime.datetime.now().microsecond)
                "id": 46,
                "role": "user",
                "password": "ae",
                "user_name": "adfase"
            }
        )

    def aux_restore_default_user_from_db(self):
        return requests.put(self.uri_user_for_edit, json.dumps({"id": 45, "role": "user", "password": "ae", "user_name": "adfase"}), headers={"Authorization": ADMIN_AUTH})

    def aux_restore_admin_user_from_db(self):
        return requests.put(self.uri_admin_for_edit,  json.dumps({"id": 46, "role": "admin", "user_name": "asdasd", "password": "65464"}), headers={"Authorization": ADMIN_AUTH})


    # set default user to admin
    def test_set_user_to_admin_without_token(self):
        user_to_admin = self.aux_get_edit_user_setted_to_admin()
        response = requests.put(self.uri_user_for_edit, user_to_admin)
        self.assertEquals(response.status_code, 401)

    def test_set_user_to_admin_with_invalid_token(self):
        user_to_admin = self.aux_get_edit_user_setted_to_admin()
        response = requests.put(self.uri_user_for_edit, user_to_admin, headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_user_to_admin_with_default_user_token_self_account(self):
        user_to_admin = self.aux_get_edit_user_setted_to_admin()
        response = requests.put(self.uri_user_for_edit, user_to_admin, headers={"Authorization": self.user_for_edit_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_user_to_admin_with_default_user_token_another_user_account(self):
        '''
        User 44 trying to change user 45
        '''
        user_to_admin = self.aux_get_edit_user_setted_to_admin()
        response = requests.put(self.uri_user_for_edit, user_to_admin, headers={"Authorization": DEFAULT_USER_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_user_to_admin_with_admin_token(self):
        user_to_admin = self.aux_get_edit_user_setted_to_admin()
        response = requests.put(self.uri_user_for_edit, user_to_admin, headers={"Authorization": ADMIN_AUTH})
        self.assertEquals(response.status_code, 204)

        clear_db = self.aux_restore_default_user_from_db()
        self.assertEquals(clear_db.status_code, 204)


    # set admin user to defalt user (this can't be done whatever is the token)
    def test_set_admin_to_default_user_without_token(self):
        admin_to_user = self.aux_get_edit_admin_setted_to_default_user()
        response = requests.put(self.uri_admin_for_edit, admin_to_user)
        self.assertEquals(response.status_code, 401)

    def test_set_admin_to_default_user_with_invalid_token(self):
        admin_to_user = self.aux_get_edit_admin_setted_to_default_user()
        response = requests.put(self.uri_admin_for_edit, admin_to_user, headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_admin_to_default_user_with_default_user_token(self):
        admin_to_user = self.aux_get_edit_admin_setted_to_default_user()
        response = requests.put(self.uri_admin_for_edit, admin_to_user, headers={"Authorization": DEFAULT_USER_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_admin_to_default_user_with_admin_token(self):
        admin_to_user = self.aux_get_edit_admin_setted_to_default_user()
        response = requests.put(self.uri_admin_for_edit, admin_to_user, headers={"Authorization": ADMIN_AUTH})
        self.assertEquals(response.status_code, 204)

        clear_db = self.aux_restore_admin_user_from_db()
        self.assertEquals(clear_db.status_code, 204)


    def aux_restore_default_user_to_delete(self):
        return requests.post(HOST + "/scrum-list/user-list/register/",
            json.dumps({
                "user_name": "user_delete_test",
                "password": "user_delete_test",
                "description": "User for deletion tests",
                "role": "user"
            })
                             )

    def aux_restore_admin_to_delete(self):
        return requests.post(HOST + "/scrum-list/user-list/register/",
            json.dumps({
                "user_name": "admin_delete_test",
                "password": "admin_delete_test",
                "role": "admin",
                "description": "Admin for deletion tests"
            }),
            headers={"Authorization": ADMIN_AUTH}
        )

    def aux_get_default_user_to_delete_dict(self):
        #return dict( json.loads( requests.get("http://localhost:8001/scrum-list/user-list/filter/user_name/eq/user_delete_test").text ) )[0]
        response = requests.get(self.uri_user_for_delete, headers={"Authorization": ADMIN_AUTH})
        return (json.loads( response.text ))[0]

    def aux_get_admin_user_to_delete_dict(self):
        #return dict( json.loads( requests.get("http://localhost:8001/scrum-list/user-list/filter/user_name/eq/admin_delete_test").text ) )[0]
        response = requests.get(self.uri_admin_for_delete, headers={"Authorization": ADMIN_AUTH})
        return (json.loads( response.text ))[0]

    def aux_get_default_user_authorization(self):
        response = requests.post("http://localhost:8001/scrum-list/user-list/login/", json.dumps({"user_name": "user_delete_test", "password": "user_delete_test"}) )
        return "Bearer " + response.headers["x-access-token"]

    def aux_get_admin_user_authorization(self):
        response = requests.post("http://localhost:8001/scrum-list/user-list/login/", json.dumps({"user_name": "admin_delete_test", "password": "admin_delete_test"}) )
        return "Bearer " + response.headers["x-access-token"]

    # delete default user
    def test_delete_default_user_without_token(self):
        default_user_dict = self.aux_get_default_user_to_delete_dict()
        response = requests.delete(self.uri_sctum_user_list + str(default_user_dict["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_with_invalid_token(self):
        default_user_dict = self.aux_get_default_user_to_delete_dict()
        response = requests.delete(self.uri_sctum_user_list + str(default_user_dict["id"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_with_default_user_token_self_account(self):
        default_user_dict = self.aux_get_default_user_to_delete_dict()
        default_user_owner_auth = self.aux_get_default_user_authorization()

        response = requests.delete(self.uri_sctum_user_list + str(default_user_dict["id"]), headers={"Authorization": default_user_owner_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_with_default_user_token_another_user_account(self):
        default_user_dict = self.aux_get_default_user_to_delete_dict()
        response = requests.delete(self.uri_sctum_user_list + str(default_user_dict["id"]), headers={"Authorization": DEFAULT_USER_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_with_admin_token(self):
        default_user_dict = self.aux_get_default_user_to_delete_dict()
        response = requests.delete(self.uri_sctum_user_list + str(default_user_dict["id"]), headers={"Authorization": ADMIN_AUTH})
        self.assertEquals(response.status_code, 204)

        restore_response = self.aux_restore_default_user_to_delete()
        self.assertEquals(restore_response.status_code, 201)

    # delete admin user
    def test_delete_admin_user_without_token(self):
        admin_user_dict = self.aux_get_admin_user_to_delete_dict()
        response = requests.delete(self.uri_sctum_user_list + str(admin_user_dict["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_with_invalid_token(self):
        admin_user_dict = self.aux_get_admin_user_to_delete_dict()
        response = requests.delete(self.uri_sctum_user_list + str(admin_user_dict["id"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_with_default_user_token(self):
        admin_user_dict = self.aux_get_admin_user_to_delete_dict()
        response = requests.delete(self.uri_sctum_user_list + str(admin_user_dict["id"]), headers={"Authorization": DEFAULT_USER_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_with_admin_user_token(self):
        admin_user_dict = self.aux_get_admin_user_to_delete_dict()
        response = requests.delete(self.uri_sctum_user_list + str(admin_user_dict["id"]), headers={"Authorization": ADMIN_AUTH})
        self.assertEquals(response.status_code, 401)

#python manage.py test scrum.tests.ScrumUserRegisterTest --testrunner=scrum.tests.NoDbTestRunner
class ScrumUserRegisterTest(SimpleTestCase):
    def setUp(self):
        self.register_base_uri = HOST + "/scrum-list/user-list/register/"
        #self.default_admin_auth = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhZG1pbiIsImF2YXRhciI6IiIsImlkIjozMX0.YSoZxCMa-JNnxFi_sxTYe0B5asfYutsuG3X_qgePd5M"
        #self.default_user_auth = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDQsInVzZXJfbmFtZSI6InVzZXJfdGVzdCIsImF2YXRhciI6IiJ9.WkRj5ZO8crRHOmO8Z8-fT9SOzZ8wRIRJxtGijCkSFvU"

    def aux_create_default_user(self):
        user_name_num = str(datetime.datetime.now().microsecond)
        user_name_pass = str(datetime.datetime.now().microsecond)
        #print("-----------------------------------------------------------------")
        #print("NEW USER: user_" + user_name_num + " | password " + user_name_pass)
        #print("-----------------------------------------------------------------\n")
        return json.dumps({"user_name": "user_" + user_name_num, "password": user_name_pass})

    def aux_create_admin_user(self):
        return json.dumps({
            "user_name": "user_" + str(datetime.datetime.now().microsecond),
            "password": str(datetime.datetime.now().microsecond),
            "role": "admin"
        })

    def aux_remove_created_user_from_db(self, response):
        # clear database from the user that test just created
        content_location_url = HOST + "/scrum-list/user-list/" + response.headers["Content-Location"].split("/")[-1]
        return requests.delete(content_location_url, headers={"Authorization": ADMIN_AUTH})
        #delete_response = requests.delete(HOST + content_location_url, headers={"Authorization": self.default_admin_auth})
        #self.assertEquals(delete_response.status_code, 204)

    def test_register_default_user_without_token(self):
        user_json = self.aux_create_default_user()
        response = requests.post(self.register_base_uri, data=user_json, headers={"Content-Type": "application/json"})
        self.assertEquals(response.status_code, 201)
        self.assertIn("x-access-token", response.headers.keys())

        delete_response = self.aux_remove_created_user_from_db(response)
        self.assertEquals(delete_response.status_code, 204)

    def test_register_default_user_with_invalid_token(self):
        user_json = self.aux_create_default_user()
        response = requests.post(self.register_base_uri, data=user_json, headers={
            "Content-Type": "application/json",
            "Authorization": INVALID_AUTH
        })
        self.assertEquals(response.status_code, 201)
        self.assertIn("x-access-token", response.headers.keys())

        delete_response = self.aux_remove_created_user_from_db(response)
        self.assertEquals(delete_response.status_code, 204)

    def test_register_default_user_with_default_user_token(self):
        user_json = self.aux_create_default_user()
        response = requests.post(self.register_base_uri, data=user_json, headers={
            "Content-Type": "application/json",
            "Authorization": DEFAULT_USER_AUTH
        })
        self.assertEquals(response.status_code, 201)
        self.assertIn("x-access-token", response.headers.keys())

        delete_response = self.aux_remove_created_user_from_db(response)
        self.assertEquals(delete_response.status_code, 204)

    def test_register_default_user_with_admin_user_token(self):
        user_json = self.aux_create_default_user()
        response = requests.post(self.register_base_uri, data=user_json, headers={
            "Content-Type": "application/json",
            "Authorization": ADMIN_AUTH
        })
        self.assertEquals(response.status_code, 201)
        self.assertIn("x-access-token", response.headers.keys())

        delete_response = self.aux_remove_created_user_from_db(response)
        self.assertEquals(delete_response.status_code, 204)

    def test_register_admin_user_without_token(self):
        admin_user_json = self.aux_create_admin_user()
        response = requests.post(self.register_base_uri, data=admin_user_json, headers={
            "Content-Type": "application/json"
        })
        self.assertEquals(response.status_code, 401)
        #self.assertIn("x-access-token", response.headers.keys())

        #self.aux_remove_created_user_from_db(response)

    def test_register_admin_user_with_invalid_token(self):
        admin_user_json = self.aux_create_admin_user()
        response = requests.post(self.register_base_uri, data=admin_user_json, headers={
            "Content-Type": "application/json",
            "Authorization": INVALID_AUTH
        })
        self.assertEquals(response.status_code, 401)

    def test_register_admin_user_with_default_user_token(self):
        admin_user_json = self.aux_create_admin_user()
        response = requests.post(self.register_base_uri, data=admin_user_json, headers={
            "Content-Type": "application/json",
            "Authorization": DEFAULT_USER_AUTH
        })
        self.assertEquals(response.status_code, 401)
        #self.assertIn("x-access-token", response.headers.keys())

        #self.aux_remove_created_user_from_db(response)

    def test_register_admin_user_with_admin_user_token(self):
        admin_user_json = self.aux_create_admin_user()
        response = requests.post(self.register_base_uri, data=admin_user_json, headers={
            "Content-Type": "application/json",
            "Authorization": ADMIN_AUTH
        })
        self.assertEquals(response.status_code, 201)
        self.assertIn("x-access-token", response.headers.keys())

        #delete_response = self.aux_remove_created_user_from_db(response)
        #self.assertEquals(delete_response.status_code, 204)

class ScrumUserLoginTest(SimpleTestCase):
    def setUp(self):
        pass


#python manage.py test scrum.tests.TaskListTest --testrunner=scrum.tests.NoDbTestRunner
class TaskListTest(SimpleTestCase):
    def setUp(self):
        self.tasks_base_uri = HOST + "/scrum-list/task-list"

    '''
    {
        "id": 889,
        "name": "tarefa_editada_1",
        "description": null,
        "status": "1",
        "order": null,
        "started": null,
        "due": null,
        "completed": null,
        "sprint": null,
        "responsible": "http://localhost:8001/scrum-list/user-list/31/",
        "project": null,
        "typeContinuousActivity": null,
        "impediments": [],
        "to_string": "tarefa_editada_1"
    }
    '''

    def aux_create_task_for_default_user(self):
        return json.dumps(
            {
                "name": "task_" + str(datetime.datetime.now().microsecond),
                "responsible": "http://localhost:8001/scrum-list/user-list/44/" # admin user id = 44
            }
        )

    def aux_create_task_for_admin_user(self):
        return json.dumps(
            {
                "name": "task_" + str(datetime.datetime.now().microsecond),
                "responsible": "http://localhost:8001/scrum-list/user-list/31/" # admin user id = 31
            }
        )

    def aux_create_task_for_inexistent_user(self):
        return json.dumps(
            {
                "name": "task_" + str(datetime.datetime.now().microsecond),
                "responsible": "http://localhost:8001/scrum-list/user-list/20/"
            }
        )

    def aux_remove_created_task_from_db(self, response):
        # clear database from the task that test just created
        content_location_url = response.headers["Content-Location"]
        requests.delete(HOST + content_location_url, headers={"Authorization": ADMIN_AUTH})


    def test_list_all_tasks_without_token(self):
        response = requests.get(self.tasks_base_uri)
        self.assertEquals(response.status_code, 401)

    def test_list_all_tasks_with_invalid_token(self):
        response = requests.get(self.tasks_base_uri)
        self.assertEquals(response.status_code, 401)

    def test_list_all_tasks_with_default_user_token(self):
        response = requests.get(self.tasks_base_uri, headers={"Authorization": DEFAULT_USER_AUTH})
        self.assertEquals(response.status_code, 200)

    def test_list_all_tasks_with_admin_token(self):
        response = requests.get(self.tasks_base_uri, headers={"Authorization": ADMIN_AUTH})
        self.assertEquals(response.status_code, 200)


    # create task for defautl user
    def test_create_task_for_default_user_without_token(self):
        task_for_user = self.aux_create_task_for_default_user()
        response = requests.post(self.tasks_base_uri, data=task_for_user, headers={
            "Content-Type": "application/json"
        })
        self.assertEquals(response.status_code, 401)

    def test_create_task_for_default_user_with_invalid_token(self):
        task_for_user = self.aux_create_task_for_default_user()
        response = requests.post(self.tasks_base_uri, data=task_for_user, headers={
            "Content-Type": "application/json",
            "Authorization": INVALID_AUTH
        })
        self.assertEquals(response.status_code, 401)

    def test_create_task_for_default_user_with_default_user_token_self_task(self):
        task_for_user = self.aux_create_task_for_default_user()
        response = requests.post(self.tasks_base_uri, data=task_for_user, headers={
            "Content-Type": "application/json",
            "Authorization": DEFAULT_USER_AUTH
        })
        self.assertEquals(response.status_code, 201)
        self.aux_remove_created_task_from_db(response)

    def test_create_task_for_default_user_with_admin_token(self):
        task_for_user = self.aux_create_task_for_default_user()
        response = requests.post(self.tasks_base_uri, data=task_for_user, headers={
            "Content-Type": "application/json",
            "Authorization": ADMIN_AUTH
        })
        self.assertEquals(response.status_code, 201)
        self.aux_remove_created_task_from_db(response)


    # create task for admin user
    def test_create_task_for_admin_without_token(self):
        task_for_admin = self.aux_create_task_for_admin_user()
        response = requests.post(self.tasks_base_uri, data=task_for_admin, headers={
            "Content-Type": "application/json"
        })
        self.assertEquals(response.status_code, 401)

    def test_create_task_for_admin_with_invalid_token(self):
        task_for_admin = self.aux_create_task_for_admin_user()
        response = requests.post(self.tasks_base_uri, data=task_for_admin, headers={
            "Content-Type": "application/json",
            "Authorization": INVALID_AUTH
        })
        self.assertEquals(response.status_code, 401)

    def test_create_task_for_admin_with_default_user_token(self):
        task_for_admin = self.aux_create_task_for_admin_user()
        response = requests.post(self.tasks_base_uri, data=task_for_admin, headers={
            "Content-Type": "application/json",
            "Authorization": DEFAULT_USER_AUTH
        })
        self.assertEquals(response.status_code, 401)

    def test_create_task_for_admin_with_default_admin_token(self):
        task_for_admin = self.aux_create_task_for_admin_user()
        response = requests.post(self.tasks_base_uri, data=task_for_admin, headers={
            "Content-Type": "application/json",
            "Authorization": ADMIN_AUTH
        })
        self.assertEquals(response.status_code, 201)
        self.aux_remove_created_task_from_db(response)


    # create task for inexistent user
    def test_create_task_for_inexistent_user_without_token(self):
        task_for_inexistent_user = self.aux_create_task_for_inexistent_user()
        response = requests.post(self.tasks_base_uri, data=task_for_inexistent_user, headers={
            "Content-Type": "application/json"
        })
        self.assertEquals(response.status_code, 401)

    def test_create_task_for_inexistent_user_with_invalid_token(self):
        task_for_inexistent_user = self.aux_create_task_for_inexistent_user()
        response = requests.post(self.tasks_base_uri, data=task_for_inexistent_user, headers={
            "Content-Type": "application/json",
            "Authorization": INVALID_AUTH
        })
        self.assertEquals(response.status_code, 401)

    def test_create_task_for_inexistent_user_with_default_user_token(self):
        task_for_inexistent_user = self.aux_create_task_for_inexistent_user()
        response = requests.post(self.tasks_base_uri, data=task_for_inexistent_user, headers={
            "Content-Type": "application/json",
            "Authorization": DEFAULT_USER_AUTH
        })
        self.assertEquals(response.status_code, 401)

    def test_create_task_for_inexistent_user_with_admin_token(self):
        task_for_inexistent_user = self.aux_create_task_for_inexistent_user()
        response = requests.post(self.tasks_base_uri, data=task_for_inexistent_user, headers={
            "Content-Type": "application/json",
            "Authorization": ADMIN_AUTH
        })
        self.assertEquals(response.status_code, 400)

#python manage.py test scrum.tests.TaskDetailTest --testrunner=scrum.tests.NoDbTestRunner
class TaskDetailTest(SimpleTestCase):
    def setUp(self):
        self.uri_task_list = HOST + "/scrum-list/task-list/"
        self.uri_user_register = HOST + "/scrum-list/user-list/register/"

        self.uri_user_task_for_edit = HOST + "/scrum-list/task-list/908"
        self.uri_admin_task_for_edit = HOST + "/scrum-list/task-list/909"
        self.uri_alternativa_user_task_for_edit = HOST + "/scrum-list/task-list/910"

        self.uri_default_user = HOST + "/scrum-list/user-list/45"
        # token from user 45
        self.default_user_auth = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdmF0YXIiOiIiLCJpZCI6NDUsInVzZXJfbmFtZSI6InVzZXJfZWRpdF90ZXN0In0.XXKiughzkh2tWNwqokwJo6y-5GIR7wqq5uEXxOQdz_o"

        self.uri_default_user_alternative = HOST + "/scrum-list/user-list/44"
        self.uri_admin = HOST + "/scrum-list/user-list/46"

        self.uri_admin_for_test_task = HOST + "/scrum-list/user-list/filter/user_name/eq/admin_user_to_test_tasks"
        self.uri_admin_task = HOST + "/scrum-list/task-list/filter/name/eq/admin_user_task"
        self.aux_create_admin_user_to_test_tasks()
        self.aux_create_task_for_admin_user()
        self.uri_alternative_admin_for_test_task = HOST + "/scrum-list/user-list/filter/user_name/eq/alternative_admin_user_to_test_tasks"
        self.uri_alternative_admin_task = HOST + "/scrum-list/task-list/filter/name/eq/alternative_admin_user_task"
        self.aux_create_alternative_admin_user_to_test_tasks()
        self.aux_create_task_for_alternative_admin_user()
        self.uri_user_for_test_task = HOST + "/scrum-list/user-list/filter/user_name/eq/default_user_to_test_tasks"
        self.uri_user_task = HOST + "/scrum-list/task-list/filter/name/eq/default_user_task"
        self.aux_create_default_user_to_test_tasks()
        self.aux_create_task_for_default_user()
        self.uri_alternative_user_for_test_task = HOST + "/scrum-list/user-list/filter/user_name/eq/alternative_user_to_test_tasks"
        self.uri_alternative_user_task = HOST + "/scrum-list/task-list/filter/name/eq/alternative_user_task"
        self.aux_create_alternative_default_user_to_test_tasks()
        self.aux_create_task_for_alternative_default_user()

    '''
    {
        "id": 889,
        "name": "tarefa_editada_1",
        "description": null,
        "status": "1",
        "order": null,
        "started": null,
        "due": null,
        "completed": null,
        "sprint": null,
        "responsible": "http://localhost:8001/scrum-list/user-list/31/",
        "project": null,
        "typeContinuousActivity": null,
        "impediments": [],
        "to_string": "tarefa_editada_1"
    }
    '''
    def aux_get_edit_task_setted_to_admin(self):
        return json.dumps({"id": 908, "name": "default_user_task_edit", "responsible": self.uri_admin})

    def aux_get_edit_task_setted_to_default_user(self):
        return json.dumps({"id": 909, "name": "admin_task", "responsible": self.uri_default_user})

    def aux_get_edit_task_setted_to_default_user_alternative(self):
        '''
        Setting task from default user 44 to default user 45
        '''
        return json.dumps({"id": 910, "name": "default_user_task_edit2", "responsible": self.uri_default_user})

    def aux_restore_default_user_task(self):
        return requests.put(
            self.uri_user_task_for_edit,
            json.dumps({"id": 908, "name": "default_user_task_edit", "responsible": "http://localhost:8001/scrum-list/user-list/45"}),
            headers={"Authorization": ADMIN_AUTH}
        )

    def aux_restore_admin_task(self):
        return requests.put(
            self.uri_admin_task_for_edit,
            json.dumps({"id": 909, "name": "admin_task", "responsible": "http://localhost:8001/scrum-list/user-list/46"}),
            headers={"Authorization": ADMIN_AUTH}
        )


    def test_set_task_to_default_user_without_token(self):
        admin_task_setted_to_default_user = self.aux_get_edit_task_setted_to_default_user()
        response = requests.put(self.uri_admin_task_for_edit, admin_task_setted_to_default_user)
        self.assertEquals(response.status_code, 401)

    def test_set_task_to_default_user_with_invalid_token(self):
        admin_task_setted_to_default_user = self.aux_get_edit_task_setted_to_default_user()
        response = requests.put(self.uri_admin_task_for_edit, admin_task_setted_to_default_user, headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_task_to_default_user_with_default_user_token_self_account(self):
        admin_task_setted_to_default_user = self.aux_get_edit_task_setted_to_default_user()
        response = requests.put(self.uri_admin_task_for_edit, admin_task_setted_to_default_user, headers={"Authorization": self.default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_task_to_default_user_with_default_user_token_another_user_account(self):
        default_user_task_setted_to_another_default_user = self.aux_get_edit_task_setted_to_default_user_alternative()
        response = requests.put(self.uri_alternativa_user_task_for_edit, default_user_task_setted_to_another_default_user, headers={"Authorization": self.default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_task_to_default_user_with_admin_user_token(self):
        admin_task_setted_to_default_user = self.aux_get_edit_task_setted_to_default_user()
        response = requests.put(self.uri_admin_task_for_edit, admin_task_setted_to_default_user, headers={"Authorization": ADMIN_AUTH})
        self.assertEquals(response.status_code, 204)

        restore_response = self.aux_restore_admin_task()
        self.assertEquals(restore_response.status_code, 204)


    def test_set_task_to_admin_user_without_token(self):
        user_task_setted_to_admin = self.aux_get_edit_task_setted_to_admin()
        response = requests.put(self.uri_user_task_for_edit, user_task_setted_to_admin)
        self.assertEquals(response.status_code, 401)

    def test_set_task_to_admin_user_with_invalid_token(self):
        user_task_setted_to_admin = self.aux_get_edit_task_setted_to_admin()
        response = requests.put(self.uri_user_task_for_edit, user_task_setted_to_admin, headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_task_to_admin_user_with_default_user_token(self):
        '''
        Default user 45 is trying to transfer the task to admin user
        '''
        user_task_setted_to_admin = self.aux_get_edit_task_setted_to_admin()
        response = requests.put(self.uri_user_task_for_edit, user_task_setted_to_admin, headers={"Authorization": self.default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_task_to_admin_user_with_admin_user_token(self):
        user_task_setted_to_admin = self.aux_get_edit_task_setted_to_admin()
        response = requests.put(self.uri_user_task_for_edit, user_task_setted_to_admin, headers={"Authorization": ADMIN_AUTH})
        self.assertEquals(response.status_code, 204)

        restore_response = self.aux_restore_default_user_task()
        self.assertEquals(restore_response.status_code, 204)


    # delete task tests
    def aux_create_admin_user_to_test_tasks(self):
        data = {
            "user_name": "admin_user_to_test_tasks",
            "password": "admin_user_to_test_tasks",
            "role": "admin"
        }
        requests.post(self.uri_user_register, json.dumps(data),
                          headers={
                              "Authorization": ADMIN_AUTH,
                              "Content-Type": "application/json"
                          }
                      )

    def aux_create_alternative_admin_user_to_test_tasks(self):
        data = {
            "user_name": "alternative_admin_user_to_test_tasks",
            "password": "alternative_admin_user_to_test_tasks",
            "role": "admin"
        }
        requests.post(self.uri_user_register, json.dumps(data),
                          headers={
                              "Authorization": ADMIN_AUTH,
                              "Content-Type": "application/json"
                          }
                      )

    def aux_create_default_user_to_test_tasks(self):
        data = {
            "user_name": "default_user_to_test_tasks",
            "password": "default_user_to_test_tasks",
            "role": "user"
        }
        requests.post(self.uri_user_register, json.dumps(data),
                          headers={
                              "Authorization": ADMIN_AUTH,
                              "Content-Type": "application/json"
                          }
                      )

    def aux_create_alternative_default_user_to_test_tasks(self):
        data = {
            "user_name": "alternative_user_to_test_tasks",
            "password": "alternative_user_to_test_tasks",
            "role": "user"
        }
        requests.post(self.uri_user_register, json.dumps(data),
                          headers={
                              "Authorization": ADMIN_AUTH,
                              "Content-Type": "application/json"
                          }
                      )


    def aux_get_admin_user_to_test_tasks_dict(self):
        response = requests.get(self.uri_admin_for_test_task, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]

    def aux_get_alternative_admin_user_to_test_tasks_dict(self):
        response = requests.get(self.uri_alternative_admin_for_test_task, headers={"Authorization": ADMIN_AUTH})
        return (json.loads( response.text ))[0]

    def aux_get_default_user_to_test_tasks_dict(self):
        response = requests.get(self.uri_user_for_test_task, headers={"Authorization": ADMIN_AUTH})
        return (json.loads( response.text ))[0]

    def aux_get_alternative_user_to_test_tasks_dict(self):
        response = requests.get(self.uri_alternative_user_for_test_task, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]


    def aux_get_admin_user_authorization(self):
        response = requests.post("http://localhost:8001/scrum-list/user-list/login/", json.dumps({"user_name": "admin_user_to_test_tasks", "password": "admin_user_to_test_tasks"}) )
        return "Bearer " + response.headers["x-access-token"]

    def aux_get_alternative_admin_user_authorization(self):
        response = requests.post("http://localhost:8001/scrum-list/user-list/login/", json.dumps({"user_name": "alternative_admin_user_to_test_tasks", "password": "alternative_admin_user_to_test_tasks"}) )
        return "Bearer " + response.headers["x-access-token"]

    def aux_get_default_user_authorization(self):
        response = requests.post("http://localhost:8001/scrum-list/user-list/login/", json.dumps({"user_name": "default_user_to_test_tasks", "password": "default_user_to_test_tasks"}) )
        return "Bearer " + response.headers["x-access-token"]

    def aux_get_alternative_default_user_authorization(self):
        response = requests.post("http://localhost:8001/scrum-list/user-list/login/", json.dumps({"user_name": "alternative_user_to_test_tasks", "password": "alternative_user_to_test_tasks"}) )
        return "Bearer " + response.headers["x-access-token"]


    def aux_create_task_for_admin_user(self):
        admin_user_id = self.aux_get_admin_user_to_test_tasks_dict()["id"]
        admin_user_auth = self.aux_get_admin_user_authorization()
        data = {
            "name": "admin_user_task",
            "responsible": "http://localhost:8001/scrum-list/user-list/" + str(admin_user_id)
        }
        return requests.post(self.uri_task_list, json.dumps(data),
                             headers={"Authorization": admin_user_auth, "Content-Type": "application/json"})

    def aux_create_task_for_alternative_admin_user(self):
        alternative_admin_user_id = self.aux_get_alternative_admin_user_to_test_tasks_dict()["id"]
        alternative_admin_user_auth = self.aux_get_alternative_admin_user_authorization()
        data = {
            "name": "alternative_admin_user_task",
            "responsible": "http://localhost:8001/scrum-list/user-list/" + str(alternative_admin_user_id)
        }
        return requests.post(self.uri_task_list, json.dumps(data),
                             headers={"Authorization": alternative_admin_user_auth, "Content-Type": "application/json"})

    def aux_create_task_for_default_user(self):
        default_user_id = self.aux_get_default_user_to_test_tasks_dict()["id"]
        default_user_auth = self.aux_get_default_user_authorization()
        data = {
            "name": "default_user_task",
            "responsible": "http://localhost:8001/scrum-list/user-list/" + str(default_user_id)
        }
        return requests.post(self.uri_task_list, json.dumps(data),
                             headers={"Authorization": default_user_auth, "Content-Type": "application/json"})

    def aux_create_task_for_alternative_default_user(self):
        alternative_user_id = self.aux_get_alternative_user_to_test_tasks_dict()["id"]
        alternative_user_auth = self.aux_get_alternative_default_user_authorization()
        data = {
            "name": "alternative_user_task",
            "responsible": "http://localhost:8001/scrum-list/user-list/" + str(alternative_user_id)
        }
        return requests.post(self.uri_task_list, json.dumps(data),
                             headers={"Authorization": alternative_user_auth, "Content-Type": "application/json"})

    def aux_get_task_of_admin_user_dict(self):
        response = requests.get(self.uri_admin_task, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]

    def aux_get_task_of_alternative_admin_user_dict(self):
        response = requests.get(self.uri_alternative_admin_task, headers={"Authorization": ADMIN_AUTH})
        return (json.loads( response.text ))[0]

    def aux_get_task_of_default_user_dict(self):
        response = requests.get(self.uri_user_task, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]

    def aux_get_task_of_alternative_default_user_dict(self):
        response = requests.get(self.uri_alternative_user_task, headers={"Authorization": ADMIN_AUTH})
        return (json.loads( response.text ))[0]


    def test_delete_default_user_task_without_token(self):
        response = requests.delete(self.uri_task_list + str(self.aux_get_task_of_default_user_dict()["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_task_with_invalid_token(self):
        response = requests.delete(self.uri_task_list + str(self.aux_get_task_of_default_user_dict()["id"]),
                                   headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_task_with_default_user_token_self_task(self):
        response = requests.delete(self.uri_task_list + str(self.aux_get_task_of_default_user_dict()["id"]),
                                   headers={"Authorization": self.aux_get_default_user_authorization()})
        self.assertEquals(response.status_code, 204)

        #restoring task
        restore_response = self.aux_create_task_for_default_user()
        self.assertEquals(restore_response.status_code, 201)

    def test_delete_default_user_task_with_default_user_token_another_user_task(self):
        '''
        Alternative dafault user trying to delete dafault user task
        '''
        response = requests.delete(self.uri_task_list + str(self.aux_get_task_of_default_user_dict()["id"]),
                                   headers={"Authorization": self.aux_get_alternative_default_user_authorization()})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_task_with_admin_user_token(self):
        '''
        Admin dafault user trying to delete dafault user task
        '''
        response = requests.delete(self.uri_task_list + str(self.aux_get_task_of_default_user_dict()["id"]),
                                   headers={"Authorization": self.aux_get_admin_user_authorization()})
        self.assertEquals(response.status_code, 204)

        #restoring task
        restore_response = self.aux_create_task_for_default_user()
        self.assertEquals(restore_response.status_code, 201)


    def test_delete_admin_user_task_without_token(self):
        response = requests.delete(self.uri_task_list + str(self.aux_get_task_of_admin_user_dict()["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_task_with_invalid_token(self):
        response = requests.delete(self.uri_task_list + str(self.aux_get_task_of_admin_user_dict()["id"]),
                                   headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_task_with_default_user_token(self):
        '''
        Default user trying to delete admin task
        '''
        response = requests.delete(self.uri_task_list + str(self.aux_get_task_of_admin_user_dict()["id"]),
                                   headers={"Authorization": self.aux_get_default_user_authorization()})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_task_with_admin_user_token_self_task(self):
        response = requests.delete(self.uri_task_list + str(self.aux_get_task_of_admin_user_dict()["id"]),
                                   headers={"Authorization": self.aux_get_admin_user_authorization()})
        self.assertEquals(response.status_code, 204)

        restore_response = self.aux_create_task_for_admin_user()
        self.assertEquals(restore_response.status_code, 201)

    def test_delete_admin_user_task_with_admin_user_token_another_admin_task(self):
        '''
        Alternative admin user trying to delete admin task
        '''
        response = requests.delete(self.uri_task_list + str(self.aux_get_task_of_admin_user_dict()["id"]),
                                   headers={"Authorization": self.aux_get_alternative_admin_user_authorization()})
        self.assertEquals(response.status_code, 401)


class ProjectListTest(SimpleTestCase):
    def setUp(self):
        pass

    def test_list_all_projects_without_token(self):
        pass

    def test_list_all_projects_with_invalid(self):
        pass

    def test_list_all_projects_with_default_user_token(self):
        pass

    def test_list_all_projects_with_admin_token(self):
        pass


    def test_create_project_for_default_user_without_token(self):
        pass

    def test_create_project_for_default_user_with_invalid_token(self):
        pass

    def test_create_project_for_default_user_with_default_user_token_self_account(self):
        ''' Administrative responsible: default user (self account) | technical responsable: default user (self account) '''
        pass

    def test_create_project_for_default_user_with_defallt_user_token_another_account(self):
        ''' Administrative responsible: default user (self account) | technical responsable: default user (another user account) '''
        pass

    def test_create_project_for_default_user_with_admin_user_token(self):
        pass


    def test_create_project_for_admin_user_without_token(self):
        pass

    def test_create_project_for_admin_user_with_invalid_token(self):
        pass

    def test_create_project_for_admin_user_with_default_user_token(self):
        pass

    def test_create_project_for_admin_user_with_admin_user_token_self_account(self):
        ''' Administrative responsible: admin user (self account) | technical responsable: admin user (another user account) '''
        pass

    def test_create_project_for_admin_user_with_admin_user_token_another_admin_account(self):
        ''' Administrative responsible: admin user (self account) | technical responsable: default user (another admin user account) '''
        pass

#python manage.py test scrum.tests.ProjectDetailTest --testrunner=scrum.tests.NoDbTestRunner
class ProjectDetailTest(SimpleTestCase):
    def setUp(self):
        self.url_user_register = HOST + "/scrum-list/user-list/register/"
        self.url_project_list = HOST + "/scrum-list/project-list/"
        self.url_user_login = HOST + "/scrum-list/user-list/login/"

        self.aux_create_admin_to_test_project()
        self.aux_create_default_user_to_test_project()
        self.aux_create_alternative_admin_user_to_test_project()
        self.aux_create_alternative_user_to_test_project()

        self.aux_create_project_to_admin_user()
        self.aux_create_project_to_default_user()
        self.aux_create_project_to_alternative_admin()
        self.aux_create_project_to_alternative_user()


    #@skip("This isn't a test")
    def aux_create_admin_to_test_project(self):
        data = json.dumps({
            "user_name": "admin_user_to_test_project",
            "password": "admin_user_to_test_project",
            "role": "admin"
        })
        requests.post(self.url_user_register, data, headers={"Authorization": ADMIN_AUTH, "Content-Type": "application/json"})

    #@skip("This isn't a test")
    def aux_create_default_user_to_test_project(self):
        data = json.dumps({
            "user_name": "default_user_to_test_project",
            "password": "default_user_to_test_project",
        })
        requests.post(self.url_user_register, data, headers={"Authorization": ADMIN_AUTH, "Content-Type": "application/json"})

    #@skip("This isn't a test")
    def aux_create_alternative_admin_user_to_test_project(self):
        data = json.dumps({
            "user_name": "alternative_admin_user_to_test_project",
            "password": "alternative_admin_user_to_test_project",
            "role": "admin"
        })
        requests.post(self.url_user_register, data, headers={"Authorization": ADMIN_AUTH,"Content-Type": "application/json"})

    #@skip("This isn't a test")
    def aux_create_alternative_user_to_test_project(self):
        data = json.dumps({
            "user_name": "alternative_user_to_test_project",
            "password": "alternative_user_to_test_project",
        })
        requests.post(self.url_user_register, data, headers={"Authorization": ADMIN_AUTH, "Content-Type": "application/json"})


    #@skip("This isn't a test")
    def aux_get_admin_user_to_test_project_dict(self):
        url = HOST + "/scrum-list/user-list/filter/user_name/eq/admin_user_to_test_project"
        response = requests.get(url, headers={"Authorization": ADMIN_AUTH})
        #print("STATUS:"+ str(response.status_code))
        return json.loads( response.text )[0]

    #@skip("This isn't a test")
    def aux_get_alternative_admin_user_to_test_project_dict(self):
        url = HOST + "/scrum-list/user-list/filter/user_name/eq/alternative_admin_user_to_test_project"
        response = requests.get(url, headers={"Authorization": ADMIN_AUTH})
        return (json.loads( response.text ))[0]

    #@skip("This isn't a test")
    def aux_get_default_user_to_test_project_dict(self):
        url = HOST + "/scrum-list/user-list/filter/user_name/eq/default_user_to_test_project"
        response = requests.get(url, headers={"Authorization": ADMIN_AUTH})
        return (json.loads( response.text ))[0]

    #@skip("This isn't a test")
    def aux_get_alternative_user_to_test_project_dict(self):
        url = HOST + "/scrum-list/user-list/filter/user_name/eq/alternative_user_to_test_project"
        response = requests.get(url, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]


    #@skip("This isn't a test")
    def aux_get_admin_user_authorization(self):
        response = requests.post(self.url_user_login, json.dumps({"user_name": "admin_user_to_test_project", "password": "admin_user_to_test_project"}) )
        return "Bearer " + response.headers["x-access-token"]

    #@skip("This isn't a test")
    def aux_get_default_user_authorization(self):
        response = requests.post(self.url_user_login, json.dumps({"user_name": "default_user_to_test_project", "password": "default_user_to_test_project"}) )
        return "Bearer " + response.headers["x-access-token"]

    #@skip("This isn't a test")
    def aux_get_alternative_admin_user_authorization(self):
        response = requests.post(self.url_user_login, json.dumps({"user_name": "alternative_admin_user_to_test_project", "password": "alternative_admin_user_to_test_project"}) )
        return "Bearer " + response.headers["x-access-token"]

    #@skip("This isn't a test")
    def aux_get_alternative_user_authorization(self):
        response = requests.post(self.url_user_login, json.dumps({"user_name": "alternative_user_to_test_project", "password": "alternative_user_to_test_project"}) )
        return "Bearer " + response.headers["x-access-token"]


    #@skip("This isn't a test")
    def aux_create_project_to_admin_user(self):
        user_id = str(self.aux_get_admin_user_to_test_project_dict()["id"])
        user_auth = self.aux_get_admin_user_authorization()
        data = json.dumps({
            "name": "admin_project_to_edit",
            "administrative_responsible": HOST + "/scrum-list/user-list/" + user_id,
            "technical_responsible": HOST + "/scrum-list/user-list/" + user_id,
        })
        return requests.post(self.url_project_list, data, headers={"Authorization": user_auth, "Content-Type": "application/json"})

    #@skip("This isn't a test")
    def aux_create_project_to_default_user(self):
        user_id = str(self.aux_get_default_user_to_test_project_dict()["id"])
        user_auth = self.aux_get_default_user_authorization()
        data = json.dumps({
            "name": "default_user_project_to_edit",
            "administrative_responsible": HOST + "/scrum-list/user-list/" + user_id,
            "technical_responsible": HOST + "/scrum-list/user-list/" + user_id,
        })
        return requests.post(self.url_project_list, data, headers={"Authorization": user_auth, "Content-Type": "application/json"})

    #@skip("This isn't a test")
    def aux_create_project_to_alternative_admin(self):
        user_id = str(self.aux_get_alternative_admin_user_to_test_project_dict()["id"])
        user_auth = self.aux_get_alternative_admin_user_authorization()
        data = json.dumps({
            "name": "alternative_admin_project_to_edit",
            "administrative_responsible": HOST + "/scrum-list/user-list/" + user_id,
            "technical_responsible": HOST + "/scrum-list/user-list/" + user_id,
        })
        return requests.post(self.url_project_list, data, headers={"Authorization": user_auth, "Content-Type": "application/json"})

    #@skip("This isn't a test")
    def aux_create_project_to_alternative_user(self):
        user_id = str(self.aux_get_alternative_user_to_test_project_dict()["id"])
        user_auth = self.aux_get_alternative_user_authorization()
        data = json.dumps({
            "name": "alternative_user_project_to_adit",
            "administrative_responsible": HOST + "/scrum-list/user-list/" + user_id,
            "technical_responsible": HOST + "/scrum-list/user-list/" + user_id,
        })
        return requests.post(self.url_project_list, data, headers={"Authorization": user_auth, "Content-Type": "application/json"})

    #@skip("This isn't a test")
    def restore_admin_project(self):
        project_id = self.aux_get_admin_project_dict()["id"]
        admin_user_id = self.aux_get_admin_user_to_test_project_dict()["id"]
        data = json.dumps( {
            "id": project_id,
            "name": "admin_project_to_edit",
            "administrative_responsible": HOST + "/scrum-list/user-list/" + str(admin_user_id),
            "technical_responsible": HOST + "/scrum-list/user-list/" + str(admin_user_id),
        } )

        admin_auth = self.aux_get_admin_user_authorization()
        return requests.put(self.url_project_list + str(project_id), data, headers={"Authorization": admin_auth, "Content-Type": "application/json"})

    #@skip("This isn't a test")
    def restore_default_user_project(self):
        project_id = self.aux_get_default_user_project_dict()["id"]
        default_user_id = self.aux_get_default_user_to_test_project_dict()["id"]
        data = json.dumps( {
            "id": project_id,
            "name": "default_user_project_to_edit",
            "administrative_responsible": HOST + "/scrum-list/user-list/" + str(default_user_id),
            "technical_responsible": HOST + "/scrum-list/user-list/" + str(default_user_id),
        } )

        default_user_auth = self.aux_get_default_user_authorization()
        return requests.put(self.url_project_list + str(project_id), data, headers={"Authorization": ADMIN_AUTH, "Content-Type": "application/json"})


    #@skip("This isn't a test")
    def aux_get_admin_project_dict(self):
        response = requests.get(self.url_project_list + "filter/name/eq/admin_project_to_edit", headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]

    #@skip("This isn't a test")
    def aux_get_default_user_project_dict(self):
        response = requests.get(self.url_project_list + "filter/name/eq/default_user_project_to_edit", headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]

    #@skip("This isn't a test")
    def aux_get_alternative_admin_project_dict(self):
        response = requests.get(self.url_project_list + "filter/name/eq/alternative_admin_project_to_edit", headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]

    #@skip("This isn't a test")
    def aux_get_alternative_user_project_dict(self):
        response = requests.get(self.url_project_list + "filter/name/eq/alternative_user_project_to_adit", headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]


    #@skip("This isn't a test")
    def aux_get_admin_project_setted_to_default_user_project_dict(self):
        project_id = str(self.aux_get_admin_project_dict()["id"])
        default_user_id = self.aux_get_default_user_to_test_project_dict()["id"]
        return {
            "id": project_id,
            "name": "admin_project_to_edit",
            "administrative_responsible": HOST + "/scrum-list/user-list/" + str(default_user_id),
            "technical_responsible": HOST + "/scrum-list/user-list/" + str(default_user_id),
        }

    #@skip("This isn't a test")
    def aux_get_admin_project_setted_to_alternative_user_project_dict(self):
        project_id = str(self.aux_get_admin_project_dict()["id"])
        alternative_user_id = self.aux_get_alternative_user_to_test_project_dict()["id"]
        return {
            "id": project_id,
            "name": "admin_project_to_edit",
            "administrative_responsible": HOST + "/scrum-list/user-list/" + str(alternative_user_id),
            "technical_responsible": HOST + "/scrum-list/user-list/" + str(alternative_user_id),
        }

    #@skip("This isn't a test")
    def aux_get_default_user_project_setted_to_admin_user_project_dict(self):
        project_id = self.aux_get_default_user_project_dict()["id"]
        admin_user_id = self.aux_get_admin_user_to_test_project_dict()["id"]
        return {
            "id": project_id,
            "name": "default_user_project_to_edit",
            "administrative_responsible": HOST + "/scrum-list/user-list/" + str(admin_user_id),
            "technical_responsible": HOST + "/scrum-list/user-list/" + str(admin_user_id),
        }

    #@skip("This isn't a test")
    def aux_get_admin_user_project_setted_to_alternative_admin_project_dict(self):
        project_id = self.aux_get_admin_project_dict()["id"]
        alternative_admin_id = self.aux_get_admin_user_to_test_project_dict()["id"]
        return {
            "id": project_id,
            "name": "default_user_project_to_edit",
            "administrative_responsible": HOST + "/scrum-list/user-list/" + str(alternative_admin_id),
            "technical_responsible": HOST + "/scrum-list/user-list/" + str(alternative_admin_id),
        }


    # Changing project responsable from admin to default user (alternative user is also an defalt user)
    def test_set_project_from_admin_to_default_user_without_token(self):
        admin_proj_set_default_user_dict = self.aux_get_admin_project_setted_to_default_user_project_dict()
        response = requests.put(
            self.url_project_list + str(admin_proj_set_default_user_dict["id"]),
            json.dumps(admin_proj_set_default_user_dict),
            headers={"Content-Type": "application/json"}
        )
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_admin_to_default_user_with_invalid_token(self):
        admin_proj_set_default_user_dict = self.aux_get_admin_project_setted_to_default_user_project_dict()
        response = requests.put(
            self.url_project_list + str(admin_proj_set_default_user_dict["id"]),
            json.dumps(admin_proj_set_default_user_dict),
            headers={"Authorization": INVALID_AUTH, "Content-Type": "application/json"}
        )
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_admin_to_default_user_with_default_user_token(self):
        admin_proj_set_default_user_dict = self.aux_get_admin_project_setted_to_default_user_project_dict()
        default_user_auth = self.aux_get_default_user_authorization()
        response = requests.put(
            self.url_project_list + str(admin_proj_set_default_user_dict["id"]),
            json.dumps(admin_proj_set_default_user_dict),
            headers={"Authorization": default_user_auth, "Content-Type": "application/json"}
        )
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_admin_to_alternative_user_with_default_user_token(self):
        admin_proj_set_alternative_user_dict = self.aux_get_admin_project_setted_to_alternative_user_project_dict()
        default_user_auth = self.aux_get_default_user_authorization()
        response = requests.put(
            self.url_project_list + str(admin_proj_set_alternative_user_dict["id"]),
            json.dumps(admin_proj_set_alternative_user_dict),
            headers={"Authorization": default_user_auth, "Content-Type": "application/json"}
        )
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_admin_to_default_user_with_admin_user_token(self):
        admin_proj_set_default_user_dict = self.aux_get_admin_project_setted_to_default_user_project_dict()
        admin_user_auth = self.aux_get_admin_user_authorization()
        response = requests.put(
            self.url_project_list + str(admin_proj_set_default_user_dict["id"]),
            json.dumps(admin_proj_set_default_user_dict),
            headers={"Authorization": admin_user_auth, "Content-Type": "application/json"}
        )
        self.assertEquals(response.status_code, 204)

        #restore_response = self.restore_admin_project()
        #self.assertEquals(restore_response.status_code, 204)


    # Changing project responsable from default user to admin and alternative admin user
    def test_set_project_from_default_user_to_admin_user_without_token(self):
        default_user_proj_set_admin_user = self.aux_get_default_user_project_setted_to_admin_user_project_dict()
        response = requests.put(
            self.url_project_list + str(default_user_proj_set_admin_user["id"]),
            json.dumps(default_user_proj_set_admin_user),
            headers={"Content-Type": "application/json"}
        )
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_default_user_to_admin_user_with_invalid_token(self):
        default_user_proj_set_admin_user = self.aux_get_default_user_project_setted_to_admin_user_project_dict()
        response = requests.put(
            self.url_project_list + str(default_user_proj_set_admin_user["id"]),
            json.dumps(default_user_proj_set_admin_user),
            headers={"Authorization": INVALID_AUTH, "Content-Type": "application/json"}
        )
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_default_user_to_admin_user_with_default_user_token(self):
        default_user_proj_set_admin_user = self.aux_get_default_user_project_setted_to_admin_user_project_dict()
        response = requests.put(
            self.url_project_list + str(default_user_proj_set_admin_user["id"]),
            json.dumps(default_user_proj_set_admin_user),
            headers={"Authorization": self.aux_get_default_user_authorization(), "Content-Type": "application/json"}
        )
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_default_user_to_admin_user_with_admin_user_token(self):
        default_user_proj_set_admin_user = self.aux_get_default_user_project_setted_to_admin_user_project_dict()
        response = requests.put(
            self.url_project_list + str(default_user_proj_set_admin_user["id"]),
            json.dumps(default_user_proj_set_admin_user),
            headers={"Authorization": self.aux_get_admin_user_authorization(), "Content-Type": "application/json"}
        )
        self.assertEquals(response.status_code, 204)

        #restore_response = self.restore_default_user_project()
        #self.assertEquals(restore_response.status_code, 204)

    def test_set_project_from_admin_user_to_alternative_admin_user_with_admin_token(self):
        admin_user_proj_set_alternative_admin = self.aux_get_admin_user_project_setted_to_alternative_admin_project_dict()
        response = requests.put(
            self.url_project_list + str(admin_user_proj_set_alternative_admin["id"]),
            json.dumps(admin_user_proj_set_alternative_admin),
            headers={"Authorization": self.aux_get_admin_user_authorization(), "Content-Type": "application/json"}
        )
        self.assertEquals(response.status_code, 204)

        #restore_response = self.restore_admin_project()
        #self.assertEquals(restore_response.status_code, 204)


    def test_delete_default_user_project_without_token(self):
        response = requests.delete(self.url_project_list + str(self.aux_get_default_user_project_dict()["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_project_with_invalid_token(self):
        response = requests.delete(self.url_project_list + str(self.aux_get_default_user_project_dict()["id"]),
                                   headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_project_with_default_user_token_self_project(self):
        response = requests.delete(self.url_project_list + str(self.aux_get_default_user_project_dict()["id"]),
                                   headers={"Authorization": self.aux_get_default_user_authorization()})
        self.assertEquals(response.status_code, 204)

        #restoring task
        restore_response = self.aux_create_project_to_default_user()
        self.assertEquals(restore_response.status_code, 201)

    def test_delete_default_user_project_with_default_user_token_another_user_project(self):
        '''
        Alternative dafault user trying to delete dafault user project
        '''
        response = requests.delete(self.url_project_list + str(self.aux_get_default_user_project_dict()["id"]),
                                   headers={"Authorization": self.aux_get_alternative_user_authorization()})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_project_with_admin_user_token(self):
        '''
        Admin dafault user trying to delete dafault user task
        '''
        response = requests.delete(self.url_project_list + str(self.aux_get_default_user_project_dict()["id"]),
                                   headers={"Authorization": self.aux_get_admin_user_authorization()})
        self.assertEquals(response.status_code, 204)

        #restoring project
        restore_response = self.aux_create_project_to_default_user()
        self.assertEquals(restore_response.status_code, 201)


    def test_delete_admin_user_project_without_token(self):
        response = requests.delete(self.url_project_list + str(self.aux_get_admin_project_dict()["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_project_with_invalid_token(self):
        response = requests.delete(self.url_project_list + str(self.aux_get_admin_project_dict()["id"]),
                                   headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_project_with_default_user_token(self):
        '''
        Default user trying to delete admin task
        '''
        response = requests.delete(self.url_project_list + str(self.aux_get_admin_project_dict()["id"]),
                                   headers={"Authorization": self.aux_get_default_user_authorization()})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_project_with_admin_user_token_self_project(self):
        response = requests.delete(self.url_project_list + str(self.aux_get_admin_project_dict()["id"]),
                                   headers={"Authorization": self.aux_get_admin_user_authorization()})
        self.assertEquals(response.status_code, 204)

        restore_response = self.aux_create_project_to_admin_user()
        self.assertEquals(restore_response.status_code, 201)

    def test_delete_admin_user_project_with_admin_user_token_another_admin_project(self):
        '''
        Alternative admin user trying to delete admin project
        '''
        response = requests.delete(self.url_project_list + str(self.aux_get_admin_project_dict()["id"]),
                                   headers={"Authorization": self.aux_get_alternative_admin_user_authorization()})
        self.assertEquals(response.status_code, 204)

        restore_response = self.aux_create_project_to_admin_user()
        self.assertEquals(restore_response.status_code, 201)