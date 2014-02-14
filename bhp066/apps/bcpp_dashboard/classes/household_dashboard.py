import re

from datetime import datetime, date

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from edc.dashboard.base.classes import Dashboard
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_household.models import Household, HouseholdStructure, HouseholdLogEntry, HouseholdLog
from apps.bcpp_household_member.choices import HOUSEHOLD_MEMBER_ACTION
from apps.bcpp_household_member.models import HouseholdMember, EnrolmentChecklist, HouseholdInfo, Loss
from apps.bcpp_survey.models import Survey


class HouseholdDashboard(Dashboard):

    view = 'household_dashboard'
    dashboard_name = 'Household Dashboard'
    dashboard_url_name = 'household_dashboard_url'
    base_fields = ('id', 'created', 'modified', 'user_created', 'user_modified', 'hostname_created', 'hostname_modified')

    def __init__(self, dashboard_type, dashboard_id, dashboard_model, dashboard_models=None, **kwargs):
        self._plot = None
        self._household = None
        self._household_members = None
        self._household_structure = None
        self._household_log = None
        self._current_member_count = None
        self._enrolment_checklist = None
        self._household_info = None
        self._first_survey = None
        self._survey = None
        self._surveys = None
        self._mapper_name = None
        dashboard_type_list = ['household', 'household_structure']
        dashboard_models = {'household': Household, 'household_structure': HouseholdStructure}
        super(HouseholdDashboard, self).__init__(dashboard_type, dashboard_id, dashboard_model, dashboard_type_list, dashboard_models)
        self.first_name = kwargs.get('first_name')
        # self.check_members_have_registered_subject()
        self.mapper_name = kwargs.get('mapper_name')

    def add_to_context(self):
        super(HouseholdDashboard, self).add_to_context()

        self.context.add(
            home='bcpp_survey',
            household_member_actions=[action[0] for action in HOUSEHOLD_MEMBER_ACTION],
            title='',  # 'A. Household Composition',
            household_meta=Household._meta,
            household_member_meta=HouseholdMember._meta,
            loss_meta=Loss._meta,
            household_structure_meta=HouseholdStructure._meta,
            household_log_entry_meta=HouseholdLogEntry._meta,
            enrolment_checklist_meta=EnrolmentChecklist._meta,
            household_info_meta=HouseholdInfo._meta,
            plot=self.household.plot,
            household=self.household,
            household_identifier=self.household.household_identifier,
            household_structure=self.household_structure,
            household_members=self.household_members,
            household_log=self.household_log,
            household_log_entries=self.household_log_entries,
            first_name=self.first_name,
            current_member_count=self.current_member_count,
            survey=self.survey,
            rendered_surveys=self.render_surveys(),
            allow_edit_members=self.allow_edit_members(),
            has_household_log_entry=self.has_household_log_entry(),
            household_info=self.household_info,
            mapper_name=self.mapper_name,
            subject_dashboard_url='subject_dashboard_url',
            household_dashboard_url=self.dashboard_url_name,
            )

    def has_household_log_entry(self):
        """Confirms there is an househol_log_entry for today."""
        today = date.today()
        if self.household_log:
            if not HouseholdLogEntry.objects.filter(
                household_log=self.household_log,
                report_datetime__year=today.year,
                report_datetime__month=today.month,
                report_datetime__day=today.day):
                return False
        return True

    @property
    def household_info(self):
        self._household_info = None
        if HouseholdInfo.objects.filter(household_structure=self.household_structure):
            self._household_info = HouseholdInfo.objects.get(household_structure=self.household_structure)
        return self._household_info

    @property
    def survey(self):
        return self.current_survey

    @property
    def current_survey(self):
        """Sets to the current survey using today's date."""
        if Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() == 1:
            self._current_survey = Survey.objects.get(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today())
        elif Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() >= 1:
            raise TypeError('Unable to set attribute _survey given survey=None and today\'s date. More than one survey exists for the given datetime (today). Either specify a survey or given a different date. Got {0}.'.format(Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today())))
        elif Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() == 0:
            raise TypeError('Unable to set attribute _survey given survey=None and today\'s date. No survey exists to include the given datetime (today). Either create a new survey or update an existing survey\'s start and end date to include today.')
        else:
            self._current_survey = None
        return self._current_survey

    @property
    def first_survey(self):
        """Returns the first survey and there should always be at least one."""
        if not self._first_survey:
            try:
                self._first_survey = Survey.objects.all().order_by('datetime_start')[0]
            except:
                pass
        return self._first_survey

    @property
    def surveys(self):
        if not self._surveys:
            self._surveys = [(self.survey, '')]
            for survey in Survey.objects.all().exclude(pk=self.survey.pk).order_by('datetime_start'):
                # if a household_structure does not exist for this household and survey, create otherwise get
                if not HouseholdStructure.objects.filter(household=self.household, survey=survey):
                    household_structure = HouseholdStructure.objects.create(household=self.household, survey=survey)
                else:
                    household_structure = HouseholdStructure.objects.get(household=self.household, survey=survey)
                url = reverse(self.dashboard_url_name, kwargs={'dashboard_type': self.dashboard_type,
                                                               'dashboard_model': 'household_structure',
                                                               'dashboard_id': household_structure.pk})
                self._surveys.append((survey, url))
        return self._surveys

    @property
    def household_structure(self):
        """Sets the household_structure instance."""
        if not self._household_structure:
            if issubclass(self.dashboard_model, HouseholdStructure):
                self._household_structure = self.dashboard_model_instance
            elif issubclass(self.dashboard_model, Household):
                self._household_structure = HouseholdStructure.objects.get(household__pk=self.household.pk, survey=self.survey)
        return self._household_structure

    @property
    def household(self):
        """Sets the household instance."""
        if not self._household:
            if isinstance(self.dashboard_model_instance, Household):
                self._household = self.dashboard_model_instance
            elif isinstance(self.dashboard_model_instance, HouseholdStructure):
                self._household = self.dashboard_model_instance.household
        return self._household

    @property
    def household_members(self):
        """Returns a queryset of household members for this household structure (and therefore survey)."""
        if not self._household_members:
            self.create_household_members_for_new_survey()
            self._household_members = HouseholdMember.objects.filter(
                household_structure=self.household_structure,
                ).order_by('first_name')
        return self._household_members

    @property
    def household_log(self):
        if not self._household_log:
            if not HouseholdLog.objects.filter(household_structure=self.household_structure):
                self._household_log = HouseholdLog.objects.create(household_structure=self.household_structure)
            else:
                self._household_log = HouseholdLog.objects.get(household_structure=self.household_structure)
        return self._household_log

    @property
    def current_member_count(self):
        try:
            self._current_member_count = self.household_members.count()
        except:
            self._current_member_count = 0

    def allow_edit_members(self):
        allow_edit_members = False
        if hasattr(settings, 'ALLOW_CHANGES_OTHER_SURVEYS') and settings.ALLOW_CHANGES_OTHER_SURVEYS:
            allow_edit_members = True
        else:
            if self.survey:
                if self.survey.datetime_start <= datetime.today() and datetime.today() <= self.survey.datetime_end:
                    allow_edit_members = True
        return allow_edit_members

    def check_members_have_registered_subject(self):
        """Checks that a corresponding RegisteredSubject exists for each member in this household."""
        for household_member in self.household_members:
            if not RegisteredSubject.objects.filter(registration_identifier=household_member.internal_identifier):
                raise ValueError('{0} expects all household_members to have '
                                 'an entry in RegisterSubject. Got None for {1}.'.format(self, household_member,))

    @property
    def household_log_entries(self):
        return HouseholdLogEntry.objects.filter(household_log__household_structure=self.household_structure)

    def create_household_members_for_new_survey(self):
        """ Prepares a householdstructure for a new survey by fetching a list of the
        householdstructure members for a given householdstructure from the FIRST
        survey and adds them to the new survey.

        ..todo:: This can be improved to check if someone has moved or died and
                 if there are members identified in interim surveys.
        """
        if self.first_survey:
            # add members from most recent first survey to current survey
            household_structure = HouseholdStructure.objects.get(household=self.household_structure.household, survey=self.first_survey)
            for hm in  HouseholdMember.objects.filter(household_structure__household=household_structure.household):
                if not HouseholdMember.objects.filter(
                        household_structure=self.household_structure,
                        registered_subject=hm.registered_subject):
                    options = {}
                    [options.update({key: value}) for key, value in hm.__dict__.iteritems() if not key.startswith('_') and not key in self.base_fields]
                    options.update({
                        'household_structure_id': self.household_structure.pk,
                        'registered_subject_id': hm.registered_subject.pk,
                        'survey_id': self.survey.pk,
                        'age_in_years': None,  # TODO: can this be incremented or at least accurate for consented subjects?
                        'nights_out': None,
                        'present': '-',
                        'lives_in_household': '-',
                        'member_status': None})
                    HouseholdMember.objects.create(**options)

    def render_surveys(self):
        """Renders to string the surveys."""
        return render_to_string('surveys.html', {'surveys': self.surveys, 'survey': self.survey})

#     def get_household_members_as_list(self):
#         """Returns a list of household members for this dashboard."""
#         return [hm for hm in self.household_members]

