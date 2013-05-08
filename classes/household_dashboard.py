import re
from datetime import datetime
from django.conf.urls.defaults import patterns, url
from django.conf import settings
from django.db.models import get_model
from bhp_dashboard.classes import Dashboard
from bhp_registration.models import RegisteredSubject
from bcpp_household.models import HouseholdStructureMember, Household, HouseholdStructure, HouseholdSurvey, HouseholdLogEntry, HouseholdLog
from bcpp_survey.models import Survey
from bcpp_household.choices import HOUSEHOLD_MEMBER_ACTION


class HouseholdDashboard(Dashboard):

    def __init__(self, **kwargs):

        super(HouseholdDashboard, self).__init__(**kwargs)
        self.subject_type = 'household'  # yuk
        self.dashboard_type = 'household'
        self.household_structure = None
        self.household_structure_members = None
        self.current_member_count = None
        self.survey = None
        self.surveys = None
        self.context.add(
            home=kwargs.get('home', 'bcpp_survey'),
            search_name=kwargs.get('search_name', 'household'),
            household_member_actions=[action[0] for action in HOUSEHOLD_MEMBER_ACTION],
            membership_forms={'ABSENT': get_model('bcpp_subject', 'subjectabsentee')},
            title='Household Dashboard',
            )

    def create(self, **kwargs):
        subject_rccs = []
        household_log = []
        household_log_entries = []
        allow_edit_members = False
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        re_survey_slug = re.compile('bcpp\-year\-[0-9]{1}')
        re_survey_name = re.compile('BCPP\ Year\ [0-9]{1}')

        self.household_identifier = kwargs.get('household_identifier')
        self.first_name = kwargs.get('first_name')
        survey = kwargs.get('survey')
        if re_pk.match(str(survey)):
            self.survey = Survey.objects.get(pk=survey)
        elif re_survey_slug.match(str(survey)):
            self.survey = Survey.objects.get(survey_slug=survey)
        elif re_survey_name.match(str(survey)):
            self.survey = Survey.objects.get(survey_name=survey)
        else:
            if Survey.objects.filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()):
                self.survey = Survey.objects.get(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today())
        self.dashboard_identifier = self.household_identifier
        self.household = Household.objects.get(household_identifier=self.household_identifier)
        if self.survey:
            allow_edit_members = False
            if hasattr(settings, 'ALLOW_CHANGES_OTHER_SUVERYS') and settings.ALLOW_CHANGES_OTHER_SUVERYS:
                allow_edit_members = True
            else:
                if self.survey:
                    if self.survey.datetime_start <= datetime.today() and datetime.today() <= self.survey.datetime_end:
                        allow_edit_members = True
            if HouseholdStructure.objects.filter(household=self.household, survey=self.survey):
                self.household_structure = HouseholdStructure.objects.get(household=self.household, survey=self.survey)
                # list household members in side bar
                self.household_structure_members = HouseholdStructureMember.objects.filter(
                                                        household_structure__household=self.household,
                                                        household_structure__survey=self.survey,
                                                        ).order_by('household_structure', 'first_name')
                for household_structure_member in self.household_structure_members:
                    if not RegisteredSubject.objects.filter(registration_identifier=household_structure_member.internal_identifier):
                        raise ValueError('{0} expects all household_structure_members to have '
                                         'an entry in RegisterSubject. Got None for {1}.'.format(self, household_structure_member,))
                if not HouseholdLog.objects.filter(household=self.household, survey=self.survey):
                    household_log = HouseholdLog.objects.create(household=self.household, survey=self.survey)
                else:
                    household_log = HouseholdLog.objects.get(household=self.household, survey=self.survey)
                household_log_entries = HouseholdLogEntry.objects.filter(household_log__household=self.household, household_log__survey=self.survey)
                self.current_member_count = self.household_structure_members.count()
        self.surveys = Survey.objects.all().order_by('survey_name')

        # call super to initialize default context
        super(HouseholdDashboard, self).create(**kwargs)
        household_surveys = HouseholdSurvey.objects.filter(household=self.household)
        self.context.add(
            household=self.household,
            household_identifier=self.household_identifier,
            household_surveys=household_surveys,
            household_structure=self.household_structure,
            household_structure_members=self.household_structure_members,
            subject_rccs=subject_rccs,
            household_log=household_log,
            household_log_entries=household_log_entries,
            first_name=self.first_name,
            current_member_count=self.current_member_count,
            survey=self.survey,
            surveys=self.surveys,
            allow_edit_members=allow_edit_members,
            )

    def get_urlpatterns(self, view, regex, **kwargs):

        regex['pk'] = '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}'
        regex['survey_slug'] = 'bcpp\-year\-[0-9]{1}|mobile\-year\-[0-9]{1}'
        regex['content_type_map'] = '\w+'

        self.urlpatterns = patterns(view,

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/(?P<survey>{survey_slug})/(?P<first_name>\w+)/(?P<gender>\w+)/(?P<initials>\w+)/(?P<household_structure_member>{pk})/$'.format(**regex),
              'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/(?P<survey>{survey_slug})/(?P<household_structure>{pk})/(?P<registered_subject>{pk})/(?P<household_structure_member>{pk})/$'.format(**regex),
              'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/(?P<survey>{survey_slug})/(?P<first_name>\w+)/$'.format(**regex),
              'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/(?P<survey>{survey_slug})/(?P<household_structure_member>{pk})/$'.format(**regex),
              'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/(?P<survey>{survey_slug})/$'.format(**regex),
              'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/(?P<survey>{survey_slug})/(?P<household>{pk})/$'.format(**regex),
              'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/(?P<survey>{survey_slug})/(?P<household_structure>{pk})/$'.format(**regex),
              'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household>{pk})/(?P<household_identifier>{household_identifier})/(?P<survey>{pk})/$'.format(**regex),
              'dashboard',
                name="dashboard_url"
                ),

            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_identifier>{household_identifier})/$'.format(**regex),
              'dashboard',
                name="dashboard_url"
                ),
            )
        return self.urlpatterns
