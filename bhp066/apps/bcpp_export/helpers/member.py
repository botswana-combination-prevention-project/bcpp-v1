from copy import copy
from datetime import date

from edc.map.classes import site_mappers
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_household.choices import HOUSEHOLD_STATUS
from apps.bcpp_household.constants import ELIGIBLE_REPRESENTATIVE_PRESENT
from apps.bcpp_household.models.household_log import HouseholdLogEntry
from apps.bcpp_household_member.constants import BHS, UNDECIDED, ANNUAL, ABSENT, REFUSED, HTC
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household_member.models import SubjectRefusal, SubjectAbsenteeEntry
from apps.bcpp_subject.models.subject_consent import SubjectConsent
from apps.bcpp_survey.models import Survey

from .base_helper import BaseHelper
from .plot import Plot


class Member(BaseHelper):
    """
    For example::
        from apps.bcpp_export.helpers import Subject, Plot as PlotCls, Member
        data_errors = []
        members = []
        for household_member in HouseholdMember.objects.filter(
                is_consented=True, household_structure__household__plot__community='digawana').order_by('-created')[0:25]:
            print household_member.internal_identifier
            member = Member(household_member)
            if member.data_errors:
                data_errors.append(member.data_errors)
            members.append(member)

    See all for on type of message:
        [dct.get('consented') for dct in data_errors if 'consented' in dct]

    """

    def __init__(self, household_member):
        super(Member, self).__init__()
        site_mappers.autodiscover()
        self.errors = {}
        self.household_member = household_member
        self.internal_identifier = self.household_member.internal_identifier
        self.household_membership = HouseholdMember.objects.filter(
            internal_identifier=self.household_member.internal_identifier).order_by('created')
        self.household_membership_status = {
            hm.household_structure.survey.survey_slug: hm.member_status for hm in self.household_membership}
        self.household_membership_survey = {
            hm.household_structure.survey.survey_slug: hm for hm in self.household_membership}
        self.registered_subject = RegisteredSubject.objects.get(
            registration_identifier=self.household_member.internal_identifier)
        self.update_plot()
        self.update_member()
        self.update_member_status()
        self.update_household_log()
        self.update_survey()
        self.update_refusal()
        self.update_absentee()

    def __repr__(self):
        return 'Member({0.household_member!r})'.format(self)

    def __str__(self):
        return '{0.household_member!r}'.format(self)

    @property
    def unique_key(self):
        return self.internal_identifier

    def customize_for_csv(self):
        super(Member, self).customize_for_csv()
        self.data['registered_subject'] = self.data['registered_subject'].registration_identifier
        self.data['household_member'] = self.data['household_member'].internal_identifier
        del self.data['household_membership']
        del self.data['household_membership_status']
        del self.data['household_membership_survey']
        del self.data['member_survey']
        del self.data['household_log']
        del self.data['plot']

    def update_plot(self):
        self.plot = Plot(household_member=self.household_member)
        self.plot_identifier = self.plot.plot_identifier
        self.recruitment_type = 'household_survey' if not self.plot_identifier == 'clinic' else 'clinic'
        self.community = self.plot.community

    def update_member(self):
        """Set attributes from the HouseholdMember instance."""
        self.enumeration_min_date = self.household_membership[0].created.date()
        self.first_name = self.household_membership[0].first_name
        self.gender = self.household_membership[0].gender
        self.nights_away = '0-3'

        fieldattrs = [('age_in_years', 'age_in_years'),
                      ('created', 'enumeration_date'),
                      ('visit_attempts', 'member_visit_attempts'),
                      ('is_consented', 'member_consented'),
                      ('study_resident', 'study_resident'),
                      ('relation', 'relation_to_hoh'),
                      ]
        model_cls = HouseholdMember
        for survey in Survey.objects.all():
            self._update(
                survey.survey_abbrev, fieldattrs, model_cls,
                '',
                self.household_membership_survey.get(survey.survey_slug)
                )

    def update_member_status(self):
        """Sets attributes related to member status."""
        for survey in Survey.objects.all():
            try:
                member_status = self.household_membership_survey.get(survey.survey_slug).member_status
                setattr(self, '{}_{}'.format('member_status', survey.survey_abbrev.lower()),
                        member_status)
                if member_status not in [ABSENT, BHS, HTC, REFUSED]:
                    print 'Warning: household_member.internal_identifier{} has member_status of {}.'.format(
                        self.internal_identifier, member_status)
            except AttributeError:
                setattr(self, '{}_{}'.format('member_status', survey.survey_abbrev.lower()), None)

    def update_household_log(self):
        """Set attributes from the HouseholdLog for this member's household."""
        self.household_log = [
            h for h in HouseholdLogEntry.objects.filter(
                household_log__household_structure=self.household_member.household_structure).order_by(
                    'report_datetime')]
        self.household_log_date = [h.report_datetime for h in self.household_log]
        self.household_log_status = [h.household_status for h in self.household_log]

    def update_survey(self):
        """Set attributes related to the surveys the member has been enumerated in."""
        self.surveys_enumerated = [hm.household_structure.survey.survey_slug for hm in self.household_membership]
        self.member_survey = site_mappers.get_mapper(
            self.community)
        try:
            self.member_survey_name = self.member_survey.survey_dates.get(
                self.household_member.household_structure.survey.survey_slug).name.upper()
        except AttributeError:
            print ('Warning: Unexpected survey slug! Mappers not configured for survey_slug {0!r}.'
                   ).format(self.household_member.household_structure.survey.survey_slug)
        self.member_survey_start_date = self.member_survey.survey_dates.get(
            self.household_member.household_structure.survey.survey_slug).start_date
        self.member_survey_full_enrollment_date = self.member_survey.survey_dates.get(
            self.household_member.household_structure.survey.survey_slug).full_enrollment_date
        self.member_survey_smc_start_date = self.member_survey.survey_dates.get(
            self.household_member.household_structure.survey.survey_slug).smc_start_date

    def update_refusal(self):
        """Set attributes related to member refusal, if relevant."""
        fieldattrs = [('refusal_date', 'subject_refusal_date')]
        model_cls = SubjectRefusal
        for survey in Survey.objects.all():
            subject_refusal = self._update(
                survey.survey_abbrev, fieldattrs, model_cls,
                'household_member',
                self.household_membership_survey.get(survey.survey_slug)
                )
            try:
                setattr(self, '{}_{}'.format('subject_refusal_reason', survey.survey_abbrev.lower()),
                        subject_refusal.reason_other if not subject_refusal.reason.upper() == 'OTHER' else subject_refusal.reason_other)
            except AttributeError:
                setattr(self, '{}_{}'.format('subject_refusal_reason', survey.survey_abbrev.lower()), None)
            try:
                setattr(self, '{}_{}'.format('member_refused', survey.survey_abbrev.lower()),
                        self.household_membership_survey.get(survey.survey_slug).refused)
            except AttributeError:
                setattr(self, '{}_{}'.format('member_refused', survey.survey_abbrev.lower()), None)

    def update_absentee(self):
        """Set attributes related to member absenteeism, if relevant."""
        fieldattrs = [('report_datetime', 'member_absent_date'),
                      ('absent', 'member_absent')]
        model_cls = SubjectAbsenteeEntry
        for survey in Survey.objects.all():
            subject_absentee_entry = self._update(
                survey.survey_abbrev, fieldattrs, model_cls,
                'subject_absentee__household_member',
                self.household_membership_survey.get(survey.survey_slug)
                )
            try:
                setattr(self, '{}_{}'.format('member_absent_reason', survey.survey_abbrev.lower()),
                        subject_absentee_entry.reason_other if not subject_absentee_entry.reason.upper() == 'OTHER' else subject_absentee_entry.reason_other)
            except AttributeError:
                setattr(self, '{}_{}'.format('member_absent_reason', survey.survey_abbrev.lower()), None)

    @property
    def data_errors(self):
        """Checks for known data error conditions and returns error messages as a dictionary."""
        data_errors = {'member_status': [], 'enumeration_date': [],
                       'household_status': [], 'consented': [],
                       'household_log': []}
        # 1. test if only uses current HOUSEHOLD_STATUS options
        condition = list(set(
            [item for item in self.household_log_status if item not in [tpl[0] for tpl in HOUSEHOLD_STATUS]]
            ))
        if condition:
            data_errors['household_status'].append(
                'Invalid household status options in {}. Got {}'.format(self.community, condition))
        # 2. confirm is_consented agrees with SubjectConsent
        try:
            SubjectConsent.objects.get(household_member=self.household_member)
            consented = True
        except SubjectConsent.DoesNotExist:
            consented = False
        if self.member_consented != consented:
            data_errors['consented'].append(
                'household_member.is_consented should be \'{0!r}\' in {1!r}'.format(consented, self.community))
        if self.member_consented and self.member_status not in [BHS, ANNUAL]:
            data_errors['consented'].append(
                'member_status should be {0!r} for consented member in {1!r}.'.format(BHS, self.community))
        # 3.enumeration date must me in the log
        if self.enumeration_date not in self.household_log_date:
            data_errors['enumeration_date'].append(
                'enumeration date does not match a household log '
                'report date in {}, self.community'.format(self.community))
        # 4. member_status and consented
        if self.member_status == BHS and not self.member_consented:
            data_errors['member_status'].append(
                'not consented but member_status is {} in {}'.format(BHS, self.community))
        if self.member_status != BHS and self.member_consented:
            data_errors['member_status'].append(
                'consented but member_status is {} in {}'.format(BHS, self.community))
        # 5. member_status and survey date
        if self.member_status == UNDECIDED and self.member_survey.end_date < date.today():
            data_errors['member_status'].append(
                'member_status cannot be {} for completed {} survey in {}.'.format(
                    UNDECIDED, self.member_survey.name, self.community))
        # log status valid for enumeration
        if ELIGIBLE_REPRESENTATIVE_PRESENT not in self.household_log_status:
            data_errors['household_log'].append('Members enumerated but no valid log entry.')
        self._data_errors = copy(data_errors)
        for k, v in data_errors.iteritems():
            if not v:
                del self._data_errors[k]
        return self._data_errors
