from django.db import models
from bhp_base_model.models import BaseUuidModel


class Link (BaseUuidModel):

    label = models.CharField(
        max_length=25,
        help_text='Button or link label')
    app_label = models.CharField(
        max_length=25,
        help_text='app containing the ajax.py')
    ajax_method = models.CharField(
        max_length=25,
        help_text='name of method in ajax.py')
    dashboard_type = models.CharField(
        max_length=25)
    is_active = models.BooleanField(
        default=True)
    objects = models.Manager()

    def __unicode__(self):
        return self.label

    class Meta:
        app_label = 'bhp_subject_summary'
