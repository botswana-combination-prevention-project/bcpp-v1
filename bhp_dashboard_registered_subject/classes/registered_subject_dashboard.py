import re
from textwrap import wrap
from django.conf import settings
from django.db import models
from django.db.models import TextField, Count, get_model
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import patterns, url
from django.template.loader import render_to_string
from django.utils import translation
from bhp_common.utils import convert_from_camel
from bhp_entry_rules.classes import rule_groups
from bhp_visit.classes import MembershipFormHelper
from bhp_dashboard.classes import Dashboard
from lab_clinic_api.classes import EdcLab
from bhp_entry.classes import ScheduledEntry, AdditionalEntry
from bhp_entry.models import ScheduledEntryBucket
from bhp_visit.exceptions import MembershipFormError
from bhp_appointment.models import Appointment
from bhp_visit.models import MembershipForm
from bhp_lab_entry.models import ScheduledLabEntryBucket, AdditionalLabEntryBucket
from bhp_visit_tracking.models import BaseVisitTracking
from bhp_registration.models import RegisteredSubject
from bhp_subject_summary.models import Link
from bhp_locator.models import BaseLocator
from bhp_data_manager.models import ActionItem
from bhp_subject_config.models import SubjectConfiguration
from lab_requisition.models import BaseBaseRequisition
from lab_packing.models import BasePackingList
from bhp_consent.models import BaseConsent
from scheduled_entry_context import ScheduledEntryContext


class RegisteredSubjectDashboard(Dashboard):

    """ Create and add to a default clinic 'registered subject' dashboard context and render_to_response from a view in shell.

        Args:
            * dashboard_type: type of dashboard, something like \'subject\' or \'household'\. Comes from view/URL.
            * dashboard_model: the model name of format \'model_name\' of a model class used by the dashboard to get core values like registered subject, subject identifier, etc. Comes from view/URL.
            * dashboard_id: the pk value of the dashboard model. Comes from view/URL.

        Keyword Args:
            * dashboard_type_list: a list of allowed values for dashboard_type, e.g. ['maternal']. Hard coded in the child class.
            * dashboard_models: a dictionary of allowed dashboard models. Defaults are added for the visit model, Appointment, and RegisteredSubject. Users probably will add the consent model as well in the child class
            * dashboard_category: actually is the membership_form.category which is used to filter membership forms to display for this dashboard.
            * visit_model: the visit model class.
            * registered_subject: an instance of registered_subject for the current subject.
            * show: either \'forms\' or \'appointments\'.

        Subclass in your local xxxx_dashboard classes module::

            from datetime import timedelta, date
            from bhp_dashboard_registered_subject.classes import RegisteredSubjectDashboard
            from maikalelo_infant.models import Birth, InfantVisit
            from maikalelo_maternal.models import MaternalConsent, MaternalLocator, MaternalEnrollment
            from maikalelo_lab.models import InfantRequisition

            class InfantDashboard(RegisteredSubjectDashboard):

                view = 'infant_dashboard'  # may specify here or pass as parameter for :func:`get_urlpatterns`

                def __init__(self, **kwargs):
                    self.dashboard_type = 'infant'
                    kwargs.update({'dashboard_models': {'birth': Birth}})
                    super(InfantDashboard, self).__init__(**kwargs)
                    self.requisition_model = InfantRequisition

                def add_to_context(self):
                    super(InfantDashboard, self).add_to_context()
                    self.context.add(
                        home='maikalelo',
                        title='Infant Dashboard',
                        infant_birth=self.get_infant_birth(),
                        maternal_consent=self.get_consent(),
                        )

                def get_visit_model(self):
                    return InfantVisit

                def set_requisition_model(self):
                    self._requisition_model = InfantRequisition

                def set_membership_form_category(self):
                    self._membership_form_category = 'infant'

                def set_dashboard_type_list(self):
                    self._dashboard_type_list = ['infant']
                ...


        For now you still need to add a view to the xxxx_dashboard views module. For example::

            from django.contrib.auth.decorators import login_required
            from django.shortcuts import render_to_response
            from django.template import RequestContext
            from dom_dashboard.classes import InfantDashboard
            from dom_infant.models import InfantBirth

            @login_required
            def infant_dashboard(request, **kwargs):
                dashboard = InfantDashboard(
                    dashboard_type=kwargs.get('dashboard_type'),
                    dashboard_id=kwargs.get('dashboard_id'),
                    dashboard_model=kwargs.get('dashboard_model'),
                    dashboard_category=kwargs.get('dashboard_category'),
                    registered_subject=kwargs.get('registered_subject'),
                    show=kwargs.get('show'),
                    dashboard_type_list=['infant'],
                    dashboard_models={'infant_birth': InfantBirth})
                return render_to_response(
                    'infant_dashboard.html',
                    dashboard.get_context().get(),
                    context_instance=RequestContext(request))


        You also need to update your urls.py in the local dashboard app. See :func:`get_urlpatterns`.
        """

    view = None
    dashboard_url_name = 'subject_dashboard_url'

    def __init__(self, dashboard_type, dashboard_id, dashboard_model, dashboard_type_list=None, dashboard_models=None, dashboard_category=None, visit_model=None, registered_subject=None, show=None, **kwargs):
        dashboard_models = dashboard_models or {}
        dashboard_models.update({'appointment': Appointment})
        self._visit_model = None
        if visit_model:  # usually None, except in testing, usually provided by the subclass. needed now regardless since passing method for one of the dashboard models below
            self._set_visit_model(visit_model)
        dashboard_models.update({'visit': self._get_visit_model})  # yes, i am passing the method, not calling it
        super(RegisteredSubjectDashboard, self).__init__(dashboard_type, dashboard_id, dashboard_model, dashboard_type_list, dashboard_models)

        self._additional_entry_bucket = None
        self._additional_lab_bucket = None
        self._appointment = None
        self._appointment_code = None
        self._appointment_continuation_count = None
        self._appointment_row_template = None
        self._appointment_zero = None
        self._appointments = None
        self._categories = None
        self._consent = None
        self._extra_url_context = None
        self._language = None
        self._locator_inst = None
        self._locator_model = None
        self._has_requisition_model = None
        self._membership_form_category = None
        self._packing_list_model = None
        self._registered_subject = None
        self._requisition_model = None
        self._scheduled_entry_bucket = None
        self._scheduled_entry_bucket_meta = None
        self._scheduled_lab_bucket = None
        self._show = None
        self._site_lab_tracker = None
        self._subject_configuration = None
        self._subject_hiv_history = None
        self._subject_hiv_status = None
        self._subject_identifier = None
        self._subject_membership_models = None
        self._subject_type = None
        self._view = None
        self._visit_messages = []
        self._visit_model = None
        self._visit_model_instance = None
        self.exclude_others_if_keyed_model_name = ''
        self.is_dispatched, self.dispatch_producer = False, None
        self.selected_visit = None

        self._set_registered_subject(registered_subject)
        self._set_membership_form_category(dashboard_category)
        self.set_show(show)

    def add_to_context(self):

        # TODO: is this necessary?
        #self.set_subject_type(kwargs.get('subject_type') or kwargs.get('dashboard_type'))
#         if self.get_registered_subject():
#             self.context.add(
#                 registered_subject=self.get_registered_subject(),
#                 subject_identifier=self.get_subject_identifier(),
#                 subject_hiv_history=self.get_subject_hiv_history(),
#                 subject_hiv_status=self.get_subject_hiv_status(),
#                 subject_configuration=self.get_subject_configuration(),
#                 )
        self.context.add(
            subject_dashboard_url=self.get_dashboard_url_name(),
            show=self.get_show(),
            registered_subject=self.get_registered_subject(),
            subject_identifier=self.get_subject_identifier(),
            subject_hiv_history=self.get_subject_hiv_history(),
            subject_hiv_status=self.render_subject_hiv_status(),
            subject_configuration=self.get_subject_configuration(),
            appointment_meta=Appointment._meta,
            subject_configuration_meta=SubjectConfiguration._meta,
            appointment_row_template=self.get_appointment_row_template(),
            appointment=self.get_appointment(),
            appointments=self.get_appointments(),
            appointment_visit_attr=self._get_visit_model()._meta.object_name.lower(),
            visit_attr=convert_from_camel(self._get_visit_model()._meta.object_name),
            visit_model=self._get_visit_model(),
            visit_model_instance=self._get_visit_model_instance(),
            visit_instance=self.get_appointment_continuation_count(),
            visit_code=self.get_appointment_code(),
            visit_model_meta=self._get_visit_model()._meta,
            visit_messages=self.get_visit_messages(),
            membership_forms=self.get_subject_membership_models(),
            keyed_membership_forms=self.get_keyed_subject_membership_models(),
            unkeyed_membership_forms=self.get_unkeyed_subject_membership_models(),
            form_language_code=self.get_language(),
            extra_url_context=self.get_extra_url_context(),
            )
        if self.get_show() == 'forms':
            self._add_or_update_entry_buckets()
            self._run_rule_groups()
            self.context.add(
                scheduled_entry_bucket_meta=self.get_scheduled_entry_meta(),
                scheduled_entry_bucket=self.get_scheduled_entry_bucket(),  # TODO: things takes a long time!!
                scheduled_lab_bucket=self.get_scheduled_lab_bucket(),
                additional_entry_bucket=self.get_additional_entry_bucket(),
                additional_lab_bucket=self.get_additional_lab_bucket(),
                requisition_model=self._get_requisition_model(),
                rendered_scheduled_forms=self.render_scheduled_forms()
                )
            if self._get_requisition_model():
                self.context.add(requisition_model_meta=self._get_requisition_model()._meta)
            self.render_summary_links()
        self.context.add(rendered_action_items=self.render_action_item())
        self.context.add(rendered_locator=self.render_locator())
        self.context.add(local_results=self.render_labs())

    @classmethod
    def add_to_urlpattern_string(cls):
        return '(?P<show>{show})/'

    @classmethod
    def add_to_urlpattern_string_kwargs(cls):
        return {'show': 'appointments|forms'}

    def get_home_url(self):
        """Returns a home url."""
        return reverse(self.get_dashboard_url_name(), kwargs={'dashboard_type': self.get_dashboard_type(),
                                                              'dashboard_model': self.get_dashboard_model_name(),
                                                              'dashboard_id': self.get_dashboard_id(),
                                                              'show': 'forms'})

    def verify_dashboard_model(self, value):
        """Verify the dashboard model has a way to get to registered_subject."""
        for model in value.itervalues():
            if model:
                if not 'get_registered_subject' in dir(model):
                    raise ImproperlyConfigured('RegisteredSubjectDashboard dashboard_model {0} must have method get_registered_subject(). See {1}.'.format(model, self))

    def set_site_lab_tracker(self):
        """Sets to the site_lab_tracker.

        (Direct import at the top of the module causes a circular import for sphinx.)"""
        from bhp_lab_tracker.classes import site_lab_tracker
        self._site_lab_tracker = site_lab_tracker

    def get_site_lab_tracker(self):
        if not self._site_lab_tracker:
            self.set_site_lab_tracker()
        return self._site_lab_tracker

    def set_scheduled_entry_meta(self):
        ScheduledEntryBucket = models.get_model('bhp_entry', 'ScheduledEntryBucket')
        self._scheduled_entry_bucket_meta = ScheduledEntryBucket._meta

    def get_scheduled_entry_meta(self):
        if not self._scheduled_entry_bucket_meta:
            self.set_scheduled_entry_meta()
        return self._scheduled_entry_bucket_meta

    def set_subject_hiv_status(self):
        """Sets to the value returned by the site_lab_tracker for this registered subject."""
        self._subject_hiv_status = None
        if self.get_registered_subject():
            self._subject_hiv_status = self.get_site_lab_tracker().get_current_value('HIV', self.get_registered_subject().subject_identifier, self.get_registered_subject().subject_type)[0]
        return self._subject_hiv_status

    def get_subject_hiv_status(self):
        if not self._subject_hiv_status:
            self.set_subject_hiv_status()
        return self._subject_hiv_status

    def set_subject_hiv_history(self):
        """Sets to the value returned by the site_lab_tracker for this registered subject."""
        self._subject_hiv_history = None
        if self.get_registered_subject():
            self._subject_hiv_history = self.get_site_lab_tracker().get_history_as_string('HIV', self.get_registered_subject().subject_identifier, self.get_registered_subject().subject_type)
        return self._subject_hiv_history

    def get_subject_hiv_history(self):
        if not self._subject_hiv_history:
            self.set_subject_hiv_history()
        return self._subject_hiv_history

    def set_view(self, value=None):
        """Sets the name of the view coming from __init__ for the url."""
        self._view = value or 'subject_dashboard'  # TODO: default this for now, but should be removed
        if not self._view:
            raise TypeError('Attribute _view may not be None. See {0}'.format(self))

    def get_view(self):
        if not self._view:
            self.set_view()
        return self._view

    def set_consent(self):
        raise ImproperlyConfigured('Users must override this method. See {0}'.format(self))

    def _set_consent(self):
        self.set_consent()
        if self._consent:
            if not isinstance(self._consent, BaseConsent):
                raise TypeError('Expected an instance of BaseConsent. Got {0}. See {1}'.format(self._consent, self))

    def get_consent(self):
        if not self._consent:
            self._set_consent()
        return self._consent

    def set_language(self):
        """Sets to the language of consent.

        If the consent has not been defined for this dashboard, just take the settings LANGUAGE attribute."""
        try:
            if self.get_consent():
                self.get_consent().language
                translation.activate(self.get_consent().language)
            self._language = translation.get_language()
        except:
            self._language = settings.LANGUAGE_CODE

    def get_language(self):
        if not self._language:
            self.set_language()
        return self._language

    def set_appointment_row_template(self, template_file=None):
        self._appointment_row_template = template_file or 'appointment_row.html'

    def get_appointment_row_template(self):
        if not self._appointment_row_template:
            self.set_appointment_row_template()
        return self._appointment_row_template

    def set_registered_subject(self, registered_subject=None):
        """Sets the registered_subject instance, may be overridden by users."""
        pass

    def _set_registered_subject(self, registered_subject=None):
        self._registered_subject = registered_subject
        self.set_registered_subject(registered_subject)
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if not self._registered_subject and self.get_dashboard_model() == RegisteredSubject:
            self._registered_subject = RegisteredSubject.objects.filter(pk=self.get_dashboard_id()).order_by('-created')[0]
        elif not self._registered_subject and 'get_registered_subject' in dir(self.get_dashboard_model()):
            self._registered_subject = self.get_dashboard_model_instance().get_registered_subject()
        elif not self._registered_subject and re_pk.match(str(registered_subject)):
            # is registered_subject a pk? TODO: how could this be if dashboard_model is not registered_subject?
            self._registered_subject = RegisteredSubject.objects.get(pk=registered_subject)
        elif not self._registered_subject and self.get_appointment():
            # can i get it from an appointment? TODO: is this even possible?
            self._registered_subject = self.get_appointment().get_registered_subject()
        elif self._registered_subject:
            if not isinstance(self._registered_subject, RegisteredSubject):
                raise TypeError('Expected instance of RegisteredSubject. See {0}'.format(self))
        else:
            pass
        if not self._registered_subject:
            raise TypeError('Attribute \'_registered_subject\' may not be None. Perhaps add method get_registered_subject() to the model {0}. See {1}'.format(self.get_dashboard_model(), self))

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
                    raise AttributeError('Unable to determine appointment for SubjectDashboard {0} using parameter \'appointment\'. Got {1}. See {2}.'.format(self.__class__, appointment, self))
            if appointment_code:
                if Appointment.objects.filter(registered_subject=self.get_registered_subject(), visit_definition__code=appointment_code, visit_instance=appointment_continuation_count):
                    self._appointment = Appointment.objects.get(registered_subject=self.get_registered_subject(), visit_definition__code=appointment_code, visit_instance=appointment_continuation_count)
        if not self._appointment:
            if self.get_dashboard_model_name() == 'appointment':
                self._appointment = Appointment.objects.get(pk=self.get_dashboard_id())
            elif self.get_dashboard_model_name() == 'visit':
                self._appointment = self._get_visit_model_instance().get_appointment()
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
                if Appointment.objects.filter(registered_subject=self.get_appointment().registered_subject, visit_definition=self.get_appointment().visit_definition, visit_instance=0) > 1:
                    self.delete_duplicate_appointments(inst=self)
                self._appointment_zero = Appointment.objects.get(registered_subject=self.get_appointment().registered_subject, visit_definition=self.get_appointment().visit_definition, visit_instance=0)

    def get_appointment_zero(self):
        if not self._appointment_zero:
            self.set_appointment_zero()
        return self._appointment_zero

    @classmethod
    def delete_duplicate_appointments(cls, inst=None, visit_model=None):
        """Deletes all but one duplicate appointments as long as they are not related to a visit model."""
        if not visit_model:
            visit_model = inst.get_visit_model()
        appointments = Appointment.objects.values('registered_subject__pk', 'visit_definition', 'visit_instance').all().annotate(num=Count('pk')).order_by()
        dups = [a for a in appointments if a.get('num') > 1]
        for dup in dups:
            num = dup['num']
            del dup['num']
            for dup_appt in Appointment.objects.filter(**dup):
                if not visit_model.objects.filter(appointment=dup_appt):
                    try:
                        print 'delete {0}'.format(dup_appt)
                        dup_appt.delete()
                        num -= 1
                    except:
                        pass
                    if num == 1:
                        break  # leave one

    def set_appointment_code(self, value=None):
        self._appointment_code = value

    def get_appointment_code(self):
        if not self._appointment_code:
            self.set_appointment_code()
        return self._appointment_code

    def set_appointment_continuation_count(self, value=None):
        self._appointment_continuation_count = value

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

    def _set_visit_model(self, visit_model=None):
        self._visit_model = visit_model
        if not self._visit_model:
            raise TypeError('Attribute _visit_model may not be None. Override the method to return a visit mode class or specify at init.')
        if not issubclass(self._visit_model, BaseVisitTracking):
            raise TypeError('Expected visit model class to be a subclass of BaseVisitTracking. Got {0}. See {1}.'.format(self._visit_model, self))

    def get_visit_model(self):
        """gets a user defined visit model and passes to the setter.

        Users may override.
        """
        return None

    def _get_visit_model(self):
        """Returns the visit model class."""
        if not self._visit_model:
            self._set_visit_model(visit_model=self.get_visit_model())
        return self._visit_model

    def get_visit_model_attrname(self):
        """Returns what is assumed to be the field name for the visit model in appointment based on the visit model object name."""
        return convert_from_camel(self._get_visit_model()._meta.object_name)

    def get_visit_model_rel_attrname(self):
        """Returns what is assumed to be the field name for the visit model in appointment based on the visit model object name."""
        return self._get_visit_model()._meta.object_name.lower()

    def set_visit_model_instance(self, model_inst=None, pk=None, appointment=None):
        """Sets the visit model instance but may be None."""
        self._visit_model_instance = None
        if model_inst:
            self._visit_model_instance = model_inst
        elif pk:
            self._visit_model_instance = self._get_visit_model().objects.get(pk=pk)
        elif appointment:
            self._visit_model_instance = self._get_visit_model().objects.get(appointment=appointment)
        elif self.get_dashboard_model_name() == 'visit':
            self._visit_model_instance = self._get_visit_model().objects.get(pk=self.get_dashboard_id())
        elif self.get_dashboard_model_name() == 'appointment':
            try:
                self._visit_model_instance = getattr(self.get_appointment(), self.get_visit_model_rel_attrname())
            except self._get_visit_model().DoesNotExist:
                pass
        else:
            pass
        if self._visit_model_instance:
            if not isinstance(self._visit_model_instance, self._get_visit_model()):
                raise TypeError('Expected an instance of visit model class {0} using (model_inst={1}, pk={2}, appointment={3} and self.get_dashboard_model_name()={4}). See {5}.'.format(self._get_visit_model(), model_inst, pk, appointment, self.get_dashboard_model_name(), self))

    def _get_visit_model_instance(self):
        if not self._visit_model_instance:
            self.set_visit_model_instance()
        return self._visit_model_instance

    def set_requisition_model(self):
        """Users must override if requisitions are used to specify the requisition model."""
        self._requisition_model = None

    def _set_requisition_model(self):
        self._requisition_model = self.get_requisition_model()
        if self._get_has_requisition_model():
            if not self._requisition_model:
                raise TypeError('Attribute _requisition model cannot be None. See {0}'.format(self))
            if not issubclass(self._requisition_model, BaseBaseRequisition):
                raise TypeError('Expected a subclass of BaseBaseRequisition. Got {0}. See {1}.'.format(self._requisition_model, self))

    def _get_requisition_model(self):
        if not self._requisition_model:
            self._set_requisition_model()
        return self._requisition_model

    def get_requisition_model(self):
        """Users must override if requisitions are used to return the requisition model."""
        self._set_has_requisition_model(False)
        return None

    def _set_has_requisition_model(self, value=None):
        """Sets to True unless deliberately set to False."""
        self._has_requisition_model = True
        if value == False:
            self._has_requisition_model = False

    def _get_has_requisition_model(self):
        """Returns a boolean indicating if the class has a requisition model (default: True).

        .. note:: :func:`get_requisition_model` will set this to False by default."""
        if self._has_requisition_model == None:
            self._set_has_requisition_model()
        return self._has_requisition_model

    def _set_packing_list_model(self):
        self._packing_list_model = self.get_packing_list_model()
        if not self._packing_list_model:
            raise TypeError('Attribute \'_packing_list_model\' may not be None. Override the getter. See {0}'.format(self))
        if not issubclass(self._packing_list_model, BasePackingList):
            raise TypeError('Expected a subclass of BasePackingList. Got {0}. See {1}.'.format(self._packing_list_model, self))

    def _get_packing_list_model(self):
        if not self._packing_list_model:
            self._set_packing_list_model()
        return self._packing_list_model

    def get_packing_list_model(self):
        """Users must override if requisitions are used to specify the requisition model."""
        return None

    def set_membership_form_category(self, value=None):
        """Sets to a category name needed to filter the MembershipForm model.

        Must be a category appearing in the MembershipForm model, see :func:`check_category`.

        Users may override if the category name is not coming from the URL."""
        pass

    def _set_membership_form_category(self, value=None):
        """Sets the membership_form_category for this registered subject dashboard need to filter the QuerySet of Membership forms to display on the dashboard.

        .. note:: The category name no longer defaults to the registered subject \'subject type\'."""
        self._membership_form_category = value
        if not self._membership_form_category:
            self.set_membership_form_category()
        #if not self._membership_form_category:
        #    self._membership_form_category = value or self.get_subject_type()
        # check if this category exists in the MembershipForm model
        if not self._membership_form_category:
            raise ImproperlyConfigured('Attribute \'_membership_form_category\' may not be None. Must be one of {0}. '
                                 'The category should either come from the URL or from overridden dashboard method \'set_membership_form_category\'. See {1}.'.format(self.get_categories(), self))
        self.check_category(self._membership_form_category)

    def get_membership_form_category(self):
        if not self._membership_form_category:
            self._set_membership_form_category()
        return self._membership_form_category

    def check_category(self, category):
        """Checks for given category if any instances of MembershipForm exist.

        Dashboard needs these to display keyed and unkeyed models listed in the MembershipForms model."""
        if category not in self.get_categories():
            raise ImproperlyConfigured('Invalid membership_form category. Attribute \'_membership_form_category\'=\'{0}\' not found in MembershipForms. Must be one of {1}. See {2}.'.format(category, self.get_categories(), self))

    def set_categories(self, value=None):
        """Sets to a list of valid categories.

        .. note:: the list of categories is based on those that appear in the MembershipForm category field.
                  The MembershipForm field \'category\' may be a string of category names delimited by a comma."""
        self._categories = []
        categories = MembershipForm.objects.values('category').order_by('category').distinct()
        # turn into a list, split and strip
        for c in categories:
            self._categories.extend([x.strip() for x in c['category'].split(',')])
        self._categories = list(set(self._categories))
        if not self._categories:
            raise MembershipFormError('Attribute _categories may not be None. Have any membership forms been defined?. See module \'bhp_visit\'. See {0}'.format(self))

    def get_categories(self):
        if not self._categories:
            self.set_categories()
        return self._categories

    def _add_or_update_entry_buckets(self):
        """ Adds missing bucket entries and flags added and existing entries as keyed or not keyed (only)."""
        if self._get_visit_model_instance():
            scheduled_entry = ScheduledEntry()
            scheduled_entry.add_or_update_for_visit(self._get_visit_model_instance())
            # if requisition_model has been defined, assume scheduled labs otherwise pass
            if self._get_requisition_model():
                ScheduledLabEntryBucket.objects.add_for_visit(
                    visit_model_instance=self._get_visit_model_instance(),
                    requisition_model=self._get_requisition_model())
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
        AdditionalEntryBucket = models.get_model('bhp_entry', 'AdditionalEntryBucket')
        self._additional_entry_bucket = AdditionalEntryBucket.objects.filter(registered_subject=self.get_registered_subject())

    def get_additional_entry_bucket(self):
        if not self._additional_entry_bucket:
            self.set_additional_entry_bucket()
        return self._additional_entry_bucket

    def set_subject_type(self):
        self._subject_type = self.get_registered_subject().subject_type

    def get_subject_type(self):
        if not self._subject_type:
            self.set_subject_type()
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
            raise TypeError('attribute subject_identifier may not be None. See {0}'.format(self))

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

    def set_show(self, value):
        self._show = value or 'appointments'

    def get_show(self):
        if not self._show:
            self.set_show()
        return self._show

    def set_subject_membership_models(self):
        """Sets to a dictionary of membership "models" that are keyed model instances and unkeyed model classes.

        Membership forms can also be proxy models ... see mochudi_subject.models."""
        helper = MembershipFormHelper()
        self._subject_membership_models = helper.get_membership_models_for(
            self.get_registered_subject(),
            self.get_membership_form_category(),
            extra_grouping_key=self.exclude_others_if_keyed_model_name)

    def get_subject_membership_models(self, key=None):
        if not self._subject_membership_models:
            self.set_subject_membership_models()
        return self._subject_membership_models

    def get_keyed_subject_membership_models(self):
        return self.get_subject_membership_models().get('keyed', [])

    def get_unkeyed_subject_membership_models(self):
        return self.get_subject_membership_models().get('unkeyed', [])

    def _run_rule_groups(self):
        """ Runs rules in any rule groups if visit_code is known and update entries as (new, not required) when the visit dashboard is refreshed.

        If status is 'keyed' and the form is actually keyed, do nothing."""
        if not self.get_subject_identifier():
            raise AttributeError('set value of subject_identifier before calling dashboard create() when scheduled_entry_bucket_rules exist')
        # run rules if visit_code is known -- user selected, that is user clicked to see list of
        # scheduled entries for a given visit.

        # TODO: on data entry, is the visit_model_instance always 0 or the actual instance 0,1,2, etc
        if self._get_visit_model_instance():
            rule_groups.update_all(self._get_visit_model_instance())

    def render_summary_links(self, template_filename=None):
        """Renders the side bar template for subject summaries."""
        if not template_filename:
            template_filename = 'summary_side_bar.html'
        summary_links = render_to_string(template_filename, {
                'links': Link.objects.filter(dashboard_type=self.get_dashboard_type()),
                'subject_identifier': self.get_subject_identifier()})
        self.context.add(summary_links=summary_links)

    def render_labs(self):
        """Renders labs for the template side bar if the requisition model is set, by default will not update.

        .. seealso:: :class:`lab_clinic_api.classes.EdcLab`"""

        if self._get_requisition_model():
            edc_lab = EdcLab()
            return edc_lab.render(self.get_subject_identifier(), False)
        return ''

    def get_locator_model(self):
        """Users should override to return the Locator model class.

        If not overridden, the locator information will not be rendered for the template."""
        return None

    def _set_locator_model(self):
        """Sets the locator model class which must be a subclass of bhp_locator.BaseLocator."""
        self._locator_model = self.get_locator_model()
        if self._locator_model:
            if not issubclass(self._locator_model, BaseLocator):
                raise TypeError('Locator model must be a subclass of BaseLocator. See {0}'.format(self))
        #if not self._locator_model:
        #    raise TypeError('Attribute _locator_model may not be None. See {0}'.format(self))

    def _get_locator_model(self):
        if not self._locator_model:
            self._set_locator_model()
        return self._locator_model

    def _set_locator_inst(self):
        """Sets to a locator model instance for the registered_subject."""
        self._locator_inst = None
        if self.get_locator_model():
            registered_subject = self.get_locator_registered_subject() or self.get_registered_subject()
            if self.get_locator_model().objects.filter(registered_subject=registered_subject):
                self._locator_inst = self.get_locator_model().objects.get(registered_subject=registered_subject)

    def _get_locator_inst(self):
        if not self._locator_inst:
            self._set_locator_inst()
        return self._locator_inst

    def get_locator_registered_subject(self):
        """Users may override to return a registered_subject other than the current or None -- used to filter the locator model.

        For example, current subject is an infant, need mother\'s registered subject instance to filter Locator model."""
        return self.get_registered_subject()

    def get_locator_visit_model(self):
        """Users may override to return a visit_model other than the current or None -- used to filter the locator model."""
        return self.get_visit_model()

    def _get_locator_visit_model_attrname(self):
        return convert_from_camel(self.get_locator_visit_model()._meta.object_name)

    def get_locator_scheduled_visit_code(self):
        """ Returns visit where the locator is scheduled, TODO: maybe search visit definition for this?."""
        return None

    def get_locator_template(self):
        """Users may override to return a custom locator template.

        Defaults to 'locator_include.html'."""
        return 'locator_include.html'

    def render_locator(self):
        """Renders to string the locator for the current locator instance if it is set.

        .. note:: getting access to the correct visit model instance for the locator
                  is a bit tricky. locator model is usually scheduled once for the
                  subject type and otherwise edited from the dashboard sidebar. It may
                  also be 'added' from the dashboard sidebar. Either way, the visit model
                  instance is required -- that being the instance that was (or would
                  have been) used if updated as a scheduled form. If the dashboard is
                  in appointments mode, there is no selected visit model instance.
                  Similarly, if the locator is edited from another dashboard, such as
                  the infant dashboard with maternal/infant pairs, the maternal visit
                  instance is not known. Some methods may be overriden to solve this.
                  They all have 'locator' in the name."""
        context = {}
        if self._get_locator_model():
            locator_add_url = None
            locator_change_url = None
            if not self._get_locator_inst():
                context.update({'locator': None})
                locator_add_url = reverse('admin:' + self._get_locator_model()._meta.app_label + '_' + self._get_locator_model()._meta.module_name + '_add')
            if self._get_locator_inst():
                context.update({'locator': self._get_locator_inst()})
                locator_change_url = reverse('admin:' + self._get_locator_model()._meta.app_label + '_' + self._get_locator_model()._meta.module_name + '_change', args=(self._get_locator_inst().pk, ))
                for field in self._get_locator_inst()._meta.fields:
                    if isinstance(field, (TextField)):
                        value = getattr(self._get_locator_inst(), field.name)
                        if value:
                            setattr(self._get_locator_inst(), field.name, '<BR>'.join(wrap(value, 25)))
            context.update({
                'subject_dashboard_url': self.get_dashboard_url_name(),
                'dashboard_type': self.get_dashboard_type(),
                'dashboard_model': self.get_dashboard_model_name(),
                'dashboard_id': self.get_dashboard_id(),
                'show': self.get_show(),
                'registered_subject': self.get_registered_subject(),
                'visit_attr': self.get_visit_model_attrname(),
                'visit_model_instance': self._get_visit_model_instance(),
                'appointment': self.get_appointment(),
                'locator_add_url': locator_add_url,
                'locator_change_url': locator_change_url})
        # subclass may insert / update context values (e.g. visit stuff)
            context = self.update_locator_context(context)
        return render_to_string(self.get_locator_template(), context)

    def update_locator_context(self, context):
        """Update context to set visit information if needing something other than the default."""
        if context.get('visit_model_instance'):
            if not isinstance(context.get('visit_model_instance'), self.get_locator_visit_model()):
                context['visit_model_instance'] = None
        if not context.get('visit_model_instance'):
            if self._get_locator_inst():
                visit_model_instance = getattr(self._get_locator_inst(), self._get_locator_visit_model_attrname())
            else:
                locator_visit_code = self.get_locator_scheduled_visit_code()
                visit_model_instance = None
                if self.get_locator_model().objects.filter(registered_subject=self.get_locator_registered_subject()):
                    visit_model_instance = self.get_locator_model().objects.get(registered_subject=self.get_locator_registered_subject()).maternal_visit
                elif self.get_locator_visit_model().objects.filter(appointment__registered_subject=self.get_locator_registered_subject(), appointment__visit_definition__code=locator_visit_code, appointment__visit_instance=0):
                    visit_model_instance = self.get_locator_visit_model().objects.get(appointment__registered_subject=self.get_locator_registered_subject(), appointment__visit_definition__code=locator_visit_code, appointment__visit_instance=0)
                else:
                    pass
            if visit_model_instance:
                context.update({'visit_attr': convert_from_camel(visit_model_instance._meta.object_name), 'visit_model_instance': visit_model_instance})
        return context

    def render_action_item(self, action_item_cls=None, template=None, **kwargs):
        """Renders to string the action_items for the current registered subject."""
        from bhp_crypto.fields import EncryptedTextField
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
            'dashboard_model': self.get_dashboard_model_name(),
            'dashboard_id': self.get_dashboard_id(),
            'show': self.get_show(),
            'action_item_meta': action_item_cls._meta})
        return rendered_action_items

    def render_scheduled_forms(self):
        """Renders the Scheduled Entry Forms section of the dashboard using the context class ScheduledEntryContext."""
        template = 'scheduled_entries.html'
        scheduled_entries = []
        for scheduled_entry in self.get_scheduled_entry_bucket():
            inst = ScheduledEntryContext(scheduled_entry, self.get_appointment(), self.get_visit_model())
            scheduled_entries.append(inst.get_context())
        rendered_scheduled_forms = render_to_string(template, {
            'scheduled_entries': scheduled_entries,
            'visit_attr': self.get_visit_model_attrname(),
            'visit_model_instance': self._get_visit_model_instance(),
            'registered_subject': self.get_registered_subject().pk,
            'appointment': self.get_appointment().pk,
            'dashboard_type': self.get_dashboard_type(),
            'dashboard_model': self.get_dashboard_model_name(),
            'dashboard_id': self.get_dashboard_id(),
            'subject_dashboard_url': self.get_dashboard_url_name(),
            'show': self.get_show()})
        return rendered_scheduled_forms

    def get_subject_hiv_template(self):
        return 'subject_hiv_status.html'

    def render_subject_hiv_status(self):
        """Renders to string a to a url to the historymodel for the subject_hiv_status."""
        if self.get_subject_hiv_status():
            change_list_url = reverse('admin:bhp_lab_tracker_historymodel_changelist')
            return render_to_string(self.get_subject_hiv_template(), {
                'subject_hiv_status': self.get_subject_hiv_status(),
                'subject_identifier': self.get_subject_identifier(),
                'subject_type': self.get_subject_type(),
                'change_list_url': change_list_url})
        return ''
