from django.core.exceptions import MultipleObjectsReturned
from django.template.loader import render_to_string

from edc.subject.appointment.models import Appointment
from edc.subject.appointment_helper.classes import AppointmentHelper
from edc.subject.visit_schedule.models import ScheduleGroup, VisitDefinition, MembershipForm

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
        """Returns a queryset on one appointment relative to the subject consent household member"""
        self._appointments = super(BaseSubjectDashboard, self).appointments
        appointments = []
        for appointment in self._appointments:
            try:
                subject_visit = SubjectVisit.objects.get(appointment=appointment)
                if subject_visit.household_member == self.household_member:
                    appointments.append(appointment)
            except SubjectVisit.DoesNotExist:
                if appointment.subject_visit_id is None:
                    appointments.append(appointment)
                pass
        self._appointments = appointments
        return self._appointments

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

#     def create_next_appointment(self):
#         """Creates the next appointment subsequent to BASELINE (T0) or the last.
# 
#         BASELINE appointment is created by the consent."""
#         if self.next_visit_defintion:
#             AppointmentHelper().create_all(
#                 self.registered_subject,
#                 self.__class__.__name__.lower(),
#                 using='default',
#                 source='BaseAppointmentMixin',
#                 visit_definitions=[self.next_visit_definition])
# 
#     @property
#     def next_visit_definition(self):
#         """Returns the next visit_definiton instance following the time_point of the last appointment."""
#         if not self._next_visit_definition:
#             try:
#                 if not self.household_member == self.consent.household_member:
#                     try:
#                         Appointment.objects.get(
#                             registered_subject=self.registered_subject,
#                             visit_definition__code__in=BASELINE_CODES)
#                     except Appointment.DoesNotExist:
#                         raise ValueError('Expected baseline (T0) appointment to exist for consented subject. Got None.')
#                     if self.household_member in self.consent.household_member.next_members:
#                         schedule_group = ScheduleGroup.objects.get(
#                             membership_form__content_type_map__model=self.consent._meta.object_name.lower())
#                         try:
#                             last_annual_appointment = Appointment.objects.filter(
#                                 registered_subject=self.registered_subject,
#                                 visit_definition__time_point__gt=0,
#                                 schedule_group=schedule_group
#                                 ).order_by('-visit_definition__time_point')[0]
#                             # get next timepoint for this schedule group
#                             for visit_definition in VisitDefinition.objects.filter(
#                                     schedule_group=schedule_group,
#                                     time_point__gt=last_annual_appointment.visit_definition.time_point,
#                                     ).order_by('time_point'):
#                                 self._next_visit_definition = visit_definition
#                                 break
#                         except IndexError:
#                             self._next_visit_definition = VisitDefinition.objects.get(schedule_group=schedule_group, time_point=0)
#             except AttributeError:
#                 # no consent
#                 pass
#         return self._next_visit_definition
# 
#     def next_members(self):
#         for household_member in HouseholdMember.objects.filter(
#             registered_subject=self.registered_subject,
#             household_structure__survey__datetime_start__gt=).order_by('household_structure__survey__datetime_start'):
#             next_members.append(household_member)
#         return next_members

    @property
    def subject_referral(self):
        """Returns this household members subject_referral instance or None."""
        try:
            subject_referral = SubjectReferral.objects.get(subject_visit__household_member=self.household_member)
        except SubjectReferral.DoesNotExist:
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
