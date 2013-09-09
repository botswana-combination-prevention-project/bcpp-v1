from django.db import models


class LabEntryManager(models.Manager):

    def get_by_natural_key(self, visit_definition_code, name):
        VisitDefinition = models.get_model('bhp_visit', 'VisitDefinition')
        Panel = models.get_model('lab_panel', 'Panel')
        visit_definition = VisitDefinition.objects.get_by_natural_key(visit_definition_code)
        panel = Panel.objects.get_by_natural_key(name)
        return self.get(panel=panel, visit_definition=visit_definition)
