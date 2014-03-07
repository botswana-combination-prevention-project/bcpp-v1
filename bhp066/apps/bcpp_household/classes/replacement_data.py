from datetime import datetime as DT

class ReplacementData(object):

    def __init__(self, *args, **kwargs):
        self._members = None
        self._h_structure = None
        self._replacement_plot = None

    def replace_refusals(self, plot):
        """Check if a plot has household refusals that would make it be replaced."""
        from apps.bcpp_household.models import Household
        replaced = []
        if plot.status == 'residential_habitable':
            if plot.household_count == 1:
                household = Household.objects.get(plot=plot)
                if self.evaluate_head_of_household_refusal(household):
                    replaced.append(self.evaluate_head_of_household_refusal(household))
                    return replaced
                else:
                    if self.evaluate_refusals(household):
                        replaced.append(self.evaluate_refusals(household))
                        return replaced
            if plot.household_count >= 2:
                households = Household.objects.filter(plot=plot)
                for household in households:
                    #Does this current household qualify the plot to be replaced?
                    if self.evaluate_head_of_household_refusal(household):
                        replaced.append(self.evaluate_head_of_household_refusal(household))
                    else:
                        if self.evaluate_refusals(household):
                            replaced.append(self.evaluate_refusals(household))
                return replaced
        return None

    def replacement_absentees_ineligibles(self, plot):
        """Check if a plot has absentees that would make it be replaced."""
        from apps.bcpp_household.models import Household
        replaced = []
        if plot.status == 'residential_habitable':
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
                    if self.unavailable_members(household):
                        replaced.append(self.unavailable_members(household))
                    if self.no_eligible_rep(household):
                        replaced.append(self.no_eligible_rep(household))
                return replaced
        return None

    def evaluate_head_of_household_refusal(self, household):
        """Check if head of household refused memebers to participate."""
        if household.allowed_to_enumerate == 'no':
            return household

    def no_eligible_rep(self, household):
        return None
#         from apps.bcpp_household.models import HouseholdLogEntry
#         household_logs = HouseholdLogEntry.objects.filter(household_log__household_structure__household=household)
#         h_log_dates = []
#         for h_log in household_logs:
#             h_log_dates.append(DT(h_log.report_datetime))
#         report_datetime = max(h_log_dates)
#         latest_log = HouseholdLogEntry.objects.get(household_log__household_structure__household=household, report_datetime=report_datetime)
#         if latest_log.household_status == 'eligible_representative_absent' and latest_log.supervisor_vdc_confirm == 'Yes':
#             replacement_household = household
#             return replacement_household
#         return replacement_household

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
        return replacement_household

    def unavailable_members(self, household):
        from apps.bcpp_household.models import HouseholdLogEntry
        replacement_household = None
        h_log_dates = []
        if household.enumeration_attempts == 3:
            household_logs = HouseholdLogEntry.objects.filter(household_log__household_structure__household=household)
            for h_log in household_logs:
                h_log_dates.append(DT(h_log.report_datetime))
            report_datetime = max(h_log_dates)
            latest_log = HouseholdLogEntry.objects.get(household_log__household_structure__household=household, report_datetime=report_datetime)
            if latest_log.household_status == 'no_household_informant' and latest_log.supervisor_vdc_confirm == 'Yes':
                replacement_household = household
                return replacement_household
        return replacement_household

    def evaluate_absentees(self, household):
        from apps.bcpp_household.models import HouseholdStructure
        from apps.bcpp_household_member.models import HouseholdMember
        from apps.bcpp_household_member.models import SubjectAbsentee, SubjectAbsenteeEntry
        replacement_household = None
        members = None
        if HouseholdStructure.objects.filter(household=household):
            h_structure = HouseholdStructure.objects.get(household=household)
            if HouseholdMember.objects.filter(household_structure=h_structure):
                members = HouseholdMember.objects.filter(household_structure=h_structure)
        if members:
            for member in members:
                if member.age_in_years >= 16 and member.study_resident == 'Yes' and member.member_status == 'ABSENT':
                    sub_absentee = SubjectAbsentee.objects.get(household_member=member)
                    num_absentee_entries = SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee).count()
                    if num_absentee_entries == '3':#Then we have found a reason not to replace this plot
                        replacement_household = household
        return replacement_household
