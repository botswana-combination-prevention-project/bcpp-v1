from datetime import datetime

from django.db import models

from ..constants import  ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, BHS_LOSS, HTC, HTC_ELIGIBLE, NOT_ELIGIBLE, NOT_REPORTED, REFUSED, UNDECIDED, REFUSED_HTC


class HouseholdMemberHelper(object):

    def __init__(self):
        self._subject_absentee = None
        self._subject_htc = None
        self._subject_refused = None
        self._subject_undecided = None
        self._enrollment_loss = False
        self.household_member = None
        self._reported = None

    @property
    def reported(self):
        """Returns True if there is some report on this member (e.g. absent, undecided, refused, consented)"""
        if self.subject_absentee or self.subject_refused or self.subject_undecided or self.subject_consented:
            return True
        return False

    @property
    def is_htc_adult(self):
        return self.household_member.age_in_years >= 18

    @property
    def subject_htc(self):
        return self._subject_htc

    @subject_htc.setter
    def subject_htc(self, is_htc):
        """Returns the current member status as HTC eligible or HTC or None."""
        self._subject_htc = None
        if is_htc:
            if not self.household_member.eligible_member and self.household_member.eligible_htc and self.household_member.household_structure.enrolled:
                if (self.household_member.is_minor or self.household_member.is_adult) and self.household_member.refused:
                    self._subject_htc = HTC_ELIGIBLE
                if self.is_htc_adult > 64:
                    self._subject_htc = HTC_ELIGIBLE

    @property
    def subject_absentee(self):
        """Returns the current member status as absent or None."""
        return self._subject_absentee

    @subject_absentee.setter
    def subject_absentee(self, is_absent):
        self._subject_absentee = None
        SubjectAbsentee = models.get_model('bcpp_household_member', 'SubjectAbsentee')
        SubjectAbsenteeEntry = models.get_model('bcpp_household_member', 'SubjectAbsenteeEntry')
        if is_absent:
            self.subject_status_factory('SubjectAbsentee', ABSENT)
            self._subject_absentee = ABSENT
            self.subject_undecided = False
            self.subject_refused = False
            self.enrollment_loss = False
        else:
            if not SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member=self.household_member).exists():
                SubjectAbsentee.objects.filter(household_member=self.household_member).delete()

    @property
    def subject_undecided(self):
        """Returns the current member status as undecided or None."""
        return self._subject_undecided

    @subject_undecided.setter
    def subject_undecided(self, is_undecided):
        self._subject_undecided = None
        SubjectUndecided = models.get_model('bcpp_household_member', 'SubjectUndecided')
        SubjectUndecidedEntry = models.get_model('bcpp_household_member', 'SubjectUndecidedEntry')
        if is_undecided:
            self.subject_status_factory('SubjectUndecided', UNDECIDED)
            self._subject_undecided = UNDECIDED
            self.subject_absentee = False
            self.subject_refused = False
            self.enrollment_loss = False
        else:
            if not SubjectUndecidedEntry.objects.filter(subject_undecided__household_member=self.household_member).exists():
                SubjectUndecided.objects.filter(household_member=self.household_member).delete()

    @property
    def subject_refused(self):
        """Returns the current member status as refused or None."""
        return self._subject_refused

    @subject_refused.setter
    def subject_refused(self, is_refused):
        self._subject_refused = None
        if is_refused:
            if not self.household_member.refused:
                self._subject_refused = REFUSED
            self.subject_absentee = False
            self.subject_undecided = False
            self.enrollment_loss = False

    @property
    def enrollment_loss(self):
        """Returns the current member status as enrollment to BHS loss or None.

        Screening loss implies the subject failed eligibility to BHS when completing the enrollment checklist."""
        return self._enrollment_loss

    @enrollment_loss.setter
    def enrollment_loss(self, is_enrollment_loss):
        self._enrollment_loss = None
        if is_enrollment_loss:
            if self.household_member.bhs_loss:
                self._enrollment_loss = BHS_LOSS
            self.subject_absentee = False
            self.subject_undecided = False
            self._subject_refused = False

    @property
    def subject_consented(self):
        if self.consented:
            return BHS
        return None

    @property
    def consented(self):
        """Returns True if the subject has consented.

        ..note:: if the subject consent is in the process of being saved this will return False
                 while household_member.is_consented will be True. """
        SubjectConsent = models.get_model('bcpp_subject', 'SubjectConsent')
        return SubjectConsent.objects.filter(household_member=self).exists()

    @property
    def eligible_htc(self):
        """Returns True if subject is eligible for HTC.

        Subject is eligible for HTC if the household is enrolled and the subject:
            1. is not eligible for BHS based on age and/or residency (eligible_member)
            2. is an eligible_member but refuses before eligibility
            3. is an eligible_member and refuses after passing eligibility
            4. is an eligible_member and fails eligibility and completes the loss form."""
        self._eligible_htc = False
        if not self.household_member.is_consented:
            if self.household_member.household_structure.enrolled:
                if not self.household_member.eligible_member:
                    self._eligible_htc = True
                if self.household_member.eligible_member and not self.household_member.enrollment_checklist_completed:
                    self.household_member.eligible_htc = self.household_member.refused
                if self.household_member.eligible_member and self.household_member.enrollment_checklist_completed and self.household_member.bhs_loss:
                    self.household_member.eligible_htc = self.household_member.refused
                elif not self.household_member.eligible_subject and self.household_member.enrollment_checklist_completed:
                    self.household_member.eligible_htc = True
                else:
                    self.household_member.eligible_htc = (self.household_member.age_in_years >= 16)

    def calculate_new_member_status(self):
        """Updates the member status from the post-save signal for new household_members."""
        member_status = NOT_REPORTED
        if not self.household_member.eligible_member and not self.household_member.eligible_htc:
            member_status = NOT_ELIGIBLE
        elif not self.household_member.eligible_member and self.household_member.eligible_htc:
            member_status = HTC_ELIGIBLE
        else:
            if self.household_member.present_today == 'No':
                self.subject_absentee = True
                member_status = self.subject_absentee
        if not member_status:
            member_status = self.calculate_member_status_without_hint()
        return member_status

    def calculate_member_status_with_hint(self, member_status_hint):
        """Updates the member status from the save method using a "hint" or value passed on from the model instance being saved."""
        if self.household_member.is_consented:
            member_status = BHS
        else:
            member_status = None
            if member_status_hint == ABSENT:
                self.subject_absentee = True
                member_status = self.subject_absentee
            elif member_status_hint == UNDECIDED:
                self.subject_undecided = True
                member_status = self.subject_undecided
            elif member_status_hint == REFUSED:
                self.subject_refused = True
                member_status = self.subject_refused
            elif member_status_hint == NOT_REPORTED:
                member_status = self.household_member.__class__.objects.get(pk=self.household_member.pk).member_status
            elif member_status_hint == HTC_ELIGIBLE:
                self.subject_htc = True
                member_status = self.subject_htc
            elif member_status_hint == HTC:
                if self.household_member.eligible_member and self.household_member.eligible_htc and (self.household_member.refused or not self.household_member.eligible_subject):
                    member_status = HTC
            else:
                pass
        if not member_status:
            member_status = self.calculate_member_status_without_hint()
        return member_status

    def calculate_member_status_without_hint(self):
        member_status = None
        if self.household_member.is_consented:
            member_status = BHS
        else:
            if self.household_member.eligible_subject and not self.household_member.refused:
                member_status = BHS_ELIGIBLE
            elif self.household_member.eligible_subject and self.household_member.refused and self.household_member.eligible_htc:
                member_status = HTC_ELIGIBLE
            elif self.household_member.eligible_member and not self.household_member.eligible_subject and not self.household_member.enrollment_checklist_completed and self.household_member.refused:
                member_status = HTC_ELIGIBLE
            elif self.household_member.eligible_member and not self.household_member.eligible_subject and not self.household_member.enrollment_checklist_completed:
                member_status = BHS_SCREEN
            elif self.household_member.eligible_member and not self.household_member.eligible_subject and self.household_member.enrollment_checklist_completed and not self.household_member.eligible_htc:
                member_status = NOT_ELIGIBLE
            elif self.household_member.eligible_member and not self.household_member.eligible_subject and self.household_member.enrollment_checklist_completed and self.household_member.eligible_htc:
                member_status = HTC_ELIGIBLE
            elif self.household_member.eligible_htc and self.household_member.refused:
                member_status = HTC_ELIGIBLE
            elif not self.household_member.eligible_member and self.household_member.eligible_htc:
                member_status = HTC_ELIGIBLE
            elif not self.household_member.eligible_member and not self.household_member.eligible_htc:
                member_status = NOT_ELIGIBLE
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

    @property
    def member_status_choices(self):
        if not self.household_member.member_status:
            raise TypeError('household_member.member_status cannot be None')
        options = []
        if self.household_member.is_consented:
            # consent overrides everything
            options = [BHS]
        else:
            if ((not self.household_member.eligible_member or not self.household_member.eligible_subject)
                and not self.household_member.eligible_htc):
                options = [NOT_ELIGIBLE]
            elif self.household_member.eligible_member and self.household_member.eligible_subject:
                options = [ABSENT, BHS_ELIGIBLE, UNDECIDED, REFUSED]
            elif ((not self.household_member.eligible_member or not self.household_member.eligible_subject)
                  and self.household_member.eligible_htc):  # TODO: are any of the first two values are implied by the third?
                options = [HTC_ELIGIBLE, HTC, REFUSED_HTC]
            elif (self.household_member.eligible_member and not self.household_member.enrollment_checklist_completed
                  and not self.household_member.refused):
                options = [ABSENT, BHS_SCREEN, UNDECIDED, REFUSED]
            elif self.household_member.refused and not self.household_member.eligible_htc:
                options = [REFUSED, BHS_SCREEN]
            elif self.household_member.refused and self.household_member.eligible_htc:
                options = [BHS_SCREEN, HTC_ELIGIBLE, HTC, REFUSED_HTC]
            else:
                raise TypeError('ERROR: household_member.refused={0},self.household_member.eligible_htc={1},self.household_member.eligible_member={2} '
                'should never occur together'.format(self.household_member.refused, self.household_member.eligible_htc, self.household_member.eligible_member))
        # append the current member_status
        options.append(self.household_member.member_status)
        # sort and remove duplicates
        options = list(set(options))
        options.sort()
        return [(item, item) for item in options]
