from datetime import datetime

from django.db import models

from ..constants import  ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, HTC, HTC_ELIGIBLE, NOT_ELIGIBLE, NOT_REPORTED, REFUSED, UNDECIDED, REFUSED_HTC


class HouseholdMemberHelper(object):

    def __init__(self):
        self._subject_absentee = None
        self._subject_htc = None
        self._subject_refused = None
        self._subject_undecided = None
        self.household_member = None
        self.reported = False

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
            self.reported = True
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
            self.reported = True
        else:
            if not SubjectUndecidedEntry.objects.filter(subject_undecided__household_member=self.household_member).exists():
                SubjectUndecided.objects.filter(household_member=self.household_member).delete()
            self._subject_undecided = None

    @property
    def subject_refused(self):
        return self._subject_refused

    @subject_refused.setter
    def subject_refused(self, is_refused):
        self._subject_refused = None
        if is_refused:
            if not self.household_member.refused:
                self._subject_refused = REFUSED
            self.subject_absentee = False
            self.subject_undecided = False

    @property
    def consented(self):
        """Returns True if the subject has consented.

        ..note:: if the subject consent is in the process of being saved this will return False
                 while household_member.is_consented will be True. """
        SubjectConsent = models.get_model('bcpp_subject', 'SubjectConsent')
        return SubjectConsent.objects.filter(household_member=self).count() == 1

    def calculate_new_member_status(self, exception_cls=None):
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
            member_status = self.calculate_member_status_without_hint(exception_cls)
        return member_status

    def calculate_member_status_with_hint(self, member_status_hint, exception_cls=None):
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
            member_status = self.calculate_member_status_without_hint(exception_cls)
        return member_status

    def calculate_member_status_without_hint(self, exception_cls=None):
        member_status = None
        if self.household_member.is_consented:
            member_status = BHS
        else:
            if self.household_member.eligible_subject and not self.household_member.refused:
                member_status = BHS_ELIGIBLE
            elif self.household_member.eligible_subject and self.household_member.refused and self.household_member.eligible_htc:
                member_status = HTC_ELIGIBLE
            elif self.household_member.eligible_member and not self.household_member.eligible_subject and not self.household_member.eligibility_checklist_filled and self.household_member.refused:
                member_status = HTC_ELIGIBLE
            elif self.household_member.eligible_member and not self.household_member.eligible_subject and not self.household_member.eligibility_checklist_filled:
                member_status = BHS_SCREEN
            elif self.household_member.eligible_member and not self.household_member.eligible_subject and self.household_member.eligibility_checklist_filled and not self.household_member.eligible_htc:
                member_status = NOT_ELIGIBLE
            elif self.household_member.eligible_member and not self.household_member.eligible_subject and self.household_member.eligibility_checklist_filled and self.household_member.eligible_htc:
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
            # BHS options
#             if self.household_member.eligible_member:
#                 options += [ABSENT, BHS_SCREEN, UNDECIDED, REFUSED]
#             if self.household_member.eligible_subject:
#                 options.remove(BHS_SCREEN)
#                 options += [ABSENT, BHS_ELIGIBLE, UNDECIDED, REFUSED]
#             if self.household_member.refused:
#                 options.remove(UNDECIDED)
#                 options.remove(ABSENT)
#                 options.append(REFUSED)
#             # HTC options
#             if self.household_member.eligible_htc:
#                 options += [HTC, REFUSED_HTC]
            if ((not self.household_member.eligible_member or self.household_member.eligible_subject is False) 
                and not self.household_member.eligible_htc):
                #younger than 16, older than 64, not a study resident
                #Initially BHS Potential, Failed eligibility checklist
                #Not eligible for HTC
                options = [NOT_ELIGIBLE]
            elif self.household_member.eligible_member and self.household_member.eligible_subject is True:
                #BHS potential, has filled eligibility checklist and passed it.
                options = [ABSENT, BHS_ELIGIBLE, UNDECIDED, REFUSED]
            elif ((not self.household_member.eligible_member or self.household_member.eligible_subject is False) 
                  and self.household_member.eligible_htc):
                #Older than 64 and now eligible for HTC
                #Initially BHS Potential, Failed eligibility checklist and now eligible for HTC
                options = [HTC_ELIGIBLE, HTC, REFUSED_HTC]
            elif (self.household_member.eligible_member and self.household_member.eligible_subject is None
                  and not self.household_member.refused):
                #BHS potential, has not filled eligibility checklist yet, and has not officially refused BHS
                #Could be ABSENT/UNDECIDED
                options = [ABSENT, BHS_SCREEN, UNDECIDED, REFUSED]
            elif self.household_member.refused and not self.household_member.eligible_htc:
                #A refusal that is not yet eligible for HTC
                options = [REFUSED, BHS_SCREEN]
            elif self.household_member.refused and self.household_member.eligible_htc:
                #A refusal that is now eligible for HTC, dont wana have REFUSED in there, now its only about HTC
                options = [BHS_SCREEN, HTC_ELIGIBLE, HTC, REFUSED_HTC]
            else:
                raise TypeError('ERROR: household_member.refused={0},self.household_member.eligible_htc={1},self.household_member.eligible_member={2} '
                'should never occur together'.format(self.household_member.refused, self.household_member.eligible_htc, self.household_member.eligible_member))
#             if self.household_member.refused:
#                 options.remove(UNDECIDED)
#                 options.remove(ABSENT)
#                 options.append(REFUSED)
#             # HTC options
#             if self.household_member.eligible_htc:
#                 options += [HTC, REFUSED_HTC]
        # append the current member_status
        options.append(self.household_member.member_status)
        # sort and remove duplicates
        options = list(set(options))
        options.sort()
        return [(item, item) for item in options]
