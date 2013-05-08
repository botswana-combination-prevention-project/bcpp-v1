import copy
from django.conf.urls import patterns, url
from bhp_dashboard_registered_subject.classes import RegisteredSubjectDashboard
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment
from bcpp_household.models import HouseholdStructureMember
from bcpp_subject.models import SubjectVisit
from bcpp_lab.models import SubjectRequisition
from bcpp_survey.models import Survey


class SubjectDashboard(RegisteredSubjectDashboard):

    def __init__(self, **kwargs):
        self.dashboard_type = 'subject'
        super(SubjectDashboard, self).__init__(**kwargs)
        self.visit_model = SubjectVisit
        self.requisition_model = SubjectRequisition
        self.visit_model_app_label = SubjectVisit._meta.app_label
        self.visit_model_name = SubjectVisit._meta.module_name
        self._appointment = None
        self._set_appointment(kwargs.get('appointment', None))
        self.subject_type = 'subject'
        self.survey = None
        self.household_structure_member = None
        self.household = None
        self.household_structure = None
        self.subject_consent = None
        self.exclude_others_if_keyed_model_name = 'subjectconsent'
#         self.include_after_exclusion_model_keyed = ['subjectreferral', ]
        self.context.add(
            visit_model_name=self.visit_model_name,
            appointment=self._get_appointment(),
            requisition_model=SubjectRequisition,
            visit_model=self.visit_model,
            visit_model_app_label=self.visit_model_app_label,
            subject_type=self.subject_type,
            home=kwargs.get('home', 'bcpp_survey'),
            search_name=kwargs.get('search_name', 'subject'),
            )

    def _set_appointment(self, appointment):
        self._appointment = None
        if appointment:
            if isinstance(appointment, Appointment):
                self._appointment = appointment
            elif isinstance(appointment, basestring):
                if Appointment.objects.filter(pk=appointment):
                    self._appointment = Appointment.objects.get(pk=appointment)
            else:
                raise AttributeError('Unable to determine appointment for SubjectDashboard {0}'.format(self.__class__))

    def _get_appointment(self, appointment=None):
        if not self._appointment:
            self._set_appointment(appointment)
        return self._appointment

    def create(self, **kwargs):
        household_structure_members = None
        # must have this
        self.household_structure_member = kwargs.get('household_structure_member')
        self.subject_identifier = kwargs.get('subject_identifier')
        self.dashboard_identifier = kwargs.get('subject_identifier')
        # the household_structure is allowed to be null, but hopefully not
        if self.household_structure_member.household_structure:
            self.household = self.household_structure_member.household_structure.household
            self.household_structure = self.household_structure_member.household_structure
            # list household members in side bar
            household_structure_members = HouseholdStructureMember.objects.filter(
                                              household_structure_id=self.household_structure_member.household_structure_id
                                              ).order_by('household_structure', 'first_name')
        # must have this
        self.survey = self.household_structure_member.survey
        if not self.subject_identifier:
            self.subject_consent = kwargs.get('subject_consent', None)
            if self.subject_consent:
                self.dashboard_identifier = self.subject_consent.subject_identifier
        if not self.subject_identifier:
            # subject is not consented for this survey, just a household_structure_member
            # of this survey. but no matter what
            # the RegisteredSubject instance exists. registered_subject may not have a
            # subject_identifier if subject has NEVER consented
            # for any survey
            if RegisteredSubject.objects.filter(registration_identifier=self.household_structure_member.internal_identifier).exists():
                registered_subject = RegisteredSubject.objects.get(registration_identifier=self.household_structure_member.internal_identifier)
                if registered_subject.subject_identifier:
                    # was consented for a previous survey
                    self.dashboard_identifier = registered_subject.subject_identifier
                else:
                    # never consented so never given an identifier
                    if self.household_structure_member.household_structure:
                        self.dashboard_identifier = '%s (%s) %s of household %s' % (registered_subject.first_name,
                                                                                    registered_subject.initials,
                                                                                    registered_subject.gender,
                                                                                    self.household_structure_member.household_structure.household.household_identifier)
                    else:
                        self.dashboard_identifier = '%s (%s) %s of household UNKNOWN' % (registered_subject.first_name,
                                                                                         registered_subject.initials,
                                                                                         registered_subject.gender,)
            else:
                # ...not sure you'll ever get here since registered_subject instance is
                # created when the household_structure_member
                # instance is created.
                self.dashboard_identifier = '%s (%s) %s NEW MEMBER' % (self.household_structure_member.first_name,
                                                                       self.household_structure_member.initials,
                                                                       self.household_structure_member.gender)
        options = copy.copy(kwargs)
        options.update({'membership_form_category': self.survey.survey_slug})
        super(SubjectDashboard, self).create(**options)
        if not self.survey:
            raise ValueError('{0} requires a value for survey. Got None.'.format(self,))
        kwargs.update({'household': self.household})
        kwargs.update({'survey': self.survey})
        kwargs.update({'household_structure_members': household_structure_members})
        kwargs.update({'household_structure': self.household_structure})
        kwargs.update({'extra_url_context': '&household_structure_member=%s&survey=%s' % (self.household_structure_member.pk, self.survey.survey_slug,)})
        self.context.add(**kwargs)

    def get_urlpatterns(self, view, regex, **kwargs):
        super(SubjectDashboard, self).get_urlpatterns(view, regex, **kwargs)
        regex['pk'] = '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}'
        regex['panel'] = '\d+'
        regex['content_type_map'] = '[a-z0-9]+'

        urlpatterns = patterns(view,
           url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_structure_member>{pk})/(?P<appointment>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
           url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_structure_member>{pk})/(?P<subject_identifier>{subject_identifier})/(?P<appointment>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
           url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registration_identifier>{pk})/$'.format(**regex),
                  'dashboard',
                    name="dashboard_url"
                    ),
           url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/$'.format(**regex),
              'dashboard',
               name="dashboard_url"
                ),
           url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_structure_member>{pk})/(?P<registered_subject>{pk})/$'.format(**regex),
                  'dashboard',
                    name="dashboard_url"
                    ),)

        for survey in Survey.objects.all():
            regex['survey_slug'] = survey.survey_slug
            urlpatterns += patterns(view,
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<household_structure_member>{pk})/(?P<survey>{survey_slug})/(?P<appointment>{pk})/$'.format(**regex),
                    'dashboard',
                    name="dashboard_visit_url"
                    ),
                url(r'^(?P<subject_visit>{pk})/(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<household_structure_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/$'.format(**regex),
                    'dashboard',
                    name="dashboard_visit_add_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<household_structure_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/(?P<content_type_map>{content_type_map})/$'.format(**regex),
                    'dashboard',
                    name="dashboard_visit_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<household_structure_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/(?P<panel>{panel})/$'.format(**regex),
                    'dashboard',
                    name="dashboard_visit_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_visit>{pk})/(?P<subject_identifier>{subject_identifier})/(?P<household_structure_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/(?P<panel>{panel})/$'.format(**regex),
                    'dashboard',
                    name="dashboard_visit_add_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<household_structure_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/$'.format(**regex),
                    'dashboard',
                    name="dashboard_visit_url"
                    ),

                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<household_structure_member>{pk})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<survey>{survey_slug})/$'.format(**regex),
                    'dashboard',
                    name="dashboard_visit_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<survey>{survey_slug})/(?P<subject_identifier>{subject_identifier})/(?P<registered_subject>{pk})/(?P<household_structure_member>{pk})/$'.format(**regex),
                  'dashboard',
                    name="dashboard_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<survey>{survey_slug})/(?P<subject_identifier>{subject_identifier})/(?P<appointment>{pk})/(?P<household_structure_member>{pk})/$'.format(**regex),
                  'dashboard',
                    name="dashboard_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<survey>{survey_slug})/(?P<subject_identifier>{pk})/(?P<registered_subject>{pk})/(?P<household_structure_member>{pk})/$'.format(**regex),
                  'dashboard',
                    name="dashboard_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<survey>{survey_slug})/(?P<household_structure_member>{pk})/$'.format(**regex),
                  'dashboard',
                    name="dashboard_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<survey>{survey_slug})/(?P<pk>{pk})/$'.format(**regex),
                  'dashboard',
                    name="dashboard_url_pk"
                    ))
        return urlpatterns
