import requests, os, sys
#se'rvidor = ''
#servidor = 'http://LUC00557347.ibge.gov.br/'
SERVER = 'http://LUC00557196:8000/'
#SERVER = "http://172.30.11.72:8000/"

class RequestTest():
    def __init__(self, uri, expec_status_code, method='GET', default_server=SERVER):
        self.method = method
        self.uri = default_server + uri
        self.expec_status_code = expec_status_code

arr_get_for_non_spatial_resource = [
    RequestTest("controle-list/usuario-list/1/", 200),
    RequestTest("controle-list/usuario-list/1/nome,email", 200),
    RequestTest("controle-list/usuario-list/1/projection/nome,email", 200),
]

arr_get_for_collection = [
    RequestTest('controle-list/gasto-list/count-resource', 200),
    RequestTest('controle-list/gasto-list/offset-limit/1&10', 200),
    RequestTest('controle-list/gasto-list/offset-limit/1&10/data,valor', 400),
    RequestTest('controle-list/gasto-list/group-by-count/tipo_gasto', 200),
    RequestTest('controle-list/gasto-list/filter/tipo_gasto/eq/3', 200),
    RequestTest('api/bcim/unidades-federativas/filter/geom/within/' + SERVER + 'api/bcim/municipios/3159407/geom/*', 200),
    RequestTest('api/bcim/unidades-federativas/?*contains=POINT(-42 -21)', 200),
    RequestTest('api/bcim/unidades-federativas/?*contains=POINT(-42 -21)&sigla=RJ', 200),
    RequestTest('api/bcim/unidades-federativas/?*contains=URL&sigla=RJ', 200),
    RequestTest('api/bcim/unidades-federativas/contains/POINT(-42 -21)', 200),
    RequestTest('api/bcim/aldeias-indigenas/within/POLYGON((-41.8 -21.2,-41.8 -17.8,-28.8 -17.8,-28.8 -21.,-41.8 -21.2))/', 200),
    RequestTest('api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*', 200),
    RequestTest('api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/PA/*', 200),
    RequestTest('api/bcim/unidades-federativas/filter/sigla/in/ES&PA/', 200),
    RequestTest('api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*or/within/' + SERVER + 'api/bcim/unidades-federativas/PA/*', 200),
    RequestTest('api/bcim/aldeias-indigenas/filter/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/PA/*', 200),
    RequestTest('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*', 200),
    RequestTest('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*', 200),
    RequestTest('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*', 200),
    RequestTest('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*', 200),
    RequestTest('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*', 200),
    RequestTest('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*or/' + SERVER + 'api/bcim/unidades-federativas/PR/*', 200),
    RequestTest('api/bcim/municipios/within/{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}', 200),
    RequestTest('api/bcim/municipios/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*', 200),
    RequestTest('api/bcim/municipios/filter/geom/overlaps/' + SERVER + 'api/bcim/unidades-federativas/ES/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*and/geocodigo/startswith/32/', 200),
    RequestTest('api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/PA/', 200),
    RequestTest('api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/PA', 200),
    RequestTest('api/bcim/aldeias-indigenas/collect/nome&geom/buffer/0.5', 200),
    RequestTest('api/bcim/unidades-federativas/filter/sigla/in/RJ&ES/*collect/nome&geom/buffer/0.2', 200),
    RequestTest('api/bcim/aldeias-indigenas/offset-limit/0&2/nome,geom,nomeabrev/*collect/nome&geom/buffer/0.5', 400), # WRONG SINTAX (SERVER EXECUTE ONLY api/bcim/aldeias-indigenas/offset-limit/0/2/ and ignore the rest - act as offset-limit operation)
    RequestTest('api/bcim/aldeias-indigenas/offset-limit/0&2/nome,geom/*collect/geom/buffer/0.5', 400), # WRONG SINTAX (SERVER EXECUTE ONLY api/bcim/aldeias-indigenas/offset-limit/0/2/ and ignore the rest - act as offset-limit operation)
]

arr_get_for_spatial_operations = [
    RequestTest("api/bcim/unidades-federativas/ES/area", 200),
    RequestTest("api/bcim/unidades-federativas/ES/boundary", 200),
    RequestTest("api/bcim/unidades-federativas/ES/buffer/0.2", 200),
    RequestTest("api/bcim/unidades-federativas/ES/centroid", 200),
    RequestTest("api/bcim/unidades-federativas/ES/contains/" + SERVER + "api/bcim/aldeias-indigenas/587/", 200),
    RequestTest("api/bcim/unidades-federativas/ES/convex_hull", 200),
    RequestTest("api/bcim/aldeias-indigenas/587/coords", 200),
    RequestTest("api/bcim/trechos-hidroviarios/59121/crosses/" + SERVER + "api/bcim/municipios/3126406", 200),
    RequestTest("api/bcim/unidades-federativas/RJ/difference/" + SERVER + "api/bcim/municipios/3304300/", 200),
    RequestTest("api/bcim/unidades-federativas/ES/dims", 200),
    RequestTest("api/bcim/aldeias-indigenas/589/disjoint/" + SERVER + "api/bcim/unidades-federativas/RJ/", 200),
    RequestTest("api/bcim/unidades-federativas/ES/distance/" + SERVER + "api/bcim/unidades-federativas/AM/", 200),
    RequestTest("api/bcim/unidades-federativas/ES/empty", 200),
    RequestTest("api/bcim/unidades-federativas/ES/envelope", 200),
    RequestTest("api/bcim/unidades-federativas/ES/equals/" + SERVER + "api/bcim/unidades-federativas/ES/", 200),
    RequestTest("api/bcim/unidades-federativas/ES/equals_exact/" + SERVER + "api/bcim/unidades-federativas/ES/", 200),
    RequestTest("api/bcim/unidades-federativas/ES/ewkb", 200),
    RequestTest("api/bcim/unidades-federativas/ES/ewkt", 200),
    RequestTest("api/bcim/unidades-federativas/ES/extent", 200),
    RequestTest("api/bcim/unidades-federativas/ES/geom_type", 200),
    RequestTest("api/bcim/unidades-federativas/ES/geom_typeid", 200),
    RequestTest("api/bcim/unidades-federativas/ES/hasz", 200),
    RequestTest("api/bcim/unidades-federativas/ES/hex", 200),
    RequestTest("api/bcim/unidades-federativas/ES/hexewkb", 200),
    RequestTest("api/bcim/unidades-federativas/ES/intersection/" + SERVER + "api/bcim/unidades-federativas/RJ/envelope/", 200),
    RequestTest("api/bcim/unidades-federativas/ES/intersects/" + SERVER + "api/bcim/unidades-federativas/RJ/", 200),
    RequestTest("api/bcim/aldeias-indigenas/587/json", 200),
    RequestTest("api/bcim/aldeias-indigenas/587/kml", 200),
    RequestTest("api/bcim/trechos-hidroviarios/59121/length", 200),
    RequestTest("api/bcim/unidades-federativas/ES/num_geom", 200),
    RequestTest("api/bcim/municipios/3301009/overlaps/" + SERVER + "api/bcim/unidades-federativas/ES", 200),
    RequestTest("api/bcim/unidades-federativas/ES/point_on_surface", 200),
    RequestTest("api/bcim/unidades-federativas/ES/relate/" + SERVER + "api/bcim/unidades-federativas/GO/", 200),
    RequestTest("api/bcim/unidades-federativas/ES/relate_pattern/" + SERVER + "api/bcim/unidades-federativas/GO/&FF*FF****", 200),
    RequestTest("api/bcim/trechos-hidroviarios/59121/ring", 200),
    RequestTest("api/bcim/unidades-federativas/ES/simple", 200),
    RequestTest("api/bcim/unidades-federativas/ES/simplify/0.0&False", 200),
    RequestTest("api/bcim/unidades-federativas/ES/srid", 200),
    RequestTest("api/bcim/unidades-federativas/ES/srs", 200),
    RequestTest("api/bcim/vegetacoes-de-restinga/2947/sym_difference/" + SERVER + "api/bcim/unidades-federativas/ES", 200),
    RequestTest("api/bcim/unidades-federativas/AM/touches/" + SERVER + "api/bcim/unidades-federativas/RJ/", 200),
    RequestTest("api/bcim/unidades-federativas/ES/transform/4326&false", 200),
    RequestTest("api/bcim/unidades-federativas/ES/union/" + SERVER + "api/bcim/unidades-federativas/RJ", 200),
    RequestTest("api/bcim/unidades-federativas/ES/valid", 200),
    RequestTest("api/bcim/unidades-federativas/ES/valid_reason", 200),
    RequestTest("api/bcim/aldeias-indigenas/587/within/" + SERVER + "api/bcim/unidades-federativas/ES/", 200),
    RequestTest("api/bcim/unidades-federativas/ES/wkb", 200),
    RequestTest("api/bcim/unidades-federativas/ES/wkt", 200),
    RequestTest("api/bcim/aldeias-indigenas/589/x", 200),
    RequestTest("api/bcim/aldeias-indigenas/589/y", 200),
    RequestTest("api/bcim/aldeias-indigenas/589/z", 200),
    RequestTest("api/bcim/trechos-hidroviarios/59121/x", 200),
    RequestTest("api/bcim/trechos-hidroviarios/59121/y", 200),
    RequestTest("api/bcim/trechos-hidroviarios/59121/z", 200),
]

arr_get_for_projection = [
    # only attributes
    RequestTest("api/bcim/unidades-federativas/nome", 200),
    RequestTest("api/bcim/unidades-federativas/nome/", 200),
    RequestTest("api/bcim/unidades-federativas/nome,geom", 200),
    RequestTest("api/bcim/unidades-federativas/nome,geom/", 200),
    RequestTest("api/bcim/unidades-federativas/projection/nome,geocodigo", 200), # attributes and projection
    RequestTest("api/bcim/unidades-federativas/projection/nome,geocodigo/", 200),
    # filter
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES", 200),
    RequestTest("api/bcim/unidades-federativas/projection/nome,geocodigo/filter/sigla/in/RJ&ES", 200),
    # collect
    RequestTest("api/bcim/unidades-federativas/collect/geom&nome/upper", 200),
    RequestTest("api/bcim/unidades-federativas/projection/geom,nome/collect/geom&nome/upper", 200),
    RequestTest("api/bcim/unidades-federativas/projection/sigla,geocodigo/collect/geom&nome/upper", 400), # collected attributes not in projection (must fail)
    RequestTest("api/bcim/unidades-federativas/projection/sigla,geocodigo/collect/geom&sigla/lower", 400), # operated attribute in projection but lists differs (priorize projection in this case)
    # count_resource
    RequestTest("api/bcim/unidades-federativas/count-resource", 200),
    RequestTest("api/bcim/unidades-federativas/projection/nome,geocodigo/count-resource", 200),
    # filter_and_collect
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES/*collect/geocodigo&sigla/lower", 200),
    RequestTest("api/bcim/unidades-federativas/projection/geocodigo,sigla/filter/sigla/in/RJ&ES/*collect/geocodigo&sigla/lower", 200),
    RequestTest("api/bcim/unidades-federativas/projection/geocodigo,sigla/filter/sigla/in/RJ&ES/*collect/sigla&geom/buffer/0.2", 400), # (must return status code 400)
    # filter_and_count_resource
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES/*count-resource", 200),
    RequestTest("api/bcim/unidades-federativas/projection/nome,geocodigo/filter/sigla/in/RJ&ES/*count-resource", 200),
    # offset_limit
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/", 200),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/nome,geocodigo/", 400),
    RequestTest("api/bcim/unidades-federativas/projection/geocodigo,sigla/offset-limit/0&2/", 200),
    RequestTest("api/bcim/unidades-federativas/projection/geocodigo,sigla/offset-limit/0&2/sigla,geocodigo/", 400),
    RequestTest("api/bcim/unidades-federativas/projection/geocodigo,sigla/offset-limit/0&2/nome,geocodigo,sigla/", 400), # WRONG SINTAX (SERVER EXECUTE ONLY api/bcim/unidades-federativas/projection/geocodigo,sigla/offset-limit/0/2/ and ignore the rest - act as offset-limit operation)
    # distinct
    RequestTest("controle-list/usuario-list/distinct/email", 200),
    RequestTest("controle-list/usuario-list/distinct/id&nome&email", 200),
    RequestTest("controle-list/usuario-list/projection/nome,email,data_nascimento/distinct/nome&email", 200),
    # offset_limit_and_collect
    RequestTest("api/bcim/unidades-federativas/offset-limit/5&2/collect/sigla&geom/buffer/0.8", 200),
    RequestTest("api/bcim/unidades-federativas/offset-limit/5&2/geom,sigla/*collect/sigla&geom/buffer/0.8", 400),
    RequestTest("api/bcim/unidades-federativas/offset-limit/5&2/sigla,geom,nome/*collect/sigla&geom/buffer/0.8", 400), # WRONG SINTAX (SERVER EXECUTE ONLY api/bcim/unidades-federativas/offset-limit/5/2/ and ignore the rest - act as offset-limit operation)
    RequestTest("api/bcim/unidades-federativas/projection/sigla,geom/offset-limit/5&2/collect/sigla&geom/buffer/0.8", 200),
    RequestTest("api/bcim/unidades-federativas/projection/sigla,geom/offset-limit/5&2/sigla,geocodigo/*collect/sigla&geom/buffer/0.8", 400), # projection list == collect list != offset_limit list # WRONG SINTAX (SERVER EXECUTE ONLY api/bcim/unidades-federativas/projection/sigla,geom/offset-limit/5/2/ and ignore the rest - act as offset-limit operation)
    RequestTest("api/bcim/unidades-federativas/projection/sigla,geom/offset-limit/5&2/sigla,geom/*collect/nome&sigla&geom/buffer/0.8", 400), # projection list == offset_limit list != collect list # WRONG SINTAX (SERVER EXECUTE ONLY api/bcim/unidades-federativas/projection/sigla,geom/offset-limit/5/2/ and ignore the rest - act as offset-limit operation)
    RequestTest("api/bcim/unidades-federativas/projection/sigla,geom/offset-limit/5&2/sigla,geom/collect/sigla&geom/buffer/0.8", 400), # projection list == offset_limit list == collect list # WRONG SINTAX (SERVER EXECUTE ONLY api/bcim/unidades-federativas/projection/sigla,geom/offset-limit/5/2/ and ignore the rest - act as offset-limit operation)

    #FeatureCollection operations
    RequestTest("api/bcim/aldeias-indigenas/within/" + SERVER + "api/bcim/unidades-federativas/ES/", 200),
    RequestTest("api/bcim/aldeias-indigenas/projection/nome,nomeabrev/within/" + SERVER + "api/bcim/unidades-federativas/ES/", 200),
    RequestTest("api/bcim/unidades-federativas/contains/" + SERVER + "api/bcim/aldeias-indigenas/623", 200),
    RequestTest("api/bcim/unidades-federativas/projection/sigla,geom/contains/" + SERVER + "api/bcim/aldeias-indigenas/623", 200),
]

arr_get_for_complex_requests = [
    #("api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/ES/*collect/geom/buffer/0.2/!union/(" + SERVER + "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/geom/buffer/0.2), 200),"
    RequestTest("api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/ES/*collect/geom/buffer/0.2/!union!/" + SERVER + "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/geom/buffer/0.2", 200),
    RequestTest("api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/ES/*collect/nome&geom/buffer/0.2/!union!/" + SERVER + "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/nome&geom/buffer/0.2", 200),
    RequestTest("api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/nome&geom/buffer/0.2/!union!/" + SERVER + "api/bcim/unidades-federativas/MG/envelope/", 200),
    RequestTest("api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/nome&geom/buffer/0.2/!union!/Polygon((-51.04196101779323 -22.915330279829785, -39.86109832699603 -22.915330279829785, -39.86109832699603 -14.227537498798952, -51.04196101779323 -14.227537498798952, -51.04196101779323 -22.915330279829785))", 200),
]

arr_get_for_geometry_collection_operation = [
    RequestTest("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/", 200),
    RequestTest("api/bcim/aldeias-indigenas/projection/nome/within/"+ SERVER +"api/bcim/unidades-federativas/ES/", 200),
    RequestTest("api/bcim/aldeias-indigenas/projection/geom,nome/within/"+ SERVER +"api/bcim/unidades-federativas/ES/", 200),
    RequestTest("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*count-resource", 200),
    RequestTest("api/bcim/aldeias-indigenas/projection/nome/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*count-resource", 200),
    RequestTest("api/bcim/aldeias-indigenas/projection/nome,geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*count-resource", 200),
    RequestTest("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/nome/upper", 200),
    RequestTest("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/geom&nome/upper", 200),
    RequestTest("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/geom/buffer/1.2", 200),
    RequestTest("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/nome&geom/buffer/1.2", 200),
    RequestTest("api/bcim/aldeias-indigenas/projection/nome/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/nome/upper", 200),
    RequestTest("api/bcim/aldeias-indigenas/projection/geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/geom/buffer/1.2", 200),
    RequestTest("api/bcim/aldeias-indigenas/projection/geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/nome&geom/buffer/1.2", 400),
    RequestTest("api/bcim/aldeias-indigenas/projection/nome,geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/geom&nome/upper", 200),
    RequestTest("api/bcim/aldeias-indigenas/projection/nome,geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/nome/upper", 400),
    RequestTest("api/bcim/aldeias-indigenas/projection/geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/geom&nome/upper", 400),
]

arr_get_for_join_operation = [
        # NonSpatialResource (1 resource) join FeatureResource (1 resource) (Not joinable)
    #RequestTest("controle-list/usuario-list/1/join/data_nascimento&geocodigo/" + SERVER + "api/bcim/unidades-federativas/ES", 400),

        # NonSpatialResource (1 resource) join FeatureResource (n resources) (Not joinable)
    #RequestTest("controle-list/usuario-list/1/join/data_nascimento&geocodigo/" + SERVER + "api/bcim/unidades-federativas/", 400),

        # FeatureResource (1 resource) join NonSpatialResource (1 resource)
    RequestTest("api/bcim/municipios/3304557/join/geocodigo&geocodigo/http://172.30.10.86/api/munic-2015/planejamento-urbano-list/3243/", 200),
    RequestTest('api/bcim/unidades-federativas/ES/join/geocodigo&uf_geocodigo/{"uf_geocodigo":"32","pib_estimado":1000000000}', 200),
    #("api/bcim/unidades-federativas/ES/join/geocodigo&geocodigo/http://gabriel:8880/estados-list/unidade-federativa-list/2/", 200),

        # FeatureResource (1 resource) join CollectionResource (n resources)
    RequestTest("api/bcim/municipios/3304557/join/geocodigo&cod_municipio/http://172.30.10.86/api/pib-municipio/faturamento-list/filter/cod_municipio/eq/3304557", 200),
    #("api/bcim/unidades-federativas/ES/join/geocodigo&geocodigo/http://gabriel:8880/estados-list/unidade-federativa-list/", 200),

        # FeatureResource join NonSpatialResource (Not joinable)
    RequestTest("api/bcim/municipios/3304557/join/geocodigo&nome/http://172.30.10.86/api/munic-2015/planejamento-urbano-list/3243/", 400),
    #("api/bcim/unidades-federativas/ES/join/geocodigo&nome/http://gabriel:8880/estados-list/unidade-federativa-list/2/", 400),

        # FeatureCollection (n resources) join CollectionResource (n resources)
    RequestTest("api/bcim/unidades-federativas/join/geocodigo&cod_estado/http://172.30.10.86/esporte-list/cond-funcionamento-list/", 200),
    #("api/bcim/unidades-federativas/join/geocodigo&geocodigo/http://gabriel:8880/estados-list/unidade-federativa-list/", 200),

        # CollectionResource (n resources) join FeatureCollection (n resources)
    #("esporte-list/cond-funcionamento-list/join/cod_estado&geocodigo/http://172.30.10.86/api/bcim/unidades-federativas/offset_limit/0&2/geocodigo,nome,geom", 200),

        # FeatureCollection (n resources) join CollectionResource (n resources)
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG/join/geocodigo&cod_estado/http://172.30.10.86/esporte-list/cond-funcionamento-list/filter/cod_estado/in/31&32&33&35/", 200),
]

arr_options_for_collection_operation = [
    RequestTest("controle-list/usuario-list/filter/id/gt/5/", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/collect/nome/upper", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/collect/id&email/upper", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/count-resource", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/offset-limit/0&2", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/offset-limit/0&2/nome", 400, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/offset-limit/0&2/nome,email", 400, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/distinct/nome", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/group-by/nome", 400, method="OPTIONS"), # the operation 'group_by' doesn't exists anymore
    RequestTest("controle-list/usuario-list/group-by-count/nome", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/filter/id/gt/5/*collect/nome/upper", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/filter/id/gt/5/*collect/id&email/upper", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/filter/id/gt/5/*count-resource", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/offset-limit/0&2/collect/nome/upper", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/offset-limit/0&2/collect/id&nome/upper", 200, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/offset-limit/0&2/nome/collect/nome/upper", 400, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/offset-limit/0&2/nome,id/collect/id&nome/upper", 400, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/offset-limit/0&2/nome/collect/id&nome/upper", 400, method="OPTIONS"),
    RequestTest("controle-list/usuario-list/filter/id/gt/5/*count-resource", 200, method="OPTIONS"),

    # Collection operation used by FeatureCollection
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP", 200, method="OPTIONS"),

    RequestTest("api/bcim/unidades-federativas/collect/nome/upper", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/collect/nome&sigla/lower", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/collect/geom&sigla/lower", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/collect/sigla&geom/buffer/0.2", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/collect/geom/buffer/0.2", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/collect/geom/area", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/collect/sigla&geom/area", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/collect/sigla&geom/point_on_surface", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/collect/geom/point_on_surface", 200, method="OPTIONS"),

    RequestTest("api/bcim/unidades-federativas/count-resource", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/nome", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/nome,sigla", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/nome,geom", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/geom", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/distinct/nome", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/group-by/nome", 400, method="OPTIONS"), # the operation 'group_by' doesn't exists anymore
    RequestTest("api/bcim/unidades-federativas/group-by-count/nome", 200, method="OPTIONS"),

    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP/*collect/nome/upper", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP/*collect/nome&sigla/lower", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP/*collect/geom&sigla/lower", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP/*collect/sigla&geom/buffer/0.2", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP/*collect/geom/buffer/0.2", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP/*collect/geom/area", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP/*collect/sigla&geom/area", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP/*collect/sigla&geom/point_on_surface", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP/*collect/geom/point_on_surface", 200, method="OPTIONS"),

    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/collect/nome/upper", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/collect/nome&sigla/lower", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/collect/geom&sigla/lower", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/collect/sigla&geom/buffer/0.2", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/collect/geom/buffer/0.2", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/collect/geom/area", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/collect/sigla&geom/area", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/collect/sigla&geom/point_on_surface", 200, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/collect/geom/point_on_surface", 200, method="OPTIONS"),

    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/nome/collect/nome/upper", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/nome,sigla/collect/nome&sigla/lower", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/sigla,geom/collect/geom&sigla/lower", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/sigla,geom/collect/sigla&geom/buffer/0.2", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/geom/collect/geom/buffer/0.2", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/geom/collect/geom/area", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/sigla,geom/collect/sigla&geom/area", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/sigla,geom/collect/sigla&geom/point_on_surface", 400, method="OPTIONS"),
    RequestTest("api/bcim/unidades-federativas/offset-limit/0&2/geom/collect/geom/point_on_surface", 400, method="OPTIONS"),

    RequestTest("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG&SP/*count-resource", 200, method="OPTIONS"),
]

# The suffixed requests just need simple tests (once requests suffixed with '.jsonld' is just repassed to options() method)
# More complex tests must be applied in OPTIONS requests (without suffix)
arr_get_for_collect_operation_context = [
    RequestTest("controle-list/usuario-list/filter/id/gt/5.jsonld", 200),
    RequestTest("controle-list/usuario-list/collect/nome/upper.jsonld", 200),
    RequestTest("controle-list/usuario-list/collect/id&email/upper.jsonld", 200),
    RequestTest("controle-list/usuario-list/projection/id,email/collect/id&email/upper.jsonld", 200),
    RequestTest("controle-list/usuario-list/projection/email/collect/id&email/upper.jsonld", 400),
    RequestTest("api/bcim/unidades-federativas/collect/nome/upper.jsonld", 200),
    RequestTest("api/bcim/unidades-federativas/collect/nome&sigla/lower.jsonld", 200),
    RequestTest("api/bcim/unidades-federativas/collect/geom&sigla/lower.jsonld", 200),
    RequestTest("api/bcim/unidades-federativas/collect/sigla&geom/buffer/0.2.jsonld", 200),
    RequestTest("api/bcim/unidades-federativas/collect/geom/buffer/0.2.jsonld", 200),
    RequestTest("api/bcim/unidades-federativas/collect/geom/area.jsonld", 200),
    RequestTest("api/bcim/unidades-federativas/collect/sigla&geom/area.jsonld", 200),
    RequestTest("api/bcim/unidades-federativas/collect/sigla&geom/point_on_surface.jsonld", 200),
    RequestTest("api/bcim/unidades-federativas/collect/geom/point_on_surface.jsonld", 200),
    RequestTest("api/bcim/unidades-federativas/projection/sigla,geom/collect/sigla&geom/area.jsonld", 200),
    RequestTest("api/bcim/unidades-federativas/projection/sigla/collect/sigla&geom/area.jsonld", 400),

]

arr_get_for_tiff_resource = [
    RequestTest('raster/imagem-exemplo-tile1-list/61/', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/bands', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/destructor', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/driver', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/extent', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/geotransform', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/height', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/info', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/metadata', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/name', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/origin', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/ptr', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/ptr_type', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/scale', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/skew', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/srid', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/srs', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/transform/3086', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/vsi_buffer', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/warp', 200),
    RequestTest('raster/imagem-exemplo-tile1-list/61/width', 200),
]

arr_options_for_tiff_resource = [
    RequestTest('raster/imagem-exemplo-tile1-list/61/', 200, method='OPTIONS')
]

def test_requests(request_test_list, test_label=''):
    default_init_test_label = "Initializing test set:"
    init_label_len = len(test_label) + len(default_init_test_label) + 5
    print("\n\n" + init_label_len * "*" + "\n* " + default_init_test_label  + " " + test_label + " *\n" + init_label_len * "*" + "\n\n")

    requests_with_error = []
    for request_test in request_test_list:
        print('Executing: ' + request_test.uri)

        if request_test.method == 'OPTIONS':
            res = requests.options(request_test.uri)
        else:
            res = requests.get(request_test.uri)

        if res.status_code != request_test.expec_status_code:#not in (200, 201,202,203,204,300,301,302,303):
            print('Failed: ' + request_test.uri + ' ' + str(res.status_code) + ' != ' + str(request_test.expec_status_code) + ' (Expected)')
            #url_status_code_status_ret = list(request_test)
            #url_status_code_status_ret.append(res.status_code)
            requests_with_error.append( (request_test.uri, request_test.expec_status_code, res.status_code) )
    if len(requests_with_error) > 0:
        print("***************The urls below failed****************")
        for req_str_error in requests_with_error:
            print(req_str_error[0] + ' ' + str(req_str_error[2]) + ' != ' + str(req_str_error[1]) + ' (Expected)')
        print("***************failed urls****************")
    else:
        print("*********Sucess***********")

    default_fin_test_label = "End of test set:"
    fin_label_len = len(test_label) + len(default_fin_test_label) + 5
    print("\n\n" + fin_label_len * "*" + "\n* " + default_fin_test_label + " " + test_label + " *\n" + fin_label_len * "*" + "\n\n")

'''
test_requests(arr_get_for_non_spatial_resource, test_label = "Tests for NonSpatialResource")
test_requests(arr_get_for_collection, test_label="Generic tests to collection operations")
test_requests(arr_get_for_spatial_operations, test_label="Tests for spatial operations")
test_requests(arr_get_for_complex_requests, test_label="Tests for complex requests")
test_requests(arr_get_for_projection, test_label="Tests for FeatureCollection with and without projection")
test_requests(arr_get_for_geometry_collection_operation, test_label="Tests for spatial collection operations")
#test_requests(arr_get_for_join_operation, test_label="Tests for join operation")
test_requests(arr_options_for_collection_operation, test_label = "Tests OPTIONS for Collection operations")
test_requests(arr_get_for_collect_operation_context, test_label = "Tests GET for Collect operation context")
test_requests(arr_get_for_tiff_resource, test_label = "Tests GET for TiffResource")
test_requests(arr_options_for_tiff_resource, test_label = "Tests OPTIONS for TiffResource")
'''

print("\n\n" + 25 * "X" + "\nX End of all test sets  X\n" + 25 * "X" + "\n\n")

args = sys.argv
if '-a' in args:
    '''
    print("\n\n\n<<< INITIALIZING SINTAX CHECK TEST SET >>>\n")
    print("\n\n<<< Testing GenericOperationsSintaxTest >>>")
    os.system("python manage.py test hyper_resource.tests.GenericOperationsSintaxTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing CollectionOperationsSintaxTest >>>")
    os.system("python manage.py test hyper_resource.tests.CollectionOperationsSintaxTest --testrunner=hyper_resource.tests.NoDbTestRunner")

    # GET Tests
    print("\n\n\n<<< INITIALIZING GET TEST SET >>>\n")
    print("\n\n<<< Testing CollectOperationTest >>>")
    os.system("python manage.py test hyper_resource.tests.CollectOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing GroupBySumOperationTest >>>")
    os.system("python manage.py test hyper_resource.tests.GroupBySumOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing ProjectionOperationTest >>>")
    os.system("python manage.py test hyper_resource.tests.ProjectionOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing FilterOperationTest >>>")
    os.system("python manage.py test hyper_resource.tests.FilterOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    #print("\n\n<<< Testing JoinOperationTest >>>")
    #os.system("python manage.py test hyper_resource.tests.JoinOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing EntryPointTest >>>")
    os.system("python manage.py test hyper_resource.tests.EntryPointTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing RasterTest >>>")
    os.system("python manage.py test hyper_resource.tests.RasterTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing FeatureCollectionTest >>>")
    os.system("python manage.py test hyper_resource.tests.FeatureCollectionTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing FeatureResourceTest >>>")
    os.system("python manage.py test hyper_resource.tests.FeatureResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    '''

    # OPTIONS Tests
    print("\n\n\n<<< INITIALIZING OPTIONS TEST SET >>>\n")
    print("\n\n<<< Testing OptionsForCollectOperationTest >>>")
    os.system("python manage.py test hyper_resource.tests.OptionsForCollectOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    #print("\n\n<<< Testing OptionsForProjectionOperation >>>")
    #os.system("python manage.py test hyper_resource.tests.OptionsForProjectionOperation --testrunner=hyper_resource.tests.NoDbTestRunner")

    #print("\n\n<<< Testing OptionsForJoinOperationTest >>>")
    #os.system("python manage.py test hyper_resource.tests.OptionsForJoinOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner")

    print("\n\n<<< Testing OptionsEntryPointTest >>>")
    os.system("python manage.py test hyper_resource.tests.OptionsEntryPointTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing OptionsForRasterTest >>>")
    os.system("python manage.py test hyper_resource.tests.OptionsForRasterTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    #print("\n\n<<< Testing OptionsFeatureCollectionTest >>>")
    #os.system("python manage.py test hyper_resource.tests.OptionsFeatureCollectionTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing RequestOptionsTest >>>")
    os.system("python manage.py test hyper_resource.tests.RequestOptionsTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    #print("\n\n<<< Testing GetRequestContextTest >>>")
    #os.system("python manage.py test hyper_resource.tests.GetRequestContextTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    #print("\n\n<<< Testing OptionsFeatureResourceTest >>>")
    #os.system("python manage.py test hyper_resource.tests.OptionsFeatureResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing OptionsCollectionResource >>>")
    os.system("python manage.py test hyper_resource.tests.OptionsCollectionResource --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing OptionsNonSpatialResource >>>")
    os.system("python manage.py test hyper_resource.tests.OptionsNonSpatialResource --testrunner=hyper_resource.tests.NoDbTestRunner")


    # HEAD Tests
    print("\n\n\n<<< INITIALIZING HEAD TEST SET >>>\n")
    print("\n\n<<< Testing HeadEntryPointTest >>>")
    os.system("python manage.py test hyper_resource.tests.HeadEntryPointTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing HeadFeatureCollectionTest >>>")
    os.system("python manage.py test hyper_resource.tests.HeadFeatureCollectionTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing AllowedMethodsForEntryPoint >>>")
    os.system("python manage.py test hyper_resource.tests.AllowedMethodsForEntryPoint --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing AllowedMethodsForNonSpatialResource >>>")
    os.system("python manage.py test hyper_resource.tests.AllowedMethodsForNonSpatialResource --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing AllowedMethodsForCollectionResource >>>")
    os.system("python manage.py test hyper_resource.tests.AllowedMethodsForCollectionResource --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing AllowedMethodsForTiffCollectionResource >>>")
    os.system("python manage.py test hyper_resource.tests.AllowedMethodsForTiffCollectionResource --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing AllowedMethodsForTiffResourceTest >>>")
    os.system("python manage.py test hyper_resource.tests.AllowedMethodsForTiffResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing AllowedMethodsForFeatureResourceTest >>>")
    os.system("python manage.py test hyper_resource.tests.AllowedMethodsForFeatureResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing AllowedMethodsForFeatureCollectionResourceTest >>>")
    os.system("python manage.py test hyper_resource.tests.AllowedMethodsForFeatureCollectionResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing HeadFeatureResourceTest >>>")
    os.system("python manage.py test hyper_resource.tests.HeadFeatureResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner")

    # Not classified
    print("\n\n\n<<< INITIALIZING NOT CLASSIFIED TEST SET >>>\n")
    print("\n\n<<< Testing PaginationTest >>>")
    os.system("python manage.py test hyper_resource.tests.PaginationTest --testrunner=hyper_resource.tests.NoDbTestRunner")
    print("\n\n<<< Testing LinkHeaderTest >>>")
    os.system("python manage.py test hyper_resource.tests.LinkHeaderTest --testrunner=hyper_resource.tests.NoDbTestRunner")