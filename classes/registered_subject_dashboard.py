import re
from textwrap import wrap
from django.db import models
from django.db.models import TextField
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import patterns, url
from django.template.loader import render_to_string
from bhp_common.utils import convert_from_camel
from bhp_crypto.fields import EncryptedTextField
from bhp_entry.models import AdditionalEntryBucket, ScheduledEntryBucket
from bhp_lab_entry.models import ScheduledLabEntryBucket, AdditionalLabEntryBucket
from bhp_entry_rules.classes import rule_groups
from bhp_appointment.models import Appointment
from bhp_visit.models import MembershipForm
from bhp_visit.classes import MembershipFormHelper
from bhp_visit_tracking.models import BaseVisitTracking
from bhp_registration.models import RegisteredSubject
from bhp_dashboard.classes import Dashboard
from bhp_subject_summary.models import Link
from lab_clinic_api.classes import EdcLab
from lab_requisition.models import BaseBaseRequisition
from lab_packing.models import BasePackingList
from bhp_entry.classes import ScheduledEntry, AdditionalEntry
from bhp_locator.models import BaseLocator
from bhp_lab_tracker.classes import lab_tracker
from bhp_data_manager.models import ActionItem
from bhp_subject_config.models import SubjectConfiguration


class RegisteredSubjectDashboard(Dashboard):

    """ Create and add to a default clinic 'registered subject' dashboard context and render_to_response from a view in shell. """

    def __init__(self, **kwargs):
        super(RegisteredSubjectDashboard, self).__init__(**kwargs)
        self._registered_subject = None
        self._subject_identifier = None
        self._subject_type = None
        self._appointment_row_template = None
        self._appointment = None
        self._appointment_zero = None
        self._appointments = None
        self._appointment_code = None
        self._appointment_continuation_count = None
        self._visit_model = None
        self._requisition_model = None
        self._packing_list_model = None
        self._visit_model_instance = None
        self._subject_configuration = None
        self._extra_url_context = None
        self._show = None
        self._scheduled_entry_bucket = None
        self._scheduled_lab_bucket = None
        self._additional_entry_bucket = None
        self._additional_lab_bucket = None
        self._membership_models = None
        self._visit_messages = []

        self.selected_visit = None
        self._subject_hiv_status = None
        self.is_dispatched, self.dispatch_producer = False, None
        self.exclude_others_if_keyed_model_name = ''
        self.add_to_dashboard_model_reference({'appointment': Appointment})

    def create(self, **kwargs):
        self.set_show(kwargs.get('show'))
        self.add_to_dashboard_model_reference({'visit': self.get_visit_model})
        super(RegisteredSubjectDashboard, self).create(**kwargs)
        self.set_subject_type(kwargs.get('subject_type') or kwargs.get('dashboard_type'))
        self._set_membership_form_category(kwargs.get('membership_form_category', None))
        self._set_registered_subject(kwargs.get('registered_subject', None))
        self.set_dashboard_model()
        if self.get_registered_subject():
            subject_hiv_status = lab_tracker.get_current_value('HIV', self.get_registered_subject().subject_identifier)[0]
            subject_hiv_history = lab_tracker.get_history_as_string('HIV', self.get_registered_subject().subject_identifier)
            self.context.add(
                registered_subject=self.get_registered_subject(),
                subject_identifier=self.get_subject_identifier(),
                subject_type=self.get_subject_type(),
                subject_hiv_history=subject_hiv_history,
                subject_hiv_status=subject_hiv_status,
                subject_configuration=self.get_subject_configuration(),
                )
        self.context.add(
            show=self.get_show(),
            appointment_meta=Appointment._meta,
            subject_configuration_meta=SubjectConfiguration._meta,
            extra_url_context=self.get_extra_url_context(),
            appointment_row_template=self.get_appointment_row_template(),
            appointment=self.get_appointment(),
            appointments=self.get_appointments(),
            appointment_visit_attr=self.get_visit_model()._meta.object_name.lower(),
            visit_attr=convert_from_camel(self.get_visit_model()._meta.object_name),
            visit_model=self.get_visit_model(),
            visit_model_instance=self.get_visit_model_instance(),
            visit_instance=self.get_appointment_continuation_count(),
            visit_code=self.get_appointment_code(),
            #visit_model_app_label=self.visit_model_app_label,  # TODO: needed??
            visit_model_meta=self.get_visit_model()._meta,
            visit_messages=self.get_visit_messages(),
            )
        self.context.add(
            membership_forms=self.get_membership_models(),
            keyed_membership_forms=self.get_keyed_membership_models(),
            unkeyed_membership_forms=self.get_unkeyed_membership_models()
            )
        if self.get_show() == 'forms':
            self._add_or_update_entry_buckets()
            self._run_rule_groups()
            self.context.add(
                scheduled_entry_bucket_meta=ScheduledEntryBucket._meta,
                scheduled_entry_bucket=self.get_scheduled_entry_bucket(),
                scheduled_lab_bucket=self.get_scheduled_lab_bucket(),
                additional_entry_bucket=self.get_additional_entry_bucket(),
                additional_lab_bucket=self.get_additional_lab_bucket(),
                )
            self.render_summary_links()
        self.context.add(rendered_action_items=self.render_action_item())

        # lab stuff
        if self.get_packing_list_model():
            self.context.add(packinglist_meta=self.get_packing_list_model()._meta)
        if self.get_requisition_model():
            self.context.add(requisition_meta=self.get_requisition_model()._meta)

    def set_appointment_row_template(self, template_file=None):
        self._appointment_row_template = template_file or 'appointment_row.html'

    def get_appointment_row_template(self):
        if not self._appointment_row_template:
            self.set_appointment_row_template()
        return self._appointment_row_template

#     def set_dashboard_identifier(self):
#         #TODO: what is this used for?
#         self._dashboard_identifier = None
#         if self.get_registered_subject():
#             self._dashboard_identifier = ('{0} [{1}] {2}'
#                 ).format(
#                      self.get_registered_subject().first_name,
#                      self.get_registered_subject().initials,
#                      self.get_registered_subject().gender)
#         else:
#             self._dashboard_identifier = self.get_subject_identifier()
# 
#     def get_dashboard_identifier(self):
#         if not self._dashboard_identifier:
#             self.set_dashboard_identifier()
#         return self._dashboard_identifier

    def set_registered_subject(self, registered_subject=None, pk=None):
        """Sets the registered_subject instance, may be overridden by users."""
        self._registered_subject = registered_subject
        if not self._registered_subject and pk:
            self._registered_subject = RegisteredSubject.objects.get(pk=pk)
        if not self._registered_subject:
            if self.get_dashboard_model_key() == 'registered_subject':
                # may have more than on, so take most recent
                self._registered_subject = RegisteredSubject.objects.filter(registered_subject=self.get_dashboard_id()).order_by('-created')[0]

    def _set_registered_subject(self, registered_subject=None):
        self.set_registered_subject(registered_subject)
        if not self._registered_subject:
            re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
            if re_pk.match(str(registered_subject)):
                self._registered_subject = RegisteredSubject.objects.get(pk=registered_subject)
            elif self.get_appointment():
                    self._registered_subject = self.get_appointment().registered_subject
        if self._registered_subject:
            if not isinstance(self._registered_subject, RegisteredSubject):
                raise TypeError('Expected instance of RegisteredSubject.')
        else:
            self._registered_subject = []

    def get_registered_subject(self):
        if not self._registered_subject:
            self._set_registered_subject()
        return self._registered_subject

    def set_appointment(self, appointment=None, appointment_code=None, appointment_continuation_count=None):
        """Sets the appointment that has focus using either appointment_code or both appointment_code and appointment_continuation_count.

        self._appointment is allowed to be None if no appointment has focus.

        Users may override."""
        self._appointment = None

    def _set_appointment(self, appointment=None, appointment_code=None, appointment_continuation_count=None):
        self._appointment = None
        appointment_code = appointment_code or self.get_appointment_code()
        appointment_continuation_count = appointment_continuation_count or self.get_appointment_continuation_count() or 0
        self.set_appointment(appointment, appointment_code, appointment_continuation_count)
        if not self._appointment:
            if appointment:
                if isinstance(appointment, Appointment):
                    self._appointment = appointment
                elif isinstance(appointment, basestring):
                    if Appointment.objects.filter(pk=appointment):
                        self._appointment = Appointment.objects.get(pk=appointment)
                else:
                    raise AttributeError('Unable to determine appointment for SubjectDashboard {0} using parameter \'appointment\'. Got {1}'.format(self.__class__, appointment))
            if appointment_code:
                if Appointment.objects.filter(registered_subject=self.get_registered_subject(), visit_definition__code=appointment_code, visit_instance=appointment_continuation_count):
                    self._appointment = Appointment.objects.get(registered_subject=self.get_registered_subject(), visit_definition__code=appointment_code, visit_instance=appointment_continuation_count)
        if not self._appointment:
            if self.get_dashboard_model_key() == 'appointment':
                self._appointment = Appointment.objects.get(pk=self.get_dashboard_id())
            elif self.get_dashboard_model_key() == 'visit':
                self._appointment = self.get_visit_model_instance().appointment
        if self._appointment:
            self.set_appointment_code(self._appointment.visit_definition.code)
            self.set_appointment_continuation_count(self._appointment.visit_instance)

    def get_appointment(self):
        if not self._appointment:
            self._set_appointment()
        return self._appointment

    def set_appointment_zero(self):
        self._appointment_zero = None
        if self.get_appointment():
            if self.get_appointment().visit_instance == 0:
                self._appointment_zero = self.get_appointment()
            else:
                self._appointment_zero = Appointment.objects.get(registered_subject=self.get_appointment().registered_subject, visit_definition=self.get_appointment().visit_definition, visit_instance=0)

    def get_appointment_zero(self):
        if not self._appointment_zero:
            self.set_appointment_zero()
        return self._appointment_zero

    def set_appointment_code(self, value=None):
        self._appointment_code = value
        #if not self._appointment_code:
        #    if self.get_visit_model_instance():
        #        self._appointment_code = self.get_visit_model_instance().appointment.visit_definition.code

    def get_appointment_code(self):
        if not self._appointment_code:
            self.set_appointment_code()
        return self._appointment_code

    def set_appointment_continuation_count(self, value=None):
        self._appointment_continuation_count = value
        #if not self._appointment_continuation_count:
        #    if self.get_visit_model_instance():
        #        self._appointment_continuation_count = self.get_visit_model_instance().appointment.visit_instance

    def get_appointment_continuation_count(self):
        if not self._appointment_continuation_count:
            self.set_appointment_continuation_count()
        return self._appointment_continuation_count

    def set_appointments(self):
        """Returns all appointments for this registered_subject or just one (if given a appointment_code and appointment_continuation_count).

        Could show
            one
            all
            only for this membership form category (which is the subject type)
            only those for a given membership form
            only those for a visit definition grouping
            """
        self._appointments = None
        #if self.get_appointment_code() and self.get_appointment_continuation_count():
        if self.get_show() == 'forms':
            self._appointments = [self.get_appointment()]
        else:
            # or filter appointments for the current membership category
            # schedule_group__membership_form
            codes = MembershipForm.objects.codes_for_category(membership_form_category=self.get_membership_form_category())
            self._appointments = Appointment.objects.filter(
                registered_subject=self.get_registered_subject(),
                visit_definition__code__in=codes).order_by('visit_definition__code', 'visit_instance', 'appt_datetime')

    def get_appointments(self):
        if not self._appointments:
            self.set_appointments()
        return self._appointments

    def set_visit_model(self, subject_type=None, visit_model=None):
        """Sets the attribute self._visit model (visit model class) if one is not provided as a parameter when calling :func:`_set_visit_model`.

        Users must override if this is called.

        For example::
            def set_visit_model(self):
                if self.get_dashboard_type() == 'subject':
                    self._visit_model = SubjectVisit

        """
        self._visit_model = visit_model
        if not self._visit_model:
            raise ImproperlyConfigured('Override method set_visit_model() if you wish to get a visit model class not returned by the view.')

    def _set_visit_model(self):
        self.set_visit_model()
        if not self._visit_model:
            raise TypeError('Attribute _visit_model_class may not be None')
        if not issubclass(self._visit_model, BaseVisitTracking):
            raise TypeError('Expected visit model class to be a subclass of BaseVisitTracking. Got {0}'.format(self._visit_model))

    def get_visit_model(self):
        """Returns the visit model class."""
        if not self._visit_model:
            self._set_visit_model()
        return self._visit_model

    def set_visit_model_instance(self, model_inst=None, pk=None, appointment=None):
        """Sets the visit model instance but may be None."""
        self._visit_model_instance = None
        if model_inst:
            self._visit_model_instance = model_inst
        elif pk:
            self._visit_model_instance = self.get_visit_model().objects.get(pk=pk)
        elif appointment:
            self._visit_model_instance = self.get_visit_model().objects.get(appointment=appointment)
        elif self.get_dashboard_model_key() == 'visit':
            self._visit_model_instance = self.get_visit_model().objects.get(pk=self.get_dashboard_id())
        elif self.get_dashboard_model_key() == 'appointment':
            # warning, this assumes the subject visit attribute is based on the model name SubjectVisit (which it should be!).
            try:
                self._visit_model_instance = getattr(self.get_appointment(), self.get_visit_model()._meta.object_name.lower())
            except self.get_visit_model().DoesNotExist:
                pass
        else:
            pass
        if self._visit_model_instance:
            if not isinstance(self._visit_model_instance, self.get_visit_model()):
                raise TypeError('Expected an instance of visit model class {0} using (model_inst={1}, pk={2}, appointment={3} and self.get_dashboard_model_key()={4}).'.format(self.get_visit_model(), model_inst, pk, appointment, self.get_dashboard_model_key()))

    def get_visit_model_instance(self):
        if not self._visit_model_instance:
            self.set_visit_model_instance()
        return self._visit_model_instance

    def set_requisition_model(self):
        """Users must override if requisitions are used to specify the requisition model."""
        self._requisition_model = None

    def _set_requisition_model(self):
        self._requisition_model = None
        self.set_requisition_model()
        if not issubclass(self._requisition_model, BaseBaseRequisition):
            raise TypeError('Expected a subclass of BaseBaseRequisition. Got {0}.'.format(self._requisition_model))

    def get_requisition_model(self):
        if not self._requisition_model:
            self._set_requisition_model()
        return self._requisition_model

    def set_packing_list_model(self):
        """Users must override if requisitions are used to specify the requisition model."""
        self._packing_list_model = None

    def _set_packing_list_model(self):
        self._packing_list_model = None
        self.set_packing_list_model()
        if not issubclass(self._packing_list_model, BasePackingList):
            raise TypeError('Expected a subclass of BasePackingList. Got {0}.'.format(self._packing_list_model))

    def get_packing_list_model(self):
        if not self._packing_list_model:
            self._set_packing_list_model()
        return self._packing_list_model

    def set_membership_form_category(self, value=None):
        """Users may override."""
        return None

    def _set_membership_form_category(self, value=None):
        """Sets the membership_form_category, otherwise just uses subject type."""
        self.set_membership_form_category()
        if not self._membership_form_category:
            self._membership_form_category = value or self.get_subject_type()
        if not self._membership_form_category:
            raise AttributeError('Attribute \'_membership_form_category\' cannot be None')

    def get_membership_form_category(self):
        if not self._membership_form_category:
            self._set_membership_form_category()
        return self._membership_form_category

    def _add_or_update_entry_buckets(self):
        """ Adds missing bucket entries and flags added and existing entries as keyed or not keyed (only)."""
        if self.get_visit_model_instance():
            scheduled_entry = ScheduledEntry()
            scheduled_entry.add_or_update_for_visit(self.get_visit_model_instance())
            # if requisition_model has been defined, assume scheduled labs otherwise pass
            if self.get_requisition_model():
                ScheduledLabEntryBucket.objects.add_for_visit(
                    visit_model_instance=self.get_visit_model_instance(),
                    requisition_model=self.get_requisition_model())
        if self.get_registered_subject():
            additional_entry = AdditionalEntry()
            additional_entry.update_for_registered_subject(self.get_registered_subject())

    def add_visit_message(self, message):
        self._visit_messages.append(message)

    def get_visit_messages(self):
        return self._visit_messages

    def set_scheduled_entry_bucket(self):
        """ Sets the scheduled bucket entries using the appointment with instance=0 and adds to context ."""
        self._scheduled_entry_bucket = None
        if self.get_appointment():
            self._scheduled_entry_bucket = ScheduledEntry().get_entries_for(
                appointment=self.get_appointment_zero(),
                entry_category='clinic',
                registered_subject=self.get_registered_subject())

    def get_scheduled_entry_bucket(self):
        if not self._scheduled_entry_bucket:
            self.set_scheduled_entry_bucket()
        return self._scheduled_entry_bucket

    def set_scheduled_lab_bucket(self):
        """ Sets the scheduled lab bucket entries using the appointment with instance=0 and adds to context ."""
        self._scheduled_lab_bucket = None
        if self.get_appointment():
            self._scheduled_lab_bucket = ScheduledLabEntryBucket.objects.get_scheduled_labs_for(
                                            registered_subject=self.get_registered_subject(),
                                            appointment=self.get_appointment_zero(),
                                            visit_code=self.get_appointment().visit_definition.code)

    def get_scheduled_lab_bucket(self):
        if not self._scheduled_lab_bucket:
            self.set_scheduled_lab_bucket()
        return self._scheduled_lab_bucket

    def set_additional_lab_bucket(self):
        """ Gets the additional lab bucket entries using the appointment with instance=0 and adds to context ."""
        self._additional_lab_bucket = None
        if self.get_appointment():
            self._additional_lab_bucket = AdditionalLabEntryBucket.objects.get_labs_for(registered_subject=self.get_registered_subject(),
                                                                                  appointment=self.get_appointment_zero())

    def get_additional_lab_bucket(self):
        if not self._additional_lab_bucket:
            self.set_additional_lab_bucket()
        return self._additional_lab_bucket

    def set_additional_entry_bucket(self):
        self._additional_entry_bucket = AdditionalEntryBucket.objects.filter(registered_subject=self.get_registered_subject())

    def get_additional_entry_bucket(self):
        if not self._additional_entry_bucket:
            self.set_additional_entry_bucket()
        return self._additional_entry_bucket

    def set_subject_type(self, value=None):
        if not value:
            self._subject_type = self.get_registered_subject().subject_type
        else:
            self._subject_type = value

    def get_subject_type(self, value=None):
        return self._subject_type

    def set_subject_identifier(self, value=None):
        self._subject_identifier = None
        if value:
            self._subject_identifier = value
        else:
            if self.get_registered_subject():
                self._subject_identifier = self.get_registered_subject().get_subject_identifier()
        if self.get_registered_subject() and self._subject_identifier:
            if self.get_registered_subject().get_subject_identifier() != self._subject_identifier:
                raise TypeError(('Subject identifier on registered subject {0} not the same as '
                                 'subject identifier on dashboard {1}!').format(self.get_registered_subject().get_subject_identifier(), self._subject_identifier))
        if not self._subject_identifier:
            raise TypeError('attribute subject_identifier may not be None')

    def get_subject_identifier(self):
        if not self._subject_identifier:
            self.set_subject_identifier()
        return self._subject_identifier

    def _set_subject_configuration(self):
        self._subject_configuration = None
        if self.get_subject_identifier():
            if SubjectConfiguration.objects.filter(subject_identifier=self.get_subject_identifier()):
                self._subject_configuration = SubjectConfiguration.objects.get(subject_identifier=self.get_subject_identifier())

    def get_subject_configuration(self):
        if not self._subject_configuration:
            self._set_subject_configuration()
        return self._subject_configuration

    def set_extra_url_context(self, value=None):
        self._extra_url_context = value or ''
#         if self._extra_url_context == {}:
#             self._extra_url_context = ''

    def get_extra_url_context(self):
        if not self._extra_url_context:
            self.set_extra_url_context()
        return self._extra_url_context

    def set_show(self, value):
        self._show = value or 'appointments'

    def get_show(self):
        if not self._show:
            self.set_show()
        return self._show

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

    def set_membership_models(self):
        """Sets to a dictionary of membership "models" that are keyed model instances and unkeyed model classes.

        Membership forms can also be proxy models ... see mochudi_subject.models."""
        self._membership_models = MembershipFormHelper().get_membership_models_for(
            self.get_registered_subject(),
            self.get_membership_form_category(),
            extra_grouping_key=self.exclude_others_if_keyed_model_name)
            #include_after_exclusion_model_keyed=self.include_after_exclusion_model_keyed)

    def get_membership_models(self, key=None):
        if not self._membership_models:
            self.set_membership_models()
        return self._membership_models

    def get_keyed_membership_models(self):
        return self.get_membership_models().get('keyed', [])

    def get_unkeyed_membership_models(self):
        return self.get_membership_models().get('unkeyed', [])

    def _run_rule_groups(self):
        """ Runs rules in any rule groups if visit_code is known and update entries as (new, not required) when the visit dashboard is refreshed.

        If status is 'keyed' and the form is actually keyed, do nothing."""
        if not self.get_subject_identifier():
            raise AttributeError('set value of subject_identifier before calling dashboard create() when scheduled_entry_bucket_rules exist')
        # run rules if visit_code is known -- user selected, that is user clicked to see list of
        # scheduled entries for a given visit.

        # TODO: on data entry, is the visit_model_instance always 0 or the actual instance 0,1,2, etc
        if self.get_visit_model_instance():
            rule_groups.update_all(self.get_visit_model_instance())

    def next_url_in_scheduled_entry_bucket(self, obj, visit_attr, entry_order, dashboard_type, dashboard_id, dashboard_model):
        retval = (None, None, None)
        if not visit_attr or not entry_order:
            return retval
        self.set_show('forms')
        self.set_dashboard_type(dashboard_type)
        self.set_dashboard_id(dashboard_id)
        self.set_dashboard_model_key(dashboard_model)
        visit = getattr(obj, visit_attr)
        self.set_visit_model(visit_model=visit.__class__)
        self.set_visit_model_instance(visit)
        self._run_rule_groups()
        scheduled_entry_bucket = ScheduledEntry().get_next_entry_for(entry_order, self.get_appointment(), self.get_registered_subject())
        if scheduled_entry_bucket:
            url = reverse('admin:{0}_{1}_add'.format(scheduled_entry_bucket.entry.content_type_map.app_label, scheduled_entry_bucket.entry.content_type_map.module_name))
            retval = (url, self.get_visit_model_instance(), scheduled_entry_bucket.entry.entry_order)
        return retval

    def render_summary_links(self, template_filename=None):
        """Renders the side bar template for subject summaries."""
        if not template_filename:
            template_filename = 'summary_side_bar.html'
        summary_links = render_to_string(template_filename, {
                'links': Link.objects.filter(dashboard_type=self.get_dashboard_type()),
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
        source_registered_subject = kwargs.get('registered_subject', self.get_registered_subject())
        if isinstance(locator_cls, models.Model) or locator_cls is None:
            raise TypeError('Expected first parameter to be a Locator model class. Got an instance. Please correct in local dashboard view.')
        if locator_cls is None:
            raise TypeError('Expected first parameter to be a Locator model class. Got None. Please correct in local dashboard view.')
        if not issubclass(locator_cls, BaseLocator):
            raise TypeError('Expected first parameter to be a subclass of BaseLocator model class. Please correct in local dashboard view.')
        locator_add_url = reverse('admin:' + locator_cls._meta.app_label + '_' + locator_cls._meta.module_name + '_add')
        if not template:
            template = 'locator_include.html'
        if locator_cls.objects.filter(registered_subject=source_registered_subject):
            locator_instance = locator_cls.objects.get(registered_subject=source_registered_subject)
            for field in locator_instance._meta.fields:
                if isinstance(field, (TextField, EncryptedTextField)):
                    value = getattr(locator_instance, field.name)
                    if value:
                        setattr(locator_instance, field.name, '<BR>'.join(wrap(value, 25)))
        else:
            locator_instance = None
        return render_to_string(template, {'locator': locator_instance,
                                           'subject_dashboard_url': self.get_subject_dashboard_url(),
                                           'dashboard_type': self.get_dashboard_type(),
                                           'dashboard_model': self.get_dashboard_model_key(),
                                           'dashboard_id': self.get_dashboard_id(),
                                           'show': self.get_show(),
                                           'locator_add_url': locator_add_url})

    def render_action_item(self, action_item_cls=None, template=None, **kwargs):
        """Renders to string the action_items for the current registered subject."""
        source_registered_subject = kwargs.get('registered_subject', self.get_registered_subject())
        action_item_cls = action_item_cls or ActionItem
        if isinstance(action_item_cls, models.Model):
            raise TypeError('Expected first parameter to be a Action Item model class. Got an instance. Please correct in local dashboard view.')
        #action_item_add_url = reverse('admin:' + action_item_cls._meta.app_label + '_' + action_item_cls._meta.module_name + '_add')
        if not template:
            template = 'action_item_include.html'
        action_items = action_item_cls.objects.filter(registered_subject=source_registered_subject, display_on_dashboard=True, status='Open')
        action_item_instances = []
        if action_items:
            for action_item in action_items:
                for field in action_item._meta.fields:
                    if isinstance(field, (TextField, EncryptedTextField)):
                        value = getattr(action_item, field.name)
                        if value:
                            setattr(action_item, field.name, '<BR>'.join(wrap(value, 25)))
                action_item_instances.append(action_item)
        if action_item_instances:
            self.context.add(action_item_message='Action items exist for this subject. Please review and resolve if possible.')
        else:
            self.context.add(action_item_message=None)
        rendered_action_items = render_to_string(template, {
            'action_items': action_item_instances,
            'registered_subject': self.get_registered_subject(),
            'dashboard_type': self.get_dashboard_type(),
            'dashboard_model': self.get_dashboard_model_key(),
            'dashboard_id': self.get_dashboard_id(),
            'show': self.get_show(),
            'action_item_meta': action_item_cls._meta})
        return rendered_action_items

    def get_urlpatterns(self, view, regex, **kwargs):
        """Gets the url_patterns for the dashboard view.

        Called in the urls.py"""
        regex['pk'] = '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}'
        if regex.get('dashboard_model', None):
            regex['dashboard_model'] += '|visit|appointment|registered_subject'
        else:
            regex.update({'dashboard_model': 'visit|appointment|registered_subject'})
        if not regex.get('dashboard_type', None):
            regex.update({'dashboard_type': 'subject'})
        regex.update({'show': 'appointments|forms'})
        #regex['panel'] = '\d+'
        #regex['content_type_map'] = '[a-z0-9]+'
        #if 'registration_identifier' not in regex.keys():
        #    regex['registration_identifier'] = '[A-Z0-9]{6,8}'

        urlpatterns = patterns(view,
            url(r'^(?P<dashboard_type>{dashboard_type})/(?P<dashboard_model>{dashboard_model})/(?P<dashboard_id>{pk})/(?P<show>{show})/$'.format(**regex),
              'subject_dashboard',
                name="subject_dashboard_url"
                ))
        return urlpatterns
