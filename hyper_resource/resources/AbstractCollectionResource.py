from hyper_resource.resources.AbstractResource import *

COLLECTION_TYPE = "Collection"
GROUP_BY_SUM_PROPERTY_NAME = "sum"

class AbstractCollectionResource(AbstractResource):

    def __init__(self):
        super(AbstractCollectionResource, self).__init__()
        self.queryset = None

    def default_resource_representation(self):
        return COLLECTION_TYPE

    def define_resource_representation_by_only_attributes(self, request, attributes_functions_str):
        return self.resource_representation_or_default_resource_representation(request)

    def define_resource_representation_from_collect_operation(self, request, attributes_functions_str):
        raise NotImplementedError("'define_resource_representation_by_collect_operation' must be implemented in subclasses")

    def define_resource_representation_from_count_resource_operation(self, request, attributes_functions_str):
        resource_representation_by_accept = self.resource_representation_or_default_resource_representation(request)
        if resource_representation_by_accept == self.dict_by_accept_resource_representation()[CONTENT_TYPE_OCTET_STREAM]:
            return bytes
        return self.get_operation_type_called(attributes_functions_str).return_type

    def define_resource_representation_from_distinct_operation(self, request, attributes_functions_str):
        resource_representation_by_accept = self.resource_representation_or_default_resource_representation(request)
        if resource_representation_by_accept != self.default_resource_representation():
            return resource_representation_by_accept
        return self.return_type_for_distinct_operation(attributes_functions_str)

    def attributes_functions_str_is_filter_with_spatial_operation(self, attributes_functions_str):
        arr_str = attributes_functions_str.split('/')[1:]

        geom_ops = self.operation_controller.geometry_operations_dict()

        for str_ in arr_str:
            if self.is_spatial_attribute(str_):
                ind = arr_str.index(str_)

                if ind + 1 <= len(arr_str):
                    return arr_str[ind + 1] in geom_ops()

        return False

    def split_combined_operation(self, attributes_functions_str):
        #oc = BaseOperationController()
        operators_list = ['*' + key for key in self.operation_controller.expression_operators_dict().keys()]
        operators_list.extend( ['*' + key for key in self.operation_controller.expression_logical_operators().keys()] )

        attrs_functs_str = self.remove_last_slash(attributes_functions_str)
        attrs_funcs_arr = attrs_functs_str.split('/')
        if '/*' in attrs_functs_str:
            second_oper_init = None
            for attr_func in attrs_funcs_arr:
                if attr_func.startswith('*') and attr_func not in operators_list:
                    second_oper_init = attr_func
                    break

            if second_oper_init is None:
                first_oper_snippet = attrs_functs_str
                second_oper_snippet = None
            else:
                first_oper_snippet = attrs_functs_str[:attrs_functs_str.index(second_oper_init)-1]
                second_oper_snippet = attrs_functs_str[attrs_functs_str.index(second_oper_init)+1:]
        else:
            first_oper_snippet = attrs_functs_str
            second_oper_snippet = None
        return (first_oper_snippet, second_oper_snippet)

    def extract_collect_operation_snippet(self, attributes_functions_str):
        if self.path_has_projection(attributes_functions_str):
            collect_oper_snippet_arr = self.remove_projection_from_path(attributes_functions_str).split('/')
        else:
            collect_oper_snippet_arr = self.remove_last_slash(attributes_functions_str).split('/')

        if self.operation_controller.collect_collection_operation_name not in collect_oper_snippet_arr\
                and '*' + self.operation_controller.collect_collection_operation_name not in collect_oper_snippet_arr:
            raise SyntaxError('"' + attributes_functions_str + '" does not contains a correct "' + self.operation_controller.collect_collection_operation_name + '" operation syntax')

        if '*' + self.operation_controller.collect_collection_operation_name in collect_oper_snippet_arr:
            collect_idx = collect_oper_snippet_arr.index('*' + self.operation_controller.collect_collection_operation_name)
            collect_oper_snippet_arr[collect_idx] = collect_oper_snippet_arr[collect_idx][1:]
        else:
            collect_idx = collect_oper_snippet_arr.index(self.operation_controller.collect_collection_operation_name)

        return '/'.join( collect_oper_snippet_arr[collect_idx:] )

    def extract_collect_operation_attributes(self, attributes_functions_str, as_string=False):
        collect_oper_snippet_arr = self.extract_collect_operation_snippet(attributes_functions_str).split("/")
        collect_attrs = collect_oper_snippet_arr[1]
        return collect_attrs.replace('&', ',') if as_string else collect_attrs.split('&')

    def extract_operation_snippet_from_collect_operation_str(self, attributes_functions_str):
        operation_in_collect_arr =  self.extract_collect_operation_snippet(attributes_functions_str).split("/")[2:]
        return "/".join(operation_in_collect_arr)

    def get_operation_in_collect_return_type(self, attributes_functions_str):
        operation_in_collect_name = self.extract_collect_operation_snippet(attributes_functions_str).split("/")[2]
        return BaseOperationController().dict_all_operation_dict()[operation_in_collect_name].return_type

    def projection_attrs_equals_collect_attrs(self, attributes_functions_str):
        projection_attrs = self.extract_projection_attributes(attributes_functions_str)
        collected_attributes = self.extract_collect_operation_attributes(attributes_functions_str)
        projection_attrs.sort()
        collected_attributes.sort()

        return projection_attrs == collected_attributes

    def split_offset_limit_and_collect_operation(self, attributes_functions_str, add_collect_attrs_in_offset_limit=True):
        offset_limit_snippet = '/'.join( self.remove_last_slash(attributes_functions_str).split('/')[:3] )
        collect_operation_snippet = '/'.join( self.remove_last_slash(attributes_functions_str).split('/')[3:] )

        if add_collect_attrs_in_offset_limit:
            collect_attrs = self.extract_collect_operation_attributes(attributes_functions_str, as_string=True)
            offset_limit_snippet = self.operation_controller.projection_operation_name + '/' + collect_attrs + '/' + offset_limit_snippet

        return offset_limit_snippet, collect_operation_snippet

    def path_has_filter_operation(self, attributes_functions_str):
        att_funcs = self.remove_last_slash(attributes_functions_str).split('/')
        return len(att_funcs) > 1 and (att_funcs[0].lower() == self.operation_controller.filter_collection_operation_name)

    # Responds an array of operations name.
    # Should be overridden
    def array_of_operation_name(self):
        collection_operations_array = list(self.operation_controller.collection_operations_dict().keys())
        collection_operations_array.extend(self.operation_controller.internal_collection_operations_dict().keys())

        return collection_operations_array

    def _dict_all_operation_dict(self):
        operations_dict = self.operation_controller.internal_collection_operations_dict()
        operations_dict.update(self.operation_controller.dict_all_operation_dict())

        return operations_dict

    def get_operation_type_called(self, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        operations_dict = self._dict_all_operation_dict()
        return operations_dict[operation_name]

    def get_operation_name_from_path(self, attributes_functions_str):
        arr_att_funcs = self.remove_last_slash(attributes_functions_str).lower().split('/')

        # join operation has priority
        if self.path_has_join_operation(attributes_functions_str):
            return self.operation_controller.join_operation_name

        if self.path_has_projection(attributes_functions_str):
            path_without_projection = self.remove_projection_from_path(attributes_functions_str)
            first_part_name = self.operation_controller.projection_operation_name if path_without_projection == '' else arr_att_funcs[2]
        else:
            first_part_name = arr_att_funcs[0]

        if first_part_name not in self.array_of_operation_name():
            return None

        #if (first_part_name == self.operation_controller.offset_limit_collection_operation_name
        if  first_part_name == self.operation_controller.filter_collection_operation_name\
            and '/*' + self.operation_controller.collect_collection_operation_name in attributes_functions_str:
            return first_part_name + '-and-collect'

        if  first_part_name == self.operation_controller.offset_limit_collection_operation_name\
            and len(arr_att_funcs) > 3 and arr_att_funcs[3] == self.operation_controller.collect_collection_operation_name:
            return first_part_name + '-and-collect'

        if first_part_name == self.operation_controller.collect_collection_operation_name and '/*filter' in attributes_functions_str:
            return first_part_name + '-and-filter'

        if first_part_name == self.operation_controller.filter_collection_operation_name and '/*count-resource' in attributes_functions_str:
            return first_part_name + '-and-count-resource'

        return first_part_name

    # ---------------------------------------- REQUIRED OBJECT FOR OPERATIONS ----------------------------------------
    def required_object_for_count_resource_operation(self,request, attributes_functions_str):
        c_type_by_operation = self.define_content_type_by_operation(request, self.get_operation_name_from_path(attributes_functions_str))
        operation_name = self.operation_controller.count_resource_collection_operation_name
        return RequiredObject({operation_name: self.model_class().objects.count()}, c_type_by_operation, self.object_model, 200)

    def required_object_for_offset_limit_operation(self, request, attributes_functions_str):
        if not self.offset_limit_operation_sintax_is_ok(attributes_functions_str):
            return self.required_object_for_invalid_sintax(attributes_functions_str)

        queryset_or_objects = self.get_objects_from_offset_limit_operation(attributes_functions_str)

        if self.path_has_projection(attributes_functions_str):
            projection_atts_str = self.extract_projection_attributes(attributes_functions_str, as_string=True)
            objects = self.get_object_serialized_by_only_attributes(projection_atts_str, queryset_or_objects)

            return RequiredObject(objects, self.content_type_or_default_content_type(request), queryset_or_objects, 200)

        return self.required_object(request, queryset_or_objects)

    def required_object_for_distinct_operation(self,request, attributes_functions_str):
        queryset_or_objects =  self.get_objects_from_distinct_operation(attributes_functions_str)

        if self.path_has_projection(attributes_functions_str):
            projection_attrs = self.extract_projection_attributes(attributes_functions_str, as_string=True)
            serialized_data = self.get_object_serialized_by_only_attributes(projection_attrs, queryset_or_objects)

            return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), queryset_or_objects, 200)

        return self.required_object(request, queryset_or_objects)

    def required_object_for_group_by_count_operation(self, request, attributes_functions_str):
        objects =  self.get_objects_from_group_by_count_operation(attributes_functions_str)
        serialized_data = self.get_objects_serialized_by_aggregation_operation(attributes_functions_str, objects)
        return self.required_object_for_aggregation_operation(request, serialized_data)

    def required_object_for_group_by_sum_operation(self, request, attributes_functions_str):
        objects = self.get_objects_from_group_by_sum_operation(attributes_functions_str)
        serialized_data = self.get_objects_serialized_by_aggregation_operation(attributes_functions_str, objects)
        return self.required_object_for_aggregation_operation(request, serialized_data)

    def required_object_for_filter_operation(self, request, attributes_functions_str):
        #if not self.filter_operation_sintax_is_ok(attributes_functions_str):
        #    return self.required_object_for_invalid_sintax(attributes_functions_str)

        business_objects = self.get_objects_from_filter_operation(attributes_functions_str)

        if self.path_has_projection(attributes_functions_str):
            attrs_funcs_str = self.extract_projection_attributes(attributes_functions_str, as_string=True)
            serialized_data = self.get_object_serialized_by_only_attributes(attrs_funcs_str, business_objects)

        else:
            serialized_data = self.serializer_class(business_objects, many=True, context={'request': request}).data

        return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), business_objects, 200)

    def required_object_for_collect_operation(self, request, attributes_functions_str):
        collect_operation_snippet = self.remove_last_slash(attributes_functions_str)

        if self.path_has_projection(collect_operation_snippet):
            if self.projection_attrs_equals_collect_attrs(collect_operation_snippet):
                collect_operation_snippet = self.remove_projection_from_path(attributes_functions_str)
            else:
                message = 'Projection attributes list must be the same as collect operation attributes list'
                return self.required_object_for_invalid_sintax(attributes_functions_str, message)

        business_objects = self.get_objects_from_collect_operation(collect_operation_snippet)

        return RequiredObject(business_objects, self.content_type_or_default_content_type(request), business_objects, 200)

    def required_object_for_filter_and_collect_collection_operation(self, request, attributes_functions_str):
        filter_and_collect_operation_snippet = self.remove_last_slash(attributes_functions_str)

        if self.path_has_projection(filter_and_collect_operation_snippet) \
           and not self.projection_attrs_equals_collect_attrs(filter_and_collect_operation_snippet):
            message = 'Projection attributes list must be the same as collect operation attributes list'

            return self.required_object_for_invalid_sintax(attributes_functions_str, message)

        business_objects = self.get_objects_from_filter_and_collect_operation(filter_and_collect_operation_snippet)
        collect_operation_snippet = self.extract_collect_operation_snippet(filter_and_collect_operation_snippet)
        serialized_data = self.get_objects_serialized_by_collect_operation(collect_operation_snippet, business_objects)
        return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), business_objects, 200)

    def required_object_for_offset_limit_and_collect_collection_operation(self, request, attributes_functions_str):
        if not self.offset_limit_operation_sintax_is_ok(attributes_functions_str):
            return self.required_object_for_invalid_sintax(attributes_functions_str)

        offset_limit_and_collect_snippet = self.remove_last_slash(attributes_functions_str)

        if self.path_has_projection(attributes_functions_str) and not self.projection_attrs_equals_collect_attrs(attributes_functions_str):
            message = 'Projection attributes list and offset_limit attributes list must be the same as collect operation attributes list'
            return self.required_object_for_invalid_sintax(attributes_functions_str, message)

        business_objects = self.get_objects_from_offset_limit_and_collect_operation(offset_limit_and_collect_snippet)
        collect_operation_snippet = self.extract_collect_operation_snippet(offset_limit_and_collect_snippet)
        serialized_data = self.get_objects_serialized_by_collect_operation(collect_operation_snippet, business_objects)
        return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), business_objects, 200)

    def required_object_for_filter_and_count_resource_collection_operation(self, request, attributes_functions_str):
        attrs_funcs_str = self.remove_projection_from_path(attributes_functions_str)
        filter_operation_params = attrs_funcs_str[0:attrs_funcs_str.index('/*')]
        q_object = self.q_object_for_filter_expression(filter_operation_params)
        num_objs = self.model_class().objects.filter(q_object).count()

        return RequiredObject({"count_resource": num_objs}, CONTENT_TYPE_JSON, self.object_model, 200)

    def required_object(self, request, business_objects):
        serialized_data = self.serializer_class(business_objects, many=True, context={'request': request}).data
        required_obj =  RequiredObject(serialized_data,self.content_type_or_default_content_type(request), business_objects, 200)

        return required_obj

    def required_object_for_aggregation_operation(self, request, a_dictionary):
        required_obj =  RequiredObject(a_dictionary,self.content_type_or_default_content_type(request), a_dictionary, 200)

        return required_obj

    def required_object_for_simple_path(self, request):
        objects = self.get_objects_from_simple_path()
        serializer = self.serializer_class(objects, many=True, context={'request': request})
        required_object = RequiredObject(serializer.data, self.content_type_or_default_content_type(request), objects, 200)
        self.temporary_content_type= required_object.content_type

        return required_object

    def required_object_for_only_attributes(self, request, attributes_functions_str):
        attrs_funcs_str = self.remove_projection_from_path(attributes_functions_str, remove_only_name=True)
        return super(AbstractCollectionResource, self).required_object_for_only_attributes(request, attrs_funcs_str)
        #objects = self.get_object_by_only_attributes(attrs_funcs_str)
        #serialized_data = self.get_object_serialized_by_only_attributes(attrs_funcs_str, objects)
        #content_type = self.content_type_or_default_content_type(request)

        #return RequiredObject(serialized_data, content_type, objects, 200)

    # ---------------------------------------- REQUIRED CONTEXT FOR OPERATIONS ----------------------------------------
    def required_context_for_filter_operation(self, request, attributes_functions_str):
        context = self.get_context_for_filter_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_collect_operation(self, request, attributes_functions_str):
        if self.path_has_projection(attributes_functions_str):
            projection_attrs = self.extract_projection_attributes(attributes_functions_str)
            collect_attrs = sorted( self.extract_collect_operation_attributes(attributes_functions_str) )

            if projection_attrs != collect_attrs:
                message = 'Projection attributes list must be the same as collect operation attributes list'
                return self.required_object_for_invalid_sintax(attributes_functions_str, message=message)

        context = self.get_context_for_collect_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_count_resource_operation(self, request, attributes_functions_str):
        context = self.get_context_for_count_resource_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_offset_limit_operation(self, request, attributes_functions_str):
        if not self.offset_limit_operation_sintax_is_ok(attributes_functions_str):
            return self.required_object_for_invalid_sintax(attributes_functions_str)

        context = self.get_context_for_offset_limit_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_distinct_operation(self, request, attributes_functions_str):
        context = self.get_context_for_distinct_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_group_by_operation(self, request, attributes_functions_str):
        context = self.get_context_for_group_by_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_group_by_count_operation(self, request, attributes_functions_str):
        context = self.get_context_for_group_by_count_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_group_by_sum_operation(self, request, attributes_functions_str):
        context = self.get_context_for_group_by_sum_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_offset_limit_and_collect_operation(self, request, attributes_functions_str):
        if not self.offset_limit_operation_sintax_is_ok(attributes_functions_str):
            return self.required_object_for_invalid_sintax(attributes_functions_str)

        return self.required_context_for_collect_operation(request, attributes_functions_str)

    def required_context_for_simple_path(self, request):
        resource_type = self.resource_representation_or_default_resource_representation(request)
        return RequiredObject(self.context_resource.context(resource_type), CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def generics_collection_operation_name(self):
       return self.operation_controller.feature_collection_operations_dict().keys()

    def q_object_for_filter_array_of_terms(self, array_of_terms):
        return FactoryComplexQuery().q_object_for_filter_expression(None, self.model_class(), array_of_terms)

    def q_object_for_filter_expression(self, attributes_functions_str):
        if attributes_functions_str[-1] == '*' \
            or (attributes_functions_str[-1] == '/'
            and attributes_functions_str[-2] == '*'):
                arr = attributes_functions_str[:-1].split('/')

        else:
            arr = attributes_functions_str.split('/')

        if self.path_has_url(attributes_functions_str):
            arr = self.attribute_functions_str_with_url_splitted_by_slash(attributes_functions_str)

        return FactoryComplexQuery().q_object_for_filter_expression(None, self.model_class(), arr[1:])

    # ---------------------------------------- GET OBJECTS FROM OPERATION  ----------------------------------------
    def get_objects_from_filter_operation(self, attributes_functions_str):
        if self.path_has_projection(attributes_functions_str):
            attrs_funcs_str = self.remove_projection_from_path(attributes_functions_str)
            q_object = self.q_object_for_filter_expression(attrs_funcs_str)
            attrs_arr = self.extract_projection_attributes(attributes_functions_str)

            return self.model_class().objects.filter(q_object).values(*attrs_arr)

        else:
            q_object = self.q_object_for_filter_expression(attributes_functions_str)

            return self.model_class().objects.filter(q_object)

    def get_objects_from_collect_operation(self, attributes_functions_str, queryset=None):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split('/')
        objects = self.model_class().objects.all() if queryset is None else queryset

        collect_object_list = []
        attrs_from_object = attrs_funcs_arr[1].split('&')
        attrs_out_of_operation = attrs_from_object[:-1]
        operated_attr = attrs_from_object[-1]

        operation_name = attrs_funcs_arr[2]
        operation_params = attrs_funcs_arr[3:]

        for obj_or_dict in objects:
            obj_attrs_dict = {}

            for attr in attrs_out_of_operation:
                obj_attrs_dict[attr] = obj_or_dict[attr] if type(obj_or_dict) is dict else getattr(obj_or_dict, attr)

            value_to_operation = obj_or_dict[operated_attr] if type(obj_or_dict) is dict else getattr(obj_or_dict, operated_attr)
            operated_value = self._execute_attribute_or_method(value_to_operation, operation_name, operation_params)

            obj_attrs_dict[operation_name] = operated_value
            collect_object_list.append(obj_attrs_dict)

        return collect_object_list

    def get_objects_from_filter_and_collect_operation(self, attributes_functions_str):
        filter_oper_snippet = attributes_functions_str[:attributes_functions_str.index("*")]
        collect_oper_snippet = attributes_functions_str[attributes_functions_str.index("*")+1:]
        filtered_collection = self.get_objects_from_filter_operation(filter_oper_snippet)
        collected_objects = self.get_objects_from_collect_operation(collect_oper_snippet, filtered_collection)

        return collected_objects

    def get_objects_from_offset_limit_and_collect_operation(self, attributes_functions_str):
        offset_limit_snippet , collect_operation_snippet = self.split_offset_limit_and_collect_operation(attributes_functions_str, add_collect_attrs_in_offset_limit=True)
        queryset_or_objects = self.get_objects_from_offset_limit_operation(offset_limit_snippet)
        collected_objects = self.get_objects_from_collect_operation(collect_operation_snippet, queryset=queryset_or_objects)

        return collected_objects

    def get_objects_from_distinct_operation(self, attributes_functions_str):
        attrs_funcs_no_projection = self.remove_last_slash(attributes_functions_str)

        if self.path_has_projection(attributes_functions_str):
            projection_attrs = self.extract_projection_attributes(attributes_functions_str)
            attrs_funcs_no_projection = self.remove_projection_from_path(attrs_funcs_no_projection)

        attrs_funcs_list = attrs_funcs_no_projection.split('/')
        distinct_parameters = attrs_funcs_list[1].split('&')

        if self.path_has_projection(attributes_functions_str):
            return self.model_class().objects.distinct(*distinct_parameters).values(*projection_attrs)

        else:
            return self.model_class().objects.distinct(*distinct_parameters)

    def get_objects_from_group_by_count_operation(self, attributes_functions_str):
        attributes_functions_list = self.remove_last_slash(attributes_functions_str).split('/')
        parameters = attributes_functions_list[1:][0].split(',')

        return self.model_class().objects.values(*parameters).annotate(count=Count(*parameters))

    def get_objects_from_group_by_sum_operation(self, attributes_functions_str):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split("/")[1]
        grouper, sum_attr = attrs_funcs_arr.split(PARAM_SEPARATOR)
        return self.model_class().objects.all().values( grouper ).annotate( **{GROUP_BY_SUM_PROPERTY_NAME: Sum( sum_attr )} )

    def get_objects_from_offset_limit_operation(self, attributes_functions_str):
        if self.path_has_projection(attributes_functions_str):
            selected_attrs = self.extract_projection_attributes(attributes_functions_str)
            attrs_funcs_without_projection = self.remove_projection_from_path(attributes_functions_str).split("/")
        else:
            selected_attrs = None
            attrs_funcs_without_projection = self.remove_last_slash(attributes_functions_str).split('/')

        offset_str, limit_str = attrs_funcs_without_projection[1].split("&")
        offset, limit = int(offset_str), int(limit_str)

        # starting from 0 or 1 has the same effect
        offset = offset if offset == 0 else offset - 1

        if selected_attrs is not None:
            return self.model_class().objects.values(*selected_attrs)[offset:offset + limit]
        return self.model_class().objects.all()[offset:offset + limit]

    # ---------------------------------------- GET CONTEXT FROM OPERATION  ----------------------------------------
    def get_context_for_filter_operation(self, request, attributes_functions_str):
        context = self.get_context_for_operation(request, attributes_functions_str)
        context["@context"].update(self.context_resource.attributes_contextualized_dict())
        return context

    def get_context_for_collect_operation(self, request, attributes_functions_str):
        context = {}
        return_type_for_collect_operation = self.return_type_for_collect_operation(attributes_functions_str)
        context["@type"] = self.context_resource.get_vocabulary_for(return_type_for_collect_operation)

        collect_attributes_arr = self.extract_collect_operation_attributes(attributes_functions_str)
        if len(collect_attributes_arr) == 1:
            return_type_for_oper_in_collect = self.get_operation_in_collect_return_type(attributes_functions_str)
            context["@id"] = self.context_resource.get_vocabulary_for(return_type_for_oper_in_collect)
        else:
            context["@id"] = self.context_resource.get_vocabulary_for(object)

        context.update(self.context_resource.get_context_superclass_by_return_type(return_type_for_collect_operation))

        context["@context"] = self.get_context_for_attributes_in_collect_operation(request, attributes_functions_str)
        context["@context"].update(self.context_resource.get_subClassOf_term_definition())
        #context["@context"].pop(self.geometry_field_name())
        resource_representation = self.define_resource_representation_from_collect_operation(request, attributes_functions_str)
        context['hydra:supportedOperations'] = self.context_resource.supportedOperationsFor(self.object_model, resource_representation)
        return context

    def get_context_for_attributes_in_collect_operation(self, request, attributes_functions_str):
        attrs_and_oper_context = {}
        attrs = self.extract_collect_operation_attributes(attributes_functions_str)
        attrs.pop()

        operation_in_collect = self.extract_collect_operation_snippet(attributes_functions_str).split('/')[2]
        oper_in_collect_return_type = self.get_operation_in_collect_return_type(attributes_functions_str)

        operated_attr_context = self.context_resource.attribute_contextualized_dict_for_type(oper_in_collect_return_type)
        attrs_and_oper_context.update( {operation_in_collect: operated_attr_context} )

        for attr in attrs:
            acontext_for_field = self.context_resource.attribute_contextualized_dict_for_field(self.field_for(attr))
            attrs_and_oper_context.update( {attr: acontext_for_field} )
        return attrs_and_oper_context

    def get_context_for_count_resource_operation(self, request, attributes_functions_str):
        #context = self.get_context_for_operation(request, attributes_functions_str)

        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        count_resource_return_type = self.return_type_for_count_resource_operation(attributes_functions_str)
        context = self.context_resource.get_resource_id_and_type_by_operation_return_type(operation_name, count_resource_return_type)

        resource_representation = self.define_resource_representation_from_count_resource_operation(request, attributes_functions_str)
        context['hydra:supportedOperations'] = self.context_resource.supportedOperationsFor(self.object_model, resource_representation)

        context['@context'] = self.context_resource.get_subClassOf_term_definition()
        context['@context'].update(self.context_resource.get_operation_return_type_term_definition(operation_name, count_resource_return_type))
        return context

    def get_context_for_distinct_operation(self, request, attributes_functions_str):
        return self.get_context_for_filter_operation(request, attributes_functions_str)
        #distinct_oper_name = self.operation_controller.distinct_collection_operation_name
        #distinct_return_type = self.return_type_for_distinct_operation(attributes_functions_str)
        #context = self.context_resource.get_resource_id_and_type_by_operation_return_type(distinct_oper_name, distinct_return_type)

        #resource_representation = self.define_resource_representation_from_distinct_operation(request, attributes_functions_str)
        #context['hydra:supportedOperations'] = self.context_resource.supportedOperationsFor(self.object_model, resource_representation)

        #context['@context'] = self.context_resource.get_subClassOf_term_definition()
        #return context

    def get_context_for_offset_limit_operation(self, request, attributes_functions_str):
        return self.get_context_for_filter_operation(request, attributes_functions_str)
        #raise NotImplementedError("'required_context_for_offset_limit_operation' must be implemented in subclasses")

    def get_context_for_group_by_operation(self, request, attributes_functions_str):
        resource_type = self.resource_representation_or_default_resource_representation(request)
        context = self.get_context_for_operation_resource_type(attributes_functions_str, resource_type)

        attr_name = self.remove_last_slash(attributes_functions_str).split('/')[-1]
        context_dict_for_attr = {}
        context_dict_for_attr[attr_name] = self.context_resource.attribute_contextualized_dict_for_field(self.field_for(attr_name))
        context["@context"] = context_dict_for_attr
        return context

    def get_context_for_group_by_count_operation(self, request, attributes_functions_str):
        resource_type = self.resource_representation_or_default_resource_representation(request)
        context = self.get_context_for_operation_resource_type(attributes_functions_str, resource_type)
        context["@context"] = self.context_resource.get_hydra_term_definition()
        context["@context"].update(self.context_resource.get_subClassOf_term_definition())

        attr_name = self.remove_last_slash(attributes_functions_str).split('/')[-1]
        context_dict_for_attr = {}
        context_dict_for_attr[attr_name] = self.context_resource.attribute_contextualized_dict_for_field(self.field_for(attr_name))
        context["@context"].update(context_dict_for_attr)

        context["@context"].update(
            {
                "count": {
                    "@id": "http://schema.org/Integer",
                    "@type": "http://schema.org/Integer"
                }
            }
        )

        #context.update(self.context_resource.get_default_context_superclass())
        return context

    def get_context_for_group_by_sum_operation(self, request, attributes_functions_str):
        context = self.get_context_for_operation(request, attributes_functions_str)
        group_by_attr = self.remove_last_slash(attributes_functions_str).split("/")[1]
        grouper, _ = group_by_attr.split(PARAM_SEPARATOR)

        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        operation_return_type = self.execute_method_to_get_return_type_from_operation(attributes_functions_str)
        group_by_term_definition_dict = self.context_resource.get_operation_return_type_term_definition(operation_name, operation_return_type)

        context['@context'].update(
            {
                GROUP_BY_SUM_PROPERTY_NAME: group_by_term_definition_dict[operation_name],
                grouper: self.context_resource.attribute_contextualized_dict_for_field(self.field_for(grouper))
            }
        )

        return context


    # -------------------------------------- GET RETURN TYPE FROM OPERATION  --------------------------------------
    def return_type_by_only_attributes(self, attributes_functions_str):
        return COLLECTION_TYPE

    def return_type_for_collect_operation(self, attributes_functions_str):
        return COLLECTION_TYPE

    def return_type_for_filter_operation(self, attributes_functions_str):
        return COLLECTION_TYPE

    def return_type_for_count_resource_operation(self, attributes_functions_str):
        return int

    def return_type_for_offset_limit_operation(self, attributes_functions_str):
        return COLLECTION_TYPE

    def return_type_for_distinct_operation(self, attributes_functions_str):
        return COLLECTION_TYPE

    def return_type_for_offset_limit_and_collect_operation(self, attributes_functions_str):
        return COLLECTION_TYPE

    def return_type_for_group_by_count_operation(self, attributes_functions_str):
        return COLLECTION_TYPE

    def return_type_for_group_by_sum_operation(self, attributes_functions_str):
        return COLLECTION_TYPE

    def transform_queryset_in_object_model_list(self, queryset):
        if type(queryset[0]) == self.model_class():
            return queryset

        objs_list = []

        for object_ in queryset:
            model_object = self.model_class()()

            for attr in object_:
                setattr(model_object, attr, object_[attr])

            objs_list.append(model_object)

        return objs_list

    # Have to be overridden
    def get_objects_from_specialized_operation(self, attributes_functions_str):
        pass


    def get_objects_serialized_by_collect_operation(self, attributes_functions_str, objects):
        collect_operatiion_snippet = self.remove_last_slash(attributes_functions_str)
        collect_operation_arr = collect_operatiion_snippet.split('/')
        operation_name = collect_operation_arr[2]
        operated_attr = collect_operation_arr[1].split('&')[-1]

        collected_attrs = self.extract_collect_operation_attributes(collect_operatiion_snippet)
        if operated_attr not in objects[0].keys():
            collected_attrs[-1] = operation_name
        collected_attrs_str = ",".join(collected_attrs)

        return self.get_object_serialized_by_only_attributes(collected_attrs_str, objects)

    def get_objects_serialized_by_aggregation_operation(self, attributes_functions_str, objects):
        return list(objects)

    def converter_collection_operation_parameters(self, operation_name, parameters):
        operation_name_lower = operation_name.lower()

        # gets the dict whit all operations for collections
        collection_operations_dict = self.operation_controller.collection_operations_dict()

        if operation_name_lower in collection_operations_dict:
            # if operation_name is a collection operations dict key, return the related Type_Called
            type_called = collection_operations_dict[operation_name_lower]

            # convert each element in 'parameter' to the respective parameter type in Type_Called.parameters
            converted_parameters = [ConverterType().value_converted(param, parameters[i]) for i, param in enumerate(type_called.parameters)]

            return converted_parameters

        # returning the parameters without conversion
        return parameters

    def operation_names_model(self):
        return self.operation_controller.collection_operations_dict()

    def get_generic_operation_name(self, attributes_functions_str):
        if attributes_functions_str[-1] != '/':
            att_func_str = attributes_functions_str + '/'

        else:
            att_func_str = attributes_functions_str

        first_op_name = att_func_str[:att_func_str.find('/')]
        if first_op_name not in self.generics_collection_operation_name():
            return None

        idx = -1

        if first_op_name == 'filter':
            idx = att_func_str.find('/*collect')

        elif first_op_name == 'collect':
            idx = att_func_str.find('/*filter')

        if idx == -1:
            return 'get_objects_from_%s_operation' % first_op_name

        partial_str = att_func_str[(idx +2):]
        second_op_name = partial_str[:partial_str.find('/')]

        return 'get_objects_from_{first_op_name}_and_{second_op_name}_operation'.format(
            first_op_name=first_op_name, second_op_name=second_op_name)

    #Responds a dictionary(key=operation_name, value=method_to_execute).Should be overridden
    def operation_name_method_dic(self):
        d = super(AbstractCollectionResource, self).operation_name_method_dic()
        d.update({
            self.operation_controller.offset_limit_collection_operation_name: self.required_object_for_offset_limit_operation,
            self.operation_controller.offset_limit_and_collect_collection_operation_name: self.required_object_for_offset_limit_and_collect_collection_operation,
            self.operation_controller.filter_and_collect_collection_operation_name: self.required_object_for_filter_and_collect_collection_operation,
            self.operation_controller.filter_and_count_resource_collection_operation_name: self.required_object_for_filter_and_count_resource_collection_operation,
            self.operation_controller.count_resource_collection_operation_name: self.required_object_for_count_resource_operation,
            self.operation_controller.distinct_collection_operation_name: self.required_object_for_distinct_operation,
            #self.operation_controller.group_by_collection_operation_name: self.required_object_for_group_by_operation,
            self.operation_controller.group_by_count_collection_operation_name: self.required_object_for_group_by_count_operation,
            self.operation_controller.filter_collection_operation_name: self.required_object_for_filter_operation,
            self.operation_controller.collect_collection_operation_name: self.required_object_for_collect_operation,
            self.operation_controller.group_by_sum_collection_operation_name: self.required_object_for_group_by_sum_operation,
        })
        return d

    def operation_name_context_dic(self):
        dicti = super(AbstractCollectionResource, self).operation_name_context_dic()
        dicti.update({
            self.operation_controller.filter_collection_operation_name: self.required_context_for_filter_operation,
            self.operation_controller.collect_collection_operation_name: self.required_context_for_collect_operation,
            self.operation_controller.count_resource_collection_operation_name: self.required_context_for_count_resource_operation,
            self.operation_controller.offset_limit_collection_operation_name: self.required_context_for_offset_limit_operation,
            self.operation_controller.distinct_collection_operation_name: self.required_context_for_distinct_operation,
            #self.operation_controller.group_by_collection_operation_name: self.required_context_for_group_by_operation,
            self.operation_controller.group_by_count_collection_operation_name: self.required_context_for_group_by_count_operation,
            self.operation_controller.filter_and_collect_collection_operation_name: self.required_context_for_collect_operation,
            self.operation_controller.offset_limit_and_collect_collection_operation_name: self.required_context_for_offset_limit_and_collect_operation,
            self.operation_controller.filter_and_count_resource_collection_operation_name: self.required_context_for_count_resource_operation,
            self.operation_controller.group_by_sum_collection_operation_name: self.required_context_for_group_by_sum_operation,
        })
        return dicti

    def operation_name_return_type_dic(self):
        dicti = super(AbstractCollectionResource, self).operation_name_return_type_dic()
        dicti.update({
            self.operation_controller.filter_collection_operation_name:                     self.return_type_for_filter_operation,
            self.operation_controller.collect_collection_operation_name:                    self.return_type_for_collect_operation,
            self.operation_controller.count_resource_collection_operation_name:             self.return_type_for_count_resource_operation,
            self.operation_controller.offset_limit_collection_operation_name:               self.return_type_for_offset_limit_operation,
            self.operation_controller.distinct_collection_operation_name:                   self.return_type_for_distinct_operation,
            self.operation_controller.group_by_count_collection_operation_name:             self.return_type_for_group_by_count_operation,
            self.operation_controller.filter_and_collect_collection_operation_name:         self.return_type_for_collect_operation,
            self.operation_controller.offset_limit_and_collect_collection_operation_name:   self.return_type_for_offset_limit_and_collect_operation,
            self.operation_controller.filter_and_count_resource_collection_operation_name:  self.return_type_for_count_resource_operation,
            self.operation_controller.group_by_sum_collection_operation_name:               self.return_type_for_group_by_sum_operation,
        })
        return dicti

    def operation_name_resource_representation_dic(self):
        dicti = super(AbstractCollectionResource, self).operation_name_resource_representation_dic()
        dicti.update({
            self.operation_controller.filter_collection_operation_name:                     self.define_resource_representation_by_operation,
            self.operation_controller.collect_collection_operation_name:                    self.define_resource_representation_by_operation,
            self.operation_controller.count_resource_collection_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.offset_limit_collection_operation_name:               self.define_resource_representation_by_operation,
            self.operation_controller.distinct_collection_operation_name:                   self.define_resource_representation_by_operation,
            self.operation_controller.group_by_count_collection_operation_name:             self.define_resource_representation_by_operation,
            self.operation_controller.filter_and_collect_collection_operation_name:         self.define_resource_representation_by_operation,
            self.operation_controller.offset_limit_and_collect_collection_operation_name:   self.define_resource_representation_by_operation,
            self.operation_controller.filter_and_count_resource_collection_operation_name:  self.define_resource_representation_by_operation,
            self.operation_controller.group_by_sum_collection_operation_name:               self.define_resource_representation_by_operation,
        })
        return dicti

    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        self.inject_e_tag()
        attributes_functions_str = self.kwargs.get('attributes_functions')

        if self.is_simple_path(attributes_functions_str):
            self.add_allowed_methods(['delete', 'post'])
            return self.required_object_for_simple_path(request)

        if self.path_has_only_attributes(attributes_functions_str):
            return self.required_object_for_only_attributes(request, attributes_functions_str)

        if self.is_complex_request(request):
            if ENABLE_COMPLEX_REQUESTS:
                return self.required_object_for_complex_request(request)
            return self.required_object_for_invalid_sintax(attributes_functions_str, message="Complex requests is not enabled")

        res = self.get_required_object_from_method_to_execute(request, attributes_functions_str)
        if res is None:
            return self.required_object_for_invalid_sintax(attributes_functions_str)
        return res

    def options(self, request, *args, **kwargs):
        required_object = self.basic_options(request, *args, **kwargs)
        response = Response(data=required_object.representation_object, content_type=required_object.content_type, status=required_object.status_code)
        if required_object.status_code == 200:
            self.add_options_headers(request, response)
        return response

    def head(self, request, *args, **kwargs):
        if self.is_simple_path(self.kwargs.get('attributes_functions')):
            self.add_allowed_methods(['delete', 'post'])
        return super(AbstractCollectionResource, self).head(request, *args, **kwargs)

    def basic_post(self, request):
        response =  Response(status=status.HTTP_201_CREATED, content_type=CONTENT_TYPE_JSON)
        response['Content-Location'] = request.path + str(self.object_model.pk)
        self.add_cors_headers_in_header(response)

        return response

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            obj = serializer.save()
            self.object_model = obj

            return self.basic_post(request)

        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.add_cors_headers_in_header(response)
        return response

    def get_object_by_only_attributes(self, attribute_names_str):
        attribute_names_str_as_array = self.remove_last_slash(attribute_names_str).split(',')
        return self.model_class().objects.values(*attribute_names_str_as_array)

    def get_objects_from_simple_path(self):
        return self.model_class().objects.all()

    # ----------------------------------------- OPERATION SINTAX CHECK  -----------------------------------------
    def offset_limit_operation_sintax_is_ok(self, attributes_functions_str):
        if self.path_has_projection(attributes_functions_str):
            offset_limit_snippet_arr = self.remove_projection_from_path(attributes_functions_str).split('/')
        else:
            offset_limit_snippet_arr = self.remove_last_slash(attributes_functions_str).split('/')

        if offset_limit_snippet_arr[0] != self.operation_controller.offset_limit_collection_operation_name:
            return False

        try:
            offset, limit = offset_limit_snippet_arr[1].split("&")
            if int(offset) < 0 or int(limit) < 0:
                return False
        except (ValueError, IndexError):
            return False

        if len(offset_limit_snippet_arr) > 2 and not self.is_operation(offset_limit_snippet_arr[2]):
            return False
        return True

    def convert_value_to_filter_attribute_type(self, type_to_convert_value, literal_value_str):
        try:
            converter = ConverterType()
            return converter.value_converted( type_to_convert_value, literal_value_str)
            # TIP: Return the uri with parameters converted is more eficient than return True or False
        except:
            return None

    def filter_operation_expression_operator_index(self, attributes_functions_arr):
        try:
            return attributes_functions_arr.index('or')
        except:
            pass

        and_index = -1
        for idx, attr_funct in enumerate(attributes_functions_arr):
            if attr_funct == 'and' and attributes_functions_arr[idx - 2] != 'between':
                return idx
        else:
            return and_index

    def filter_operation_sintax_first_three_index_is_ok(self, attributes_functions_arr):
        if len(attributes_functions_arr) < 3:
            return False
        if attributes_functions_arr[0] != self.operation_controller.filter_collection_operation_name:
            return False
        if not self.is_attribute(attributes_functions_arr[1]):
            return False

        expression_operator = attributes_functions_arr[2]
        if expression_operator not in self.operation_controller.expression_operators_dict().keys():
            return False
        if self.operation_controller.expression_operator_expects_parameter(expression_operator) and len(attributes_functions_arr) == 3:
            return False

        return True

    def filter_operation_sintax_fourth_index_is_ok(self, attributes_functions_arr):
        if len(attributes_functions_arr) == 3:
            return True

        value_to_convert = attributes_functions_arr[3]
        type_to_convert_value = type(self.field_for(attributes_functions_arr[1]))
        value_converted_or_none = self.convert_value_to_filter_attribute_type(type_to_convert_value, value_to_convert)

        return True if value_converted_or_none else False

    def filter_operation_sintax_fifth_index_is_ok(self, attributes_functions_arr):
        if len(attributes_functions_arr) < 5:
            return True

        expression_operator = attributes_functions_arr[2]
        if self.operation_controller.expression_operator_expects_parameter(expression_operator):
            # special treatement for between operator
            if expression_operator == 'between' and attributes_functions_arr[4] != 'and':
                return False

            if not attributes_functions_arr[4] in self.operation_controller.expression_logical_operators():
                return False

        return True

    def filter_operation_sintax_ending_is_ok(self, attributes_functions_arr):
        last_index_value = attributes_functions_arr[-1]
        if last_index_value in self.operation_controller.dict_all_operation_dict():
            return True

        if last_index_value in self.operation_controller.expression_operators_dict() and\
            not self.operation_controller.expression_operator_expects_parameter(last_index_value):
            return True

        value_to_convert = attributes_functions_arr[-1]

        if len(attributes_functions_arr) > 5 and attributes_functions_arr[-4] == 'between': # if len(array) > 5 could have 'between'
            type_to_convert_value = type(self.field_for(attributes_functions_arr[-5]))
        else:
            type_to_convert_value = type(self.field_for(attributes_functions_arr[-3]))
        value_converted_or_none = self.convert_value_to_filter_attribute_type(type_to_convert_value, value_to_convert)

        return True if value_converted_or_none else False

    def filter_operation_sintax_is_ok(self, attributes_functions_str):
        if self.path_has_projection(attributes_functions_str):
            attributes_functions_str = self.remove_projection_from_path(attributes_functions_str)

        if self.path_has_url(attributes_functions_str):
            attributes_functions_arr = self.attribute_functions_str_with_url_splitted_by_slash(attributes_functions_str)
        else:
            attributes_functions_arr = self.remove_last_slash(attributes_functions_str).split('/')

        if not self.filter_operation_sintax_first_three_index_is_ok(attributes_functions_arr):
            return False
        if not self.filter_operation_sintax_fourth_index_is_ok(attributes_functions_arr):
            return False
        if not self.filter_operation_sintax_fifth_index_is_ok(attributes_functions_arr):
            return False

        expression_operator_index = self.filter_operation_expression_operator_index(attributes_functions_arr)

        if expression_operator_index != -1:
            recursive_sintax_check_str = "filter" + "/" + "/".join(attributes_functions_arr[expression_operator_index+1:])
            return self.filter_operation_sintax_is_ok( recursive_sintax_check_str )
        return self.filter_operation_sintax_ending_is_ok(attributes_functions_arr)


