from datetime import timedelta

from django.apps import apps as django_apps
from django.db import models
from django.conf import settings

from edc_map.site_mappers import site_mappers

from bcpp_household.plot_identifier import PlotIdentifier


class SubjectUndecidedEntryManager(models.Manager):
    def get_by_natural_key(self, report_datetime, household_identifier, survey_name, subject_identifier_as_pk):
        margin = timedelta(microseconds=999)
        SubjectUndecided = django_apps.get_model('bcpp_household_member', 'SubjectUndecided')
        subject_undecided = SubjectUndecided.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(report_datetime__range=(report_datetime - margin, report_datetime + margin),
                        subject_undecided=subject_undecided)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            nt = PlotIdentifier.get_notebook_plot_lists()
            if PlotIdentifier.get_notebook_plot_lists():
                return super(SubjectUndecidedEntryManager, self).get_queryset().filter(
                    subject_undecided__household_member__household_structure__household__plot__community=community,
                    subject_undecided__household_member__household_structure__household__plot__plot_identifier__in=nt)
            else:
                return super(SubjectUndecidedEntryManager, self).get_queryset().filter(
                    subject_undecided__household_member__household_structure__household__plot__community=community)
        return super(SubjectUndecidedEntryManager, self).get_queryset()
