from django.conf import settings
from django.db import models
from django.db.models import get_model

from edc.map.classes import site_mappers

from bhp066.apps.bcpp_household.classes import PlotIdentifier


class HouseholdMemberManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk):
        HouseholdStructure = get_model('bcpp_household', 'HouseholdStructure')
        RegisteredSubject = get_model('registration', 'RegisteredSubject')
        household_structure = HouseholdStructure.objects.get_by_natural_key(household_identifier, survey_name)
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(household_structure=household_structure, registered_subject=registered_subject)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_current_mapper().map_area
            if PlotIdentifier.get_notebook_plot_lists():
                return super(HouseholdMemberManager, self).get_queryset().filter(
                    household_structure__household__plot__community=community,
                    household_structure__household__plot__plot_identifier__in=PlotIdentifier.get_notebook_plot_lists(),
                )
            else:
                return super(HouseholdMemberManager, self).get_queryset().filter(household_structure__household__plot__community=community,)
        return super(HouseholdMemberManager, self).get_queryset()
