import re
from datetime import datetime
from django.conf.urls.defaults import patterns, url
from django.conf import settings
from django.db.models import get_model
from bhp_dashboard.classes import Dashboard
from bhp_registration.models import RegisteredSubject
from bcpp_household.models import Household, HouseholdStructure, HouseholdLogEntry, HouseholdLog
from bcpp_household_member.models import HouseholdMember, EnrolmentChecklist
from bcpp_survey.models import Survey
from bcpp_household.choices import HOUSEHOLD_MEMBER_ACTION
from bhp_section.classes import site_sections
from bhp_map.classes import site_mappers


class HouseholdDashboard(Dashboard):

    def __init__(self):
        super(HouseholdDashboard, self).__init__()
        self._household_members = None
        self._household_structure = None
        self._household_log = None
        self._current_member_count = None
        self._enrolment_checklist = None
        self._survey = None
        # TODO: section/search stuff should move to base class
        section = site_sections.get('household')
        self.context.add(
            section_name=section().get_section_name(),
            search_type=section().get_search_type(section().get_section_name()),
            home='bcpp_survey',
            search_name='household',
            household_member_actions=[action[0] for action in HOUSEHOLD_MEMBER_ACTION],
            membership_forms={'ABSENT': get_model('bcpp_subject', 'subjectabsentee')},
            title='A. Household Composition',
            household_meta=Household._meta,
            household_member_meta=HouseholdMember._meta,
            household_structure_meta=HouseholdStructure._meta,
            enrolment_checklist_meta=EnrolmentChecklist._meta,
            )

    def create(self, **kwargs):
        """Sets the template context for the dashboard given the survey and household.

        .. note:: the participation form is a property on the HouseholdMember model so there is no need
                  to import and pass it to the template context here."""
        self.set_dashboard_type('household')
        self.set_survey(kwargs.get('survey'))
        self.set_household(**kwargs)
        self.dashboard_identifier = self.get_household().household_identifier

        super(HouseholdDashboard, self).create(**kwargs)

        # TODO: is this still necessary?
        self.check_members_have_registered_subject()

        self.context.add(
            household=self.get_household(),
            household_identifier=self.get_household().household_identifier,
            household_structure=self.get_household_structure(),
            household_members=self.get_household_members(),
            household_log=self.get_household_log(),
            household_log_entries=self.get_household_log_entries(),
            first_name=kwargs.get('first_name', None),
            current_member_count=self.get_current_member_count(),
            survey=self.get_survey(),
            surveys=Survey.objects.all().order_by('survey_name'),
            allow_edit_members=self.allow_edit_members(),
            )
        self.set_mapper_name(kwargs.get('mapper_name'))
        self.context.add(mapper_name=self.get_mapper_name())

    def set_mapper_name(self, value=None):
        self._mapper_name = value
        if not self._mapper_name:
            if self.get_household():
                if not 'mapper_name' in self.get_household():
                    raise AttributeError('Expected model Household to have attribute \'mapper_name\'.')
                self._mapper_name = self.get_household().mapper_name

    def get_mapper_name(self):
        if not self._mapper_name:
            self.set_mapper_name()
        return self._mapper_name

    def set_survey(self, survey):
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        re_survey_slug = re.compile('bcpp\-year\-[0-9]{1}')
        re_survey_name = re.compile('BCPP\ Year\ [0-9]{1}')
        if re_pk.match(str(survey)):
            self._survey = Survey.objects.get(pk=survey)
        elif re_survey_slug.match(str(survey)):
            self._survey = Survey.objects.get(survey_slug=survey)
        elif re_survey_name.match(str(survey)):
            self._survey = Survey.objects.get(survey_name=survey)
        else:
            if Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()):
                self._survey = Survey.objects.get(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today())

    def get_survey(self):
        if not self._survey:
            raise TypeError('Dashboard attribute _survey may not be null.')
        return self._survey

    def get_current_member_count(self):
        try:
            self._current_member_count = self.household_members.count()
        except:
            self._current_member_count = 0

    def set_household(self, **kwargs):
        household_identifier = kwargs.get('household_identifier', None)
        if not household_identifier:
            pk = kwargs.get('household_structure', None)
            if HouseholdStructure.objects.filter(pk=pk):
                household_identifier = HouseholdStructure.objects.get(pk=pk).household.household_identifier
        if not household_identifier:
            raise TypeError('Household identifier is required for the dashboard. Got None.')
        if not Household.objects.filter(household_identifier=household_identifier):
            raise TypeError('Cannot set Household for given identifier. Got {0}'.format(household_identifier))
        self._household = Household.objects.get(household_identifier=household_identifier)

    def get_household(self):
        if not self._household:
            raise TypeError('Dashboard attribute _household may not be null. Set this from kwargs in method create.')
        return self._household

    def set_household_members(self):
        self._household_members = HouseholdMember.objects.filter(
            household_structure__household=self.get_household(),
            household_structure__survey=self.get_survey(),
            ).order_by('first_name')

    def get_household_members(self):
        if not self._household_members:
            self.set_household_members()
        return self._household_members

    def get_household_structure(self):
        try:
            return HouseholdStructure.objects.get(household=self.get_household(), survey=self.get_survey())
        except:
            return None

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

    def get_urlpatterns(self, view, regex, **kwargs):
        regex['pk'] = '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}'
        regex['survey_slug'] = 'bcpp\-year\-[0-9]{1}|mobile\-year\-[0-9]{1}'
        regex['content_type_map'] = '\w+'
        return patterns(view,
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/(?P<household>{pk})/(?P<household_structure>{pk})/$'.format(**regex),
              'household_dashboard',
                name="household_dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_member>{pk})/(?P<household_identifier>{household_identifier})/$'.format(**regex),
              'household_dashboard',
                name="household_dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/(?P<household_structure>{pk})/$'.format(**regex),
              'household_dashboard',
                name="household_dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_structure>{pk})/$'.format(**regex),
              'household_dashboard',
                name="household_dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/$'.format(**regex),
              'household_dashboard',
                name="household_dashboard_url"
                ),
            )
