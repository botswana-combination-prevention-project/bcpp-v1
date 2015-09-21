from bhp066.apps.bcpp_household.constants import CONFIRMED
from bhp066.apps.bcpp_household.models.household import Household
from bhp066.apps.bcpp_household.models.household_log import HouseholdLogEntry

from .data_row import DataRow
from .report_query import TwoColumnReportQuery


class HouseholdVisitsReportQuery(TwoColumnReportQuery):

    def build(self):
        self.all_enrolled = self.visits_qs(self._households_with_all_enrolled).count()
        self.all_screened = self.visits_qs(self._households_with_all_screened).count()
        self.all_refused = self.confirmed_refusing_qs().distinct().count()

    def display_title(self):
        return "Number of Household Visits"

    def data_to_display(self):
        self.build()
        data = []
        data.append(DataRow('All members have enrolled', self.all_enrolled))
        data.append(DataRow('All members have screened', self.all_screened))
        data.append(DataRow('All confirmed refused', self.all_refused))
        return data

    def visits_qs(self, query_fn):
        households_ids = query_fn().values_list('id', flat=True)
        return HouseholdLogEntry.objects.filter(household_log__household_structure__household__pk__in=households_ids)

    def _root_households_qs(self):
        return Household.objects.filter(plot__action=CONFIRMED, created__gte=self.start_date, created__lte=self.end_date,
                                        plot__status__istartswith='occupied', community=self.community)

    def _households_with_all_enrolled(self):
        return self._root_households_qs().exclude(householdstructure__householdmember__is_consented=False)

    def _households_with_all_screened(self):
        untested = ['Not performed', 'Declined']
        hh_enrolled_qs = self._households_with_all_enrolled()
        return hh_enrolled_qs.exclude(householdstructure__householdmember__subjectvisit__hivresult__hiv_result__in=untested)

    def confirmed_refusing_qs(self):
        return HouseholdLogEntry.objects.filter(household_log__household_structure__householdmember__refused=True)
