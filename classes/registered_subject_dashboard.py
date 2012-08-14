from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url
from django.template.loader import render_to_string
from bhp_entry.models import ScheduledEntryBucket, AdditionalEntryBucket
from bhp_lab_entry.models import ScheduledLabEntryBucket, AdditionalLabEntryBucket
from bhp_bucket.classes import bucket
from bhp_appointment.models import Appointment
from bhp_visit.models import ScheduleGroup, VisitDefinition
from bhp_registration.models import RegisteredSubject
from bhp_dashboard.classes import Dashboard
from bhp_subject_summary.models import Link
from lab_clinic_api.classes import EdcLab


class RegisteredSubjectDescriptor(object):
    """ For a registered_subject instance only. """
    def __init__(self):
        self.value = RegisteredSubject.objects.none()

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if value:
            if isinstance(value, RegisteredSubject):
                self.value = value
            else:
                raise AttributeError('Can\'t set attribute \'registered_subject\'. '
                                     'Must be an instance of RegisteredSubject. '
                                     'Got {0}.'.format(type(self.registered_subject)))
        else:
            raise AttributeError('Can\'t set attribute registered_subject. Got none.')


class RegisteredSubjectDashboard(Dashboard):

    """ Create and add to a default clinic 'registered subject' dashboard context and render_to_response from a view in shell. """

    registered_subject = RegisteredSubjectDescriptor()

    def __init__(self, **kwargs):

        super(RegisteredSubjectDashboard, self).__init__(**kwargs)
        self.scheduled_entry_bucket = None
        self.additional_entry_bucket = None
        self.scheduled_lab_bucket = None
        self.additional_lab_bucket = None
        self.selected_visit = None
        self.visit = None
        self.visit_code = None
        self.visit_instance = None
        self.visit_model = None
        self.subject_identifier = None
        self.app_label = None
        self.requisition_model = None
        self.appointment_row_template = 'appointment_row.html'
        #side bar links for med, etc summaries
        self.summary_links = ''
        # limit the membership forms to those of this category
        self.membership_form_category = None
        self.exclude_others_if_keyed_model_name = ''  # this is a form name or regex pattern
        self.include_after_exclusion_model_keyed = []
        self.scheduled_entry_bucket_rules = []

    def create(self, **kwargs):
        super(RegisteredSubjectDashboard, self).create(**kwargs)
        if not self.appointment_row_template:
            self.appointment_row_template = 'appointment_row.html'
            self.context.add(appointment_row_template=self.appointment_row_template)
        self.registered_subject = kwargs.get('registered_subject', self.registered_subject)
        if self.registered_subject:
            self.subject_type = kwargs.get('subject_type', self.registered_subject.subject_type)
            # subject identifier is almost always available
            self.subject_identifier = self.registered_subject.subject_identifier
            self.dashboard_identifier = self.subject_identifier
            if not self.subject_identifier:
                # but if not, check for registration_identifier
                self.subject_identifier = self.registered_subject.registration_identifier
                self.dashboard_identifier = ('{0} [{1}] {2}'.format(self.registered_subject.first_name,
                                                                    self.registered_subject.initials,
                                                                    self.registered_subject.gender,))
            if not self.subject_identifier:
                raise AttributeError('RegisteredSubjectDashboard requires a subject_identifier. '
                                     'RegisteredSubject has no identifier for this subject.')
            self.context.add(
                registered_subject=self.registered_subject,
                subject_identifier=self.subject_identifier,
                subject_type=self.subject_type,
                )
        self.visit_code = kwargs.get('visit_code', self.visit_code)
        self.visit_instance = kwargs.get("visit_instance", self.visit_instance)
        self.visit_model = kwargs.get('visit_model', self.visit_model)
        if self.extra_url_context == {}:
            self.extra_url_context = ''
        self.context.add(
            visit_model=self.visit_model,
            visit_instance=self.visit_instance,
            visit_code=self.visit_code,
            extra_url_context=self.extra_url_context
            )
        if not self.requisition_model:
            raise AttributeError('RegisteredSubjectDashboard.create() requires attribute '
                                 '\'requisition_model\'. Got none.')
        if not self.visit_model:
            raise AttributeError('RegisteredSubjectDashboard.create() requires attribute '
                                 '\'visit_model\'. Got none.')
        else:
            self.context.add(visit_model_add_url=self._get_visit_model_url(self.visit_model))
        self._set_membership_forms()
        self._set_appointments()
        self._set_additional_entry_bucket()
        self._set_scheduled_entry_bucket()
        self._set_scheduled_lab_bucket()
        self._set_additional_lab_bucket()
        self._set_current_appointment()
        self._set_current_visit()
        self._set_summary_links()
        self._add_to_entry_buckets()
        self._run_entry_bucket_rules()

    def _add_to_entry_buckets(self):
        # update / add to entries in ScheduledEntryBucket, ScheduledLabEntryBucket
        if self.visit:
            ScheduledEntryBucket.objects.add_for_visit(visit_model_instance=self.visit)
            # if requisition_model has been defined, assume scheduled labs otherwise pass
            if hasattr(self, 'requisition_model'):
                ScheduledLabEntryBucket.objects.add_for_visit(
                    visit_model_instance=self.visit,
                    requisition_model=self.requisition_model,
                    )

    def _run_entry_bucket_rules(self, **kwargs):

        """ Runs rules in self.scheduled_entry_bucket_rules if visit_code is known.

        Add rules before calling create()
        If called, update entry status (new, not required, etc) when the visit dashboard is refreshed."""
        if not self.subject_identifier:
            raise AttributeError('set value of subject_identifier before calling dashboard create() when scheduled_entry_bucket_rules exist')
        # run rules if visit_code is known -- user selected, that is user clicked to see list of
        # scheduled entries for a given visit.
        if self.visit_code:
            # TODO: on data entry, is the visit_model_instance always 0 or the actual instance 0,1,2, etc
            if self.visit_model.objects.filter(
                appointment__registered_subject__subject_identifier=self.subject_identifier,
                appointment__visit_definition__code=self.visit_code,
                appointment__visit_instance=self.visit_instance):
                visit_model_instance = self.visit_model.objects.get(
                    appointment__registered_subject__subject_identifier=self.subject_identifier,
                    appointment__visit_definition__code=self.visit_code,
                    appointment__visit_instance=self.visit_instance)
                for rule in bucket.dashboard_rules:
                    rule.run(visit_model_instance=visit_model_instance)
                bucket.update_all(visit_model_instance)

    def _get_visit_model_url(self, visit_model):
        model_name = visit_model._meta.module_name
        app_label = visit_model._meta.app_label
        self.context.add(visit_model_app_label=app_label)
        try:
            url = reverse('admin:%s_%s_add' % (app_label, model_name))
        except:
            # model must be registered in admin
            raise ValueError('NoReverseMatch: Reverse for \'%s_%s_add\'. Check model is '
                                 'registered in admin'.format(app_label, model_name))
        self.context.add(visit_model_name=model_name)
        return url

    def _set_summary_links(self):
        # render side bar template for subject summaries
        self.summary_links = render_to_string('summary_side_bar.html', {
                'links': Link.objects.filter(dashboard_type=self.dashboard_type),
                'subject_identifier': self.subject_identifier,
                })
        self.context.add(summary_links=self.summary_links)

    def _set_scheduled_entry_bucket(self):
        # get list of scheduled crfs
        if self.visit_code:
            # filter for appointment with visit_instance=0
            appointment = Appointment.objects.get(
                              registered_subject=self.registered_subject,
                              visit_definition__code=self.visit_code,
                              visit_instance=0)
            self.scheduled_entry_bucket = ScheduledEntryBucket.objects.get_entries_for(
                                              registered_subject=self.registered_subject,
                                              appointment=appointment,
                                              visit_code=self.visit_code)
        self.context.add(scheduled_entry_bucket=self.scheduled_entry_bucket)

    def _set_scheduled_lab_bucket(self):
        # get list of scheduled crfs
        if self.visit_code:
            # filter for appointment with visit_instance=0
            appointment = Appointment.objects.get(
                             registered_subject=self.registered_subject,
                             visit_definition__code=self.visit_code,
                             visit_instance=0)
            self.scheduled_lab_bucket = ScheduledLabEntryBucket.objects.get_scheduled_labs_for(
                                            registered_subject=self.registered_subject,
                                            appointment=appointment,
                                            visit_code=self.visit_code)
        self.context.add(scheduled_lab_bucket=self.scheduled_lab_bucket)

    def _set_additional_lab_bucket(self):
        # get list of scheduled crfs
        if self.visit_code:
            # filter for appointment with visit_instance=0
            appointment = Appointment.objects.get(
                              registered_subject=self.registered_subject,
                              visit_definition__code=self.visit_code,
                              visit_instance=0)
            self.additional_lab_bucket = AdditionalLabEntryBucket.objects.get_labs_for(
                                             registered_subject=self.registered_subject,
                                             appointment=appointment)
        self.context.add(additional_lab_bucket=self.additional_lab_bucket)

    def _set_appointments(self):
        # get all appointments for this registered_subject
        # if self.visit_code and self.visit_instance, then limit to the one appointment
        appointments = None
        if self.visit_code and self.visit_instance:
            appointments = Appointment.objects.filter(registered_subject=self.registered_subject,
                                                      visit_definition__code=self.visit_code,
                                                      visit_instance=self.visit_instance)
        else:
            # or filter appointments for the current membership category

            # Note: previously, the membership_form_category was defaulted to the subject_type
            # and this method returned ALL appointment for a registered subject.
            # I now return only the registered_subject's appointments filtered for a given membership_form_category.

            # get list visit_definition__code for this membership_form_category to filter the appointments by
            codes = VisitDefinition.objects.codes_for_membership_form_category(membership_form_category=self.membership_form_category)
            # select the appointments
            appointments = Appointment.objects.filter(registered_subject=self.registered_subject,
                                                      visit_definition__code__in=codes,
                                                      ).order_by('visit_definition__code', 'visit_instance', 'appt_datetime')
        # add to the context
        self.context.add(appointments=appointments)

    def _set_current_visit(self):
        if self.appointment:
            # set the visit
            if self.visit_model:
                self.visit = self.visit_model.objects.get(appointment=self.appointment)
            else:
                raise AttributeError('Cannot determine attribute \'visit_model\' in RegisteredSubjectDashboard. Got none. Either pass as a attribute or add_to_context')
        else:
            self.visit = self.visit_model.objects.none()
        self.context.add(visit=self.visit)

    def _set_current_appointment(self):
        self.appointment = Appointment.objects.none()
        # get the appointment that has focus based on visit_code
        if self.visit_code:
            # get visit associated with this appointment (in progress) and visit code and instance
            if Appointment.objects.filter(registered_subject=self.registered_subject,
                                        visit_definition__code=self.visit_code,
                                        visit_instance=self.visit_instance,):
                # set the appointment
                self.appointment = Appointment.objects.get(
                    registered_subject=self.registered_subject,
                    visit_definition__code=self.visit_code,
                    visit_instance=self.visit_instance,
                    )
        self.context.add(appointment=self.appointment)

    def _set_additional_entry_bucket(self):
        # get additional crfs
        self.additional_entry_bucket = AdditionalEntryBucket.objects.filter(
            registered_subject=self.registered_subject
            )
        self.context.add(additional_entry_bucket=self.additional_entry_bucket)

    def _set_membership_forms(self):
        # membership forms can also be proxy models ... see mochudi_subject.models
        # you may specify the membership_form_category, otherwise just use subject type
        if not self.membership_form_category:
            self.membership_form_category = self.subject_type
        # add membership forms for this registered_subject and subject_type
        # these are the KEYED, UNKEYED schedule group membership forms
        self.membership_forms = ScheduleGroup.objects.get_membership_forms_for(
            registered_subject=self.registered_subject,
            membership_form_category=self.membership_form_category,
            exclude_others_if_keyed_model_name=self.exclude_others_if_keyed_model_name,
            include_after_exclusion_model_keyed=self.include_after_exclusion_model_keyed,
            )
        self.context.add(
            membership_forms=self.membership_forms,
            keyed_membership_forms=self.membership_forms['keyed'],
            unkeyed_membership_forms=self.membership_forms['unkeyed'],
            )

    def render_labs(self, update=False):
        # prepare results for dashboard sidebar
        edc_lab = EdcLab()
        return edc_lab.render(self.subject_identifier, False)

    def get_urlpatterns(self, view, regex, **kwargs):

        """ Generates dashboard urls.

        Add this to your urls.py of your local dashboard app.
            regex = {}
            regex['dashboard_type'] = 'subject'
            regex['subject_identifier'] = 'S[0-9]{6}\-[0-9]{2}\-[A-Z]{3}[0-9]{2}'
            regex['visit_code'] = '\w+'
            regex['visit_instance'] = '[0-9]{1}'
            subject_dashboard = SubjectDashboard()
            urlpatterns = subject_dashboard.get_urlpatterns('mochudi_survey_dashboard.views', regex, visit_field_names=['subject_visit',])"""

        regex['pk'] = '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}'
        regex['content_type_map'] = '\w+'
        visit_field_names = kwargs.get('visit_field_names', ['visit'])
        if 'registration_identifier' not in regex.keys():
            regex['registration_identifier'] = '[A-Z0-9]{6,8}'
        urlpatterns = patterns(view,
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<panel>\d+)/$'.format(**regex),
                'dashboard',
                name="dashboard_visit_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<panel>\d+)/(?P<current_entry_title>[\w\s\(\)]+)/$'.format(**regex),
                'dashboard',
                name="dashboard_visit_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<appointment>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_visit_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<appointment>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_visit_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<content_type_map>{content_type_map})/$'.format(**regex),
                'dashboard',
                name="dashboard_visit_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<appointment>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_visit_url"),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/$'.format(**regex),
                'dashboard',
                name="dashboard_visit_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/$'.format(**regex),
                'dashboard',
                name="dashboard_visit_url"
                ))

        for visit_field_name in visit_field_names:
            regex['visit_field_name'] = visit_field_name
            urlpatterns += patterns(view,
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<{visit_field_name}>{pk})/(?P<panel>\d+)/$'.format(**regex),
                    'dashboard',
                    name="dashboard_visit_add_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<{visit_field_name}>{pk})/$'.format(**regex),
                    'dashboard',
                    name="dashboard_visit_add_url"
                    ),
                url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<{visit_field_name}>{pk})/$'.format(**regex),
                    'dashboard',
                    name="dashboard_visit_add_url"
                    ))

        urlpatterns += patterns(view,
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registered_subject>{pk})/(?P<visit_definition>{pk})/(?P<visit_instance>{visit_instance})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})(?P<appointment>{pk})/(?P<subject_identifier>{subject_identifier})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<appointment>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registered_subject>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registration_identifier>{registration_identifier})/(?P<registered_subject>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<registered_subject>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registration_identifier>{registration_identifier})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registered_subject>{pk})/(?P<visit_definition>{pk})/(?P<visit_instance>{visit_instance})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<registered_subject>{pk})/(?P<subject_consent>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<pk>{pk})/$'.format(**regex),
                'dashboard',
                name="pk_dashboard_url"
                ))
        return urlpatterns
