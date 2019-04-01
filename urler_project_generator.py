import sys
import os
import django


def generate_snippets_to_url(a_name, context_name = 'include'):
    arr = []
    arr.append((' ' * 4) + 'url(r' + "'" + '^api/'+ a_name.replace('_', '-') +'-list/'+ "'" +',' + context_name +'(' +"'" +a_name+'.urls'+"'" +
               ',namespace='+"'"+ a_name+"'" +')),\n')
    '''
    arr.append((' ' * 4) + 'url(r' + "'" + '^'+ a_name +'-list/contexts/' + "'" +','+ context_name + '(' + "'"+ 'context_api.urls' +"'"+
              ', namespace =' +"'" + 'context'+"'" + ')),\n')
    arr.append((' ' * 4) + 'getHydraVocabURLPatterns(r' + "'" + "^" + a_name + '-list/hydra/' + "'" + '),\n')
    '''
    return arr


def imports_str_as_array(a_name):

    arr = []
    arr.append("from django.conf.urls import include, url\n")
    #arr.append("from hydra.urls import getHydraVocabURLPatterns\n\n")

    return arr


def generate_file(prj_name, app_name, default_name='urls.py'):
    with open(default_name, 'w+') as sr:
        for import_str in imports_str_as_array(app_name):
            sr.write(import_str)
        sr.write('\napp_name="' + prj_name + '"\n\n')
        sr.write( 'urlpatterns = (\n\n')
        for str in generate_snippets_to_url(app_name):
            sr.write(str)
        sr.write('\n')
        sr.write('\n)\n')
        #sr.write('urlpatterns += (\n\n')
        #sr.write((' ' * 4) + 'url(r' + "'" +'^api-auth/'+"'"+ ', include('+"'"+'rest_framework.urls'+"'"+ ',namespace='+"'"+'rest_framework'+"'"+')),\n')
        #sr.write('\n)\n')
        sr.write('\n\n')
        sr.close()


if __name__ == "__main__":
    if (len( sys.argv))!= 3:
        print('Usage: python viewer_generator.py django_project_name django_app_name')
        exit()

    prj_name = sys.argv[1]
    app_name = sys.argv[2]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", prj_name + ".settings")
    django.setup()
    generate_file(app_name)
    print('urls.py  has been generated')