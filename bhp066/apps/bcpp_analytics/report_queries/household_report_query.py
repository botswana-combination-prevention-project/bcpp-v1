from apps.bcpp_household.models.household import Household
from apps.bcpp_household_member.choices import HOUSEHOLD_MEMBER_ACTION as member_actions
from .data_row import DataRow


class HouseholdReportQuery(object):

    def __init__(self, community):
        self.community = community
        self.data = []
        targeted_count = self.targeted_qs().count()
        self.data.append(DataRow("Targeted", targeted_count))
        self.data.append(DataRow("Visited at least Once", self.visited_qs().count()))
        enumerated = self.enumerated_qs().count()
        self.data.append(DataRow("Enumerated", enumerated))
        self.data.append(DataRow("At least 1 member present", self.eligible_qs().distinct().count()))
        self.data.append(DataRow("All Refused", self.all_refused_qs().count()))
        total_age_eligible = self.eligible_qs().count()
        self.data.append(DataRow("Age-eligible", total_age_eligible))
        average_age_eligible = float(total_age_eligible) / (enumerated or 1)
        avg = int(average_age_eligible * 100 + 0.5) / 100.0
        self.data.append(DataRow("Average Age-eligible per Enumerated", avg))

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
