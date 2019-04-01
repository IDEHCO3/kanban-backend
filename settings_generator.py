import sys
import django
from settings_template import *
import re
import importlib
from generator_files import ALLOWED_DATABASES

def rawInput(str):
    #inputOperation = None
    try: inputOperation = raw_input
    except NameError: inputOperation = input
    return inputOperation(str)

def marge_list_elements(default_installed_apps, template_instaled_apps, app_name):
    all_apps = []

    [all_apps.append(app) for app in default_installed_apps if app not in all_apps]
    [all_apps.append(app) for app in template_instaled_apps if app not in all_apps]

    if app_name not in all_apps:
        all_apps.append(app_name)

    installed_apps = "\n\nINSTALLED_APPS = [\n"
    for app in all_apps:
        installed_apps += 4 * " " + "'" + app + "',\n"

    installed_apps += "]"
    return installed_apps

def postgres_database(sgbd_ip, sgbd_port, db_name, db_username, db_password, schemas):

    if type(schemas) == list:
        string_schemas = ','.join(schemas)
    else:
        string_schemas = 'public'

    postgres_db_snippet = "\n\nDATABASES = {\n"
    postgres_db_snippet += "\t'default': {\n"
    postgres_db_snippet += "\t\t'ENGINE': 'django.contrib.gis.db.backends.postgis',\n"
    postgres_db_snippet += "\t\t'OPTIONS': {\n"
    postgres_db_snippet += "\t\t\t'options': '-c search_path=" + string_schemas + "',\n"
    postgres_db_snippet += "\t\t},\n"

    postgres_db_snippet += "\n\t\t'HOST': '" + sgbd_ip + "',\n"#ip_sgbd,\n"
    postgres_db_snippet += "\t\t'PORT': '" + sgbd_port + "',\n"#port_sgbd,\n"
    postgres_db_snippet += "\t\t'NAME': '" + db_name + "',\n"#db_name,\n"
    postgres_db_snippet += "\t\t'USER': '" + db_username + "',\n"#user,\n"
    postgres_db_snippet += "\t\t'PASSWORD': '" + db_password + "'\n"#password\n"
    postgres_db_snippet += "\t}\n"
    postgres_db_snippet += "}"
    return postgres_db_snippet

def sqlite_database():
    sqlite_database_snippet = "\n\nDATABASES = {\n"
    sqlite_database_snippet += "\t'default': {\n"
    sqlite_database_snippet += "#GENERATED\n"
    sqlite_database_snippet += "\t\t'ENGINE': 'django.db.backends.sqlite3',\n"
    sqlite_database_snippet += "\t\t'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),\n"
    sqlite_database_snippet += "\t}\n"
    sqlite_database_snippet += "}"
    return sqlite_database_snippet

def search_line_in_settings(list_of_lines, keyword):
    # if endswith('\') searc in next line
    line = [line for line in list_of_lines if keyword in line and not line.startswith('#')][0]
    return "\n" + line

def get_struct_as_string(list_of_lines, keyword):
    #Inicia a lista na linha onde tiver a 'keyword' e finaliza na linha que tiver ^\]\\n$
    store_lines = False
    snippet = ''

    # default wrapper caracters (delimeters of list)
    delimeter_caracter_ini = '['
    delimeter_caracter_final = ']'
    delimeter_caracter_count = 0

    for line in list_of_lines:
        # starts to store the lines only when find a line with the 'keyword'
        if keyword in line:
            store_lines = True
            #the last caracter of the matched string will be the initial caracter delimeter
            delimeter_caracter_ini = re.search(r'=\s*[{([]', line).group()[-1]

            # the ']' ascii code is +2 of '[', the same for '{' and '}'
            delimeter_caracter_final = ')' if delimeter_caracter_ini == '(' else chr(ord(delimeter_caracter_ini) + 2)

        if store_lines:
            snippet += line

            if delimeter_caracter_ini in line:
                delimeter_caracter_count += 1
            if delimeter_caracter_final in line:
                delimeter_caracter_count -= 1

            # if 'delimeter_caracter_count' reach 0 it means that
            # the number of OPEN strutures caracters and CLOSE structures
            # caracters is the same (i.e. a complete data structure)
            if delimeter_caracter_count == 0:
                break

    return "\n\n" + snippet

def get_line_from_settings(environment_variable, original_settings_variables_list, original_settings_all_lines, template_settings_all_lines):
    # if 'environment_variable' isn't present in original settings.py, insert the 'environment_variable' from template
    if environment_variable not in original_settings_variables_list:
        line = search_line_in_settings(template_settings_all_lines, environment_variable)
    # otherwise, if this exists on original file, get it from original file and insert into new settings.py
    else:
        # gets the first line that contains 'environment_variable' and not starts with '#' (commentary)
        line = search_line_in_settings(original_settings_all_lines, environment_variable)

    return line

def get_struct_from_settings(environment_variable, original_settings_variables_list, original_settings_all_lines, template_settings_all_lines):
    if environment_variable not in original_settings_variables_list:
        struct = get_struct_as_string(template_settings_all_lines, environment_variable)
    else:
        struct = get_struct_as_string(original_settings_all_lines, environment_variable)

    return struct

def generate_file(package_name, app_name, generate_db='sqlite'):
    original_settings_path = package_name + '/settings.py'
    original_settings_path_dot_notation = package_name + '.settings'

    if os.path.isfile(package_name + '/original_settings.py'):
        original_settings_path = package_name + '/original_settings.py'
        original_settings_path_dot_notation = package_name + '.original_settings'


    with open(original_settings_path, 'r') as original_settings_file: # settings.py generated by django
        with open('settings_template.py', 'r') as template_setting_file:

            # the original settings.py module (created by django)
            original_settings_module = importlib.import_module(original_settings_path_dot_notation)

            # 'original_settings_variables_list' is a list of all variables in original settings.py file
            original_settings_variables_list = dir(original_settings_module)

            # 'orignal_settings_all_lines' is a list of all lines in the original settings.py file
            orignal_settings_all_lines = original_settings_file.readlines()
            template_settings_all_lines = template_setting_file.readlines()

            new_settings_data = 'import os'
            new_settings_data += get_line_from_settings('BASE_DIR', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('SECRET_KEY', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('DEBUG', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            project_name_line = get_line_from_settings('PROJECT_NAME', original_settings_variables_list,
                                                        orignal_settings_all_lines,
                                                       template_settings_all_lines).replace('A-PROJECT-NAME-TO-REPLACE', package_name)
            new_settings_data += project_name_line


            # ALLOWED_HOSTS will be writed (in the new settings.py) regardless this is in settings.py or not
            allowed_hosts_line = search_line_in_settings(template_settings_all_lines, 'ALLOWED_HOSTS')
            new_settings_data += allowed_hosts_line


            new_settings_data += get_line_from_settings('APPEND_SLASH', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('TOKEN_NEED', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += marge_list_elements(original_settings_module.INSTALLED_APPS, INSTALLED_APPS, app_name)


            #new_settings_data += marge_middleware_classes(original_settings_module.MIDDLEWARE, MIDDLEWARE_CLASSES)
            # the 'MIDDLEWARE' code will always comes from the settings_template because of the required middlewers order
            middleware_struct = get_struct_as_string(template_settings_all_lines, 'MIDDLEWARE')
            new_settings_data += middleware_struct


            new_settings_data += get_line_from_settings('ROOT_URLCONF', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_struct_from_settings('CORS_ALLOW_HEADERS', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('CORS_ORIGIN_ALLOW_ALL', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_struct_from_settings('CORS_EXPOSE_HEADERS', original_settings_variables_list,
                                                          orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_struct_from_settings('TEMPLATES', original_settings_variables_list,
                                                          orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('WSGI_APPLICATION', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            if generate_db == 'sqlite':
                if 'DATABASES' in original_settings_variables_list:# (correct is 'not') inverted logic by test purposes
                    databases_struct = get_struct_as_string(orignal_settings_all_lines, 'DATABASES')
                    new_settings_data += databases_struct
                else:
                    new_settings_data += sqlite_database()

            elif generate_db == 'postgres' or generate_db == 'postgresql':
                sgbd_ip = rawInput("Database IP (leave blank to 'localhost'): ")
                sgbd_ip = 'localhost' if sgbd_ip == None or sgbd_ip == '' else sgbd_ip
    
                sgbd_port = rawInput("Database PORT (leave blank to '5432'): ")
                sgbd_port = '5432' if sgbd_port == None or sgbd_port == '' else sgbd_port
    
                db_name = rawInput("Database NAME: ")
                db_name = 'REPLACE-TO-DATABASE-NAME' if db_name == None or db_name == '' else db_name
    
                db_username = rawInput("Database USERNAME (leave blank to 'postgres'): ")
                db_username = 'postgres' if db_username == None or db_username == '' else db_username
    
                db_password = rawInput("Database PASSWORD: ")
                schemas = rawInput("Type all schema database names separated by space or leave blank to public: ")
                schemas = 'public' if schemas == None or schemas == '' else schemas.split(' ')

                new_settings_data += postgres_database(sgbd_ip, sgbd_port, db_name, db_username, db_password, schemas)

            else:
                with open(package_name + '/settings.py', 'r') as current_settings:
                    current_settings_all_lines = current_settings.readlines()
                    databases_struct = get_struct_as_string(current_settings_all_lines, 'DATABASES')

                #if 'DATABASES' in original_settings_variables_list:
                if databases_struct != None and databases_struct != '':
                    new_settings_data += databases_struct
                else:
                    new_settings_data += "# --- NO DATABASES CONFIGURATION ---"


            new_settings_data += get_struct_from_settings('AUTH_PASSWORD_VALIDATORS', original_settings_variables_list,
                                                          orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('LANGUAGE_CODE', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('TIME_ZONE', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('USE_I18N', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('USE_L10N', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('USE_TZ', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


            new_settings_data += get_line_from_settings('STATIC_URL', original_settings_variables_list,
                                                        orignal_settings_all_lines, template_settings_all_lines)


    with open(package_name + '/new_settings.py', 'w') as new_settings:
        new_settings.write(new_settings_data)

    if not os.path.isfile(package_name + '/original_settings.py'):
        os.rename(package_name + '/settings.py', package_name + '/original_settings.py')

    if os.path.isfile(package_name + '/settings.py'):
        os.remove(package_name + '/settings.py')
    os.rename(package_name + '/new_settings.py', package_name + '/settings.py')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python settings_generator.py django_project_name django_app_name")
        exit()

    prj_name = sys.argv[1]
    app_name = sys.argv[2]

    generate_db = input('What database do i have to generate? (Leave blank to keep the databases original settings): ')
    if generate_db.lower() not in ALLOWED_DATABASES:
        print('Database option not allowed, keeping the original database configuration')

    generate_file(prj_name, app_name, generate_db.lower())

    # informs django wich is de settings file
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", prj_name + '.settings')
    # reloads the configuration
    django.setup()
    print("settings.py has generated")