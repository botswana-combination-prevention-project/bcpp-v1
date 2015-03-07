from apps.bcpp_household.models import HouseholdStructure, HouseholdLogEntry, HouseholdRefusal
from apps.bcpp_survey.models import Survey

from .base_helper import BaseHelper
from .plot import Plot
from apps.bcpp_household.models.household_assessment import HouseholdAssessment


class Household(BaseHelper):

    def __init__(self, household):
        super(Household, self).__init__()
        self.household = household
        self.household_identifier = self.household.household_identifier
        self.update_plot()
        self.update_household_structure()
        self.update_household_log()
        self.update_household_refusal()
        self.update_household_assessment()

    def __repr__(self):
        return '{0}({1.household!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.household_identifier!s}'.format(self)

    @property
    def unique_key(self):
        return self.internal_identifier

    def customize_for_csv(self):
        super(Household, self).customize_for_csv()
        del self.data['household']

    def update_plot(self):
        plot = Plot(household=self.household)
        self.community = plot.community
        self.gps_lat = plot.gps_lat
        self.gps_lon = plot.gps_lon
        self.confirmed = plot.confirmed
        self.confirmed_date = plot.confirmed_date
        self.plot_identifier = plot.plot_identifier

    def update_household_structure(self):
        lookup_string = ''
        for survey in Survey.objects.all().order_by('survey_abbrev'):
            household_structure = HouseholdStructure.objects.get(household=self.household, survey=survey)
            fieldattrs = [
                ('enrolled', 'enrolled'),
                ('enrolled_datetime', 'enrolled_datetime'),
                ('enumerated', 'enumerated'),
                ('enumeration_attempts', 'enumeration_attempts'),
                ('eligible_members', 'eligible_members'),
                ('refused_enumeration', 'refused_enumeration'),
                ('failed_enumeration', 'failed_enumeration'),
                ]
            self._update(survey.survey_abbrev, fieldattrs, HouseholdStructure, lookup_string, household_structure)

    def update_household_log(self):
        lookup_string = 'household_log__household_structure'
        for survey in Survey.objects.all().order_by('survey_abbrev'):
            household_structure = HouseholdStructure.objects.get(household=self.household, survey=survey)
            fieldattrs = [
                ('report_datetime', 'log_date'),
                ('household_status', 'log_status'),
                ]
            self._update(survey.survey_abbrev, fieldattrs, HouseholdLogEntry, lookup_string, household_structure)
            try:
                setattr(
                    self, '{}_{}'.format('log_first_date', survey.survey_abbrev),
                    min(getattr(self, '{}_{}'.format('log_date', survey.survey_abbrev.lower()))))
            except TypeError:
                setattr(
                    self, '{}_{}'.format('log_first_date', survey.survey_abbrev),
                    getattr(self, '{}_{}'.format('log_date', survey.survey_abbrev.lower())))
            try:
                setattr(
                    self, '{}_{}'.format('log_last_date', survey.survey_abbrev),
                    max(getattr(self, '{}_{}'.format('log_date', survey.survey_abbrev.lower()))))
            except TypeError:
                setattr(
                    self, '{}_{}'.format('log_last_date', survey.survey_abbrev),
                    getattr(self, '{}_{}'.format('log_date', survey.survey_abbrev.lower())))

    def update_household_refusal(self):
        lookup_string = 'household_structure'
        for survey in Survey.objects.all().order_by('survey_abbrev'):
            household_structure = HouseholdStructure.objects.get(household=self.household, survey=survey)
            fieldattrs = [
                ('report_datetime', 'refusal_datetime'),
                ]
            household_refusal = self._update(
                survey.survey_abbrev, fieldattrs, HouseholdRefusal, lookup_string, household_structure)
            try:
                setattr(
                    self, '{}_{}'.format('refusal_reason', survey.survey_abbrev.lower()),
                    household_refusal.reason_other if not household_refusal.reason.upper() == 'OTHER' else household_refusal.reason_other
                    )
            except AttributeError:
                setattr(self, '{}_{}'.format('refusal_reason', survey.survey_abbrev.lower()), None)

    def update_household_assessment(self):
        lookup_string = 'household_structure'
        for survey in Survey.objects.all().order_by('survey_abbrev'):
            household_structure = HouseholdStructure.objects.get(household=self.household, survey=survey)
            fieldattrs = [
                ('created', 'assess_datetime'),
                ('last_seen_home', 'assess_last_seen'),
                ('member_count', 'assess_count'),
                ('eligibles', 'assess_eligible'),
                ('ineligible_reason', 'assess_ineligible_reason'),
                ]
            self._update(
                survey.survey_abbrev, fieldattrs, HouseholdAssessment, lookup_string, household_structure)
