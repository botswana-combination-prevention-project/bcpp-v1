from textwrap import wrap
from datetime import datetime
from django.db import models
from django.db.models import TextField
from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url
from django.template.loader import render_to_string
from bhp_crypto.fields import EncryptedTextField
from bhp_entry.models import AdditionalEntryBucket
from bhp_lab_entry.models import ScheduledLabEntryBucket, AdditionalLabEntryBucket
from bhp_entry_rules.classes import rule_groups
from bhp_appointment.models import Appointment
from bhp_visit.models import ScheduleGroup, MembershipForm
from bhp_registration.models import RegisteredSubject
from bhp_dashboard.classes import Dashboard
from bhp_subject_summary.models import Link
from lab_clinic_api.classes import EdcLab
from bhp_entry.classes import ScheduledEntry
from bhp_locator.models import BaseLocator
from bhp_lab_tracker.classes import lab_tracker


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
        self.selected_visit = None
        self.visit_code = None
        self.visit_instance = None  # this is not a model instance!!
        self.visit_model = None
        self.visit_messages = None
        self._subject_identifier = None
        self._subject_hiv_status = None
        self._subject_type = None
        self.requisition_model = None
        self.is_dispatched, self.dispatch_producer = False, None
        self.appointment_row_template = 'appointment_row.html'
        self.appointment_map = {}
        self.exclude_others_if_keyed_model_name = ''  # this is a form name or regex pattern
        self.include_after_exclusion_model_keyed = []
        self.scheduled_entry_bucket_rules = []

    def _prepare_dispatch_subject(self):
        if self.registered_subject:
            try:
                from bhp_dispatch.helpers import is_dispatched_registered_subject
                self.is_dispatched, self.dispatch_producer = is_dispatched_registered_subject(self.registered_subject)
                self.context.add(
                    is_dispatched=self.is_dispatched,
                    dispatch_producer=self.dispatch_producer)
            except:
                pass

    def create(self, **kwargs):
        super(RegisteredSubjectDashboard, self).create(**kwargs)
        if not self.appointment_row_template:
            self.appointment_row_template = 'appointment_row.html'
            self.context.add(appointment_row_template=self.appointment_row_template)
        self.registered_subject = kwargs.get('registered_subject', self.registered_subject)
        if self.registered_subject:
            #self.is_dispatched, self.dispatch_producer = is_dispatched_registered_subject(self.registered_subject)
            self.set_subject_type(kwargs.get('subject_type'))
            # subject identifier is almost always available
            self.set_subject_identifier(self.registered_subject.subject_identifier)
            self.dashboard_identifier = self.get_subject_identifier()
            if not self.get_subject_identifier():
                # but if not, check for registration_identifier
                self.set_subject_identifier(self.registered_subject.registration_identifier)
                self.dashboard_identifier = ('{0} [{1}] {2}'.format(self.registered_subject.first_name,
                                                                    self.registered_subject.initials,
                                                                    self.registered_subject.gender,))
            if not self.get_subject_identifier():
                raise AttributeError('RegisteredSubjectDashboard requires a subject_identifier. '
                                     'RegisteredSubject has no identifier for this subject.')
            self.context.add(
                registered_subject=self.registered_subject,
                subject_identifier=self.get_subject_identifier(),
                subject_type=self.get_subject_type(),
                subject_hiv_status=self.get_subject_hiv_status(),
                )
        visit_code = kwargs.pop('visit_code', self.visit_code)
        visit_instance = kwargs.pop("visit_instance", self.visit_instance)
        visit_model = kwargs.pop('visit_model', self.visit_model)
        if self.extra_url_context == {}:
            self.extra_url_context = ''
        self.context.add(
            #is_dispatched=self.is_dispatched,
            #dispatch_producer=self.dispatch_producer,
            visit_model=visit_model,
            visit_instance=visit_instance,
            visit_code=visit_code,
            extra_url_context=self.extra_url_context
            )
        if not self.requisition_model:
            raise AttributeError('RegisteredSubjectDashboard.create() requires attribute '
                                 '\'requisition_model\'. Got none.')
        if not visit_model:
            raise AttributeError('RegisteredSubjectDashboard.create() requires attribute '
                                 '\'visit_model\'. Got none.')
        else:
            self.context.add(visit_model_add_url=self._get_visit_model_url(visit_model))
        membership_form_category = kwargs.pop('membership_form_category', None)
        self._prepare(visit_model, visit_code, visit_instance, membership_form_category, **kwargs)

    def _prepare(self, visit_model, visit_code, visit_instance, membership_form_category, **kwargs):
        self._prepare_membership_forms(membership_form_category)
        self._set_appointments(visit_code, visit_instance, **kwargs)
        self._set_current_appointment(visit_code, visit_instance)
        visit_model_instance = self._set_current_visit(visit_model, self._get_current_appointment())
        self._add_or_update_entry_buckets(visit_model_instance)
        self._run_rule_groups(self.get_subject_identifier(), visit_code, visit_model_instance)
        self._prepare_additional_entry_bucket()
        self._prepare_visit_messages(visit_code)
        self._prepare_scheduled_entry_bucket(visit_code)
        self._prepare_scheduled_lab_bucket(visit_code)
        self._prepare_additional_lab_bucket(visit_code)
        self._prepare_dispatch_subject()
        self.render_summary_links()

    def _add_or_update_entry_buckets(self, visit_model_instance):
        """ Adds missing bucket entries and flags added and existing entries as keyed or not keyed (only)."""
        if visit_model_instance:
            scheduled_entry = ScheduledEntry()
            scheduled_entry.add_or_update_for_visit(visit_model_instance)
            # if requisition_model has been defined, assume scheduled labs otherwise pass
            if hasattr(self, 'requisition_model'):
                ScheduledLabEntryBucket.objects.add_for_visit(
                    visit_model_instance=visit_model_instance,
                    requisition_model=self.requisition_model)

    def _run_rule_groups(self, subject_identifier, visit_code, visit_model_instance):
        """ Runs rules in any rule groups if visit_code is known and update entries as (new, not required) when the visit dashboard is refreshed.

        If status is 'keyed' and the form is actually keyed, do nothing."""
        if not subject_identifier:
            raise AttributeError('set value of subject_identifier before calling dashboard create() when scheduled_entry_bucket_rules exist')
        # run rules if visit_code is known -- user selected, that is user clicked to see list of
        # scheduled entries for a given visit.
        if visit_code:
            # TODO: on data entry, is the visit_model_instance always 0 or the actual instance 0,1,2, etc
            if visit_model_instance:
                rule_groups.update_all(visit_model_instance)

    def _get_visit_model_url(self, visit_model):
        model_name = visit_model._meta.module_name
        app_label = visit_model._meta.app_label
        self.context.add(visit_model_app_label=app_label)
        try:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model_name))
        except:
            # model must be registered in admin
            raise ValueError('NoReverseMatch: Reverse for \'%s_%s_add\'. Check model is '
                                 'registered in admin'.format(app_label, model_name))
        self.context.add(visit_model_name=model_name)
        return url

    def _set_appointment_map(self, visit_code):
        """Create a dictionary of appointment instances for this subject and visit_code using visit_instance(0,1,2,3...) as a key."""
        self.appointment_map = {}
        for appointment in Appointment.objects.filter(registered_subject=self.registered_subject, visit_definition__code=visit_code):
            self.appointment_map[appointment.visit_instance] = appointment

    def _get_appointment_map(self, visit_code, visit_instance=None):
        if not self.appointment_map:
            self._set_appointment_map(visit_code)
        if visit_instance:
            return self.appointment_map.get(visit_instance, None)
        else:
            return self.appointment_map

    def add_visit_message(self, message):
        self.visit_messages.append(message)

    def _prepare_visit_messages(self, visit_code):
        self.context.add(visit_messages=self.visit_messages)
        return self.visit_messages

    def _prepare_scheduled_entry_bucket(self, visit_code):
        """ Gets the scheduled bucket entries using the appointment with instance=0 and adds to context ."""
        scheduled_entry_buckets = None
        if visit_code:
            scheduled_entry = ScheduledEntry()
            scheduled_entry_buckets = scheduled_entry.get_entries_for(
                appointment=self._get_appointment_map(visit_code, '0'),
                entry_category='clinic')
        self.context.add(scheduled_entry_bucket=scheduled_entry_buckets)
        return scheduled_entry_buckets

    def _prepare_scheduled_lab_bucket(self, visit_code):
        """ Gets the scheduled lab bucket entries using the appointment with instance=0 and adds to context ."""
        scheduled_lab_bucket = None
        if visit_code:
            scheduled_lab_bucket = ScheduledLabEntryBucket.objects.get_scheduled_labs_for(
                                            registered_subject=self.registered_subject,
                                            appointment=self._get_appointment_map(visit_code, '0'),
                                            visit_code=visit_code)
        self.context.add(scheduled_lab_bucket=scheduled_lab_bucket)
        return scheduled_lab_bucket

    def _prepare_additional_lab_bucket(self, visit_code):
        """ Gets the additional lab bucket entries using the appointment with instance=0 and adds to context ."""
        additional_lab_bucket = None
        if visit_code:
            additional_lab_bucket = AdditionalLabEntryBucket.objects.get_labs_for(registered_subject=self.registered_subject,
                                                                                  appointment=self._get_appointment_map(visit_code, '0'))
        self.context.add(additional_lab_bucket=additional_lab_bucket)
        return additional_lab_bucket

    def _set_appointments(self, visit_code=None, visit_instance=None, **kwargs):
        """Returns all appointments for this registered_subject or just one (if given a visit_code and visit_instance).

        Note: visit_instance does not refer to a model instance. It is an integer 0,1,2,3...

        Could show
            one
            all
            only for this membership form category (which is the subject type)
            only those for a given membership form
            only those for a visit definition grouping
            """
        appointments = None
        if visit_code and visit_instance:
            appointments = [self._get_appointment_map(visit_code, visit_instance)]
        else:
            # or filter appointments for the current membership category
            # schedule_group__membership_form
            codes = MembershipForm.objects.codes_for_category(membership_form_category=self._get_membership_form_category())
            appointments = Appointment.objects.filter(registered_subject=self.registered_subject,
                                                      visit_definition__code__in=codes,
                                                      ).order_by('visit_definition__code', 'visit_instance', 'appt_datetime')
        self.context.add(appointments=appointments)

    def _set_current_visit(self, visit_model, appointment=None):
        if appointment:
            # set the visit
            if visit_model:
                visit = visit_model.objects.get(appointment=appointment)
            else:
                raise AttributeError('Cannot determine attribute \'visit_model\' in RegisteredSubjectDashboard. Got none. Either pass as a attribute or add_to_context')
        else:
            visit = visit_model.objects.none()
        self.context.add(visit=visit)
        return visit

    def _set_current_appointment(self, visit_code=None, visit_instance=None):
        self._appointment = Appointment.objects.none()
        # get the appointment that has focus based on visit_code
        if visit_code:
            # get visit associated with this appointment (in progress) and visit code and instance
            self._appointment = self._get_appointment_map(visit_code, visit_instance)
        self.context.add(appointment=self._appointment)

    def _get_current_appointment(self, visit_code=None, visit_instance=None):
        if not self._appointment:
            self._set_current_appointment(visit_code, visit_instance)
        return self._appointment

    def _prepare_additional_entry_bucket(self):
        # get additional crfs
        additional_entry_bucket = AdditionalEntryBucket.objects.filter(registered_subject=self.registered_subject)
        self.context.add(additional_entry_bucket=additional_entry_bucket)
        return additional_entry_bucket

    def set_subject_type(self, value=None):
        if not value:
            self._subject_type = self.registered_subject.subject_type
        else:
            self._subject_type = value

    def get_subject_type(self, value=None):
        return self._subject_type

    def set_subject_identifier(self, value=None):
        self._subject_identifier = None
        if value:
            self._subject_identifier = value
        #else:
        #    raise TypeError('Attribute subject_identifier cannot be None')

    def get_subject_identifier(self):
        if not self._subject_identifier:
            self.set_subject_identifier()
        return self._subject_identifier

    def _set_subject_hiv_status(self):
        """Sets the hiv_status to the value from bhp_lab_tracker history model."""
        RESULT = 0
        IS_DEFAULT = 1
        subject_hiv_status = lab_tracker.get_current_value('HIV', self.get_subject_identifier())
        if isinstance(subject_hiv_status, tuple):
            if subject_hiv_status[IS_DEFAULT]:
                self._subject_hiv_status = 'UNKNOWN'
            else:
                self._subject_hiv_status = subject_hiv_status[RESULT]

    def get_subject_hiv_status(self):
        if not self._subject_hiv_status:
            self._set_subject_hiv_status()
        return self._subject_hiv_status

    def _set_membership_form_category(self, membership_form_category=None):
        """Sets the membership_form_category, otherwise just uses subject type."""
        if membership_form_category:
            self._membership_form_category = membership_form_category
        else:
            self._membership_form_category = self.get_subject_type()

    def _get_membership_form_category(self):
        if not self._membership_form_category:
            self._set_membership_form_category()
        return self._membership_form_category

    def _prepare_membership_forms(self, membership_form_category=None):
        # membership forms can also be proxy models ... see mochudi_subject.models
        # add membership forms for this registered_subject and subject_type
        # these are the KEYED, UNKEYED schedule group membership forms
        self._set_membership_form_category(membership_form_category)
        membership_forms = ScheduleGroup.objects.get_membership_forms_for(self.registered_subject, self._get_membership_form_category(),
            exclude_others_if_keyed_model_name=self.exclude_others_if_keyed_model_name,
            include_after_exclusion_model_keyed=self.include_after_exclusion_model_keyed)
        self.context.add(
            membership_forms=membership_forms,
            keyed_membership_forms=membership_forms['keyed'],
            unkeyed_membership_forms=membership_forms['unkeyed'])

    def render_summary_links(self, template_filename=None):
        """Renders the side bar template for subject summaries."""
        if not template_filename:
            template_filename = 'summary_side_bar.html'
        summary_links = render_to_string(template_filename, {
                'links': Link.objects.filter(dashboard_type=self.dashboard_type),
                'subject_identifier': self.get_subject_identifier()})
        self.context.add(summary_links=summary_links)

    def render_labs(self, update=False):
        # prepare results for dashboard sidebar
        edc_lab = EdcLab()
        return edc_lab.render(self.get_subject_identifier(), False)

    def render_locator(self, locator_cls, template=None, **kwargs):
        """Renders to string the locator for the current registered subject or that passed as a keyword.

            Keywords:
                registered_subject: if locator information for the current registered subject is collected
                    on another. For example, with mother/infant pairs.
        """
        source_registered_subject = kwargs.get('registered_subject', self.registered_subject)
        if isinstance(locator_cls, models.Model) or locator_cls is None:
            raise TypeError('Expected first parameter to be a Locator model class. Got an instance. Please correct in local dashboard view.')
        if locator_cls is None:
            raise TypeError('Expected first parameter to be a Locator model class. Got None. Please correct in local dashboard view.')
        if not issubclass(locator_cls, BaseLocator):
            raise TypeError('Expected first parameter to be a subclass of BaseLocator model class. Please correct in local dashboard view.')
        visit_code = None
        visit_instance = None
        locator_add_url = reverse('admin:' + locator_cls._meta.app_label + '_' + locator_cls._meta.module_name + '_add')
        if not template:
            template = 'locator_include.html'
        if locator_cls.objects.filter(registered_subject=source_registered_subject):
            locator_instance = locator_cls.objects.get(registered_subject=source_registered_subject)
            for field in locator_instance._meta.fields:
                if isinstance(field, (TextField, EncryptedTextField)):
                    setattr(locator_instance, field.name, '<BR>'.join(wrap(getattr(locator_instance, field.name), 25)))
            if self._appointment:
                visit_code = self._appointment.visit_definition.code
                visit_instance = self._appointment.visit_instance
        else:
            locator_instance = None

        return render_to_string(template, {'locator': locator_instance,
                                           'registered_subject': self.registered_subject,
                                           'subject_identifier': self.get_subject_identifier(),
                                           'dashboard_type': self.dashboard_type,
                                           'visit_code': visit_code,
                                           'visit_instance': visit_instance,
                                           'appointment': self._appointment,
                                           'locator_add_url': locator_add_url})

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
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/(?P<visit_code>{visit_code})/(?P<visit_instance>{visit_instance})/(?P<registered_subject>{pk})/(?P<appointment>{pk})/$'.format(**regex),
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
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<subject_identifier>{subject_identifier})/$'.format(**regex),
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
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registered_subject>{pk})/$'.format(**regex),
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
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<registered_subject>{pk})/$'.format(**regex),
                'dashboard',
                name="dashboard_url"
                ),
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<pk>{pk})/$'.format(**regex),
                'dashboard',
                name="pk_dashboard_url"
                ))
        return urlpatterns
