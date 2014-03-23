

class ReplacementData(object):

    def __init__(self):
        self._replacement_plot = None

    def check_refusals(self, plot):
        """Check if a plot has household refusals that would make it be replaced."""
        from ..models import Household
        replaced = []
        if plot.status == 'residential_habitable':
            if plot.household_count == 1:
                household = Household.objects.get(plot=plot)
                if self.is_hoh_refused(household):
                    replaced.append([household, 'HOH refusal', self.producer(plot)])
                else:
                    if self.is_refusal(household):
                        replaced.append([self.is_refusal(household), 'all members refused', self.producer(plot)])
            if plot.household_count > 1:
                households = Household.objects.filter(plot=plot)
                for household in households:
                    #Does this current household qualify the plot to be replaced?
                    if self.is_hoh_refused(household):
                        replaced.append([household, 'HOH refusal', self.producer(plot)])
                    else:
                        if self.is_refusal(household):
                            replaced.append([self.is_refusal(household), 'all members refused', self.producer(plot)])
        return replaced

    def producer(self, plot):
        """Get the producer where the plot is dispatched to."""
        from edc.device.dispatch.models import DispatchContainerRegister
        container = None
        producer = None
        if DispatchContainerRegister.objects.filter(container_identifier=plot.plot_identifier):
            container = DispatchContainerRegister.objects.get(container_identifier=plot.plot_identifier)
            producer = producer.producer
        return producer

    def check_absentees_ineligibles(self, plot):
        """Check if a plot has absentees and ineligibles that would make it be replaced."""
        from ..models import Household
        replaced = []
        if plot.status == 'residential_habitable':
            if plot.household_count == 1:  # We will replace if all eligible members are absent 3 times
                household = Household.objects.get(plot=plot)
                if self.is_absent(household):
                    replaced.append(self.is_absent(household))
            if plot.household_count >= 2:  # We will replace if all eligible members in each household are absent 3 times
                households = Household.objects.filter(plot=plot)
                for household in households:
                    #Does this current household qualify the plot to be replaced?
                    if self.is_absent(household):
                        replaced.append([self.is_absent(household), 'all members are absent', self.producer(plot)])
                    if self.no_informant(household):
                        replaced.append([self.no_informant(household), 'no household informant', self.producer(plot)])
                    if self.no_eligible_rep(household):
                        replaced.append([self.no_eligible_rep(household), 'no eligible members', self.producer(plot)])
        return replaced

    def is_hoh_refused(self, household):
        """Check if head of household refused members to participate."""
        from ..models import HouseholdRefusal
        if household.household_status == 'refused' and HouseholdRefusal.objects.filter(household=household):
            return True
        return False

    def no_eligible_rep(self, household):
        replacement_household = None
        if household.enumeration_attempts == 3:
            if household.household_status == 'eligible_representative_absent':
                replacement_household = household
                return replacement_household
        return replacement_household

    def is_refusal(self, household):
        """Check if the all household member are refusals"""
        from ..models import HouseholdStructure
        from apps.bcpp_household_member.models import HouseholdMember
        replacement_household = None
        members = None
        if household.enumerated:
            h_structure = HouseholdStructure.objects.get(household=household)
            members = HouseholdMember.objects.filter(household_structure=h_structure)
            #All eligible members refused
            members_status_list = []
            for member in members:
                if member.age_in_years >= 16 and member.study_resident == 'Yes':
                    #accumulate the statuses of all eligible members
                    members_status_list.append(member.member_status)
            if members_status_list:
                #Ckeck if all the values in the member status list are the same.
                if all(map(lambda x: x == members_status_list[0], members_status_list)):
                    if members_status_list[0] == 'REFUSED':
                        #If any member had a status that is not 'REFUSE' then this plot does not qualify for replacement
                        replacement_household = household
        return replacement_household

    def no_informant(self, household):
        """Check if there is anyone to give information living in the household"""
        from ..models import HouseholdAssessment
        replacement_household = None
        if household.enumeration_attempts == 3:
            household_assessment = HouseholdAssessment.objects.filter(household=household)
            if household_assessment:
                    if household.household_status == 'no_household_informant' and household_assessment[0].vdc_househould_status in ['rarely_there', 'seasonally_there']:
                        replacement_household = household
        return replacement_household

    def is_absent(self, household):
        """Check if all members of a household are absent"""
        from ..models import HouseholdStructure
        from apps.bcpp_household_member.models import HouseholdMember, SubjectAbsentee, SubjectAbsenteeEntry
        replacement_household = None
        members = None
        if household.enumerated:
            h_structure = HouseholdStructure.objects.get(household=household)
            members = HouseholdMember.objects.filter(household_structure=h_structure)
            for member in members:
                if member.age_in_years >= 16 and member.study_resident == 'Yes' and member.member_status == 'ABSENT':
                    sub_absentee = SubjectAbsentee.objects.get(household_member=member)
                    num_absentee_entries = SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee).count()
                    if num_absentee_entries == 3:  # Then we have found a reason not to replace this plot
                        replacement_household = household
        return replacement_household

    def replacement_reason(self, replacement_item):
        """check the reason why a plot or household is being replaced."""
        from ..models import Plot
        from ..models import Household
        reason = None
        if self.is_absent(replacement_item):
            reason = 'all members are absent'
        elif self.is_hoh_refused(replacement_item):
            reason = 'HOH refusal'
        elif self.no_eligible_rep(replacement_item):
            reason = 'no eligible members'
#         elif isinstance(Plot, replacement_item):
#             if self.is_replacement_valid(replacement_item):
#                 reason = 'invalid replacement'
        return reason

    def is_replacement_valid(self, plot):
        """Check if a plot used to replace a household is valid after the plot has been confirmed.

            If the plot is not valid the replace the plot.
        """
        replaced = []
        if plot.replacement and plot.status in ['residential_not_habitable', 'non-residential']:
            replaced.append([plot, "invalid replacement"])
        return replaced
