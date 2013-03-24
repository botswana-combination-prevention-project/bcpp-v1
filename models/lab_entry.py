from django.db import models
from bhp_visit.models import VisitDefinition
from base_lab_entry import BaseLabEntry


class LabEntry(BaseLabEntry):

    """Model of metadata for each model_class linked to a visit definition.

    This model lists entry forms by visit definition used to fill
    the scheduled entry bucket for a subject once a visit is reported

    """

    visit_definition = models.ForeignKey(VisitDefinition)

    objects = models.Manager()

    def natural_key(self):
        return self.visit_definition.natural_key() + self.panel.natural_key()

    def form_title(self):
        self.content_type_map.content_type.model_class()._meta.verbose_name

    def __unicode__(self):
        return '%s: %s' % (self.visit_definition.code, self.panel.name)

    class Meta:
        app_label = 'bhp_lab_entry'
        verbose_name = "Lab Entry"
        ordering = ['visit_definition__code', 'entry_order', ]
        unique_together = ['visit_definition', 'panel', ]
