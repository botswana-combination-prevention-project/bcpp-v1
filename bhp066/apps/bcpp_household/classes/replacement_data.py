from apps.bcpp_household.constants import ELIGIBLE_REPRESENTATIVE_ABSENT


class ReplacementData(object):

    def __init__(self):
        self._replacement_plot = None

    def check_refusals(self, plot, household, household_structure):
        """Check if a plot has household refusals that would make it be replaced."""
        replaced = []
        if plot.status == 'residential_habitable':
                if self.is_hoh_refused(household_structure):
                    replaced.append([household, 'HOH refusal', self.producer(plot)])
                elif self.is_refusal(household, household_structure):
                    replaced.append([self.is_refusal(household, household_structure), 'all members refused', self.producer(plot)])
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

    def check_absentees_ineligibles(self, plot, household, household_structure):
        """Check if a plot has absentees and ineligibles that would make it be replaced."""
        replaced = []
        if plot.status == 'residential_habitable':
            if self.is_absent(household, household_structure):
                replaced.append([self.is_absent(household, household_structure), 'all members are absent', self.producer(plot)])
            if self.no_informant(household, household_structure):
                replaced.append([self.no_informant(household, household_structure), 'no household informant', self.producer(plot)])
            if self.no_eligible_rep(household):
                replaced.append([self.no_eligible_rep(household), 'no eligible members', self.producer(plot)])
        return replaced

    def is_hoh_refused(self, household_structure):
        """Check if head of household refused members to participate."""
        if household_structure.refused_enumerated:
            return True
        return False

    def no_eligible_rep(self, household):
        replacement_household = None
        if household.enumeration_attempts == 3:
            if household.reason_not_enumerated == ELIGIBLE_REPRESENTATIVE_ABSENT:
                replacement_household = household
                return replacement_household
        return replacement_household

    def is_refusal(self, household, household_structure):
        """Check if the all household member are refusals"""
        from apps.bcpp_household_member.models import HouseholdMember
        replacement_household = None
        members = None
        if household.enumerated:
            members = HouseholdMember.objects.filter(household_structure=household_structure)
            members_status_list = []
            for member in members:
                if member.age_in_years >= 16 and member.study_resident == 'Yes':  # All eligible members refused
                    members_status_list = list(set(members_status_list + [member.refused]))
            if members_status_list:
                if members_status_list[0] and len(members_status_list):
                        replacement_household = household
        return replacement_household

    def no_informant(self, household, household_structure):
        """Check if there is anyone to give information living in the household"""
        replacement_household = None
        if household.enumeration_attempts == 3:
            if household_structure.no_informant:
                replacement_household = household
        return replacement_household

    def is_absent(self, household, household_structure):
        """Check if all members of a household are absent"""
        from apps.bcpp_household_member.models import HouseholdMember, SubjectAbsentee, SubjectAbsenteeEntry
        replacement_household = None
        members = None
        if household.enumerated:
            members = HouseholdMember.objects.filter(household_structure=household_structure)
            absentee_entry_count_list = []
            for member in members:
                if member.age_in_years >= 16 and member.study_resident == 'Yes' and member.member_status == 'ABSENT':  # All eligible members absent
                    sub_absentee = SubjectAbsentee.objects.get(household_member=member)
                    num_absentee_entries = SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee).count()
                    absentee_entry_count_list = list(set(absentee_entry_count_list + [num_absentee_entries]))
            if absentee_entry_count_list:
                if absentee_entry_count_list[0] == 3 and len(absentee_entry_count_list) == 1:  # Then we have found a reason not to replace this plot
                    replacement_household = household
        return replacement_household

    def replacement_reason(self, household, household_structure):
        """check the reason why a plot or household is being replaced."""
        reason = None
        if self.is_absent(household, household_structure):
            reason = 'all members are absent'
        elif self.is_hoh_refused(household):
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
            replaced.append([plot, "invalid replacement", self.producer()])
        return replaced
