from datetime import datetime

from django.db import models

from ..constants import  ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, HTC, HTC_ELIGIBLE, NOT_ELIGIBLE, NOT_REPORTED, REFUSED, UNDECIDED


class HouseholdMemberHelper(object):

    def __init__(self):
        self._subject_absentee = None
        self._subject_htc = None
        self._subject_refused = None
        self._subject_undecided = None
        self.household_member = None

    @property
    def is_htc_adult(self):
        return self.household_member.age_in_years >= 18

    @property
    def subject_htc(self):
        return self._subject_htc

    @subject_htc.setter
    def subject_htc(self, is_htc):
        if is_htc:
            if not self.household_member.eligible_member and self.household_member.eligible_htc and self.household_member.household_structure.enrolled:
                if (self.household_member.is_minor or self.household_member.is_adult) and self.household_member.refused:
                    self._subject_htc = HTC_ELIGIBLE
                if self.is_htc_adult > 64:
                    self._subject_htc = HTC_ELIGIBLE
        else:
            self._subject_htc = None

    @property
    def subject_absentee(self):
        return self._subject_absentee

    @subject_absentee.setter
    def subject_absentee(self, is_absent):
        SubjectAbsentee = models.get_model('bcpp_household_member', 'SubjectAbsentee')
        SubjectAbsenteeEntry = models.get_model('bcpp_household_member', 'SubjectAbsenteeEntry')
        if is_absent:
            self.subject_status_factory('SubjectAbsentee', ABSENT)
            self._subject_absentee = ABSENT
            self.subject_undecided = False
            self.subject_refused = False
            self.household_member.reported = True
        else:
            if not SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member=self.household_member).exists():
                SubjectAbsentee.objects.filter(household_member=self.household_member).delete()
            self._subject_absentee = None

    @property
    def subject_undecided(self):
        return self._subject_undecided

    @subject_undecided.setter
    def subject_undecided(self, is_undecided):
        SubjectUndecided = models.get_model('bcpp_household_member', 'SubjectUndecided')
        SubjectUndecidedEntry = models.get_model('bcpp_household_member', 'SubjectUndecidedEntry')
        if is_undecided:
            self.subject_status_factory('SubjectUndecided', UNDECIDED)
            self._subject_undecided = UNDECIDED
            self.subject_absentee = False
            self.subject_refused = False
            self.household_member.reported = True
        else:
            if not SubjectUndecidedEntry.objects.filter(subject_undecided__household_member=self.household_member).exists():
                SubjectUndecided.objects.filter(household_member=self.household_member).delete()
            self._subject_undecided = None

    @property
    def subject_refused(self):
        return self._subject_refused

    @subject_refused.setter
    def subject_refused(self, is_refused):
        if is_refused:
            self._subject_refused = REFUSED
            self.subject_absentee = False
            self.subject_undecided = False

    @property
    def consented(self):
        SubjectConsent = models.get_model('bcpp_subject', 'SubjectConsent')
        self.household_member.is_consented = SubjectConsent.objects.filter(household_member=self).count() == 1
        return self.household_member.is_consented

    def calculate_member_status(self, exception_cls=None):
        """Updates the member status."""
        if not self.household_member.id:
            member_status = NOT_REPORTED
            if not self.household_member.eligible_member and not self.household_member.eligible_htc:
                member_status = NOT_ELIGIBLE
            elif not self.household_member.eligible_member and self.household_member.eligible_htc:
                member_status = HTC_ELIGIBLE
            else:
                if self.household_member.present_today == 'No':
                    self.subject_absentee = True
                    member_status = self.subject_absentee
        else:
            if self.consented:
                member_status = BHS
            else:
                # does the proposed member_status in the instance verify?
                member_status = None
                if self.household_member.member_status == ABSENT:
                    self.subject_absentee = True
                    member_status = self.subject_absentee
                elif self.household_member.member_status == UNDECIDED:
                    self.subject_undecided = True
                    member_status = self.subject_undecided
                elif self.household_member.member_status == REFUSED:
                    self.subject_refused = True
                    member_status = self.subject_refused
                elif self.household_member.member_status == NOT_REPORTED:
                    member_status = self.household_member.__class__.objects.get(pk=self.household_member.pk).member_status
                elif self.household_member.member_status == NOT_ELIGIBLE:
                    member_status = self.household_member.__class__.objects.get(pk=self.household_member.pk).member_status
                    if self.household_member.eligible_member or self.household_member.reported:
                        member_status = self.__class__.objects.get(pk=self.household_member.pk).member_status
                elif self.household_member.member_status == HTC_ELIGIBLE:
                    self.subject_htc = True
                    member_status = self.subject_htc
                elif self.household_member.member_status == HTC:
                    if self.household_member.eligible_member and self.household_member.eligible_htc and (self.household_member.refused or not self.household_member.eligible_subject):
                        member_status = HTC
#                 if not old_instance.visit_attempts < 3:
#                     #Allowed to change to member status only if visit attempts are less than 3.
#                     raise ValidationError('Invalid member status change. Visit attempts not less than 3. Got {}'.format(old_instance.visit_attempts))
                else:
                    pass
        # the proposed member_status does not verify, so try to calculate one.
        if not member_status:
            if self.household_member.eligible_subject:
                member_status = BHS_ELIGIBLE
            elif self.household_member.eligible_member and not self.household_member.eligible_subject:
                member_status = BHS_SCREEN
            elif self.household_member.eligible_htc and self.household_member.age_in_years >= 16 and self.household_member.refused and self.household_member.household_structure.enrolled:
                member_status = HTC_ELIGIBLE
            elif self.household_member.eligible_htc and not self.household_member.eligible_member and self.household_member.age_in_years >= 16:
                member_status = HTC_ELIGIBLE
            else:
                pass
        return member_status

    def subject_status_factory(self, model_string, member_status):
        """Returns an instance of the specified subject status model and creates one if it does not exist."""
        if model_string not in ['SubjectAbsentee', 'SubjectUndecided']:
            raise TypeError('Invalid subject status model for this factory. Got {0}'.format(model_string))
        instance = None
        model_cls = models.get_model('bcpp_household_member', model_string)
        try:
            instance = model_cls.objects.get(household_member=self.household_member)
        except model_cls.DoesNotExist:
            if self.household_member.member_status == member_status:
                instance = model_cls.objects.create(
                    report_datetime=datetime.today(),
                    registered_subject=self.household_member.registered_subject,
                    household_member=self.household_member,
                    survey=self.household_member.household_structure.survey,
                    )
        return instance
