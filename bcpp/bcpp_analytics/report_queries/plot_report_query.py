from django.db.models import Count, Sum

from bhp066.apps.bcpp_household.constants import CONFIRMED
from bhp066.apps.bcpp_household.models.plot import Plot

from .data_row import DataRow
from .report_query import TwoColumnReportQuery


class PlotReportQuery(TwoColumnReportQuery):
    def post_init(self, **kwargs):
        self.plots_qs = Plot.objects.filter(community__iexact=self.community,
                                            created__gte=self.start_date,
                                            created__lte=self.end_date)

    def build(self):
        self.targeted = self.targeted_qs().count()
        self.verified = self.plot_stats().get('verified_count')
        self.households = self.plot_stats().get('household_count')

    def display_title(self):
        return "Plots"

    def data_to_display(self):
        self.build()
        data = []
        data.append(DataRow('Number Targeted', self.targeted))
        data.append(DataRow('Verified Residential', self.verified))
        data.append(DataRow('Households on Verified Residential', self.households))
        return data

    def targeted_qs(self):
        return self.plots_qs.filter(selected__isnull=False)

    def confirmed_occupied_qs(self):
        return self.targeted_qs().filter(action=CONFIRMED, status__istartswith='occupied')

    def plot_stats(self):
        return self.confirmed_occupied_qs().aggregate(household_count=Sum('household_count'),
                                                      verified_count=Count('pk'))
