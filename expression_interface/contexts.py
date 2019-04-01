from hyper_resource.contexts import ContextResource


class SubBooleanOperatorResourceContext(ContextResource):
    def attributes_contextualized_dict(self):

        dic_context = {
                                   "in":  {'@id': "http:/interfaces/in", '@type': "http:/interfaces/in"},
                                   "*in":  {'@id': "http:/interfaces/in", '@type': "http:/interfaces/in"},
                                   "isnull":  {'@id': "http:/interfaces/in", '@type': "http:/interfaces/in"},
                                   "*isnull":  {'@id': "http:/interfaces/in", '@type': "http:/interfaces/in"},
                                   "isnotnull":  {'@id': "http:/interfaces/in", '@type': "http:/interfaces/in"},
                                   "*inotsnull":  {'@id': "http:/interfaces/in", '@type': "http:/interfaces/in"},
                                   "between":  {'@id': "http:/interfaces/in", '@type': "http:/interfaces/in"},
                                   "*between":  {'@id': "http:/interfaces/in", '@type': "http:/interfaces/in"},
                                   "eq":  {'@id': "http://schema.org/equal", '@type': "http://schema.org/equal"},
                                   "neq":  {'@id': "http://schema.org/nonEqual", '@type': "http://schema.org/nonEqual"},
                                   "*neq":  {'@id': "http://schema.org/nonEqual", '@type': "http://schema.org/nonEqual"},
                                   "*eq":  {'@id': "http://schema.org/equal", '@type': "http://schema.org/equal"},
                                   "*noeq":  {'@id': "http://schema.org/nonEqual", '@type': "http://schema.org/nonEqual"},
                                    "lt":  {'@id': "http://schema.org/lesser", '@type': "http://schema.org/lesser"},
                                    "*lt":  {'@id': "http://schema.org/lesser", '@type': "http://schema.org/lesser"},
                                   "lte":  {'@id': "http://schema.org/lesserOrEqual", '@type': "http://schema.org/lesserOrEqual"},
                                    "*lte":  {'@id': "http://schema.org/lesserOrEqual", '@type': "http://schema.org/lesserOrEqual"},
                                   "gt":  {'@id': "http://schema.org/greater", '@type': "http://schema.org/greater"},
                                    "*gt":  {'@id': "http://schema.org/greater", '@type': "http://schema.org/greater"},
                                   "gte":  {'@id': "http://schema.org/greaterOrEqual", '@type': "http://schema.org/greaterOrEqual"},
                                    "*gte":  {'@id': "http://schema.org/greaterOrEqual", '@type': "http://schema.org/greaterOrEqual"}

                       }

        return dic_context

    def context(self):
        self.dict_context = {}
        self.dict_context["@context"] = self.attributes_contextualized_dict()
        self.dict_context["@id"] = "http://http:/interfaces/SubBooleanOperators"
        self.dict_context["@type"] = "SubBooleanOperators"
        return self.dict_context

class LogicalOperatorResourceContext(ContextResource):
    def attributes_contextualized_dict(self):
        dic_context = {
            "or": {'@id': "http:/interfaces/or", '@type': "http:/interfaces/or"},
            "*or": {'@id': "http:/interfaces/or", '@type': "http:/interfaces/or"},
            "and": {'@id': "http:/interfaces/and", '@type': "http:/interfaces/and"},
            "*and": {'@id': "http:/interfaces/and", '@type': "http:/interfaces/and"},

        }

        return dic_context

    def context(self):
        self.dict_context = {}
        self.dict_context["@context"] = self.attributes_contextualized_dict()
        self.dict_context["@id"] = "http://http:/interfaces/LogicalOperators"
        self.dict_context["@type"] = "LogicalOperator"
        return self.dict_context
