from django.db import models

from edc.lab.lab_requisition.models import BaseRequisition
from edc.map.classes import site_mappers

from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_inspector.classes import InspectorMixin

from .packing_list import PackingList


class BaseBcppRequisition(InspectorMixin, BaseRequisition):

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.community = self.get_visit().household_member.household_structure.household.plot.community
        super(BaseBcppRequisition, self).save(*args, **kwargs)

    def get_site_code(self):
        return site_mappers.get_current_mapper().map_code

    class Meta:
        abstract = True
