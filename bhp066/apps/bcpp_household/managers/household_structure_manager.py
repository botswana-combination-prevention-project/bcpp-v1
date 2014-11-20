from django.db import models

from apps.bcpp_survey.models import Survey

from ..exceptions import AlreadyEnumerated, EligibleRepresentativeError


class HouseholdStructureManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        survey = Survey.objects.get_by_natural_key(survey_name)
        Household = models.get_model('bcpp_household', 'Household')
        household = Household.objects.get_by_natural_key(household_identifier)
        return self.get(household=household, survey=survey)

    def add_household_members_from_survey(self, household, source_survey, target_survey):
        """Adds household members from a previous survey to an
        unenumerated household structure of a new survey.

        May raise an error if RepresentativeEligibility is not found."""
        if source_survey:
            HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
            if source_survey.survey_slug == target_survey.survey_slug:
                raise ValueError('Source survey and target survey may not be the same.')
            source_household_structure = self.get(household=household, survey=source_survey)
            try:
                target_household_structure = self.get(household=household, survey=target_survey, enumerated=False)
                if target_household_structure.has_household_log_entry:
                    target_household_structure.check_eligible_representative_filled(
                        exception_cls=EligibleRepresentativeError)
                    for household_member in HouseholdMember.objects.filter(household_structure=source_household_structure):
                        try:
                            household_member = HouseholdMember.objects.get(
                                internal_identifier=household_member.internal_identifier,
                                household_structure=target_household_structure)
                        except HouseholdMember.DoesNotExist:
                            options = dict(
                                household_structure=target_household_structure,
                                first_name=household_member.first_name,
                                initials=household_member.initials,
                                age_in_years=household_member.age_in_years,
                                gender=household_member.gender,
                                relation=household_member.relation,
                                inability_to_participate=household_member.inability_to_participate,
                                internal_identifier=household_member.internal_identifier,
                            )
                            household_member = HouseholdMember.objects.create(**options)
                            print 'Added {}.'.format(household_member)
                    target_household_structure.enumerated = False
                    target_household_structure.save(update_fields=['enumerated'])  # skips current survey check in save()
            except self.model.DoesNotExist:
                raise AlreadyEnumerated(
                    'household structure {} is already enumerated.'.format(target_household_structure))
            except EligibleRepresentativeError:
                pass
