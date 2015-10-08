from django.core.management.base import BaseCommand

from bhp066.apps.bcpp_household.models.notebook_plot_list import NotebookPlotList
from django.db.models import get_model

from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_subject.models.subject_consent import SubjectConsent
from bhp066.apps.bcpp_household.models import Plot
from bhp066.apps.bcpp_household.models.household import Household
from bhp066.apps.bcpp_household_member.models import HouseholdMember


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.update_member_status()
    def is_consent_available(self, member):
        try:
            SubjectConsent.objects.get(registered_subject=member.registered_subject)
        except SubjectConsent.DoesNotExist:
            return False
        except SubjectConsent.MultipleObjectsReturned:
            return True
        return True
        
    def update_member_status(self):
        plot_identifiers = []
        NotebookPlotList = get_model("bcpp_household", "notebookplotlist")
        for nt in  NotebookPlotList.objects.all():
            plot_identifiers.append(nt.plot_identifier)
        survey = Survey.objects.get(survey_abbrev='Y2')
        for p in plot_identifiers:
            plot = Plot.objects.get(plot_identifier=p)
            for h in Household.objects.filter(plot=plot):
                for member in HouseholdMember.objects.filter(
                    household_structure__household=h,
                    household_structure__survey=survey):
                    if member.member_status == 'ANNUAL':
                        print ("Member {} member_satus is correct. skipped".format(member.registered_subject.subject))
                        continue
                    if self.is_consent_available(member):
                        member.member_status = 'ANNUAL'
                        member.is_consented = True
                        member.eligible_subject = True
                        member.eligible_member = True
                        plot.bhs = True
                        h.enrolled = True
                        member.household_structure.enrolled = True
                        member.household_structure.enrolled.save()
                        h.save()
                        plot.save()
                        member.save()
                        print ("Member {} has been saved!".format(member.registered_subject.subject))

