#Test
import os
import sys, inspect, importlib
import ast
ALLOWED_DATABASES = ['postgres', 'postgresql', 'sqlite', '']


def rawInput(str):
    inputOperation = None
    try: inputOperation = raw_input
    except NameError: inputOperation = input
    return inputOperation(str)

def main(argv):

    has_to_generate_settings = True

    size_of_arguments = len(argv)
    if size_of_arguments < 3:
        print('Usage: python generator_models_settings_files.py django_project_name django_app_name [True|False]')
        exit()
    else:
        print('-------------------------------------------------------------------------------------------------------')
        print('Generating file: models.py and settings.py. Parameter default is True, otherwise only models.py')
        print('-------------------------------------------------------------------------------------------------------')

    prj_name = argv[1]
    app_name = argv[2]

    if size_of_arguments > 3:
       has_to_generate_settings = ast.literal_eval(argv[3])

    from settings_generator import generate_file as gf_settings

    if has_to_generate_settings:
        generate_db = rawInput('What database do i have to generate? (Leave blank to keep the original settings database): ')
        if generate_db.lower() not in ALLOWED_DATABASES:
            print('Database option not allowed, keeping the original database configuration')
        gf_settings(prj_name, app_name, generate_db.lower())

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", prj_name + ".settings")

    import django
    django.setup()
    from urler_project_generator import generate_file as gf_prj_urler
    from modeler_generator import generate_file as gf_modeler
    from django.conf import settings

    file_model_app = app_name + '/models.py'
    os.system("python manage.py inspectdb > "+file_model_app)
    print('All files have been generated')

if __name__ == "__main__":
    main(sys.argv)