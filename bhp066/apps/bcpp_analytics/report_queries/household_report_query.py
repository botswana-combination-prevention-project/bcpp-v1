from apps.bcpp_household.models.household import Household
from apps.bcpp_household_member.choices import HOUSEHOLD_MEMBER_ACTION as member_actions


class HouseholdReportQuery(object):

    def __init__(self, community):
        self.community = community
        self.targeted = self.targeted_qs().count()
        self.visited = self.visited_qs().count()
        self.enumerated = self.enumerated_qs().count()
        self.at_least_one_present = self.eligible_qs().distinct().count()
        self.all_refused = self.all_refused_qs().count()
        self.total_age_eligible = self.eligible_qs().count()
        self.average_age_eligible = float(self.total_age_eligible) / (self.enumerated or 1)

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
