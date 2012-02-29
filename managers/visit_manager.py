from django.db import models

class VisitManager(models.Manager):

    def get_by_natural_key(self, registered_subject, visit_definition, visit_instance):
        return self.get(registered_subject=registered_subject, visit_definition=visit_definition, visit_instance=visit_instance)
    
    def get_by_natural_key_with_dict(self, **kwargs):
        return self.get(**kwargs)
