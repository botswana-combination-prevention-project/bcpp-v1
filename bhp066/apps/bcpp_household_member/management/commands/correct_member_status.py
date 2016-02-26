from django.core.management.base import BaseCommand
from django.db.models import get_model

from django.conf import settings
from bhp066.apps.bcpp_subject.models.subject_consent import SubjectConsent
from bhp066.apps.bcpp_export.classes.household import Household
from bhp066.apps.bcpp_export.classes.household_member import HouseholdMember
from bhp066.apps.bcpp_survey.models.survey import Survey


class Command(BaseCommand):

    args = ''
    help = ''

    def handle(self, *args, **options):
        household_identifier = args[0]
        self.correct_member_status(household_identifier)

    def correct_member_status(self, household_identifier):
        survey_slug = 'bcpp-subject-' + settings.CURRENT_SURVEY[-1]
        prv_survey = survey_slug if int(settings.CURRENT_SURVEY[-1]) > 0 else settings.CURRENT_SURVEY
        try:
            household = Household.objects.get(household_identifier=household_identifier)
            for household_member in HouseholdMember.objects.filter(household_structure__household=household):
                if not (self.verify_consent(household_member)):
                    print ("There is no consents for participart {}.".format(household_member.registered_subject))
                    continue
                if not self.verify_plot_bhs(household_member):
                    print ("plot {} is not bhs  enrolled".format(household_member.household.plot.plot_identifier))
                    continue
                if not self.verify_household_structure_enrolled(household_member):
                    print ("household structure is not enrolled {}.".format(household_member.household_structure))
                    continue
                if not self.verify_household_enrolled(household_member):
                    print ("household is not enrolled {}".format(household_member.household_structure))
                    continue
                if not (household_member.is_consented or
                        household_member.eligible_subject or household_member.eligible_member):
                    household_member.is_consented = True
                    household_member.eligible_subject = True
                    household_member.eligible_member = True
                    household_member.member_status = 'ANNUAL'
                    household_member.save(update_fields=[
                        'is_consented', 'eligible_subject', 'eligible_member', 'member_status'])
                    household_member = HouseholdMember.objects.get(
                        household_structure__survey=Survey.objects.get(survey_slug=prv_survey),
                        registered_subject=household_member.registered_subject)
                    print ('household member has been updated. new member status: {}'.format(
                        household_member.member_status))
        except Household.DoesNotExist:
            print ('Household does not exists. {}'.format(household_identifier))

    def verify_plot_bhs(self, household_member):
        plot = household_member.household_structure.household.plot
        return True if plot.bhs else False

    def verify_household_enrolled(self, household_member):
        household = household_member.household_structure.household
        return True if household.enrolled else False

    def verify_household_structure_enrolled(self, household_member):
        household_structure = household_member.household_structure
        return True if household_structure.enrolled else False

    def verify_consent(self, household_member):
        registered_subject = household_member.registered_subject
        try:
            SubjectConsent.objects.get(household_member__registered_subject=registered_subject)
        except SubjectConsent.DoesNotExist:
            print('No subject consent for participant {}'.format(registered_subject.subject_identifier))
            return False
        return True
