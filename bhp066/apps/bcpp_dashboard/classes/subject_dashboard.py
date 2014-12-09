from datetime import datetime

from django.core.exceptions import MultipleObjectsReturned
from django.template.loader import render_to_string

from edc.subject.appointment.models import Appointment
from edc.subject.appointment_helper.classes import AppointmentHelper
from edc.subject.visit_schedule.models import ScheduleGroup, VisitDefinition, MembershipForm
from edc.subject.appointment_helper.classes import AppointmentHelper
from edc.subject.appointment_helper.exceptions import AppointmentCreateError

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_subject.models import (SubjectConsent, SubjectVisit, SubjectLocator, SubjectReferral,
                                      CorrectConsent, ElisaHivResult, HivResult)
from apps.bcpp_lab.models import SubjectRequisition, PackingList

from .base_subject_dashboard import BaseSubjectDashboard
from apps.bcpp_subject.constants import BASELINE_CODES, ANNUAL_CODES


class SubjectDashboard(BaseSubjectDashboard):

    view = 'subject_dashboard'
    dashboard_name = 'Participant Dashboard'
    urlpattern_view = 'apps.bcpp_dashboard.views'
    dashboard_url_name = 'subject_dashboard_url'
    urlpatterns = [
        BaseSubjectDashboard.urlpatterns[0][:-1] + '(?P<appointment_code>{appointment_code})/$'
        ] + BaseSubjectDashboard.urlpatterns
    urlpattern_options = dict(BaseSubjectDashboard.urlpattern_options, appointment_code='T0|T1|T2|T3|T4')

    template_name = 'subject_dashboard.html'

    def __init__(self, **kwargs):
        self._next_visit_definition = None
        super(SubjectDashboard, self).__init__(**kwargs)
        self.household_dashboard_url = 'household_dashboard_url'
        self.membership_form_category = ['bcpp-survey']
        self.dashboard_type_list = ['subject']
        self.requisition_model = SubjectRequisition
        self.visit_model = SubjectVisit
        self.dashboard_models['subject_consent'] = SubjectConsent
        self.dashboard_models['household_member'] = HouseholdMember
        self.dashboard_models['visit'] = self._visit_model
        # self.appointment_code = kwargs.get('visit_code')

    def get_context_data(self, **kwargs):
        self.context = super(SubjectDashboard, self).get_context_data(**kwargs)
        try:
            membership_form_extra_url_context = '&household_member={0}'.format(self.consent.household_member.pk)
        except AttributeError:
            membership_form_extra_url_context = '&household_member={0}'.format(self.household_member.pk)
        self.context.update(
            home='bcpp',
            search_name='subject',
            household_dashboard_url=self.household_dashboard_url,
            title='Research Subject Dashboard',
            subject_consent=self.consent,
            correct_consent=self.correct_consent,
            subject_referral=self.subject_referral,
            last_subject_referral=self.last_subject_referral,
            elisa_hiv_result=self.elisa_hiv_result,
            hiv_result=self.hiv_result,
            rendered_household_members_sidebar=self.render_household_members_sidebar(),
            membership_form_extra_url_context=membership_form_extra_url_context,
            )
        return self.context

    @property
    def consent(self):
        """Returns to the subject consent instance or None."""
        try:
            subject_consent = SubjectConsent.objects.get(subject_identifier=self.subject_identifier)
        except SubjectConsent.DoesNotExist:
            subject_consent = None
        return subject_consent

    @property
    def appointments(self):
        """Returns a single apppointment as a list.

        * subject_dashboard should only display one appointment
        * select an appointment that has a subject_visit associated with THIS household_member,
        * skip an appointment that has a subject_visit associated with any other household_member,
          even if for the same registered_subject
        * select an appointment that does not have a subject_visit IF not other
          is available
        * select only one appointment
        * if no appointment is selected, try to create additional appointments
        """
        appointments = super(BaseSubjectDashboard, self).appointments
        appointment_to_show = []
        for appointment in appointments:
            try:
                subject_visit = SubjectVisit.objects.get(appointment=appointment)
                if subject_visit.household_member == self.household_member:
                    appointment_to_show.append(appointment)
                    break
            except SubjectVisit.DoesNotExist:
                appointment_to_show.append(appointment)
                break
        if not appointment_to_show:
            appointment_helper = AppointmentHelper()
            options = {
                'model_name': 'subjectconsent',
                'using': 'default',
                'base_appt_datetime': None,
                'dashboard_type': 'subject',
                'source': 'BaseAppointmentMixin',
                'visit_definitions': None,
                'verbose': False}
            try:
                appointments = appointment_helper.create_all(self.household_member.registered_subject, **options)
                appointment_to_show.append(appointments[0])
            except AppointmentCreateError:
                pass
        return appointment_to_show

    @property
    def appointment(self):
        if not self._appointment:
            if self.dashboard_model_name == 'appointment':
                self._appointment = Appointment.objects.get(pk=self.dashboard_id)
            elif self.dashboard_model_name == 'visit':
                self._appointment = self.visit_model.objects.get(pk=self.dashboard_id).appointment
            elif self.dashboard_model_name == 'household_member':
                try:
                    # TODO: is the appointment really needed??
                    # when an appointment is available
                    self._appointment = Appointment.objects.get(registered_subject=self.registered_subject)
                except Appointment.DoesNotExist:
                    # when an appointment is not available (i.e. subject has not yet consented)
                    self._appointment = None
                except MultipleObjectsReturned:
                    self._appointment = None
                except Appointment.MultipleObjectsReturned:
                    self._appointment = Appointment.objects.filter(registered_subject=self.registered_subject)[1]
            else:
                self._appointment = None
            self._appointment_zero = None
            self._appointment_code = None
            self._appointment_continuation_count = None
        return self._appointment

    @property
    def subject_referral(self):
        """Returns this household members subject_referral instance or None."""
        try:
            subject_referral = SubjectReferral.objects.get(subject_visit__household_member=self.household_member)
        except SubjectReferral.DoesNotExist:
            subject_referral = None
        return subject_referral

    @property
    def last_subject_referral(self):
        """Returns this household members subject_referral instance or None."""
        try:
            subject_referrals = SubjectReferral.objects.filter(
                referral_appt_date__lt=datetime.today()
                ).exclude(subject_visit__household_member=self.household_member).order_by('-referral_appt_date')
            subject_referral = subject_referrals[0]
        except SubjectReferral.DoesNotExist:
            subject_referral = None
        except IndexError:
            subject_referral = None
        except AttributeError:
            subject_referral = None
        return subject_referral

    @property
    def hiv_result(self):
        """Returns this household members hiv_result instance or None."""
        try:
            hiv_result = HivResult.objects.get(subject_visit__household_member=self.household_member)
        except HivResult.DoesNotExist:
            hiv_result = None
        except HivResult.MultipleObjectsReturned:
            hiv_result = HivResult.objects.filter(subject_visit__household_member=self.household_member)[1]
        return hiv_result

    @property
    def elisa_hiv_result(self):
        """Returns this household members elisa_hiv_result instance or None."""
        try:
            elisa_hiv_result = ElisaHivResult.objects.get(subject_visit__household_member=self.household_member)
        except ElisaHivResult.DoesNotExist:
            elisa_hiv_result = None
        return elisa_hiv_result

    @property
    def correct_consent(self):
        """Returns to the subject consent, if it has been completed."""
        try:
            correct_consent = CorrectConsent.objects.get(subject_consent=self.consent)
        except CorrectConsent.DoesNotExist:
            correct_consent = None
        return correct_consent

    @property
    def locator_model(self):
        """Returns the locator model used, e.g. bcpp_subject.subjectlocator."""
        return SubjectLocator

    @property
    def locator_scheduled_visit_code(self):
        """ Returns visit where the locator is scheduled, TODO: maybe search visit definition for this?."""
        return '1000'

    @property
    def packing_list_model(self):
        return PackingList

    def render_labs(self, update=False):
        return ''

    def render_household_members_sidebar(self):
        """Renders to string the household members sidebar."""
        return render_to_string('household_members_sidebar.html',
            {'household_members': self.household_members,
             'household_dashboard_url': self.household_dashboard_url,
             'household_structure': self.household_structure})
