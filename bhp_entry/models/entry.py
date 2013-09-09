from django.db import models
from bhp_content_type_map.models import ContentTypeMap
from bhp_common.choices import YES_NO_OPTIONAL
from bhp_visit.models import BaseWindowPeriodItem, VisitDefinition
from bhp_entry.choices import ENTRY_CATEGORY, ENTRY_WINDOW, ENTRY_STATUS
from bhp_entry.managers import EntryBucketManager


class Entry(BaseWindowPeriodItem):

    """Model of metadata for each model_class linked to a visit definition.

    This model lists entry forms by visit definition used to fill
    the scheduled entry bucket for a subject once a visit is reported
    """

    visit_definition = models.ForeignKey(VisitDefinition)
    content_type_map = models.ForeignKey(ContentTypeMap,
        related_name='+',
        verbose_name='entry form / model')
    entry_order = models.IntegerField()
    group_title = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='for example, may be used to add to the form title on the change form to group serveral forms')
    required = models.CharField(
        max_length=10,
        choices=YES_NO_OPTIONAL,
        default='Yes')
    entry_category = models.CharField(
        max_length=25,
        choices=ENTRY_CATEGORY,
        default='CLINIC',
        db_index=True)
    entry_window_calculation = models.CharField(
        max_length=25,
        choices=ENTRY_WINDOW,
        default='VISIT',
        help_text='Base the entry window period on the visit window period or specify a form specific window period')
    default_entry_status = models.CharField(
        max_length=25,
        choices=ENTRY_STATUS,
        default='NEW')
    objects = EntryBucketManager()

    def natural_key(self):
        return (self.visit_definition, ) + self.content_type_map.natural_key()

    def form_title(self):
        self.content_type_map.content_type.model_class()._meta.verbose_name

    def __unicode__(self):
        return '{0}: {1}'.format(self.visit_definition.code, self.content_type_map.content_type)

    class Meta:
        app_label = 'bhp_entry'
        verbose_name = "Entry"
        ordering = ['visit_definition__code', 'entry_order', ]
        unique_together = ['visit_definition', 'content_type_map', ]
