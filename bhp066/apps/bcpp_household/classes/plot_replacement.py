from ...bcpp_household_member.models import HouseholdInfo, HouseholdMember
from ..models import Household, HouseholdStructure
from apps.bcpp_household_member.models import SubjectAbsentee, SubjectAbsenteeEntry
 
 
 
class PlotReplacement(object):
 
    def __init__(self, *args, **kwargs):
        self._members = None
        self._h_structure = None
        self._replacement_plot = None
 
    def replace_refusal_plot(self, plot):
        """Check if a plot has refusal that would make it be replaced."""
        if plot.household_count == 1:
            household = Household.objects.get(plot=plot)
            if HouseholdStructure.objects.get(household=household):
                h_structure = HouseholdStructure.objects.get(household=household)
                if HouseholdMember.objects.filter(household_structure=h_structure):
                    members = HouseholdMember.objects.filter(household_structure=h_structure)
                #All eligible members refused
                members_status_list = []
                if members:
                    for member in members:
                        if member.eligible_member:
                            members_status_list.append(member.member_status)
                if members_status_list:
                    if all(map(lambda x: x == members_status_list[0], members_status_list)):
                        if members_status_list[0] == "REFUSED":
                            replacement_plot = plot
                            return replacement_plot
        if plot.household_count >= 2:
            households = Household.objects.filter(plot=plot)
            for household in households:
                if HouseholdStructure.objects.get(household=household):
                    h_structure = HouseholdStructure.objects.get(household=household)
                    if HouseholdMember.objects.filter(household_structure=h_structure):
                        members = HouseholdMember.objects.filter(household_structure=h_structure)
                #At least one household refused
                members_status_list = []
                if members:
                    for member in members:
                        if member.eligible_member:
                            members_status_list.append(member.member_status)
                if members_status_list:
                    if all(map(lambda x: x == members_status_list[0], members_status_list)):
                        if members_status_list[0] == "REFUSED":
                            replacement_plot = plot
                            return replacement_plot
        return replacement_plot
 
    def replacement_absentee(self, plot):
        """Check if a plot has absentees that would make it be replaced."""
        if plot.household_count == 1:
            household = Household.objects.get(plot=plot)
            if HouseholdStructure.objects.get(household=household):
                h_structure = HouseholdStructure.objects.get(household=household)
                if HouseholdMember.objects.filter(household_structure=h_structure):
                    members = HouseholdMember.objects.filter(household_structure=h_structure)
            #All eligible absent after 3 individual visits each
            members_status_list = []
            absentee_entries = []
            if members:
                for member in members:
                    if member.eligible_member:
                        members_status_list.append(member.member_status)
                        if members_status_list:
                            if all(map(lambda x: x == members_status_list[0], members_status_list)):
                                if members_status_list[0] == "ABSENT":
                                    sub_absentee = SubjectAbsentee.objects.get(household_member=member)
                                    num_absentee_entries = SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
                                    absentee_entries.append(SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee).count())
            if all(map(lambda x: x == member_absentee_entries_list[0], absentee_entries)):
                if absentee_entries:
                    if absentee_entries[0] == 3:
                        replacement_plot = plot
                        return replacement_plot
        if plot.household_count >= 2:
            households = Household.objects.filter(plot=plot)
            for household in households:
                if HouseholdStructure.objects.get(household=household):
                    h_structure = HouseholdStructure.objects.get(household=household)
                    if HouseholdMember.objects.filter(household_structure=h_structure):
                        members = HouseholdMember.objects.filter(household_structure=h_structure)
                #All eligible absent after 3 individual visits each
                members_status_list = []
                member_absentee_entries_list = []
                if members:
                    for member in members:
                        if member.eligible_member:
                            members_status_list.append(member.member_status)
                            if members_status_list:
                                if all(map(lambda x: x == members_status_list[0], members_status_list)):
                                    if members_status_list[0] == "ABSENT":
                                        sub_absentee = SubjectAbsentee.objects.get(household_member=member)
                                        num_absentee_entries = SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
                                        member_absentee_entries_list.append(SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee).count())
                if all(map(lambda x: x == member_absentee_entries_list[0], member_absentee_entries_list)):
                    if member_absentee_entries_list:
                        if member_absentee_entries_list[0]:
                            if member_absentee_entries_list[0] == 3:
                                replacement_plot = plot
                                return replacement_plot
        return replacement_plot
 
    def replacement_none_consented(self, plot):
        """Check if a plot has no consents to make it be replaced."""
        #A plot with more than one household.
        if plot.household_count >= 2:
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
                        replacement_plot = plot
                        return replacement_plot
        return replacement_plot