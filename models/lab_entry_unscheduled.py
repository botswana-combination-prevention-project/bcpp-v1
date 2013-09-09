from base_lab_entry import BaseLabEntry


class LabEntryUnscheduled(BaseLabEntry):

    """Model of metadata for each model_class linked to a visit definition.

    This model lists entry forms by panel used to fill
    the additional lab entry bucket for a subject
    """

    def form_title(self):
        self.content_type_map.content_type.model_class()._meta.verbose_name

    def __unicode__(self):
        return '%s' % (self.panel.name)

    class Meta:
        app_label = 'bhp_lab_entry'
        verbose_name = "Lab Entry Unscheduled"
        ordering = ['panel', 'entry_order', ]
