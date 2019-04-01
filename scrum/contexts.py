from hyper_resource.contexts import *
class ContinuousActivityDetailContext(NonSpatialResourceContext):
    pass
class ContinuousActivityListContext(AbstractCollectionResourceContext):
    pass

class EntryPointDetailContext(NonSpatialResourceContext):
    pass
class EntryPointListContext(AbstractCollectionResourceContext):
    pass

class ImpedimentDetailContext(NonSpatialResourceContext):
    pass
class ImpedimentListContext(AbstractCollectionResourceContext):
    pass

class ProjectDetailContext(NonSpatialResourceContext):
    pass
class ProjectListContext(AbstractCollectionResourceContext):
    pass

class ScrumUserDetailContext(NonSpatialResourceContext):
    pass
class ScrumUserListContext(AbstractCollectionResourceContext):
    pass

class ScrumUserLoginContext(ContextResource):

    def initalize_context(self, resource_type):
        self.dict_context = {}
        a_context = self.get_subClassOf_term_definition()
        a_context.update(self.get_hydra_term_definition())
        self.dict_context["@context"] = a_context
        self.dict_context["hydra:supportedProperties"] = self.supportedProperties()
        self.dict_context["hydra:supportedOperations"] = []
        #self.dict_context["hydra:representationName"] = self.representationName()
        #self.dict_context["hydra:iriTemplate"] = self.iriTemplates()
        self.dict_context.update(self.get_default_context_superclass())
        self.dict_context.update(self.get_default_resource_type_identification())

class SprintDetailContext(NonSpatialResourceContext):
    pass
class SprintListContext(AbstractCollectionResourceContext):
    pass

class TaskDetailContext(NonSpatialResourceContext):
    pass
class TaskListContext(AbstractCollectionResourceContext):
    pass

class TypeContinuousActivityDetailContext(NonSpatialResourceContext):
    pass
class TypeContinuousActivityListContext(AbstractCollectionResourceContext):
    pass

