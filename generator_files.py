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
    has_to_generate_views  = True
    has_to_generate_urls  = True
    has_to_generate_serializers  = True
    has_to_generate_contexters  = True

    size_of_arguments = len(argv)
    if size_of_arguments < 3:
        print('Usage: python generator_files.py django_project_name django_app_name')
        exit()
    else:
        print('-------------------------------------------------------------------------------------------------------')
        print('Changing models.py and generating files: urls.py,views.py, serializers.py e contexts.py')
        print('-------------------------------------------------------------------------------------------------------')

    prj_name = argv[1]
    app_name = argv[2]

    if size_of_arguments > 3:
        has_to_generate_views = ast.literal_eval(argv[3])
    if size_of_arguments > 4:
        has_to_generate_urls = ast.literal_eval(argv[4])
    if size_of_arguments > 5:
        has_to_generate_serializers = ast.literal_eval(argv[5])
    if size_of_arguments > 6:
        has_to_generate_contexters = ast.literal_eval(argv[6])

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", prj_name + ".settings")

    import django
    django.setup()
    from urler_project_generator import generate_file as gf_prj_urler
    from viewer_generator import generate_file as gf_viewer
    from urler_generator import generate_file as gf_urler
    from serializer_generator import generate_file as gf_serializer
    from contexter_generator import generate_file as gf_contexter
    from modeler_generator import generate_file as gf_modeler
    from django.conf import settings

    file_model_app = app_name + '/models.py'
    gf_modeler(app_name, file_model_app)

    if has_to_generate_views:
        file_view = app_name + '/views.py'
        gf_viewer(app_name, default_name=file_view)

    if has_to_generate_urls:
        file_url_prj = prj_name + '/urls.py'
        gf_prj_urler(prj_name, app_name, default_name=file_url_prj)
        file_url_app = app_name + '/urls.py'
        gf_urler(app_name, default_name=file_url_app)

    if has_to_generate_serializers:
        file_serializer_app = app_name + '/serializers.py'
        gf_serializer(app_name, default_name=file_serializer_app)

    if has_to_generate_contexters:
        file_contexter_app = app_name + '/contexts.py'
        gf_contexter(app_name, default_name=file_contexter_app)

    print('All files have been generated')


if __name__ == "__main__":
    main(sys.argv)