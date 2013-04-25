from datetime import datetime
from django.db import models
from bcpp_survey.models import Survey
 

class HouseholdStructureManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        survey = Survey.objects.get_by_natural_key(survey_name)
        Household = models.get_model('bcpp_household', 'Household')
        household = Household.objects.get_by_natural_key(household_identifier)
        return self.get(household=household, survey=survey)

    def fetch_household_members(self, household_structure, using):
        """ Prepares a householdstructure for a new survey by fetching a list of the
        householdstructure members for a given householdstructure from the most recent
        survey and add them to the new survey """
        household_structure_member_model = household_structure.householdstructuremember_set.model
        #get previous survey
        surveys = Survey.objects.using(using).filter(
            survey_group=household_structure.survey.survey_group,
            chronological_order__lt=household_structure.survey.chronological_order,
            ).order_by('-chronological_order')
        if surveys:
            previous_survey = surveys[0]
            # add members from most recent previous survey to current survey
            for hsm in  household_structure_member_model.objects.using(using).filter(
                            household_structure__household=household_structure.household,
                            household_structure__survey=previous_survey):
                if not household_structure_member_model.objects.using(using).filter(
                           household_structure=household_structure,
                           internal_identifier=hsm.internal_identifier):
                    # note internal_identifier is carried over from the hsm instance from the previous survey
                    # in this way, hsm records can be linked to registered_subject and other data
                    #(2012-05 add registered_subject as an attribute of hsm)
                    options = {
                        'created': datetime.today(),
                        'user_created': 'auto',
                        'survey': household_structure.survey,
                        'initials': hsm.initials,
                        'registered_subject': hsm.registered_subject,
                        'first_name': hsm.first_name,
                        'gender': hsm.gender,
                        'age_in_years': hsm.age_in_years,
                        'nights_out': hsm.nights_out,
                        'relation': hsm.relation,
                        'target': hsm.target,
                        'present': '-',
                        'lives_in_household': '-',
                        'member_status': None}
                    household_structure_member, created = household_structure_member_model.objects.using(using).get_or_create(
                        household_structure=household_structure,
                        internal_identifier=hsm.internal_identifier,
                        defaults=options
                        )
                    # call save method to update member count
#                     household_structure.save(using=using)
