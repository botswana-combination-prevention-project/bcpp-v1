from django.db import models
from django.conf import settings

from edc.map.classes import site_mappers

from bhp066.apps.bcpp_household.classes import PlotIdentifier


class ScheduledModelManager(models.Manager):
    """Manager for all scheduled models (those with a subject_visit fk)."""
    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk):
        SubjectVisit = models.get_model('bcpp_subject', 'SubjectVisit')
        subject_visit = SubjectVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(subject_visit=subject_visit)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_current_mapper().map_area
            nt_ls = PlotIdentifier.get_notebook_plot_lists()
            if PlotIdentifier.get_notebook_plot_lists():
                return super(ScheduledModelManager, self).get_queryset().filter(
                    subject_visit__household_member__household_structure__household__plot__community=community,
                    subject_visit__household_member__household_structure__household__plot__plot_identifier__in=nt_ls
                )
            else:
                return super(ScheduledModelManager, self).get_queryset().filter(
                    subject_visit__household_member__household_structure__household__plot__community=community)
        return super(ScheduledModelManager, self).get_queryset()
