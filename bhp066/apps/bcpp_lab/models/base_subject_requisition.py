from django.core.urlresolvers import reverse
from django.db import models

from edc.lab.lab_requisition.models import BaseRequisition
from edc.map.classes import site_mappers

from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_inspector.classes import InspectorMixin

from .packing_list import PackingList


class BaseBcppRequisition(InspectorMixin, BaseRequisition):

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.community = self.get_visit().household_member.household_structure.household.plot.community
        self.subject_identifier = self.get_visit().get_subject_identifier()
        super(BaseBcppRequisition, self).save(*args, **kwargs)

    def dispatch_container_lookup(self, using=None):
        return None

    def natural_key(self):
        return (self.requisition_identifier,)

    def get_site_code(self):
        return site_mappers.get_current_mapper().map_code

    def get_visit(self):
        raise TypeError('method \'subject_visit()\' in BaseSubjectRequisition must be overidden by the subclass')

    def get_subject_identifier(self):
        return self.get_visit().subject_identifier

    def dashboard(self):
        url = reverse('subject_dashboard_url',
                      kwargs={'dashboard_type': self.get_visit().appointment.registered_subject.subject_type.lower(),
                              'dashboard_model': 'appointment',
                              'dashboard_id': self.get_visit().appointment.pk,
                              'show': 'appointments'})
        return """<a href="{url}" />dashboard</a>""".format(url=url)
    dashboard.allow_tags = True


    class Meta:
        abstract = True
