from datetime import datetime

from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string

from edc.subject.appointment.models import Appointment
from edc.subject.appointment_helper.classes import AppointmentHelper
from edc.subject.appointment_helper.exceptions import AppointmentCreateError
from edc_consent.models.consent_type import ConsentType
from edc_device import device

from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_subject.models import (
    SubjectConsent, SubjectConsentExtended, SubjectVisit, SubjectLocator, SubjectReferral,
    CorrectConsent, ElisaHivResult, HivResult)
from bhp066.apps.bcpp_lab.models import SubjectRequisition, PackingList

from .base_subject_dashboard import BaseSubjectDashboard


class SubjectDashboard(BaseSubjectDashboard):

    view = 'subject_dashboard'
    dashboard_name = 'Participant Dashboard'
    urlpattern_view = 'apps.bcpp_dashboard.views'
    dashboard_url_name = 'subject_dashboard_url'
    urlpatterns = [
        BaseSubjectDashboard.urlpatterns[0][:-1] + '(?P<appointment_code>{appointment_code})/$'] + BaseSubjectDashboard.urlpatterns
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

    def get_context_data(self, **kwargs):
        self.context = super(SubjectDashboard, self).get_context_data(**kwargs)
        try:
            first_subject_consent = SubjectConsent.objects.filter(
                subject_identifier=self.subject_identifier).order_by('created').first()
        except SubjectConsent.DoesNotExist:
            first_consent_consent = None
        try:
            latest_subject_consent = SubjectConsent.objects.filter(
                subject_identifier=self.subject_identifier).latest()
        except SubjectConsent.DoesNotExist:
            latest_subject_consent = None
        self.context = super(SubjectDashboard, self).get_context_data(**kwargs)
        try:
            membership_form_extra_url_context = '&household_member={0}'.format(
                latest_subject_consent.household_member.pk)
        except AttributeError:
            membership_form_extra_url_context = '&household_member={0}'.format(self.household_member.pk)

        if not SubjectConsent.consent.valid_consent_for_period(
                self.subject_identifier, timezone.now()):
            unkeyed = self.context.get('unkeyed_membership_forms')
            try:
                index = unkeyed.index(SubjectConsent)
                if latest_subject_consent:
                    unkeyed.insert(index, SubjectConsentExtended)
            except ValueError:
                if latest_subject_consent:
                    unkeyed.append(SubjectConsentExtended)
                    index = unkeyed.index(SubjectConsentExtended)
                else:
                    unkeyed.append(SubjectConsent)
                    index = unkeyed.index(SubjectConsent)
            try:
                consent_type = ConsentType.objects.latest('start_datetime')
                unkeyed[index]._meta.verbose_name = 'Subject Consent V{}'.format(consent_type.version)
            except IndexError:
                pass
            if unkeyed:
                consenting_member = None
                member_being_viewed = None
                try:
                    # If you are in a site machine and trying to consent, then you are certain that you have the
                    # the household member that corresponds to the current survey. You are also certain that the
                    # the member you want to consent will always be the member of the curent survey setting in the
                    # machine.
                    consenting_member = HouseholdMember.objects.get(
                        internal_identifier=self.household_member.internal_identifier,
                        household_structure__survey=Survey.objects.current_survey())
                except HouseholdMember.DoesNotExist:
                    # If you cannot find the member of this current survey, then you are probably trying to view the
                    # dashboard of a member from the past. This can only happen in the central server.
                    if device.is_central_server:
                        member_being_viewed = self.household_member
                dashboard_member = consenting_member if consenting_member else member_being_viewed
                unkeyed_consent_context = '&household_member={0}'.format(dashboard_member.pk)
                self.context['unkeyed_consent_context'] = unkeyed_consent_context
            self.context['unkeyed_membership_forms'] = unkeyed
        self.context.update(
            home='bcpp',
            search_name='subject',
            household_dashboard_url=self.household_dashboard_url,
            title='Research Subject Dashboard',
            subject_consent=latest_subject_consent,
            first_consent=first_subject_consent,
            correct_consent=self.correct_consent(latest_subject_consent),
            subject_referral=self.subject_referral,
            last_subject_referral=self.last_subject_referral,
            elisa_hiv_result=self.elisa_hiv_result,
            hiv_result=self.hiv_result,
            rendered_household_members_sidebar=self.render_household_members_sidebar(),
            membership_form_extra_url_context=membership_form_extra_url_context)
        return self.context

    @property
    def appointments(self):
        if self.appointment:
            return [self.appointment]
        else:
            return []

    @property
    def appointment(self):

        if not self._appointment:
            try:
                appointment_helper = AppointmentHelper()
                options = {
                    'model_name': 'subjectconsent',
                    'using': 'default',
                    'base_appt_datetime': None,
                    'dashboard_type': 'subject',
                    'source': 'BaseAppointmentMixin',
                    'visit_definitions': None,
                    'verbose': False}
                appointment_helper.create_all(self.household_member.registered_subject, **options)
            except AppointmentCreateError:
                self._appointment = None
            if self.dashboard_model_name == 'appointment':
                self._appointment = Appointment.objects.get(pk=self.dashboard_id)
            elif self.dashboard_model_name == 'visit':
                self._appointment = self.visit_model.objects.get(pk=self.dashboard_id).appointment
            elif self.dashboard_model_name == 'household_member':
                survey_year = int(settings.CURRENT_SURVEY.split('-')[2])
                if ((HouseholdMember.objects.filter(registered_subject=self.registered_subject, is_consented=True).count() == survey_year) or (
                        HouseholdMember.objects.filter(registered_subject=self.registered_subject, is_consented=True).count() == 1 and
                        self.household_member.household_structure.survey.survey_slug == 'bcpp-year-1')):
                    # In this case you know for certain that the survey year in household member dashboard represents exactly the
                    # the settings.CURRENT_SURVEY in the system. Therefore just return the visit corresponding to
                    # household member's set survey.
                    visit_code = self.generate_visit_code_from_member(self.household_member)
                    try:
                        self._appointment = Appointment.objects.get(
                            registered_subject=self.registered_subject,
                            visit_definition__code=visit_code)
                    except Appointment.DoesNotExist:
                        self._appointment = None
                else:
                    if self.household_member.household_structure.survey.survey_slug == 'bcpp-year-2':
                        # When you end up here, it means you are a year 2 created member who either did not exists
                        # or was not consented in year 1. This means you are actually trying to create or view the T0
                        # appointment survey, even though you were created with year 2 survey.
                        members = HouseholdMember.objects.filter(registered_subject=self.registered_subject, is_consented=True)
                        if members.count() == 1:
                            self._appointment = Appointment.objects.get(registered_subject=self.registered_subject, visit_definition__code='T0')
                        else:
                            self._appointment = None
                    elif self.household_member.household_structure.survey.survey_slug == 'bcpp-year-3':
                        # In the case that you end up here, what it means is that you are a member created with
                        # the year 3 survey but you either trying to key or view T0 and T1 appointment surveys.
                        members = HouseholdMember.objects.filter(registered_subject=self.registered_subject, is_consented=True)
                        if members.count() == 1:
                            self._appointment = Appointment.objects.get(registered_subject=self.registered_subject, visit_definition__code='T0')
                        elif members.count() == 2:
                            self._appointment = Appointment.objects.get(registered_subject=self.registered_subject, visit_definition__code='T1')
                        else:
                            self._appointment = None
                    else:
                        self._appointment = None
            else:
                self._appointment = None
            self._appointment_zero = None
            self._appointment_code = None
            self._appointment_continuation_count = None
        return self._appointment

    def generate_visit_code_from_member(self, household_member):
        survey_year = int(household_member.household_structure.survey.survey_slug.split('-')[2])
        if survey_year < 1:
            raise TypeError('{} from household member {} is invalid.'.format(
                household_member.household_structure.survey.survey_slug,
                household_member))
        return 'T{}'.format(survey_year - 1)

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
                referral_appt_date__lt=datetime.today(),
                subject_visit__household_member__internal_identifier=self.household_member.internal_identifier).exclude(
                    subject_visit__household_member=self.household_member).order_by('-referral_appt_date')
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

    def correct_consent(self, subject_consent):
        """Returns to the subject consent, if it has been completed."""
        try:
            correct_consent = CorrectConsent.objects.get(subject_consent=subject_consent)
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
        return render_to_string(
            'household_members_sidebar.html',
            {'household_members': self.household_members,
             'household_dashboard_url': self.household_dashboard_url,
             'household_structure': self.household_structure})
