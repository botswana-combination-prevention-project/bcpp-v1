import re
from datetime import datetime, date
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.loader import render_to_string
from edc.dashboard.base.classes import Dashboard
from edc.subject.registration.models import RegisteredSubject
from apps.bcpp_household.models import Household, HouseholdStructure, HouseholdLogEntry, HouseholdLog
from apps.bcpp_household_member.models import HouseholdMember, EnrolmentChecklist, HouseholdInfo
from apps.bcpp_survey.models import Survey
from apps.bcpp_household_member.choices import HOUSEHOLD_MEMBER_ACTION


class HouseholdDashboard(Dashboard):

    view = 'household_dashboard'
    dashboard_name = 'Household Dashboard'
    dashboard_url_name = 'household_dashboard_url'

    def __init__(self, dashboard_type, dashboard_id, dashboard_model, dashboard_type_list=None, dashboard_models=None, **kwargs):
        self._plot = None
        self._household = None
        self._household_members = None
        self._household_structure = None
        self._household_log = None
        self._current_member_count = None
        self._enrolment_checklist = None
        self._household_info = None
        self._survey = None
        self._surveys = None
        self._first_name = None
        kwargs.update({'dashboard_models': {'household': Household, 'household_structure': HouseholdStructure}})
        super(HouseholdDashboard, self).__init__(dashboard_type, dashboard_id, dashboard_model, dashboard_type_list, dashboard_models=kwargs.get('dashboard_models'))
        if self.get_dashboard_model_name() == 'household':
            self.set_household()
            self.set_current_survey()
            self.set_household_structure()
        if self.get_dashboard_model_name() == 'household_structure':
            self.set_household_structure()
            self.set_survey(self.get_household_structure().survey)
            self.set_household()
        self.set_first_name(kwargs.get('first_name', None))
        # TODO: is this still necessary?
        self.check_members_have_registered_subject()
        self.set_mapper_name(kwargs.get('mapper_name'))

    def add_to_context(self):
        super(HouseholdDashboard, self).add_to_context()

        self.context.add(
            home='bcpp_survey',
            household_member_actions=[action[0] for action in HOUSEHOLD_MEMBER_ACTION],
            #membership_forms={'ABSENT': get_model('bcpp_subject', 'subjectabsentee')},
            title='',  # 'A. Household Composition',
            household_meta=Household._meta,
            household_member_meta=HouseholdMember._meta,
            household_structure_meta=HouseholdStructure._meta,
            household_log_entry_meta=HouseholdLogEntry._meta,
            enrolment_checklist_meta=EnrolmentChecklist._meta,
            household_info_meta=HouseholdInfo._meta,
            plot=self.get_plot(),
            household=self.get_household(),
            household_identifier=self.get_household().household_identifier,
            household_structure=self.get_household_structure(),
            household_members=self.get_household_members(),
            household_log=self.get_household_log(),
            household_log_entries=self.get_household_log_entries(),
            first_name=self.get_first_name(),
            current_member_count=self.get_current_member_count(),
            survey=self.get_survey(),
            rendered_surveys=self.render_surveys(),
            allow_edit_members=self.allow_edit_members(),
            has_household_log_entry=self.has_household_log_entry(),
            household_info=self.get_household_info(),
            mapper_name=self.get_mapper_name(),
            subject_dashboard_url='subject_dashboard_url',
            household_dashboard_url=self.dashboard_url_name,
            )

    def set_dashboard_type_list(self):
        self._dashboard_type_list = ['household']

    def set_first_name(self, value=None):
        self._first_name = value

    def get_first_name(self):
        if not self._first_name:
            self.set_first_name()
        return self._first_name

    def has_household_log_entry(self):
        """Confirms there is an househol_log_entry for today."""
        today = date.today()
        if self.get_household_log():
            if not HouseholdLogEntry.objects.filter(
                household_log=self.get_household_log(),
                report_datetime__year=today.year,
                report_datetime__month=today.month,
                report_datetime__day=today.day):
                return False
        return True

    def set_household_info(self):
        self._household_info = None
        if HouseholdInfo.objects.filter(household_structure=self.get_household_structure()):
            self._household_info = HouseholdInfo.objects.get(household_structure=self.get_household_structure())

    def get_household_info(self):
        if not self._household_info:
            self.set_household_info()
        return self._household_info

    def set_mapper_name(self, value=None):
        self._mapper_name = value
        if not self._mapper_name:
            if self.get_household():
                if not 'mapper_name' in dir(self.get_household()):
                    raise AttributeError('Expected model Household to have attribute \'mapper_name\'.')
                self._mapper_name = self.get_household().mapper_name

    def get_mapper_name(self):
        if not self._mapper_name:
            self.set_mapper_name()
        return self._mapper_name

    def set_survey(self, value=None):
        """Sets to the survey model class given a survey pk, slug or name or tries to determine the survey based on today\'s date.

        .. warning:: this will fail if no survey name is provided and there is more than one survey defined where
                     the survey dates overlap.
        """
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        re_survey_slug = re.compile('bcpp\-year\-[0-9]{1}')
        re_survey_name = re.compile('BCPP\ Year\ [0-9]{1}')
        if value:  # must be able to use the value or fail
            if isinstance(value, Survey):
                self._survey = value
            elif not re_pk.match(str(value)) and not re_survey_slug.match(str(value)) and not re_survey_name.match(str(value)):
                raise TypeError('Unable to set attribute _survey. Survey value specified, but expected a pk, slug or survey_name. Got {0}.'.format(value))
            elif re_pk.match(str(value)):
                self._survey = Survey.objects.get(pk=value)
            elif re_survey_slug.match(str(value)):
                self._survey = Survey.objects.get(survey_slug=value)
            elif re_survey_name.match(str(value)):
                self._survey = Survey.objects.get(survey_name=value)
            else:
                self._survey = None
        else:  # no value provided to try to figure it our using today's date
            if Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() == 1:
                # assume only one survey
                self._survey = Survey.objects.get(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today())
            elif Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() >= 1:
                raise TypeError('Unable to set attribute _survey given survey=None and today\'s date. More than one survey exists for the given datetime (today). Either specify a survey or given a different date. Got {0}.'.format(Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today())))
            elif Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() == 0:
                raise TypeError('Unable to set attribute _survey given survey=None and today\'s date. No survey exists to include the given datetime (today). Either create a new survey or update an existing survey\'s start and end date to include today.')
            else:
                self._survey = None
        if not self._survey:
            raise TypeError('Dashboard attribute _survey may not be null.')

    def set_current_survey(self):
        """Sets to the current survey using today's date."""
        if Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() == 1:
            self._survey = Survey.objects.get(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today())
        elif Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() >= 1:
            raise TypeError('Unable to set attribute _survey given survey=None and today\'s date. More than one survey exists for the given datetime (today). Either specify a survey or given a different date. Got {0}.'.format(Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today())))
        elif Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() == 0:
            raise TypeError('Unable to set attribute _survey given survey=None and today\'s date. No survey exists to include the given datetime (today). Either create a new survey or update an existing survey\'s start and end date to include today.')
        else:
            self._survey = None
        if not self._survey:
            raise TypeError('Dashboard attribute _survey may not be null.')

    def get_survey(self):
        if not self._survey:
            self.set_survey()
        return self._survey

    def set_surveys(self, value=None):
        self._surveys = [(self.get_survey(), '')]
        for survey in Survey.objects.all().exclude(pk=self.get_survey().pk).order_by('datetime_start'):
            # if a household_structure does not exist for this household and survey, create otherwise get
            if not HouseholdStructure.objects.filter(household=self.get_household(), survey=survey):
                household_structure = HouseholdStructure.objects.create(household=self.get_household(), survey=survey)
            else:
                household_structure = HouseholdStructure.objects.get(household=self.get_household(), survey=survey)
            url = reverse(self.dashboard_url_name, kwargs={'dashboard_type': self.dashboard_type,
                                                           'dashboard_model': 'household_structure',
                                                           'dashboard_id': household_structure.pk})
            self._surveys.append((survey, url))
        #self._surveys = Survey.objects.all().order_by('survey_name')

    def get_surveys(self):
        if not self._surveys:
            self.set_surveys()
        return self._surveys

    def get_current_member_count(self):
        try:
            self._current_member_count = self.household_members.count()
        except:
            self._current_member_count = 0

    def set_plot(self):
        self._plot = self.get_household()
        if not self._plot:
            raise TypeError('Attribute plot may not be None.')

    def get_plot(self):
        if not self._plot:
            self.set_plot()
        return self._plot

    def set_household_structure(self, value=None, pk=None):
        self._household_structure = value
        if not self._household_structure:
            if issubclass(self.get_dashboard_model(), HouseholdStructure):
                self._household_structure = self.get_dashboard_model_instance()
            # try to set with survey and household
            if issubclass(self.get_dashboard_model(), Household):
                self._household_structure = HouseholdStructure.objects.get(household__pk=self.get_household().pk, survey=self.get_survey())
            #elif HouseholdStructure.objects.filter(pk=pk, survey=self.get_survey()):
            #    self._household_structure = HouseholdStructure.objects.get(pk=pk, survey=self.get_survey())
        if not self._household_structure:
            raise TypeError('Household_structure cannot be None. Using {0}.'.format((value, pk)))

    def get_household_structure(self):
        if not self._household_structure:
            self.set_household_structure()
        return self._household_structure

    def set_household(self, pk=None, household_identifier=None, household_structure=None):
        """Sets the household instance using household attributes pk or household_identifier or household_strcuture."""
        self._household = None
        if isinstance(self.get_dashboard_model_instance(), Household):
            self._household = self.get_dashboard_model_instance()
        if isinstance(self.get_dashboard_model_instance(), HouseholdStructure):
            self._household = self.get_dashboard_model_instance().household
        if household_identifier and not self._household:
            if not Household.objects.filter(household_identifier=household_identifier):
                raise TypeError('Cannot set Household using the household_identifier. Got {0}'.format(household_identifier))
            self._household = Household.objects.get(household_identifier=household_identifier)
        if pk and not self._household:
            if not Household.objects.filter(pk=pk):
                raise TypeError('Cannot set Household using the pk. Got {0}'.format(pk))
            self._household = Household.objects.get(pk=pk)
        if household_structure and not self._household:
            self._household = household_structure.household
        if not self._household:
            raise TypeError('Household cannot be None. Using {0}'.format(pk, household_identifier, household_structure))

    def get_household(self):
        if not self._household:
            self.set_household()
        return self._household

    def set_household_members(self):
        """Sets to a queryset of household members for this household structure (and therefore survey)."""
        self.create_household_members_for_new_survey()
#         self._household_members = HouseholdMember.objects.filter(
#             household_structure__household=self.get_household(),
#             household_structure__survey=self.get_survey(),
#             ).order_by('first_name')
        self._household_members = HouseholdMember.objects.filter(
            household_structure=self.get_household_structure(),
            ).order_by('first_name')

    def get_household_members(self):
        """Returns a HouseholdMember queryset of household members for this dashboard."""
        if not self._household_members:
            self.set_household_members()
        return self._household_members

    def get_household_members_as_list(self):
        """Returns a list of household members for this dashboard."""
        return [hm for hm in self.get_household_members()]

    def set_household_log(self):
        if not HouseholdLog.objects.filter(household_structure=self.get_household_structure()):
            self._household_log = HouseholdLog.objects.create(household_structure=self.get_household_structure())
        else:
            self._household_log = HouseholdLog.objects.get(household_structure=self.get_household_structure())

    def get_household_log(self):
        if not self._household_log:
            self.set_household_log()
        return self._household_log

    def allow_edit_members(self):
        allow_edit_members = False
        if hasattr(settings, 'ALLOW_CHANGES_OTHER_SURVEYS') and settings.ALLOW_CHANGES_OTHER_SURVEYS:
            allow_edit_members = True
        else:
            if self.get_survey():
                if self.get_survey().datetime_start <= datetime.today() and datetime.today() <= self.get_survey().datetime_end:
                    allow_edit_members = True
        return allow_edit_members

    def check_members_have_registered_subject(self):
        for household_member in self.get_household_members():
            if not RegisteredSubject.objects.filter(registration_identifier=household_member.internal_identifier):
                raise ValueError('{0} expects all household_members to have '
                                 'an entry in RegisterSubject. Got None for {1}.'.format(self, household_member,))

    def get_household_log_entries(self):
        return HouseholdLogEntry.objects.filter(household_log__household_structure=self.get_household_structure())

    def create_household_members_for_new_survey(self):
        """ Prepares a householdstructure for a new survey by fetching a list of the
        householdstructure members for a given householdstructure from the FIRST
        survey and adds them to the new survey

        ..todo:: This can be improved to check if someone has moved or died and
                 if there are members identified in interim surveys.
        """
        #get first survey
        surveys = Survey.objects.all().order_by('datetime_start')
        if surveys:
            first_survey = surveys[0]
            # add members from most recent first survey to current survey
            for hm in  HouseholdMember.objects.filter(
                    household_structure__household=self.get_household_structure().household,
                    household_structure__survey=first_survey):
                if not HouseholdMember.objects.filter(
                        household_structure=self.get_household_structure(),
                        registered_subject=hm.registered_subject):
                    options = {}
                    [options.update({key: value}) for key, value in hm.__dict__.iteritems() if not key.startswith('_') and not key in ['id', 'created', 'modified', 'user_created', 'user_modified', 'hostname_created', 'hostname_modified']]
                    options.update(
                        {'household_structure_id': self.get_household_structure().pk,
                         'registered_subject_id': hm.registered_subject.pk,
                        'survey_id': self.get_survey().pk,
                        'age_in_years': None,  # TODO: can this be incremented or at least accurate for consented subjects?
                        'nights_out': None,
                        'present': '-',
                        'lives_in_household': '-',
                        'member_status': None})
                    HouseholdMember.objects.create(**options)

    def render_surveys(self):
        """Renders to string the surveys."""
        return render_to_string('surveys.html', {'surveys': self.get_surveys(), 'survey': self.get_survey()})
