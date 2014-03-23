from datetime import datetime

from django.db import models

from ..constants import  ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, BHS_LOSS, HTC, HTC_ELIGIBLE, NOT_ELIGIBLE, NOT_REPORTED, REFUSED, UNDECIDED, REFUSED_HTC


class HouseholdMemberHelper(object):

    def __init__(self, household_member=None):
        self._member_status_absent = None
        self._member_status_htc = None
        self._member_status_refused = None
        self._member_status_undecided = None
        self._member_status_enrollment_loss = False
        self.household_member = household_member
        self._reported = None

    def __repr__(self):
        return 'HouseholdMemberHelper({0.household_member!r})'.format(self)

    def __str__(self):
        return '({0.household_member!r})'.format(self)

    @property
    def reported(self):
        """Returns True if there is some report on this member (e.g. absent, undecided, refused, consented)"""
        if self.member_status_absent or self.member_status_refused or self.member_status_undecided or self.member_status_consented:
            return True
        return False

    @property
    def htc_adult(self):
        return self.household_member.age_in_years >= 18

    @property
    def htc_minor(self):
        return self.household_member.is_minor

    @property
    def household_enrolled(self):
        return self.household_member.household_structure.enrolled

    @property
    def member_status(self):
        return self.member_status_absent or self.member_status_htc or self.member_status_enrollment_loss or self.member_status_refused or self.member_status_undecided

    @property
    def member_status_htc(self, is_status):
        """Returns the current member status as HTC ELIGIBLE or HTC or None."""
        if is_status and self.eligible_htc:
            return HTC_ELIGIBLE
        return None

    @property
    def member_status_absent(self):
        """Returns the current member status as absent or None."""
        return self._member_status_absent

    @member_status_absent.setter
    def member_status_absent(self, is_absent):
        self._member_status_absent = None
        SubjectAbsentee = models.get_model('bcpp_household_member', 'SubjectAbsentee')
        SubjectAbsenteeEntry = models.get_model('bcpp_household_member', 'SubjectAbsenteeEntry')
        if is_absent:
            self.subject_status_factory('SubjectAbsentee', ABSENT)
            self._member_status_absent = ABSENT
            self.member_status_undecided = False
            self.member_status_refused = False
            self.member_status_enrollment_loss = False
            self.member_status_htc = False
        else:
            if not SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member=self.household_member).exists():
                SubjectAbsentee.objects.filter(household_member=self.household_member).delete()

    @property
    def member_status_undecided(self):
        """Returns the current member status as undecided or None."""
        return self._member_status_undecided

    @member_status_undecided.setter
    def member_status_undecided(self, is_undecided):
        self._member_status_undecided = None
        SubjectUndecided = models.get_model('bcpp_household_member', 'SubjectUndecided')
        SubjectUndecidedEntry = models.get_model('bcpp_household_member', 'SubjectUndecidedEntry')
        if is_undecided:
            self.subject_status_factory('SubjectUndecided', UNDECIDED)
            self._member_status_undecided = UNDECIDED
            self.member_status_absent = False
            self.member_status_refused = False
            self.member_status_enrollment_loss = False
            self.member_status_htc = False
        else:
            if not SubjectUndecidedEntry.objects.filter(subject_undecided__household_member=self.household_member).exists():
                SubjectUndecided.objects.filter(household_member=self.household_member).delete()

    @property
    def member_status_refused(self):
        """Returns the current member status as undecided or None."""
        return self._member_status_refused

    @member_status_refused.setter
    def member_status_refused(self, is_status):
        """Returns the current member status as refused or None."""
        self._member_status_refused = None
        if is_status:
            if self.refused:
                self._member_status_refused = REFUSED
                self.member_status_undecided = False
                self.member_status_absent = False
                self.member_status_enrollment_loss = False
                self.member_status_htc = False
        return self._member_status_refused

    @property
    def member_status_enrollment_loss(self):
        """Returns the current member status as enrollment to BHS loss or None.

        household_member.bhs_loss is set in the Enrollment Loss save method.

        Screening loss implies the subject failed eligibility to BHS when completing the enrollment checklist."""
        return self._member_status_enrollment_loss

    @member_status_enrollment_loss.setter
    def member_status_enrollment_loss(self, is_member_status_enrollment_loss):
        self._member_status_enrollment_loss = None
        if is_member_status_enrollment_loss:
            if self.household_member.bhs_loss:
                self._member_status_enrollment_loss = BHS_LOSS
            self.member_status_absent = False
            self.member_status_undecided = False
            self._member_status_refused = False

    @property
    def member_status_consented(self):
        if self.consented:
            return BHS
        return None

    @property
    def consented(self):
        """Returns True if the subject has consented.
 
        ..note:: if the subject consent is in the process of being saved this will return False
                 while household_member.is_consented will be True. Attribute household_member.is_consented
                 is set to True in the subject_consent save method. """
        SubjectConsent = models.get_model('bcpp_subject', 'SubjectConsent')
        return SubjectConsent.objects.filter(household_member=self).exists()

    @property
    def consenting(self):
        """Returns True if the subject is consenting (you are in the subkject consent save method).

        ..note:: if the subject consent is in the process of being saved self.consented will return False and
                this method will return True as household_member.is_consented=True. Attribute household_member.is_consented
                is set to True in the subject_consent save method. """
        return not self.consented and self.household_member.is_consented

    @property
    def eligible_htc(self):
        """Returns True if subject is eligible for HTC.

        Subject is eligible for HTC if the household is enrolled and the subject:
            1. is not eligible for BHS based on age and/or residency (eligible_member)
            2. is an eligible_member but refuses before eligibility
            3. is an eligible_member and refuses after passing eligibility
            4. is an eligible_member and fails eligibility and completes the loss form."""
        self._eligible_htc = False
        if not self.consented:
            if self.household_enrolled:
                if self.household_member.age_in_years > 64:
                    self._eligible_htc = True
                elif not self.eligible_member and self.household_member.age_in_years >= 16:
                    self._eligible_htc = True
                elif self.eligible_member:
                    if not self.enrollment_checklist_completed and self.refused:
                        self._eligible_htc = True
                    elif self.enrollment_checklist_completed and not self.eligible_subject and self.member_status_member_status_consented:
                        self._eligible_htc = True
                    elif self.enrollment_checklist_completed and self.eligible_subject and self.refused:
                        self._eligible_htc = True
                    else:
                        pass
                elif not self.eligible_subject and self.enrollment_checklist_completed:
                    self._eligible_htc = True
                else:
                    pass
        return self._eligible_htc

    @property
    def eligible_member(self):
        return ((self.household_member.is_minor or self.household_member.is_adult) and self.household_member.study_resident == 'Yes')

    @property
    def eligible_subject(self):
        """Returns True if subject is eligible as determined by passing the eligibility criteria in the enrollment checklist.

        This is set by the enrollment checklist save method."""
        return self.household_member.eligible_subject

    @property
    def enrollment_checklist_completed(self):
        """Returns True if subject has completed the enrollment checklist.

        This is set by the enrollment checklist save method."""
        return self.household_member.enrollment_checklist_completed

    @property
    def enrollment_loss_completed(self):
        """Returns True if subject has completed the enrollment loss.

        This is set by the enrollment loss save method."""
        return self.household_member.enrollment_loss_completed

    @property
    def refused(self):
        """Returns True if subject refused BHS.

        This is set by the subject_refusal save method."""
        return self.household_member.refused

    @property
    def present_today(self):
        return self.household_member.present_today

    def calculate_member_status_with_hint(self, member_status_hint):
        """Updates the member status from the save method using a "hint" or value passed on from the model instance being saved."""
        if self.consenting or self.consented:
            member_status = BHS
        elif not self.reported and self.household_member.present_today == 'No':
            self.member_status_absent = True
            member_status = self.member_status
        else:
            member_status = None
            if member_status_hint:
                if member_status_hint == ABSENT:
                    self.member_status_absent = True
                elif member_status_hint == UNDECIDED:
                    self.member_status_undecided = True
                elif member_status_hint == REFUSED:
                    self.member_status_refused = True
                elif member_status_hint == NOT_REPORTED:
                    member_status = self.household_member.__class__.objects.get(pk=self.household_member.pk).member_status
                elif member_status_hint == HTC_ELIGIBLE:
                    self.member_status_htc = True
                elif member_status_hint == HTC:
                    if self.eligible_member and self.eligible_htc and (self.refused or not self.eligible_subject):
                        member_status = HTC
                else:
                    pass
        if not member_status:
            member_status = self.calculate_member_status_without_hint()
        return member_status

    def calculate_member_status_without_hint(self):
        member_status = None
        if self.consenting or self.consented:
            member_status = BHS
        else:
            if self.eligible_subject and not self.refused:
                member_status = BHS_ELIGIBLE
            elif self.eligible_subject and self.refused and self.eligible_htc:
                member_status = HTC_ELIGIBLE
            elif self.eligible_member and not self.eligible_subject and not self.enrollment_checklist_completed and self.refused:
                member_status = HTC_ELIGIBLE
            elif self.eligible_member and not self.eligible_subject and not self.enrollment_checklist_completed:
                member_status = BHS_SCREEN
            elif self.eligible_member and not self.eligible_subject and self.enrollment_checklist_completed and not self.eligible_htc:
                member_status = NOT_ELIGIBLE
            elif self.eligible_member and not self.eligible_subject and self.enrollment_checklist_completed and self.eligible_htc:
                member_status = HTC_ELIGIBLE
            elif self.eligible_htc and self.refused:
                member_status = HTC_ELIGIBLE
            elif not self.eligible_member and self.eligible_htc:
                member_status = HTC_ELIGIBLE
            elif not self.eligible_member and not self.eligible_htc:
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
        if self.consented:
            # consent overrides everything
            options = [BHS]
        else:
            if ((not self.eligible_member or not self.eligible_subject) and not self.eligible_htc):
                options = [NOT_ELIGIBLE]
            elif ((not self.eligible_member or not self.eligible_subject) and self.eligible_htc):
                options = [HTC_ELIGIBLE, HTC, REFUSED_HTC]
            elif self.eligible_member:
                options = [ABSENT, BHS_SCREEN, BHS_ELIGIBLE, BHS, UNDECIDED, REFUSED, BHS_LOSS, HTC_ELIGIBLE, HTC, REFUSED_HTC]
                if self.eligible_subject or self.refused:
                    options.remove(ABSENT)
                    options.remove(UNDECIDED)
                    options.remove(BHS_LOSS)
                if self.eligible_subject or self.enrollment_checklist_completed:
                    options.remove(BHS_SCREEN)
                if self.enrollment_loss_completed or not self.eligible_subject:
                    options.remove(BHS_ELIGIBLE)
                    options.remove(BHS)
                if not self.eligible_htc:
                    options.remove(HTC_ELIGIBLE)
                    options.remove(HTC)
                    options.remove(REFUSED_HTC)
            else:
                raise TypeError('ERROR: household_member.refused={0},self.household_member.eligible_htc={1},self.household_member.eligible_member={2} '
                'should never occur together'.format(self.refused, self.eligible_htc, self.eligible_member))
        # append the current member_status
        options.append(self.household_member.member_status)
        # sort and remove duplicates
        options = list(set(options))
        options.sort()
        return [(item, item) for item in options]
