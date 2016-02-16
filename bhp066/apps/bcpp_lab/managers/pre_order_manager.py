from django.db import models
from django.conf import settings

from edc.map.classes import site_mappers


class PreOrderManager(models.Manager):

    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk, name):
        SubjectVisit = models.get_model('bcpp_subject', 'SubjectVisit')
        Panel = models.get_model('bcpp_lab', 'Panel')
        panel = Panel.objects.get(name=name)
        subject_visit = SubjectVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(subject_visit=subject_visit, panel=panel)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            return super(PreOrderManager, self).get_queryset().filter(
                subject_visit__household_member__household_structure__household__plot__community=community
            )
        return super(PreOrderManager, self).get_queryset()
