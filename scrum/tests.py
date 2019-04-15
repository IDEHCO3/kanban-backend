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

HOST = "http://localhost:80"

class NoDbTestRunner(DiscoverRunner):
   """ A test runner to test without database creation/deletion """

   def setup_databases(self, **kwargs):
     pass

   def teardown_databases(self, old_config, **kwargs):
     pass

ADMIN_AUTH = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhZG1pbiIsImF2YXRhciI6IiIsImlkIjozMX0.YSoZxCMa-JNnxFi_sxTYe0B5asfYutsuG3X_qgePd5M"
DEFAULT_USER_AUTH = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDQsInVzZXJfbmFtZSI6InVzZXJfdGVzdCIsImF2YXRhciI6IiJ9.WkRj5ZO8crRHOmO8Z8-fT9SOzZ8wRIRJxtGijCkSFvU"
INVALID_AUTH = "Bearer eyJ0eXAiOiJKV1QiLCJhbGcOiJIUzI1NiJ9.eyJpZCI6NDQsInVzZXJfbmFtZSI6InVzZXJfdGVzdCIsImF2YXRhciI6IiJ9.WkRj5ZO8crRHOmO8Z8-fT9SOzZ8wRIRJxtGijCkSFvU"

class KanbanTest(SimpleTestCase):
    def setUp(self):
        pass

    def aux_create_user(self, user_name, password, is_admin=False):
        user_data = {
            "user_name": user_name,
            "password": password
        }
        if is_admin:
            user_data.update({"role": "admin"})
        data = json.dumps(user_data)
        return requests.post(HOST + "/scrum-list/user-list/register/", data, headers={"Authorization": ADMIN_AUTH})

    def aux_get_user_authorization(self, user_name, password):
        response = requests.post(HOST + "/scrum-list/user-list/login/", json.dumps({"user_name": user_name, "password": password}) )
        return "Bearer " + response.headers["x-access-token"]

    def aux_find_user_by_user_name(self, user_name):
        url = HOST + "/scrum-list/user-list/filter/user_name/eq/" + user_name
        response = requests.get(url, headers={"Authorization": ADMIN_AUTH})
        return (json.loads( response.text ))[0]

    def aux_remove_last_slash(self, url_as_str):
        url = url_as_str.strip()

        if url_as_str is None or url_as_str == "":
            return url_as_str

        url = url[:-1] if url[-1] == '*' else url
        return url[:-1] if url.endswith('/') else url

#python manage.py test scrum.tests.ScrumUserDetailTest --testrunner=scrum.tests.NoDbTestRunner
class ScrumUserDetailTest(KanbanTest):
    def setUp(self):
        self.uri_sctum_user_list = HOST + "/scrum-list/user-list/"

        self.uri_user_for_edit = HOST + "/scrum-list/user-list/45"
        self.user_for_edit_auth = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDUsInVzZXJfbmFtZSI6InVzZXJfZWRpdF90ZXN0IiwiYXZhdGFyIjoiIn0.s__SQf1OxKcHxOCDdW7LwX0a2rEW-v2zwgU9QtjfdsU"

        self.uri_admin_for_edit = HOST + "/scrum-list/user-list/46"

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


    # delete default user
    def test_delete_default_user_without_token(self):
        default_user_name = "default_user_delete_test"
        post_response = self.aux_create_user(default_user_name, default_user_name, is_admin=False)
        self.assertIn(post_response.status_code, [201, 400])# response 400, the user can awready exists

        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        response = requests.delete(self.uri_sctum_user_list + str(default_user_dict["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_with_invalid_token(self):
        default_user_name = "default_user_delete_test"
        post_response = self.aux_create_user(default_user_name, default_user_name, is_admin=False)
        self.assertIn(post_response.status_code, [201, 400])# response 400, the user can awready exists

        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        response = requests.delete(self.uri_sctum_user_list + str(default_user_dict["id"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_with_default_user_token_self_account(self):
        default_user_name = "default_user_delete_test"
        post_response = self.aux_create_user(default_user_name, default_user_name, is_admin=False)
        self.assertIn(post_response.status_code, [201, 400])# response 400, the user can awready exists

        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_owner_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        response = requests.delete(self.uri_sctum_user_list + str(default_user_dict["id"]), headers={"Authorization": default_user_owner_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_with_default_user_token_another_user_account(self):
        default_user_name = "default_user_delete_test"
        post_response = self.aux_create_user(default_user_name, default_user_name, is_admin=False)
        self.assertIn(post_response.status_code, [201, 400])

        alternative_user_name = "alternative_user_delete_test"
        post_response = self.aux_create_user(alternative_user_name, alternative_user_name, is_admin=False)
        self.assertIn(post_response.status_code, [201, 400])

        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        alternative_user_dict = self.aux_find_user_by_user_name(alternative_user_name)
        response = requests.delete(self.uri_sctum_user_list + str(alternative_user_dict["id"]), headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_with_admin_token(self):
        default_user_name = "default_user_delete_test"
        post_response = self.aux_create_user(default_user_name, default_user_name, is_admin=False)
        self.assertIn(post_response.status_code, [201, 400])

        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        response = requests.delete(self.uri_sctum_user_list + str(default_user_dict["id"]), headers={"Authorization": ADMIN_AUTH})
        self.assertEquals(response.status_code, 204)

        # restoring default user
        restore_response = self.aux_create_user(default_user_name, default_user_name, is_admin=False)
        self.assertEquals(restore_response.status_code, 201)


    # delete admin user
    def test_delete_admin_user_without_token(self):
        # creating admin user
        admin_user_name = "admin_user_delete_test"
        post_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(post_response.status_code, [201, 400])

        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        response = requests.delete(self.uri_sctum_user_list + str(admin_user_dict["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_with_invalid_token(self):
        # creating admin user
        admin_user_name = "admin_user_delete_test"
        post_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(post_response.status_code, [201, 400])

        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        response = requests.delete(self.uri_sctum_user_list + str(admin_user_dict["id"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_with_default_user_token(self):
        # creating admin user
        admin_user_name = "admin_user_delete_test"
        post_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(post_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_delete_test"
        post_response = self.aux_create_user(default_user_name, default_user_name, is_admin=False)
        self.assertIn(post_response.status_code, [201, 400])
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)

        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        response = requests.delete(self.uri_sctum_user_list + str(admin_user_dict["id"]), headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_with_admin_user_token_another_account(self):
        # creating admin user
        admin_user_name = "admin_user_delete_test"
        post_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(post_response.status_code, [201, 400])

        # creating alternative admin user
        alt_admin_user_name = "alternative_admin_user_delete_test"
        post_response = self.aux_create_user(alt_admin_user_name, alt_admin_user_name, is_admin=True)
        self.assertIn(post_response.status_code, [201, 400])

        alt_admin_user_dict = self.aux_find_user_by_user_name(alt_admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        response = requests.delete(self.uri_sctum_user_list + str(alt_admin_user_dict["id"]), headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_with_admin_user_token_self_account(self):
        # creating admin user
        admin_user_name = "admin_user_delete_test"
        post_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(post_response.status_code, [201, 400])

        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        response = requests.delete(self.uri_sctum_user_list + str(admin_user_dict["id"]), headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 401) # admin users can't be deleted (nor self account)

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
                "responsible": HOST + "/scrum-list/user-list/44/" # admin user id = 44
            }
        )

    def aux_create_task_for_admin_user(self):
        return json.dumps(
            {
                "name": "task_" + str(datetime.datetime.now().microsecond),
                "responsible": HOST + "/scrum-list/user-list/31/" # admin user id = 31
            }
        )

    def aux_create_task_for_inexistent_user(self):
        return json.dumps(
            {
                "name": "task_" + str(datetime.datetime.now().microsecond),
                "responsible": HOST + "/scrum-list/user-list/20/"
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
class TaskDetailTest(KanbanTest):
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
        #self.aux_create_admin_user_to_test_tasks()
        #self.aux_create_task_for_admin_user()
        self.uri_alternative_admin_for_test_task = HOST + "/scrum-list/user-list/filter/user_name/eq/alternative_admin_user_to_test_tasks"
        self.uri_alternative_admin_task = HOST + "/scrum-list/task-list/filter/name/eq/alternative_admin_user_task"
        #self.aux_create_alternative_admin_user_to_test_tasks()
        #self.aux_create_task_for_alternative_admin_user()
        self.uri_user_for_test_task = HOST + "/scrum-list/user-list/filter/user_name/eq/default_user_to_test_tasks"
        self.uri_user_task = HOST + "/scrum-list/task-list/filter/name/eq/default_user_task"
        #self.aux_create_default_user_to_test_tasks()
        #self.aux_create_task_for_default_user()
        self.uri_alternative_user_for_test_task = HOST + "/scrum-list/user-list/filter/user_name/eq/alternative_user_to_test_tasks"
        self.uri_alternative_user_task = HOST + "/scrum-list/task-list/filter/name/eq/alternative_user_task"
        #self.aux_create_alternative_default_user_to_test_tasks()
        #self.aux_create_task_for_alternative_default_user()

    def aux_create_task_for_user(self, task_name, responsible_id, responsible_auth):
        data = {
            "name": task_name,
            "responsible": HOST + "/scrum-list/user-list/" + str(responsible_id)
        }
        return requests.post(self.uri_task_list, json.dumps(data),
                             headers={"Authorization": responsible_auth, "Content-Type": "application/json"})

    def aux_find_task_by_name(self, task_name):
        response = requests.get(HOST + "/scrum-list/task-list/filter/name/eq/" + task_name, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]

    def aux_alter_task_responsible(self, task_dict, new_responsible):
        responsible_url = "/".join( self.aux_remove_last_slash(task_dict["responsible"]).split("/")[:-1] )
        new_responsible_url = responsible_url + "/" + str(new_responsible["id"])
        task_dict["responsible"] = new_responsible_url
        return task_dict


    def test_set_task_from_default_user_to_admin_without_token(self):
        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = "default_user_task_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # changing responsible from default user to admin user
        task_dict = self.aux_find_task_by_name(default_task_name)
        new_responsible = self.aux_find_user_by_user_name(admin_user_name)
        updated_task = self.aux_alter_task_responsible(task_dict, new_responsible)
        response = requests.put(self.uri_task_list + str(task_dict["id"]), json.dumps(updated_task))
        self.assertEquals(response.status_code, 401)

    def test_set_task_from_default_user_to_admin_invalid_token(self):
        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = "default_user_task_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # changing responsible from default user to admin user
        task_dict = self.aux_find_task_by_name(default_task_name)
        new_responsible = self.aux_find_user_by_user_name(admin_user_name)
        updated_task = self.aux_alter_task_responsible(task_dict, new_responsible)
        response = requests.put(self.uri_task_list + str(task_dict["id"]), json.dumps(updated_task), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_task_from_default_user_to_admin_with_default_user_token(self):
        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = "default_user_task_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # changing responsible from default user to admin user
        task_dict = self.aux_find_task_by_name(default_task_name)
        new_responsible = self.aux_find_user_by_user_name(admin_user_name)
        updated_task = self.aux_alter_task_responsible(task_dict, new_responsible)
        response = requests.put(self.uri_task_list + str(task_dict["id"]), json.dumps(updated_task), headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_task_from_default_user_to_another_user_with_default_user_token(self):
        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = "default_user_task_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # creating admin user
        alt_user_name = "alternative_user_to_alter_task"
        create_alt_user_response = self.aux_create_user(alt_user_name, alt_user_name)
        self.assertIn(create_alt_user_response.status_code, [201, 400])

        # changing responsible from default user to alternative user
        task_dict = self.aux_find_task_by_name(default_task_name)
        new_responsible = self.aux_find_user_by_user_name(alt_user_name)
        updated_task = self.aux_alter_task_responsible(task_dict, new_responsible)
        response = requests.put(self.uri_task_list + str(task_dict["id"]), json.dumps(updated_task), headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_task_from_default_user_to_admin_with_admin_user_token(self):
        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = "default_user_task_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # changing responsible from default user to admin user
        task_dict = self.aux_find_task_by_name(default_task_name)
        new_responsible = self.aux_find_user_by_user_name(admin_user_name)
        updated_task = self.aux_alter_task_responsible(task_dict, new_responsible)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        response = requests.put(self.uri_task_list + str(task_dict["id"]), json.dumps(updated_task), headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)

        # restoring task responsible
        old_user_dict = self.aux_find_user_by_user_name(default_user_name)
        restored_task = self.aux_alter_task_responsible(task_dict, old_user_dict)
        restore_response = requests.put(self.uri_task_list + str(task_dict["id"]), json.dumps(restored_task), headers={"Authorization": admin_user_auth})
        self.assertEquals(restore_response.status_code, 204)


    def test_set_task_from_admin_user_to_default_user_without_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = "admin_user_task_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"], admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing responsible from admin to default user
        task_dict = self.aux_find_task_by_name(admin_task_name)
        new_responsible = self.aux_find_user_by_user_name(default_user_name)
        updated_task = self.aux_alter_task_responsible(task_dict, new_responsible)
        response = requests.put(self.uri_task_list + str(task_dict["id"]), json.dumps(updated_task))
        self.assertEquals(response.status_code, 401)

    def test_set_task_from_admin_user_to_default_user_with_invalid_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = "admin_user_task_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"], admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing responsible from admin to default user
        task_dict = self.aux_find_task_by_name(admin_task_name)
        new_responsible = self.aux_find_user_by_user_name(default_user_name)
        updated_task = self.aux_alter_task_responsible(task_dict, new_responsible)
        response = requests.put(self.uri_task_list + str(task_dict["id"]), json.dumps(updated_task), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_task_from_admin_user_to_default_user_with_default_user_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = "admin_user_task_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"], admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing responsible from admin to default user
        task_dict = self.aux_find_task_by_name(admin_task_name)
        new_responsible = self.aux_find_user_by_user_name(default_user_name)
        updated_task = self.aux_alter_task_responsible(task_dict, new_responsible)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        response = requests.put(self.uri_task_list + str(task_dict["id"]), json.dumps(updated_task), headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_task_from_admin_user_to_another_admin_user_with_admin_user_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating alternative admin user
        alt_admin_name = "alternative_admin_to_alter_task"
        create_user_response = self.aux_create_user(alt_admin_name, alt_admin_name, is_admin=True)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = "admin_user_task_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"], admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing responsible from admin to alternative admin user
        task_dict = self.aux_find_task_by_name(admin_task_name)
        new_responsible = self.aux_find_user_by_user_name(alt_admin_name)
        updated_task = self.aux_alter_task_responsible(task_dict, new_responsible)
        response = requests.put(self.uri_task_list + str(task_dict["id"]), json.dumps(updated_task), headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 401)


    def test_delete_default_user_task_without_token(self):
        # creating default user
        default_user_name = "default_user_to_test_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = "default_user_task"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        task_dict = self.aux_find_task_by_name(default_task_name)
        response = requests.delete(self.uri_task_list + str(task_dict["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_task_with_invalid_token(self):
        # creating default user
        default_user_name = "default_user_to_test_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = "default_user_task"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        task_dict = self.aux_find_task_by_name(default_task_name)
        response = requests.delete(self.uri_task_list + str(task_dict["id"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_task_with_default_user_token_self_task(self):
        # creating default user
        default_user_name = "default_user_to_test_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = "default_user_task"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        task_dict = self.aux_find_task_by_name(default_task_name)
        response = requests.delete(self.uri_task_list + str(task_dict["id"]), headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 204)

    def test_delete_default_user_task_with_default_user_token_another_user_task(self):
        '''
        Alternative dafault user trying to delete dafault user task
        '''
        # creating default user
        default_user_name = "default_user_to_test_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating alternative user
        alt_default_user_name = "alternative_user_to_test_task"
        create_alt_user_response = self.aux_create_user(alt_default_user_name, alt_default_user_name)
        self.assertIn(create_alt_user_response.status_code, [201, 400])

        # creating task for alternative user
        alt_user_task_name = "alternative_user_task"
        alt_user_dict = self.aux_find_user_by_user_name(alt_default_user_name)
        alt_user_auth = self.aux_get_user_authorization(alt_default_user_name, alt_default_user_name)
        create_task_response = self.aux_create_task_for_user(alt_user_task_name, alt_user_dict["id"], alt_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        task_dict = self.aux_find_task_by_name(alt_user_task_name)
        alt_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        response = requests.delete(self.uri_task_list + str(task_dict["id"]), headers={"Authorization": alt_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_task_with_admin_user_token(self):
        '''
        Admin dafault user trying to delete dafault user task
        '''
        # creating default user
        default_user_name = "default_user_to_test_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = "default_user_task"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        task_dict = self.aux_find_task_by_name(default_task_name)
        response = requests.delete(self.uri_task_list + str(task_dict["id"]), headers={"Authorization": ADMIN_AUTH})
        self.assertEquals(response.status_code, 204)


    def test_delete_admin_user_task_without_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_test_task"
        create_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        admin_task_name = "admin_user_task"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"], admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        task_dict = self.aux_find_task_by_name(admin_task_name)
        response = requests.delete(self.uri_task_list + str(task_dict["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_task_with_invalid_token(self):
        # creating default user
        admin_user_name = "admin_user_to_test_task"
        create_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        admin_task_name = "admin_user_task"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"], admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        task_dict = self.aux_find_task_by_name(admin_task_name)
        response = requests.delete(self.uri_task_list + str(task_dict["id"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_task_with_default_user_token(self):
        """
        Default user trying to delete admin task
        """
        # creating default user
        default_user_name = "default_user_to_test_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_test_task"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = "admin_user_task"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"], admin_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        task_dict = self.aux_find_task_by_name(admin_task_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        response = requests.delete(self.uri_task_list + str(task_dict["id"]), headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_task_with_admin_user_token_self_task(self):
        # creating default user
        admin_user_name = "admin_user_to_test_task"
        create_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating task for default user
        admin_task_name = "admin_user_task"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"], admin_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        task_dict = self.aux_find_task_by_name(admin_task_name)
        response = requests.delete(self.uri_task_list + str(task_dict["id"]), headers={"Authorization": admin_auth})
        self.assertEquals(response.status_code, 204)

    def test_delete_admin_user_task_with_admin_user_token_another_admin_task(self):
        """
        Alternative admin user trying to delete admin task
        """
        # creating admin user
        admin_user_name = "admin_user_to_test_task"
        create_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating alternative admin user
        alternative_admin_user_name = "alternative_admin_user_to_test_task"
        create_alternative_admin_user_response = self.aux_create_user(alternative_admin_user_name, alternative_admin_user_name, is_admin=True)
        self.assertIn(create_alternative_admin_user_response.status_code, [201, 400])

        # creating task for admin usertest_set_task_from_admin_user_to_another_admin_user_with_admin_user_token
        admin_task_name = "admin_user_task"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"], admin_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        task_dict = self.aux_find_task_by_name(admin_task_name)
        alternative_admin_user_auth = self.aux_get_user_authorization(alternative_admin_user_name, alternative_admin_user_name)
        response = requests.delete(self.uri_task_list + str(task_dict["id"]), headers={"Authorization": alternative_admin_user_auth})
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
class ProjectDetailTest(KanbanTest):
    def setUp(self):
        self.url_project_list = HOST + "/scrum-list/project-list/"

    def aux_create_project_for_user(self, project_name, responsible_id, responsible_auth):
        data = {
            "name": project_name,
            "administrative_responsible": HOST + "/scrum-list/user-list/" + str(responsible_id),
            "technical_responsible": HOST + "/scrum-list/user-list/" + str(responsible_id)
        }
        return requests.post(self.url_project_list, json.dumps(data),
                             headers={"Authorization": responsible_auth, "Content-Type": "application/json"})

    def aux_find_project_by_name(self, project_name):
        response = requests.get(HOST + "/scrum-list/project-list/filter/name/eq/" + project_name, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]

    def aux_alter_project_responsible(self, project_dict, new_responsible):
        responsible_url = "/".join( self.aux_remove_last_slash(project_dict["administrative_responsible"]).split("/")[:-1] )
        new_responsible_url = responsible_url + "/" + str(new_responsible["id"])
        project_dict["administrative_responsible"] = new_responsible_url
        project_dict["technical_responsible"] = new_responsible_url
        return project_dict

    '''
    {
        "id": 78,
        "name": "alternative_admin_project_to_edit",
        "description": null,
        "start": null,
        "end": null,
        "administrative_responsible": "http://127.0.0.1:8000/scrum-list/user-list/475",
        "technical_responsible": "http://127.0.0.1:8000/scrum-list/user-list/475",
    },
    '''


    # Changing project responsable from admin to default user (alternative user is also an defalt user)
    def test_set_project_from_admin_to_default_user_without_token(self):
        admin_user_name = "admin_user_to_alter_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        admin_project_name = "admin_project_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_project_reponse = self.aux_create_project_for_user(admin_project_name, admin_user_dict["id"], admin_user_auth)
        self.assertIn(create_project_reponse.status_code, [400, 201])

        default_user_name = "default_user_to_alter_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        project_dict = self.aux_find_project_by_name(admin_project_name)
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        updated_project = self.aux_alter_project_responsible(project_dict, default_user_dict)

        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(updated_project))
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_admin_to_default_user_with_invalid_token(self):
        admin_user_name = "admin_user_to_alter_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        admin_project_name = "admin_project_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_project_reponse = self.aux_create_project_for_user(admin_project_name, admin_user_dict["id"],
                                                                  admin_user_auth)
        self.assertIn(create_project_reponse.status_code, [400, 201])

        default_user_name = "default_user_to_alter_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        project_dict = self.aux_find_project_by_name(admin_project_name)
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        updated_project = self.aux_alter_project_responsible(project_dict, default_user_dict)

        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(updated_project), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_admin_to_default_user_with_default_user_token(self):
        admin_user_name = "admin_user_to_alter_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        admin_project_name = "admin_project_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_project_reponse = self.aux_create_project_for_user(admin_project_name, admin_user_dict["id"],
                                                                  admin_user_auth)
        self.assertIn(create_project_reponse.status_code, [400, 201])

        default_user_name = "default_user_to_alter_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        project_dict = self.aux_find_project_by_name(admin_project_name)
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        updated_project = self.aux_alter_project_responsible(project_dict, default_user_dict)

        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(updated_project),
                                headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_admin_to_alternative_user_with_default_user_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        # creating admin project
        admin_project_name = "admin_project_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_project_reponse = self.aux_create_project_for_user(admin_project_name, admin_user_dict["id"],
                                                                  admin_user_auth)
        self.assertIn(create_project_reponse.status_code, [400, 201])

        # creating alternative user
        alternative_user_name = "alternative_user_to_alter_project"
        create_alternative_user_response = self.aux_create_user(alternative_user_name, alternative_user_name)
        self.assertIn(create_alternative_user_response.status_code, [400, 201])

        # setting project to alternative user
        project_dict = self.aux_find_project_by_name(admin_project_name)
        alternative_user_dict = self.aux_find_user_by_user_name(alternative_user_name)
        updated_project = self.aux_alter_project_responsible(project_dict, alternative_user_dict)

        # creating default user (to get his authorization)
        default_user_name = "default_user_to_alter_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)

        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(updated_project),
                                headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_admin_to_default_user_with_admin_user_token(self):
        admin_user_name = "admin_user_to_alter_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        admin_project_name = "admin_project_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_project_reponse = self.aux_create_project_for_user(admin_project_name, admin_user_dict["id"],
                                                                  admin_user_auth)
        self.assertIn(create_project_reponse.status_code, [400, 201])

        default_user_name = "default_user_to_alter_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        project_dict = self.aux_find_project_by_name(admin_project_name)
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        updated_project = self.aux_alter_project_responsible(project_dict, default_user_dict)


        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(updated_project),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)

        restored_project = self.aux_alter_project_responsible(project_dict, admin_user_dict)
        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(restored_project),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)


    # Changing project responsable from default user to admin and alternative admin user
    def test_set_project_from_default_user_to_admin_user_without_token(self):
        default_user_name = "default_user_to_alter_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        default_user_project_name = "default_user_project_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_project_reponse = self.aux_create_project_for_user(default_user_project_name, default_user_dict["id"],
                                                                  default_user_auth)
        self.assertIn(create_project_reponse.status_code, [400, 201])

        admin_user_name = "admin_user_to_alter_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        project_dict = self.aux_find_project_by_name(default_user_project_name)
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        updated_project = self.aux_alter_project_responsible(project_dict, admin_user_dict)

        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(updated_project))
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_default_user_to_admin_user_with_invalid_token(self):
        default_user_name = "default_user_to_alter_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        default_user_project_name = "default_user_project_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_project_reponse = self.aux_create_project_for_user(default_user_project_name, default_user_dict["id"],
                                                                  default_user_auth)
        self.assertIn(create_project_reponse.status_code, [400, 201])

        admin_user_name = "admin_user_to_alter_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        project_dict = self.aux_find_project_by_name(default_user_project_name)
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        updated_project = self.aux_alter_project_responsible(project_dict, admin_user_dict)

        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(updated_project), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_default_user_to_admin_user_with_default_user_token(self):
        default_user_name = "default_user_to_alter_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        default_user_project_name = "default_user_project_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_project_reponse = self.aux_create_project_for_user(default_user_project_name, default_user_dict["id"],
                                                                  default_user_auth)
        self.assertIn(create_project_reponse.status_code, [400, 201])

        admin_user_name = "admin_user_to_alter_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        project_dict = self.aux_find_project_by_name(default_user_project_name)
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        updated_project = self.aux_alter_project_responsible(project_dict, admin_user_dict)

        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(updated_project),
                                headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_project_from_default_user_to_admin_user_with_admin_user_token(self):
        default_user_name = "default_user_to_alter_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        default_user_project_name = "default_user_project_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_project_reponse = self.aux_create_project_for_user(default_user_project_name, default_user_dict["id"],
                                                                  default_user_auth)
        self.assertIn(create_project_reponse.status_code, [400, 201])

        admin_user_name = "admin_user_to_alter_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        project_dict = self.aux_find_project_by_name(default_user_project_name)
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        updated_project = self.aux_alter_project_responsible(project_dict, admin_user_dict)

        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(updated_project),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)

        # restoring project
        old_project_dict = self.aux_find_project_by_name(default_user_project_name)
        original_project = self.aux_alter_project_responsible(old_project_dict, default_user_dict)
        response = requests.put(self.url_project_list + str(old_project_dict["id"]), json.dumps(original_project),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)

    def test_set_project_from_admin_to_another_admin_user_with_admin_token(self):
        admin_user_name = "admin_user_to_alter_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        admin_project_name = "admin_project_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_project_reponse = self.aux_create_project_for_user(admin_project_name, admin_user_dict["id"],
                                                                  admin_user_auth)
        self.assertIn(create_project_reponse.status_code, [400, 201])

        alternative_admin_user_name = "alternative_admin_user_to_alter_project"
        create_alternative_admin_user_response = self.aux_create_user(alternative_admin_user_name, alternative_admin_user_name, is_admin=True)
        self.assertIn(create_alternative_admin_user_response.status_code, [400, 201])

        project_dict = self.aux_find_project_by_name(admin_project_name)
        alternative_admin_user_dict = self.aux_find_user_by_user_name(alternative_admin_user_name)
        updated_project = self.aux_alter_project_responsible(project_dict, alternative_admin_user_dict)

        response = requests.put(self.url_project_list + str(project_dict["id"]), json.dumps(updated_project),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 401)


    def test_delete_default_user_project_without_token(self):
        default_user_name = "default_user_to_delete_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        # creating project for default user
        default_user_project_name = "default_user_project"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_project_response = self.aux_create_project_for_user(default_user_project_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_project_response.status_code, [201, 400])

        project_dict = self.aux_find_project_by_name(default_user_project_name)
        response = requests.delete(self.url_project_list + str(project_dict["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_project_with_invalid_token(self):
        default_user_name = "default_user_to_delete_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        # creating project for default user
        default_user_project_name = "default_user_project"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_project_response = self.aux_create_project_for_user(default_user_project_name, default_user_dict["id"],
                                                                   default_user_auth)
        self.assertIn(create_project_response.status_code, [201, 400])

        project_dict = self.aux_find_project_by_name(default_user_project_name)
        response = requests.delete(self.url_project_list + str(project_dict["id"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_project_with_default_user_token_self_project(self):
        default_user_name = "default_user_to_delete_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        # creating project for default user
        default_user_project_name = "default_user_project"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_project_response = self.aux_create_project_for_user(default_user_project_name, default_user_dict["id"],
                                                                   default_user_auth)
        self.assertIn(create_project_response.status_code, [201, 400])

        project_dict = self.aux_find_project_by_name(default_user_project_name)
        response = requests.delete(self.url_project_list + str(project_dict["id"]),
                                   headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 204)

    def test_delete_default_user_project_with_default_user_token_another_user_project(self):
        '''
        Alternative dafault user trying to delete dafault user project
        '''
        # creating default user
        default_user_name = "default_user_to_delete_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        # creating alternative user
        alternative_user_name = "alternative_user_to_delete_project"
        create_alternative_user_response = self.aux_create_user(alternative_user_name, alternative_user_name)
        self.assertIn(create_alternative_user_response.status_code, [400, 201])

        # creating project for default user
        alternative_user_project_name = "alternative_user_project"
        alternative_user_dict = self.aux_find_user_by_user_name(alternative_user_name)
        alternative_user_auth = self.aux_get_user_authorization(alternative_user_name, alternative_user_name)
        create_project_response = self.aux_create_project_for_user(alternative_user_project_name, alternative_user_dict["id"],
                                                                   alternative_user_auth)
        self.assertIn(create_project_response.status_code, [201, 400])

        project_dict = self.aux_find_project_by_name(alternative_user_project_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        response = requests.delete(self.url_project_list + str(project_dict["id"]), headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_project_with_admin_user_token(self):
        '''
        Admin dafault user trying to delete dafault user task
        '''
        # creating default user
        default_user_name = "default_user_to_delete_project"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [400, 201])

        # creating admin user
        admin_user_name = "admin_user_to_delete_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        # creating project for default user
        default_user_project_name = "default_user_project"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_project_response = self.aux_create_project_for_user(default_user_project_name, default_user_dict["id"],
                                                                   default_user_auth)
        self.assertIn(create_project_response.status_code, [201, 400])

        project_dict = self.aux_find_project_by_name(default_user_project_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        response = requests.delete(self.url_project_list + str(project_dict["id"]),
                                   headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)


    def test_delete_admin_user_project_without_token(self):
        admin_user_name = "admin_user_to_delete_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        # creating project for admin user
        admin_user_project_name = "admin_user_project"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_project_response = self.aux_create_project_for_user(admin_user_project_name, admin_user_dict["id"],
                                                                   admin_user_auth)
        self.assertIn(create_project_response.status_code, [201, 400])

        project_dict = self.aux_find_project_by_name(admin_user_project_name)
        response = requests.delete(self.url_project_list + str(project_dict["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_project_with_invalid_token(self):
        admin_user_name = "admin_user_to_delete_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        # creating project for admin user
        admin_user_project_name = "admin_user_project"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_project_response = self.aux_create_project_for_user(admin_user_project_name, admin_user_dict["id"],
                                                                   admin_user_auth)
        self.assertIn(create_project_response.status_code, [201, 400])

        project_dict = self.aux_find_project_by_name(admin_user_project_name)
        response = requests.delete(self.url_project_list + str(project_dict["id"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_project_with_default_user_token(self):
        '''
        Default user trying to delete admin task
        '''
        admin_user_name = "admin_user_to_delete_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        default_user_name = "default_user_to_delete_project"
        create_defaut_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_defaut_user_response.status_code, [400, 201])

        # creating project for admin user
        admin_user_project_name = "admin_user_project"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_project_response = self.aux_create_project_for_user(admin_user_project_name, admin_user_dict["id"],
                                                                   admin_user_auth)
        self.assertIn(create_project_response.status_code, [201, 400])

        project_dict = self.aux_find_project_by_name(admin_user_project_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        response = requests.delete(self.url_project_list + str(project_dict["id"]), headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_project_with_admin_user_token_self_project(self):
        admin_user_name = "admin_user_to_delete_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        # creating project for admin user
        admin_user_project_name = "admin_user_project"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_project_response = self.aux_create_project_for_user(admin_user_project_name, admin_user_dict["id"],
                                                                   admin_user_auth)
        self.assertIn(create_project_response.status_code, [201, 400])

        project_dict = self.aux_find_project_by_name(admin_user_project_name)
        response = requests.delete(self.url_project_list + str(project_dict["id"]), headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)

    def test_delete_admin_user_project_with_admin_user_token_another_admin_project(self):
        '''
        Alternative admin user trying to delete admin project
        '''
        admin_user_name = "admin_user_to_delete_project"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [400, 201])

        alternative_admin_user_name = "alternative_admin_user_to_delete_project"
        create_alternative_admin_user_response = self.aux_create_user(alternative_admin_user_name, alternative_admin_user_name, is_admin=True)
        self.assertIn(create_alternative_admin_user_response.status_code, [400, 201])

        # creating project for admin user
        alternative_admin_user_project_name = "alternative_admin_user_project"
        alternative_admin_user_dict = self.aux_find_user_by_user_name(alternative_admin_user_name)
        alternative_admin_user_auth = self.aux_get_user_authorization(alternative_admin_user_name, alternative_admin_user_name)
        create_project_response = self.aux_create_project_for_user(alternative_admin_user_project_name, alternative_admin_user_dict["id"],
                                                                   alternative_admin_user_auth)
        self.assertIn(create_project_response.status_code, [201, 400])

        project_dict = self.aux_find_project_by_name(alternative_admin_user_project_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        response = requests.delete(self.url_project_list + str(project_dict["id"]),
                                   headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 401)

class ImpedimentsListTest(KanbanTest):

    def test_create_impediment_without_token(self):
        pass

    def test_create_impediment_with_invalid_token(self):
        pass

    def test_create_impediment_with_default_user_token(self):
        pass

    def test_create_impediment_with_admin_token(self):
        pass


class SprintListTest(KanbanTest):
    def setUp(self):
        super(SimpleTestCase, self).setUp()
        pass

    def test_create_sprint_default_user_responsible_without_token(self):
        pass

    def test_create_sprint_default_user_responsible_invalid_token(self):
        pass

    def test_create_sprint_default_user_responsible_with_default_user_token(self):
        pass

    def test_create_sprint_default_user_responsible_with_another_user_token(self):
        pass

    def test_create_sprint_default_user_responsible_with_admin_user_token(self):
        pass


    def test_create_sprint_admin_user_responsible_without_token(self):
        pass

    def test_create_sprint_admin_user_responsible_invalid_toke(self):
        pass

    def test_create_sprint_admin_user_responsible_with_default_user_token(self):
        pass

    def test_create_sprint_admin_user_responsible_with_admin_user_token(self):
        pass

    def test_create_sprint_admin_user_responsible_with_alternative_admin_user_toke(self):
        pass


#python manage.py test scrum.tests.SprintDetailTest --testrunner=scrum.tests.NoDbTestRunner
class SprintDetailTest(KanbanTest):
    def setUp(self):
        self.url_sprint_list = HOST + "/scrum-list/sprint-list/"

    def aux_create_sprint_for_user(self, sprint_name, responsible_id, responsible_auth):
        data = {
            "code": sprint_name,
            "responsible": HOST + "/scrum-list/user-list/" + str(responsible_id)
        }
        return requests.post(self.url_sprint_list, json.dumps(data),
                             headers={"Authorization": responsible_auth, "Content-Type": "application/json"})

    def aux_find_sprint_by_name(self, sprint_name):
        response = requests.get(HOST + "/scrum-list/sprint-list/filter/code/eq/" + sprint_name, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]

    def aux_alter_sprint_responsible(self, sprint_dict, new_responsible):
        responsible_url = "/".join( self.aux_remove_last_slash(sprint_dict["responsible"]).split("/")[:-1] )
        new_responsible_url = responsible_url + "/" + str(new_responsible["id"])
        sprint_dict["responsible"] = new_responsible_url
        return sprint_dict

    '''
    {
        "id_sprint": 7,
        "code": "sprint de teste",
        "start": "2019-04-11",
        "end": "2019-04-11",
        "project": null,
        "responsible": "http://127.0.0.1/scrum-list/user-list/445"
    }
    '''


    def test_set_sprint_from_default_user_to_admin_without_token(self):
        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # changing responsible from default user to admin user
        sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        new_responsible = self.aux_find_user_by_user_name(admin_user_name)
        updated_sprint = self.aux_alter_sprint_responsible(sprint_dict, new_responsible)
        response = requests.put(self.url_sprint_list + str(sprint_dict["id_sprint"]), json.dumps(updated_sprint))
        self.assertEquals(response.status_code, 401)

    def test_set_sprint_from_default_user_to_admin_invalid_token(self):
        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # changing responsible from default user to admin user
        sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        new_responsible = self.aux_find_user_by_user_name(admin_user_name)
        updated_sprint = self.aux_alter_sprint_responsible(sprint_dict, new_responsible)
        response = requests.put(self.url_sprint_list + str(sprint_dict["id_sprint"]), json.dumps(updated_sprint), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_sprint_from_default_user_to_admin_with_default_user_token(self):
        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # changing responsible from default user to admin user
        sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        new_responsible = self.aux_find_user_by_user_name(admin_user_name)
        updated_sprint = self.aux_alter_sprint_responsible(sprint_dict, new_responsible)
        response = requests.put(self.url_sprint_list + str(sprint_dict["id_sprint"]), json.dumps(updated_sprint),
                                headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_sprint_from_default_user_to_another_user_with_default_user_token(self):
        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating alternative user
        alternative_user_name = "alternative_user_to_alter_task"
        create_alternative_user_response = self.aux_create_user(alternative_user_name, alternative_user_name)
        self.assertIn(create_alternative_user_response.status_code, [201, 400])

        # changing responsible from default user to admin user
        sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        new_responsible = self.aux_find_user_by_user_name(alternative_user_name)
        updated_sprint = self.aux_alter_sprint_responsible(sprint_dict, new_responsible)
        response = requests.put(self.url_sprint_list + str(sprint_dict["id_sprint"]), json.dumps(updated_sprint),
                                headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_sprint_from_default_user_to_admin_with_admin_user_token(self):
        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint_to_alter"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # changing responsible from default user to admin user
        sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        new_responsible = self.aux_find_user_by_user_name(admin_user_name)
        updated_sprint = self.aux_alter_sprint_responsible(sprint_dict, new_responsible)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        response = requests.put(self.url_sprint_list + str(sprint_dict["id_sprint"]), json.dumps(updated_sprint),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)

        # restoring sprint
        current_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        old_responsible = self.aux_find_user_by_user_name(admin_user_name)
        restored_sprint = self.aux_alter_sprint_responsible(current_sprint_dict, old_responsible)
        restore_response = requests.put(self.url_sprint_list + str(restored_sprint["id_sprint"]), json.dumps(restored_sprint),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(restore_response, 204)


    def test_set_sprint_from_admin_user_to_default_user_without_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # changing responsible from admin user to default user
        sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        new_responsible = self.aux_find_user_by_user_name(default_user_name)
        updated_sprint = self.aux_alter_sprint_responsible(sprint_dict, new_responsible)
        response = requests.put(self.url_sprint_list + str(sprint_dict["id_sprint"]), json.dumps(updated_sprint))
        self.assertEquals(response.status_code, 401)

    def test_set_sprint_from_admin_user_to_default_user_with_invalid_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # changing responsible from admin user to default user
        sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        new_responsible = self.aux_find_user_by_user_name(default_user_name)
        updated_sprint = self.aux_alter_sprint_responsible(sprint_dict, new_responsible)
        response = requests.put(self.url_sprint_list + str(sprint_dict["id_sprint"]), json.dumps(updated_sprint), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_sprint_from_admin_user_to_default_user_with_default_user_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # changing responsible from admin user to default user
        sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        new_responsible = self.aux_find_user_by_user_name(default_user_name)
        updated_sprint = self.aux_alter_sprint_responsible(sprint_dict, new_responsible)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        response = requests.put(self.url_sprint_list + str(sprint_dict["id_sprint"]), json.dumps(updated_sprint),
                                headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_sprint_from_admin_user_to_another_admin_user_with_admin_user_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint_to_alter"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_alter_task"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # changing responsible from admin user to default user
        sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        new_responsible = self.aux_find_user_by_user_name(default_user_name)
        updated_sprint = self.aux_alter_sprint_responsible(sprint_dict, new_responsible)
        response = requests.put(self.url_sprint_list + str(sprint_dict["id_sprint"]), json.dumps(updated_sprint),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)

        # restoring sprint
        current_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        old_responsible = self.aux_find_user_by_user_name(admin_user_name)
        restored_sprint = self.aux_alter_sprint_responsible(current_sprint_dict, old_responsible)
        restore_response = requests.put(self.url_sprint_list + str(restored_sprint["id_sprint"]), json.dumps(restored_sprint),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(restore_response.status_code, 204)


    def test_delete_default_user_sprint_without_token(self):
        # creating default user
        default_user_name = "default_user_to_test_sprint"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        response = requests.delete(self.url_sprint_list + str(sprint_dict["id_sprint"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_sprint_with_invalid_token(self):
        # creating default user
        default_user_name = "default_user_to_test_sprint"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        response = requests.delete(self.url_sprint_list + str(sprint_dict["id_sprint"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_sprint_with_default_user_token_self_sprint(self):
        # creating default user
        default_user_name = "default_user_to_test_sprint"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        response = requests.delete(self.url_sprint_list + str(sprint_dict["id_sprint"]),
                                   headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 204)

    def test_delete_default_user_sprint_with_default_user_token_another_user_sprint(self):
        '''
        Alternative dafault user trying to delete dafault user task
        '''
        # creating default user
        default_user_name = "default_user_to_test_sprint"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating alternative user sprint
        alternative_user_name = "alternative_user_to_tests_sprint"
        create_alternative_user_response = self.aux_create_user(alternative_user_name, alternative_user_name)
        self.assertIn(create_alternative_user_response.status_code, [201, 400])


        # creating sprint for alternative user
        alternative_sprint_name = "alternative_user_sprint"
        alternative_user_dict = self.aux_find_user_by_user_name(alternative_user_name)
        alternative_user_auth = self.aux_get_user_authorization(alternative_user_name, alternative_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(alternative_sprint_name, alternative_user_dict["id"],
                                                                 alternative_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        sprint_dict = self.aux_find_sprint_by_name(alternative_sprint_name)
        default_user_auth = self.aux_get_user_authorization(alternative_user_name, alternative_user_name)
        response = requests.delete(self.url_sprint_list + str(sprint_dict["id_sprint"]),
                                   headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_sprint_with_admin_user_token(self):
        '''
        Admin dafault user trying to delete dafault user task
        '''
        # creating default user
        default_user_name = "default_user_to_test_sprint"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating admin user sprint
        admin_user_name = "admin_user_to_tests_sprint"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        response = requests.delete(self.url_sprint_list + str(sprint_dict["id_sprint"]),
                                   headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)


    def test_delete_admin_user_sprint_without_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_test_sprint"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        response = requests.delete(self.url_sprint_list + str(sprint_dict["id_sprint"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_sprint_with_invalid_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_test_sprint"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        response = requests.delete(self.url_sprint_list + str(sprint_dict["id_sprint"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_sprint_with_default_user_token(self):
        """
        Default user trying to delete admin task
        """
        # creating admin user
        admin_user_name = "admin_user_to_test_sprint"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_test_sprint"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        response = requests.delete(self.url_sprint_list + str(sprint_dict["id_sprint"]),
                                   headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_sprint_with_admin_user_token_self_sprint(self):
        # creating admin user
        admin_user_name = "admin_user_to_test_sprint"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        response = requests.delete(self.url_sprint_list + str(sprint_dict["id_sprint"]), headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)

    def test_delete_admin_user_sprint_with_admin_user_token_another_admin_sprint(self):
        """
        Alternative admin user trying to delete admin task
        """
        # creating admin user
        admin_user_name = "admin_user_to_test_sprint"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating alternative admin user
        alternative_admin_user_name = "alternative_admin_user_to_test_sprint"
        create_alternative_admin_response = self.aux_create_user(alternative_admin_user_name, alternative_admin_user_name, is_admin=True)
        self.assertIn(create_alternative_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        alternative_admin_sprint_name = "alternative_admin_user_sprint"
        alternative_admin_user_dict = self.aux_find_user_by_user_name(alternative_admin_user_name)
        alternative_admin_user_auth = self.aux_get_user_authorization(alternative_admin_user_name, alternative_admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(alternative_admin_sprint_name, alternative_admin_user_dict["id"],
                                                                 alternative_admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        sprint_dict = self.aux_find_sprint_by_name(alternative_admin_sprint_name)
        response = requests.delete(self.url_sprint_list + str(sprint_dict["id_sprint"]),
                                   headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 401)


#python manage.py test scrum.tests.ImpedimentsDetailTest --testrunner=scrum.tests.NoDbTestRunner
class ImpedimentsDetailTest(KanbanTest):
    def setUp(self):
        super(ImpedimentsDetailTest, self).setUp()
        self.url_sprint_list = HOST + "/scrum-list/sprint-list/"
        self.url_impediment_list = HOST + "/scrum-list/impediment-list/"
        self.uri_task_list = HOST + "/scrum-list/task-list/"


    def aux_create_task_for_user(self, task_name, responsible_id, responsible_auth):
        data = {
            "name": task_name,
            "responsible": HOST + "/scrum-list/user-list/" + str(responsible_id)
        }
        return requests.post(self.uri_task_list, json.dumps(data),
                             headers={"Authorization": responsible_auth, "Content-Type": "application/json"})

    def aux_find_task_by_name(self, task_name):
        response = requests.get(HOST + "/scrum-list/task-list/filter/name/eq/" + task_name, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]


    def aux_create_sprint_for_user(self, sprint_name, responsible_id, responsible_auth):
        data = {
            "code": sprint_name,
            "responsible": HOST + "/scrum-list/user-list/" + str(responsible_id)
        }
        return requests.post(self.url_sprint_list, json.dumps(data),
                             headers={"Authorization": responsible_auth, "Content-Type": "application/json"})

    def aux_find_sprint_by_name(self, sprint_name):
        response = requests.get(HOST + "/scrum-list/sprint-list/filter/code/eq/" + sprint_name, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]


    def aux_create_impediment_for_user(self, impediment_name, task_id, sprint_id, user_auth):
        data = {
            "name": impediment_name,
            "sprint": HOST + "/scrum-list/sprint-list/" + str(sprint_id),
            "task": HOST + "/scrum-list/task-list/" + str(task_id)
        }
        return requests.post(self.url_impediment_list, json.dumps(data),
                             headers={"Authorization": user_auth, "Content-Type": "application/json"})

    def aux_find_impediment_by_name(self, impediment_name):
        response = requests.get(HOST + "/scrum-list/impediment-list/filter/name/eq/" + impediment_name, headers={"Authorization": ADMIN_AUTH})
        return json.loads( response.text )[0]

    def aux_alter_impediment_task(self, impediment_dict, task_dict):
        task_url = "/".join( self.aux_remove_last_slash(impediment_dict["task"]).split("/")[:-1] )
        new_task_url = task_url + "/" + str(task_dict["id"])
        impediment_dict["task"] = new_task_url
        return impediment_dict

    def aux_alter_impediment_sprint(self, impediment_dict, sprint_dict):
        sprint_url = "/".join( self.aux_remove_last_slash(impediment_dict["sprint"]).split("/")[:-1] )
        new_sprint_url = sprint_url + "/" + str(sprint_dict["id_sprint"])
        impediment_dict["sprint"] = new_sprint_url
        return impediment_dict

    '''
    {
        "id": 7,
        "name": "sprint de teste",
        "created_date": "2019-04-11",
        "resolution_date": "2019-04-11",
        "description": null,
        "sprint": "http://127.0.0.1/scrum-list/sprint-list/445",
        "task": "http://127.0.0.1/scrum-list/task-list/445"
    }
    '''

    def test_set_impediment_from_default_user_to_admin_without_token(self):
        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "default_user_impediment"
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, default_task_dict["id"],
                                                                         default_sprint_dict["id_sprint"], default_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])


        # changing impediment from default user to admin user
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)

        updated_impediment = self.aux_alter_impediment_task(impediment_dict, admin_task_dict)
        updated_impediment = self.aux_alter_impediment_sprint(updated_impediment, admin_sprint_dict)

        response = requests.put(self.url_impediment_list + str(impediment_dict["id"]), json.dumps(updated_impediment))
        self.assertEquals(response.status_code, 401)

    def test_set_impediment_from_default_user_to_admin_invalid_token(self):
        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "default_user_impediment"
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, default_task_dict["id"],
                                                                         default_sprint_dict["id_sprint"], default_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing impediment from default user to admin user
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)

        updated_impediment = self.aux_alter_impediment_task(impediment_dict, admin_task_dict)
        updated_impediment = self.aux_alter_impediment_sprint(updated_impediment, admin_sprint_dict)

        response = requests.put(self.url_impediment_list + str(impediment_dict["id"]), json.dumps(updated_impediment), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_impediment_from_default_user_to_admin_with_default_user_token(self):
        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "default_user_impediment"
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, default_task_dict["id"],
                                                                         default_sprint_dict["id_sprint"], default_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing impediment from default user to admin user
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)

        updated_impediment = self.aux_alter_impediment_task(impediment_dict, admin_task_dict)
        updated_impediment = self.aux_alter_impediment_sprint(updated_impediment, admin_sprint_dict)

        response = requests.put(self.url_impediment_list + str(impediment_dict["id"]), json.dumps(updated_impediment),
                                headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_impediment_from_default_user_to_another_user_with_default_user_token(self):
        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "default_user_impediment"
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, default_task_dict["id"],
                                                                         default_sprint_dict["id_sprint"], default_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating alternative user
        alternative_user_name = "alternative_user_to_alter_task"
        create_admin_response = self.aux_create_user(alternative_user_name, alternative_user_name)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for alternative user
        alternative_sprint_name = "alternative_user_sprint"
        alternative_user_dict = self.aux_find_user_by_user_name(alternative_user_name)
        alternative_user_auth = self.aux_get_user_authorization(alternative_user_name, alternative_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(alternative_sprint_name, alternative_user_dict["id"],
                                                                 alternative_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        alternative_task_name = 'alternative_user_task'
        create_task_response = self.aux_create_task_for_user(alternative_task_name, alternative_user_dict["id"],
                                                             alternative_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing impediment from default user to alternative user
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        alternative_task_dict = self.aux_find_task_by_name(alternative_task_name)
        alternative_sprint_dict = self.aux_find_sprint_by_name(alternative_sprint_name)

        updated_impediment = self.aux_alter_impediment_task(impediment_dict, alternative_task_dict)
        updated_impediment = self.aux_alter_impediment_sprint(updated_impediment, alternative_sprint_dict)

        response = requests.put(self.url_impediment_list + str(impediment_dict["id"]), json.dumps(updated_impediment),
                                headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_impediment_from_default_user_to_admin_with_admin_user_token(self):
        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "default_user_impediment"
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, default_task_dict["id"],
                                                                         default_sprint_dict["id_sprint"], default_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing impediment from default user to admin user
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)

        updated_impediment = self.aux_alter_impediment_task(impediment_dict, admin_task_dict)
        updated_impediment = self.aux_alter_impediment_sprint(updated_impediment, admin_sprint_dict)

        response = requests.put(self.url_impediment_list + str(impediment_dict["id"]), json.dumps(updated_impediment),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)

        # restoring impediment
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        old_task_dict = self.aux_find_task_by_name(default_task_name)
        old_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)

        restored_impediment = self.aux_alter_impediment_task(impediment_dict, old_task_dict)
        restored_impediment = self.aux_alter_impediment_sprint(restored_impediment, old_sprint_dict)

        response = requests.put(self.url_impediment_list + str(impediment_dict["id"]), json.dumps(restored_impediment),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)


    def test_set_impediment_from_admin_user_to_default_user_without_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # creating impediment for admin user
        impediment_name = "admin_user_impediment"
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, admin_task_dict["id"],
                                                                         admin_sprint_dict["id_sprint"], admin_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing impediment from admin user to default user
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)

        updated_impediment = self.aux_alter_impediment_task(impediment_dict, default_task_dict)
        updated_impediment = self.aux_alter_impediment_sprint(updated_impediment, default_sprint_dict)

        response = requests.put(self.url_impediment_list + str(impediment_dict["id"]), json.dumps(updated_impediment))
        self.assertEquals(response.status_code, 401)

    def test_set_impediment_from_admin_user_to_default_user_with_invalid_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # creating impediment for admin user
        impediment_name = "admin_user_impediment"
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, admin_task_dict["id"],
                                                                         admin_sprint_dict["id_sprint"], admin_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing impediment from admin user to default user
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)

        updated_impediment = self.aux_alter_impediment_task(impediment_dict, default_task_dict)
        updated_impediment = self.aux_alter_impediment_sprint(updated_impediment, default_sprint_dict)

        response = requests.put(self.url_impediment_list + str(impediment_dict["id"]), json.dumps(updated_impediment), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_set_impediment_from_admin_user_to_default_user_with_default_user_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # creating impediment for admin user
        impediment_name = "admin_user_impediment"
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, admin_task_dict["id"],
                                                                         admin_sprint_dict["id_sprint"], admin_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing impediment from admin user to default user
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)

        updated_impediment = self.aux_alter_impediment_task(impediment_dict, default_task_dict)
        updated_impediment = self.aux_alter_impediment_sprint(updated_impediment, default_sprint_dict)

        response = requests.put(self.url_impediment_list + str(impediment_dict["id"]), json.dumps(updated_impediment),
                                headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_set_impediment_from_admin_user_to_another_admin_user_with_admin_user_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_alter_task"
        create_admin_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # creating impediment for admin user
        impediment_name = "admin_user_impediment"
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, admin_task_dict["id"],
                                                                         admin_sprint_dict["id_sprint"], admin_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating alternative admin
        alternative_admin_user_name = "alternative_admin_to_test_impediment"
        create_user_response = self.aux_create_user(alternative_admin_user_name, alternative_admin_user_name, is_admin=True)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for alternative admin
        alternative_admin_sprint_name = "default_user_sprint"
        alternative_admin_user_dict = self.aux_find_user_by_user_name(alternative_admin_user_name)
        alternative_admin_auth = self.aux_get_user_authorization(alternative_admin_user_name, alternative_admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(alternative_admin_sprint_name, alternative_admin_user_dict["id"],
                                                                 alternative_admin_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for alternative admin
        alternative_admin_task_name = 'alternative_admin_user_task'
        create_task_response = self.aux_create_task_for_user(alternative_admin_task_name, alternative_admin_user_dict["id"],
                                                             alternative_admin_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        # changing impediment from admin user to alternative admin user
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        alternative_admin_task_dict = self.aux_find_task_by_name(alternative_admin_task_name)
        alternative_admin_sprint_dict = self.aux_find_sprint_by_name(alternative_admin_sprint_name)

        updated_impediment = self.aux_alter_impediment_task(impediment_dict, alternative_admin_task_dict)
        updated_impediment = self.aux_alter_impediment_sprint(updated_impediment, alternative_admin_sprint_dict)

        response = requests.put(self.url_impediment_list + str(impediment_dict["id"]), json.dumps(updated_impediment),
                                headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 401)


    # default user impediment is a impediment binded to a default user task and a default user sprint
    def test_delete_default_user_impediment_without_token(self):
        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"], default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "default_user_impediment"
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, default_task_dict["id"], default_sprint_dict["id_sprint"], default_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        response = requests.delete(self.url_impediment_list + str(impediment_dict["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_impediment_with_invalid_token(self):
        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "default_user_impediment"
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, default_task_dict["id"],
                                                                         default_sprint_dict["id_sprint"], default_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        response = requests.delete(self.url_impediment_list + str(impediment_dict["id"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_impediment_with_default_user_token_self_impediment(self):
        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "default_user_impediment"
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, default_task_dict["id"],
                                                                         default_sprint_dict["id_sprint"], default_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        response = requests.delete(self.url_impediment_list + str(impediment_dict["id"]),
                                   headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 204)

    def test_delete_default_user_impediment_with_default_user_token_another_user_impediment(self):
        """
        Alternative dafault user trying to delete dafault user impediment
        """
        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "default_user_impediment"
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, default_task_dict["id"],
                                                                         default_sprint_dict["id_sprint"], default_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating alternative user
        alternative_user_name = "alternative_user_to_test_impediment"
        create_alternative_user_response = self.aux_create_user(alternative_user_name, alternative_user_name)
        self.assertIn(create_alternative_user_response.status_code, [201, 400])

        alternative_user_auth = self.aux_get_user_authorization(alternative_user_name, alternative_user_name)
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        response = requests.delete(self.url_impediment_list + str(impediment_dict["id"]),
                                   headers={"Authorization": alternative_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_default_user_impediment_with_admin_user_token(self):
        """
        Admin dafault user trying to delete dafault user task
        """
        # creating default user
        default_user_name = "default_user_to_test_impediment"
        create_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_user_response.status_code, [201, 400])

        # creating sprint for default user
        default_sprint_name = "default_user_sprint"
        default_user_dict = self.aux_find_user_by_user_name(default_user_name)
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(default_sprint_name, default_user_dict["id"],
                                                                 default_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for default user
        default_task_name = 'default_user_task'
        create_task_response = self.aux_create_task_for_user(default_task_name, default_user_dict["id"],
                                                             default_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "default_user_impediment"
        default_task_dict = self.aux_find_task_by_name(default_task_name)
        default_sprint_dict = self.aux_find_sprint_by_name(default_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, default_task_dict["id"],
                                                                         default_sprint_dict["id_sprint"], default_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        # creating alternative user
        admin_user_name = "admin_user_to_test_impediment"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [201, 400])

        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        response = requests.delete(self.url_impediment_list + str(impediment_dict["id"]),
                                   headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)


    def test_delete_admin_user_impediment_without_token(self):
        # creating admin user
        admin_user_name = "admin_user_to_test_impediment"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "admin_user_impediment"
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, admin_task_dict["id"],
                                                                         admin_sprint_dict["id_sprint"], admin_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        response = requests.delete(self.url_impediment_list + str(impediment_dict["id"]))
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_sprint_with_invalid_token(self):
        ## creating admin user
        admin_user_name = "admin_user_to_test_impediment"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "admin_user_impediment"
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, admin_task_dict["id"],
                                                                         admin_sprint_dict["id_sprint"], admin_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        response = requests.delete(self.url_impediment_list + str(impediment_dict["id"]), headers={"Authorization": INVALID_AUTH})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_impediment_with_default_user_token(self):
        """
        Default user trying to delete admin task
        """
        ## creating admin user
        admin_user_name = "admin_user_to_test_impediment"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "admin_user_impediment"
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, admin_task_dict["id"],
                                                                         admin_sprint_dict["id_sprint"], admin_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        ## creating default user
        default_user_name = "default_user_to_test_impediment"
        create_default_user_response = self.aux_create_user(default_user_name, default_user_name)
        self.assertIn(create_default_user_response.status_code, [201, 400])
        default_user_auth = self.aux_get_user_authorization(default_user_name, default_user_name)

        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        response = requests.delete(self.url_impediment_list + str(impediment_dict["id"]),
                                   headers={"Authorization": default_user_auth})
        self.assertEquals(response.status_code, 401)

    def test_delete_admin_user_impediment_with_admin_user_token_self_impediment(self):
        # creating admin user
        admin_user_name = "admin_user_to_test_impediment"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "admin_user_impediment"
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, admin_task_dict["id"],
                                                                         admin_sprint_dict["id_sprint"], admin_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        response = requests.delete(self.url_impediment_list + str(impediment_dict["id"]),
                                   headers={"Authorization": admin_user_auth})
        self.assertEquals(response.status_code, 204)

    def test_delete_admin_user_impediment_with_admin_user_token_another_admin_impediment(self):
        """
        Alternative admin user trying to delete admin impediiment
        """
        # creating admin user
        admin_user_name = "admin_user_to_test_impediment"
        create_admin_user_response = self.aux_create_user(admin_user_name, admin_user_name, is_admin=True)
        self.assertIn(create_admin_user_response.status_code, [201, 400])

        # creating sprint for admin user
        admin_sprint_name = "admin_user_sprint"
        admin_user_dict = self.aux_find_user_by_user_name(admin_user_name)
        admin_user_auth = self.aux_get_user_authorization(admin_user_name, admin_user_name)
        create_sprint_response = self.aux_create_sprint_for_user(admin_sprint_name, admin_user_dict["id"],
                                                                 admin_user_auth)
        self.assertIn(create_sprint_response.status_code, [201, 400])

        # creating task for admin user
        admin_task_name = 'admin_user_task'
        create_task_response = self.aux_create_task_for_user(admin_task_name, admin_user_dict["id"],
                                                             admin_user_auth)
        self.assertIn(create_task_response.status_code, [201, 400])

        impediment_name = "admin_user_impediment"
        admin_task_dict = self.aux_find_task_by_name(admin_task_name)
        admin_sprint_dict = self.aux_find_sprint_by_name(admin_sprint_name)
        create_impediment_response = self.aux_create_impediment_for_user(impediment_name, admin_task_dict["id"],
                                                                         admin_sprint_dict["id_sprint"], admin_user_auth)
        self.assertIn(create_impediment_response.status_code, [201, 400])

        alternative_admin_name = "alternative_admin_user_to_test_impediment"
        create_alternative_admin_user_response = self.aux_create_user(alternative_admin_name, alternative_admin_name, is_admin=True)
        self.assertIn(create_alternative_admin_user_response.status_code, [201, 400])
        alternative_admin_user_auth = self.aux_get_user_authorization(alternative_admin_name, alternative_admin_name)

        impediment_dict = self.aux_find_impediment_by_name(impediment_name)
        response = requests.delete(self.url_impediment_list + str(impediment_dict["id"]),
                                   headers={"Authorization": alternative_admin_user_auth})
        self.assertEquals(response.status_code, 401)
