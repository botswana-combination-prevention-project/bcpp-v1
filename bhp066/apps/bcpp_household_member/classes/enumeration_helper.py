from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.db import models

from edc.constants import UNKNOWN

from ..exceptions import SurveyValueError, HouseholdStructureNotEnrolled

from ..constants import ANNUAL, BHS


class EnumerationHelper(object):

    def __init__(self, household, source_survey, target_survey):
        self._consented_member = None
        self.subject_consent = None
        self.household = household
        self.source_survey = source_survey
        self.target_survey = target_survey
        HouseholdStructure = models.get_model('bcpp_household', 'HouseholdStructure')
        if source_survey.survey_slug == target_survey.survey_slug:
            raise SurveyValueError('Source survey and target survey may not be the same.')
        try:
            self.source_household_structure = HouseholdStructure.objects.get(
                household=household, survey=source_survey, enumerated=True, enrolled=True)
        except HouseholdStructure.DoesNotExist:
            raise HouseholdStructureNotEnrolled(
                'Enrolled and enumerated household structure {} {} does not exist.'.format(
                    self.household, self.source_survey))
        try:
            self.target_household_structure = HouseholdStructure.objects.get(
                household=household,
                survey=target_survey)
        except HouseholdStructure.DoesNotExist:
            raise HouseholdStructure.DoesNotExist(
                'household structure {} {} does not exist.'.format(self.household, self.target_survey))

    def add_members_from_survey(self):
        """Import members from a previous household_structure into the current.

        The source HouseholdStructure must be enrolled into BHS and the target household structure
        cannot be enumerated. """
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        created = 0
        if self.consented_member:
            for household_member in HouseholdMember.objects.filter(
                    household_structure=self.source_household_structure):
                try:
                    household_member = HouseholdMember.objects.get(
                        internal_identifier=household_member.internal_identifier,
                        household_structure=self.target_household_structure)
                except HouseholdMember.DoesNotExist:
                    self.create_member_on_target(household_member)
                    created += 1

            try:
                # once enrolled, the household is considered enrolled for future surveys as well
                self.target_household_structure.enrolled = self.source_household_structure.enrolled
                self.target_household_structure.enrolled_datetime = self.source_household_structure.enrolled_datetime
                self.target_household_structure.enrolled_household_member = \
                    self.source_household_structure.enrolled_household_member
                # self.target_household_structure.enumerated = False
                self.target_household_structure.save(
                    update_fields=['enrolled_household_member', 'enrolled_datetime', 'enrolled'])
            except AttributeError:
                pass  # self.xxxxxx_household_structure is None
        total = HouseholdMember.objects.filter(household_structure=self.target_household_structure).count()
        return (created, total)

    @property
    def consented_member(self):
        """Returns a household member from the current survey who consented in a previous survey.

        If no one consented, e.g. the household_structure was not enrolled, self._consented_member
        is set to None"""
        if not self._consented_member:
            HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
            SubjectConsent = models.get_model('bcpp_subject', 'SubjectConsent')
            for household_member in HouseholdMember.objects.filter(household_structure=self.source_household_structure):
                try:
                    self.subject_consent = SubjectConsent.objects.get(household_member=household_member)
                    self.add_representative_eligibility()
                    try:
                        self._consented_member = HouseholdMember.objects.get(
                            internal_identifier=household_member.internal_identifier,
                            household_structure=self.target_household_structure)
                    except HouseholdMember.DoesNotExist:
                        self._consented_member = self.create_member_on_target(household_member)
                    self.representative_eligibility.auto_fill_member_id = self._consented_member.pk
                    self.representative_eligibility.save()
                    break
                except SubjectConsent.DoesNotExist:
                    pass
        return self._consented_member

    def add_representative_eligibility(self):
        return self.representative_eligibility

    @property
    def representative_eligibility(self):
        """Returns and if required creates a representative eligibility instance.

        If there is not a consented member in the source household structure, the
        instance will not be created and None is returned. See AttributeError."""
        RepresentativeEligibility = models.get_model('bcpp_household', 'RepresentativeEligibility')
        representative_eligibility = None
        if self.subject_consent:
            try:
                representative_eligibility = RepresentativeEligibility.objects.get(
                    household_structure=self.target_household_structure)
            except RepresentativeEligibility.DoesNotExist:
                representative_eligibility = RepresentativeEligibility.objects.create(
                    household_structure=self.target_household_structure,
                    report_datetime=datetime.today(),
                    aged_over_18='Yes',
                    household_residency='Yes',
                    verbal_script='Yes',
                    auto_filled=True)
            except AttributeError:
                pass
        return representative_eligibility

    def create_member_on_target(self, source_household_member):
        """Creates and returns a new household member on the target household structure
        using the source_household_member as a template.

        If a new household_member is not created returns None

        If 'representative eligibility' does not exist, the household member
        will not be created.
        """
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        SubjectConsent = models.get_model('bcpp_subject', 'SubjectConsent')
        new_household_member = None
        subject_consent = None
        try:
            subject_consent = SubjectConsent.objects.get(household_member=source_household_member)
            age_in_years = relativedelta(date.today(), subject_consent.dob).years
        except SubjectConsent.DoesNotExist:
            age_in_years = source_household_member.age_in_years + 1
        options = dict(
            household_structure=self.target_household_structure,
            registered_subject=source_household_member.registered_subject,
            first_name=source_household_member.first_name,
            initials=source_household_member.initials,
            age_in_years=age_in_years,  # incremented by 1 or based on consent.dob
            gender=source_household_member.gender,
            relation=source_household_member.relation,
            study_resident=source_household_member.study_resident,
            inability_to_participate=source_household_member.inability_to_participate,
            internal_identifier=source_household_member.internal_identifier,
            auto_filled=True,
            updated_after_auto_filled=False,  # will change once the record is edited via ModelAdmin
            survival_status=UNKNOWN,
            hostname_created=source_household_member.hostname_created,  # carried over to help with logistics
            hostname_modified=source_household_member.hostname_modified,  # carried over to help with logistics
            user_created=source_household_member.user_created,  # carried over to help with logistics
            user_modified=source_household_member.user_modified,  # carried over to help with logistics
        )
        try:
            new_household_member = HouseholdMember.objects.create(**options)
            if source_household_member.is_consented:
                new_household_member.is_consented = source_household_member.is_consented  # consent is forever
                new_household_member.save(update_fields=['is_consented'])
        except ValidationError:
            # 'representative eligibility' for an eligible representative has not been completed.'
            pass
        if source_household_member.member_status == BHS:
            new_household_member.member_status = ANNUAL
            new_household_member.save_base(update_fields=['member_status'])
        return new_household_member
