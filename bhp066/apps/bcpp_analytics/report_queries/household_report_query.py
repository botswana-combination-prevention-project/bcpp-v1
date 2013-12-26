from apps.bcpp_household.models.household import Household
from apps.bcpp_household_member.choices import HOUSEHOLD_MEMBER_ACTION as member_actions
from .data_row import DataRow
from .report_query import TwoColumnReportQuery


class HouseholdReportQuery(TwoColumnReportQuery):

    def post_init(self, **kwargs):
        self.targeted = self.targeted_qs().count()
        self.visited = self.visited_qs().count()
        self.enumerated = self.enumerated_qs().count()
        self.member_present = self.eligible_qs().distinct().count()
        self.all_refused = self.all_refused_qs().count()
        self.total_age_eligible = self.eligible_qs().count()
        average_age_eligible = float(self.total_age_eligible) / (self.enumerated or 1)
        self.avg_eligible_enumerated = int(average_age_eligible * 100 + 0.5) / 100.0

    def display_title(self):
        return "Households"

    def data_to_display(self):
        data = []
        data.append(DataRow("Targeted", self.targeted))
        data.append(DataRow("Visited at least Once", self.visited))
        data.append(DataRow("Enumerated", self.enumerated))
        data.append(DataRow("At least 1 member present", self.member_present))
        data.append(DataRow("All Refused", self.all_refused))
        data.append(DataRow("Age-eligible", self.total_age_eligible))
        data.append(DataRow("Average Age-eligible per Enumerated", self.avg_eligible_enumerated))
        return data

    def targeted_qs(self):
        return Household.objects.filter(plot__action='confirmed',
                                        plot__status__istartswith='occupied', community=self.community)

    def visited_qs(self):
        return self.targeted_qs().filter(householdstructure__householdlog__isnull=False)

    def enumerated_qs(self):
        return self.targeted_qs().filter(householdstructure__member_count__gte=1)

    def eligible_qs(self):
        return self.targeted_qs().filter(householdstructure__householdmember__eligible_member=True)

    def all_refused_qs(self):
        actions = [item[0] for item in member_actions if item[0] != 'REFUSED']
        return self.visited_qs().exclude(householdstructure__householdmember__member_status__in=actions)

    def age_elegible_qs(self):
        return self.enumerated_qs().filter(householdstructure__householdmember__eligible_member=True)

    @staticmethod
    def enrolled_qs(community):
        community_households = Household.objects.filter(community=community)
        return community_households.filter(householdstructure__householdmember__subjectconsent__isnull=False).distinct()

    @staticmethod
    def enrolled_ids_qs(community):
        ids = HouseholdReportQuery.enrolled_qs(community).values_list('id')
        return sum(ids, ())
