from django.conf import settings
from django.conf.urls import url
from django.core.exceptions import MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.template.loader import render_to_string

from edc.dashboard.base.classes import Dashboard

from bhp066.apps.bcpp_household.exceptions import AlreadyEnumerated
from bhp066.apps.bcpp_household.models import (
    Household, HouseholdStructure, HouseholdLogEntry, HouseholdLog, HouseholdAssessment,
    HouseholdRefusal, RepresentativeEligibility)
from bhp066.apps.bcpp_household.helpers import ReplacementHelper
from bhp066.apps.bcpp_household.models.household_work_list import HouseholdWorkList
from bhp066.apps.bcpp_household_member.exceptions import HouseholdStructureNotEnrolled
from bhp066.apps.bcpp_household_member.models import HouseholdHeadEligibility, HouseholdMember, HouseholdInfo
from bhp066.apps.bcpp_survey.models import Survey

from collections import namedtuple

SurveyTuple = namedtuple('SurveyTuple', 'survey url')


class HouseholdDashboard(Dashboard):

    template_name = 'householdstructure_dashboard.html'
    dashboard_name = 'Household Dashboard'
    dashboard_url_name = 'household_dashboard_url'
    view = 'household_dashboard'
    urlpattern_view = 'apps.bcpp_dashboard.views'
    urlpattern_options = dict(
        Dashboard.urlpattern_options,
        dashboard_model='household_structure',
        dashboard_type='household')

    base_fields = (
        'id', 'created', 'modified', 'user_created', 'user_modified', 'hostname_created', 'hostname_modified')

    def __init__(self, **kwargs):
        super(HouseholdDashboard, self).__init__(**kwargs)
        self._plot = None
        self._household = None
        self._household_members = None
        self._household_structure = None
        self._household_log = None
        self._household_assessment = None
        self._household_info = None
        self._household_refusal = None
        self._first_survey = None
        self._survey = None
        self._surveys = None
        self._mapper_name = None
        self.dashboard_type_list = ['household', 'household_structure']
        self.dashboard_models = {'household': Household, 'household_structure': HouseholdStructure}
        self.first_name = None
        self.mapper_name = None

    def get_context_data(self, **kwargs):
        self.context = super(HouseholdDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='bcpp_survey',
            appointment_code='T1',
            title='',  # 'A. Household Composition',
            household_refusal=self.household_refusal,
            household_head_eligibility=self.household_head_eligibility,
            representative_eligibility=self.representative_eligibility,
            plot=self.household.plot,
            household_assessment=self.household_assessment,
            household=self.household,
            household_identifier=self.household.household_identifier,
            household_structure=self.household_structure,
            household_members=self.household_members,
            household_log=self.household_log,
            household_log_entries=self.household_log_entries,
            first_name=self.first_name,
            current_member_count=self.current_member_count,
            survey=self.survey,
            current_survey=settings.CURRENT_SURVEY,
            rendered_surveys=self.render_surveys(),
            has_household_log_entry=self.has_household_log_entry,
            lastest_household_log_entry_household_status=self.lastest_household_log_entry_household_status,
            replaceable=ReplacementHelper(household_structure=self.household_structure).replaceable_household,
            household_info=self.household_info,
            eligible_hoh=self.eligible_hoh,
            mapper_name=self.mapper_name,
            subject_dashboard_url='subject_dashboard_url',
            household_dashboard_url=self.dashboard_url_name,
            work_list=self.work_list,
        )
        return self.context

    @property
    def work_list(self):
        try:
            work_list = HouseholdWorkList.objects.filter(household_structure=self.household_structure).last()
        except AttributeError:
            work_list = None
        except:
            work_list = None
        return work_list

    @property
    def has_household_log_entry(self):
        """Confirms there is an household_log_entry for today."""
        has_household_log_entry = False
        try:
            if self.household_log.todays_household_log_entries:
                has_household_log_entry = True
        except AttributeError:
            pass
        return has_household_log_entry

    @property
    def household_assessment(self):
        try:
            household_assessment = HouseholdAssessment.objects.get(
                household_structure=self.household_structure)
        except HouseholdAssessment.DoesNotExist:
            household_assessment = None
        return household_assessment

    @property
    def household_info(self):
        try:
            household_info = HouseholdInfo.objects.get(
                household_structure=self.household_structure)
            return household_info
        except HouseholdInfo.DoesNotExist:
            return None

    @property
    def household_refusal(self):
        try:
            household_refusal = HouseholdRefusal.objects.get(
                household_structure=self.household_structure)
        except HouseholdRefusal.DoesNotExist:
            household_refusal = None
        return household_refusal

    @property
    def lastest_household_log_entry_household_status(self):
        try:
            report_datetime = HouseholdLogEntry.objects.filter(
                household_log__household_structure=self.household_structure).aggregate(
                    Max('report_datetime')).get('report_datetime__max')
            lastest_household_log_entry = HouseholdLogEntry.objects.get(
                household_log__household_structure=self.household_structure,
                report_datetime=report_datetime)
            return lastest_household_log_entry.household_status
        except HouseholdLogEntry.DoesNotExist:
            return None

    @property
    def eligible_hoh(self):
        """Returns an instance of HouseholdHeadEligibility if there
        is a verified eligible Head of Household."""
        return self.household_head_eligibility

    @property
    def household_head_eligibility(self):
        """Returns an instance of HouseholdHeadEligibility if there
        is a verified eligible Head of Household."""
        try:
            household_head_eligibility = HouseholdHeadEligibility.objects.get(
                household_structure=self.household_structure)
        except HouseholdHeadEligibility.DoesNotExist:
            household_head_eligibility = None
        except MultipleObjectsReturned:
            # just get one
            household_head_eligibility = HouseholdHeadEligibility.objects.filter(
                household_structure=self.household_structure)[0]
        return household_head_eligibility

    @property
    def representative_eligibility(self):
        try:
            representative_eligibility = RepresentativeEligibility.objects.get(
                household_structure=self.household_structure)
        except RepresentativeEligibility.DoesNotExist:
            representative_eligibility = None
        return representative_eligibility

    @property
    def survey(self):
        """Returns the survey for the current household_structure."""
        return self.household_structure.survey

    @property
    def current_survey(self):
        """Sets to the current survey using today's date."""
        return Survey.objects.current_survey()

    @property
    def first_survey(self):
        """Returns the first survey and there should always be at least one."""
        if not self._first_survey:
            try:
                self._first_survey = Survey.objects.all().order_by('datetime_start', 'survey_name')[0]
            except IndexError:
                Survey.DoesNotExist('Unable to determine the first survey. Are any defined?')
        return self._first_survey

    @property
    def surveys(self):
        """Returns a list of surveys order by date excluding the current."""
        if not self._surveys:
            self._surveys = []
            for survey in Survey.objects.all().order_by('datetime_start'):
                household_structure = HouseholdStructure.objects.get(
                    household=self.household, survey=survey)
                _url = reverse(self.dashboard_url_name,
                               kwargs={'dashboard_type': self.dashboard_type,
                                       'dashboard_model': 'household_structure',
                                       'dashboard_id': household_structure.pk})
                self._surveys.append(SurveyTuple(survey=survey, url=_url))
        return self._surveys

    @property
    def household_structure(self):
        """Sets the household_structure instance."""
        if not self._household_structure:
            if isinstance(self.dashboard_model_instance, HouseholdStructure):
                self._household_structure = self.dashboard_model_instance
            else:
                try:
                    self._household_structure = HouseholdStructure.objects.get(pk=self.dashboard_id)
                except HouseholdStructure.DoesNotExist:
                    pass
#                     try:
#                         self._household_structure = HouseholdStructure.objects.get(
#                             household__pk=self.household.pk, survey=self.survey)
#                     except (HouseholdStructure.DoesNotExist, AttributeError):
#                         pass
        return self._household_structure

    @property
    def household(self):
        """Sets the household instance."""
        if not self._household:
            if isinstance(self.dashboard_model_instance, Household):
                self._household = self.dashboard_model_instance
            else:
                try:
                    self._household = self.dashboard_model_instance.household
                except AttributeError:
                    pass
        return self._household

    @property
    def household_members(self):
        """Returns a queryset of household members for this household structure
        (and therefore survey).

        For follow up surveys, will create new members based on the previous
        survey relative to the current household structure."""
        self._household_members = HouseholdMember.objects.filter(
            household_structure=self.household_structure).order_by('first_name')
        if not self._household_members:
            try:
                HouseholdStructure.objects.add_household_members_from_survey(
                    self.household_structure.household,
                    self.household_structure.previous.survey,
                    self.household_structure.survey)
            except AttributeError:
                pass  # no previous.survey
            except AlreadyEnumerated:
                pass
            except HouseholdStructureNotEnrolled:
                # previous survey is not erolled
                pass
        return self._household_members

    @property
    def household_log(self):
        """Returns the HouseholdLog and if it does not exist it will create one."""
        if not self._household_log:
            try:
                self._household_log = HouseholdLog.objects.get(
                    household_structure=self.household_structure)
            except HouseholdLog.DoesNotExist:
                if self.household_structure:
                    self._household_log = HouseholdLog.objects.create(household_structure=self.household_structure)
        return self._household_log

    @property
    def current_member_count(self):
        try:
            return self.household_members.count()
        except AttributeError:
            return 0

    @property
    def household_log_entries(self):
        return HouseholdLogEntry.objects.filter(
            household_log__household_structure=self.household_structure)

    def render_surveys(self):
        """Renders to string the surveys."""
        return render_to_string('surveys.html', {'surveys': self.surveys, 'survey': self.survey})
