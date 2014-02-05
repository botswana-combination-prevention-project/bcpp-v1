

class ReplacementData(object):

    def __init__(self, *args, **kwargs):
        self._members = None
        self._h_structure = None
        self._replacement_plot = None

    def replace_refusals(self, plot):
        """Check if a plot has household refusals that would make it be replaced."""
        from apps.bcpp_household.models import Household
        replaced = []
        if plot.status == 'occupied':
            if plot.household_count == 1:
                household = Household.objects.get(plot=plot)
                if self.evaluate_head_of_household_refusal(plot, household):
                    replaced.append(self.evaluate_head_of_household_refusal(plot, household))
                    return replaced
                else:
                    if self.evaluate_refusals(household):
                        replaced.append(self.evaluate_refusals(household))
                        return replaced
            if plot.household_count >= 2:
                households = Household.objects.filter(plot=plot)
                for household in households:
                    #Does this current household qualify the plot to be replaced?
                    if self.evaluate_head_of_household_refusal(plot, household):
                        replaced.append(self.evaluate_head_of_household_refusal(plot, household))
                    else:
                        if self.evaluate_refusals(household):
                            replaced.append(self.evaluate_refusals(household))
                if replaced:
                    #If a single household qualifies a plot to be replaced, then replace the whole plot
                    return replaced
        #We will return None if the plot passed does not qualify to be replaced
        return None

    def evaluate_head_of_household_refusal(self, plot, household):
        """Updates the allowed_to_enumerate field on the plot model."""
        if plot.household_count >= 2:
            if household.allowed_to_enumerate == 'no':
                return household
        if plot.household_count == 1 and plot.allowed_to_enumerate == 'no':
            return household

    def replacement_absentee(self, plot):
        """Check if a plot has absentees that would make it be replaced."""
        from apps.bcpp_household.models import Household
        replaced = []
        if plot.status == 'occupied':
            if plot.household_count == 1:#We will replace if all eligible members are absent 3 times
                household = Household.objects.get(plot=plot)
                if self.evaluate_absentees(household):
                    replaced.append(self.evaluate_absentees(household))
                    return replaced
            if plot.household_count >= 2:#We will replace if all eligible members in each household are absent 3 times
                households = Household.objects.filter(plot=plot)
                for household in households:
                    #Does this current household qualify the plot to be replaced?
                    if self.evaluate_absentees(household):
                        replaced.append(self.evaluate_absentees(household))
                        return replaced
        #We will return None if the plot passed does not qualify to be replaced
        return None

    def replacement_none_consented(self, plot):
        """Check if a plot has no consents to make it be replaced."""
        #A plot with more than one household.
        from apps.bcpp_household.models import Household, HouseholdStructure
        from apps.bcpp_household_member.models import HouseholdMember
        replaced = []
        members = None
        households = Household.objects.filter(plot=plot)
        consented_check_list = []
        for household in households:
            if HouseholdStructure.objects.get(household=household):
                h_structure = HouseholdStructure.objects.get(household=household)
                if HouseholdMember.objects.filter(household_structure=h_structure):
                    members = HouseholdMember.objects.filter(household_structure=h_structure)
            #No HH consented.
            if members:
                for member in members:
                    consented_check_list.append(member.is_consented)
            if consented_check_list:
                if all(map(lambda x: x == consented_check_list[0], consented_check_list)):
                    if consented_check_list[0] == False:
                        replaced.append(household)
                        return replaced
        return replaced

    def evaluate_refusals(self, household):
        from apps.bcpp_household.models import HouseholdStructure
        from apps.bcpp_household_member.models import HouseholdMember
        replacement_household = None
        members = None
        if HouseholdStructure.objects.filter(household=household):
                h_structure = HouseholdStructure.objects.get(household=household)
                if HouseholdMember.objects.filter(household_structure=h_structure):
                    members = HouseholdMember.objects.filter(household_structure=h_structure)
                #All eligible members refused
                members_status_list = []
                if members:
                    for member in members:
                        if member.eligible_member:
                            #accumulate the statuses of all eligible members
                            members_status_list.append(member.member_status)
                if members_status_list:
                    #Ckeck if all the values in the member status list are the same.
                    if all(map(lambda x: x == consented_check_list[0], consented_check_list)):
                        if members_status_list == 'REFUSED':
                            #If any member had a status that is not 'REFUSE' then this plot does not qualify for replacement
                            replacement_household = household
                            return replacement_household
        return replacement_household

    def evaluate_absentees(self, household):
        from apps.bcpp_household.models import HouseholdStructure
        from apps.bcpp_household_member.models import HouseholdMember
        from apps.bcpp_household_member.models import SubjectAbsentee, SubjectAbsenteeEntry
        replacement_household = None
        members = None
        dont_replace = False#Assume a plot should be replaced untill we find a reason not to replace it
        if HouseholdStructure.objects.filter(household=household):
            h_structure = HouseholdStructure.objects.get(household=household)
            if HouseholdMember.objects.filter(household_structure=h_structure):
                members = HouseholdMember.objects.filter(household_structure=h_structure)
        if members:
            for member in members:
                if member.eligible_member and member.member_status == 'ABSENT':
                    sub_absentee = SubjectAbsentee.objects.get(household_member=member)
                    num_absentee_entries = SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee).count()
                    if num_absentee_entries <= '3':#Then we have found a reason not to replace this plot
                        dont_replace = True
        if not dont_replace:
            replacement_household = household
        return replacement_household
