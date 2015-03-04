from datetime import datetime

from apps.bcpp_household.models import Household, HouseholdStructure, PlotLog, PlotLogEntry
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household.constants import TWENTY_PERCENT, FIVE_PERCENT


class Plot(object):

    def __init__(self, plot=None, household=None, household_structure=None, household_member=None):
        self.instance_datetime = datetime.today()
        self.plot_log = None
        self.household_identifier = None
        self.household_member = household_member
        self.household_structure = household_structure
        try:
            self.plot = household_member.household_structure.household.plot
            self.household = household_member.household_structure.household
        except AttributeError:
            try:
                self.plot = household_structure.household.plot
                self.household = household_structure.household
            except AttributeError:
                try:
                    self.plot = household.plot
                    self.household = household
                except AttributeError:
                    self.plot = plot
                    self.household = Household.objects.filter(plot=self.plot)
        self.plot_identifier = self.plot.plot_identifier
        self.gps_lat_target = self.plot.gps_target_lat
        self.gps_lon_target = self.plot.gps_target_lon
        self.gps_lat_actual = self.plot.gps_lat
        self.gps_lon_actual = self.plot.gps_lon
        self.household_structure = HouseholdStructure.objects.filter(household__plot=self.plot)
        self.household_member = HouseholdMember.objects.filter(household_structure__household__plot=self.plot)
        self.household_member_count = len(list(set([hm.internal_identifier for hm in self.household_member])))
        self.household_identifier = [h.household_identifier for h in self.household]
        self.household_count = len(self.household)
        self.confirmed = self.plot.action
        self.status = self.plot.status
        self.gps_lat = self.plot.gps_lat
        self.gps_lon = self.plot.gps_lon
        self.time_of_day = self.plot.time_of_day
        self.enrolled = True if self.plot.bhs else False
        if self.plot.selected == TWENTY_PERCENT:
            self.handed_to_htc = True if self.plot.htc else False
            self.random_selection = '20%'
        elif self.plot.selected == FIVE_PERCENT:
            self.handed_to_htc = True if self.plot.htc else False
            self.random_selection = '5%'
        else:
            self.handed_to_htc = False
            self.random_selection = '75%'
        self.htc_plot = True if self.plot.htc else False
        self.bhs_plot = True if self.plot.bhs else False
        self.community = self.plot.community
        self.confirmed_date = None
        try:
            self.plot_log = PlotLogEntry.objects.filter(plot_log=PlotLog.objects.get(plot=self.plot))
        except (PlotLog.DoesNotExist, PlotLogEntry.DoesNotExist):
            self.plot_log = []
        self.plot_first_visit_date = min(list(set([
            l.report_datetime.date() for l in self.plot_log
            ] or [self.plot.modified.date()])))
        self.plot_visit_date = list(set([l.report_datetime.date() for l in self.plot_log] or [self.plot.modified.date()]))
        self.plot_visit_date.sort()
        self.plot_log_status = [p.log_status for p in self.plot_log]

    def __repr__(self):
        return ('Plot(plot={0.plot!r}, household={0.household!r}, '
                'household_structure={0.household_structure!r}, '
                'household_member={0.household_member!r})').format(self)

    def __str__(self):
        return '{0.plot!s}'.format(self)

    def unique_key(self):
        return self.plot_identifier
