from bhp066.apps.bcpp_household.constants import CONFIRMED
from bhp066.apps.bcpp_household.models.household import Household

from .data_row import DataRow
from .report_query import TwoColumnReportQuery


class HouseholdReportQuery(TwoColumnReportQuery):

    def build(self):
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
        self.build()
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
        return Household.objects.filter(plot__action=CONFIRMED, created__gte=self.start_date, created__lte=self.end_date,
                                        plot__status__istartswith='occupied', community=self.community)

    def visited_qs(self):
        return self.targeted_qs().filter(householdstructure__householdlog__isnull=False)

    def enumerated_qs(self):
        return self.targeted_qs().filter(householdstructure__enumerated=True)

    def eligible_qs(self):
        return self.targeted_qs().filter(householdstructure__householdmember__eligible_member=True)

    def all_refused_qs(self):
        return self.visited_qs().filter(householdstructure__householdmember__refused=True)

    def age_elegible_qs(self):
        return self.enumerated_qs().filter(householdstructure__householdmember__eligible_member=True)

    @staticmethod
    def enrolled_qs(community, start_date, end_date):
        community_households = Household.objects.filter(community__iexact=community, created__gte=start_date, created__lte=end_date)
        return community_households.filter(householdstructure__householdmember__subjectconsent__isnull=False).distinct()

    @staticmethod
    def enrolled_ids_qs(community, start_date, end_date):
        ids = HouseholdReportQuery.enrolled_qs(community, start_date, end_date).values_list('id')
        return sum(ids, ())
