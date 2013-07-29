import copy
import re
from django.conf.urls import patterns, url
from bhp_dashboard_registered_subject.classes import RegisteredSubjectDashboard
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment
from bcpp_household_member.models import HouseholdMember
from bcpp_subject.models import SubjectVisit
from bcpp_lab.models import SubjectRequisition
from bcpp_survey.models import Survey


class SubjectDashboard(RegisteredSubjectDashboard):

    def __init__(self):
        self.dashboard_type = 'subject'
        self.subject_type = 'subject'
        super(SubjectDashboard, self).__init__()
        self.visit_model = SubjectVisit
        self.requisition_model = SubjectRequisition
        self.visit_model_app_label = SubjectVisit._meta.app_label
        self.visit_model_name = SubjectVisit._meta.module_name
        self._appointment = None
        self._survey = None
        self._household_member = None
        self._household_members = None
        self._household = None
        self.exclude_others_if_keyed_model_name = 'subjectconsent'
        self.context.add(
            visit_model_name=self.visit_model_name,
            requisition_model=SubjectRequisition,
            visit_model=self.visit_model,
            visit_model_app_label=self.visit_model_app_label,
            subject_type=self.subject_type,
            home='bcpp_survey',
            search_name='subject',
            )

    def create(self, **kwargs):
        self.set_household_member(kwargs.get('household_member', None) or kwargs.get('pk'))
        self.set_registered_subject()
        self.dashboard_identifier = self.get_subject_identifier()
        self.set_appointment(kwargs.get('appointment', None))

        options = copy.copy(kwargs)
        options.update({'membership_form_category': self.get_survey().survey_slug})
        super(SubjectDashboard, self).create(**options)

        self.context.add(
            household_member=self.get_household_member(),
            registered_subject=self.get_registered_subject(),
            subject_identifier=self.get_subject_identifier(),
            subject_consent=self.get_household_member().consent(),
            household=self.get_household(),
            survey=self.get_survey(),
            title='Subject Dashboard',
            household_members=self.get_household_members(),
            household_structure=self.get_household_member().household_structure,
            extra_url_context='&household_member={0}&survey={1}'.format(self.get_household_member().pk, self.get_survey().survey_slug),
            appointment=self.get_appointment(),
            )

    def set_survey(self):
        self._survey = self.get_household_member().survey

    def get_survey(self):
        if not self._survey:
            self.set_survey()
        return self._survey

    def set_appointment(self, appointment):
        self._appointment = None
        if appointment:
            if isinstance(appointment, Appointment):
                self._appointment = appointment
            elif isinstance(appointment, basestring):
                if Appointment.objects.filter(pk=appointment):
                    self._appointment = Appointment.objects.get(pk=appointment)
            else:
                raise AttributeError('Unable to determine appointment for SubjectDashboard {0}'.format(self.__class__))

    def get_appointment(self, appointment=None):
        if not self._appointment:
            self.set_appointment(appointment)
        return self._appointment

    def set_household_member(self, pk):
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if not pk:
            raise TypeError('Expected pk for the household member. Got None.')
        self._household_member = HouseholdMember.objects.get(pk=pk)

    def get_household_member(self):
        if not self._household_member:
            self.set_household_member()
        return self._household_member

    def set_household(self):
        self._household = self.get_household_member().household

    def get_household(self):
        if not self._household:
            self.set_household()
        return self._household

    def set_registered_subject(self, value=None):
        """Sets the registered subject using a given pk or from household member."""
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        self._registered_subject = None
        if re_pk.match(str(value)):
            self._registered_subject = RegisteredSubject.objects.get(pk=value)
        elif self.get_appointment():
            self._registered_subject = self.get_appointment()
        elif RegisteredSubject.objects.filter(registration_identifier=self.get_household_member().internal_identifier).exists():
            self._registered_subject = RegisteredSubject.objects.get(registration_identifier=self.get_household_member().internal_identifier)
        else:
            raise ValueError('Expect all household_members to have an entry in RegisterSubject. Got None for member {0}.'.format(self.get_household_member()))

    def set_subject_identifier(self, value=None):
        super(SubjectDashboard, self).set_subject_identifier(value or self.get_registered_subject().subject_identifier or self.get_registered_subject().registration_identifier)

    def set_household_members(self):
        self._household_members = HouseholdMember.objects.filter(
            household_structure=self.get_household_member().household_structure).order_by('household_structure', 'first_name')

    def get_household_members(self):
        if not self._household_members:
            self.set_household_members()
        return self._household_members

    def get_urlpatterns(self, view, regex, **kwargs):
        super(SubjectDashboard, self).get_urlpatterns(view, regex, **kwargs)
        regex['pk'] = '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}'
        regex['panel'] = '\d+'
        regex['content_type_map'] = '[a-z0-9]+'

        urlpatterns = patterns(view,
           url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_member>{pk})/(?P<appointment>{pk})/$'.format(**regex),
                'subject_dashboard',
                name="subject_dashboard_url"
                ),
           url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_member>{pk})/(?P<subject_identifier>{subject_identifier})/(?P<appointment>{pk})/$'.format(**regex),
                'subject_dashboard',
                name="subject_dashboard_url"
                ),
           url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registration_identifier>{pk})/$'.format(**regex),
                  'subject_dashboard',
                    name="subject_dashboard_url"
                    ),
           url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/$'.format(**regex),
              'subject_dashboard',
               name="subject_dashboard_url"
                ),
           url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_member>{pk})/(?P<registered_subject>{pk})/$'.format(**regex),
                  'subject_dashboard',
                    name="subject_dashboard_url"
                    ),)

        for survey in Survey.objects.all():
            regex['survey_slug'] = survey.survey_slug
            urlpatterns += patterns(view,
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<household_member>{pk})/(?P<survey>{survey_slug})/(?P<appointment>{pk})/$'.format(**regex),
                    'subject_dashboard',
                    name="subject_dashboard_visit_url"
                    ),
                url(r'^(?P<subject_visit>{pk})/(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<household_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/$'.format(**regex),
                    'subject_dashboard',
                    name="subject_dashboard_visit_add_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<household_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/(?P<content_type_map>{content_type_map})/$'.format(**regex),
                    'subject_dashboard',
                    name="subject_dashboard_visit_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<household_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/(?P<panel>{panel})/$'.format(**regex),
                    'subject_dashboard',
                    name="subject_dashboard_visit_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_visit>{pk})/(?P<subject_identifier>{subject_identifier})/(?P<household_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/(?P<panel>{panel})/$'.format(**regex),
                    'subject_dashboard',
                    name="subject_dashboard_visit_add_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<household_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/$'.format(**regex),
                    'subject_dashboard',
                    name="subject_dashboard_visit_url"
                    ),

                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/$'.format(**regex),
                    'subject_dashboard',
                    name="subject_dashboard_visit_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<survey>{survey_slug})/(?P<subject_identifier>{subject_identifier})/(?P<registered_subject>{pk})/(?P<household_member>{pk})/$'.format(**regex),
                  'subject_dashboard',
                    name="subject_dashboard_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<survey>{survey_slug})/(?P<subject_identifier>{subject_identifier})/(?P<appointment>{pk})/(?P<household_member>{pk})/$'.format(**regex),
                  'subject_dashboard',
                    name="subject_dashboard_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<survey>{survey_slug})/(?P<subject_identifier>{pk})/(?P<registered_subject>{pk})/(?P<household_member>{pk})/$'.format(**regex),
                  'subject_dashboard',
                    name="subject_dashboard_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<survey>{survey_slug})/(?P<household_member>{pk})/$'.format(**regex),
                  'subject_dashboard',
                    name="subject_dashboard_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<survey>{survey_slug})/(?P<pk>{pk})/$'.format(**regex),
                  'subject_dashboard',
                    name="subject_dashboard_url_pk"
                    ))
        return urlpatterns
