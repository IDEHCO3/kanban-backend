import sys, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kanban.settings") # HARDCODED
django.setup()

from scrum.models import ScrumUser

NO_COMMAND_ERROR_MESSAGE = """
command:
    createsuperuser
"""

def prepare_create_super_user_command():
    user_name = input("User name: ")
    password = input("Password: ")

    #try:
    create_super_user(user_name, password)
    return True
    #except:
    #    return False

COMMAND_LINE_INTERFACE_OPERATIONS = {
    "createsuperuser": prepare_create_super_user_command
}

def create_super_user(user_name, password, name='', email=None, description='', avatar='', active=True, role="admin"):
    ScrumUser.objects.create(**{
        "user_name": user_name,
        "password": password,
        "name": name,
        "email": email,
        "description": description,
        "avatar": avatar,
        "active": active,
        "role": role
    })
    '''
    name = models.CharField(max_length=100, default='')

    email = models.CharField(unique=True, max_length=100, null=True)

    password = models.CharField(unique=True, max_length=100)

    description = models.TextField(blank=True, null=True, default='')
    role = models.CharField(max_length=100, blank=True, default='user')
    avatar = models.CharField(max_length=200, blank=True, default='')
    active = models.NullBooleanField()

    user_name = models.CharField(unique=True, max_length=100)
    '''


def main(argv):

    size_of_arguments = len(argv)
    if size_of_arguments < 2:
        print('Usage: python hyper_config.py <command>')
        print(NO_COMMAND_ERROR_MESSAGE)
        exit()

    command = argv[1]
    result = COMMAND_LINE_INTERFACE_OPERATIONS[command]()
    if result:
        print("Success")
    else:
        print("Error")

if __name__ == "__main__":
    main(sys.argv)