from apps.bcpp_household.models import Household, HouseholdStructure, PlotLog, PlotLogEntry
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household.constants import TWENTY_PERCENT, FIVE_PERCENT, CONFIRMED
from apps.bcpp_survey.models import Survey

from .base_helper import BaseHelper


class Plot(BaseHelper):

    def __init__(self, plot=None, household=None, household_structure=None, household_member=None):
        super(Plot, self).__init__()
        self.household = household
        self.household_member = household_member
        self.household_structure = household_structure
        try:
            self.plot = household_member.household_structure.household.plot
        except AttributeError:
            try:
                self.plot = household_structure.household.plot
            except AttributeError:
                try:
                    self.plot = household.plot
                except AttributeError:
                    self.plot = plot
        self.update_plots()
        self.update_households()
        self.update_members()
        self.update_plot_log()

    def __repr__(self):
        return ('{0}(plot={1.plot!r})').format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.plot!s}'.format(self)

    @property
    def unique_key(self):
        return self.plot_identifier

    def customize_for_csv(self):
        self.data['household_members'] = [hm.internal_identifier for hm in self.household_members]
        super(Plot, self).customize_for_csv()
        del self.data['plot']
        del self.data['plot_logs']
        del self.data['household_member']
        del self.data['household_structure']
        del self.data['household_structures']
        del self.data['households']
        del self.data['household']

    def update_plots(self):
        if self.plot.plot_identifier.endswith('0000-00'):
            self.plot_identifier = '{}CLIN-IC'.format(self.plot.plot_identifier[:2])
        else:
            self.plot_identifier = self.plot.plot_identifier
        self.gps_lat_target = self.plot.gps_target_lat
        self.gps_lon_target = self.plot.gps_target_lon
        self.gps_lat_actual = self.plot.gps_lat
        self.gps_lon_actual = self.plot.gps_lon
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

    def update_plot_log(self):
        self.confirmed_date = None
        if self.confirmed == CONFIRMED:
            try:
                self.confirmed_date = PlotLog.objects.filter(plot=self.plot).order_by('created')[0].created
            except IndexError:
                print 'Warning: Missing plot log for confirmed plot {}.'.format(self.plot)
        try:
            self.plot_logs = PlotLogEntry.objects.filter(plot_log=PlotLog.objects.get(plot=self.plot))
        except (PlotLog.DoesNotExist, PlotLogEntry.DoesNotExist):
            self.plot_logs = []
        self.plot_log_first_date = min(list(set([
            l.report_datetime.date() for l in self.plot_logs
            ] or [self.plot.modified.date()])))
        self.plot_log_dates = list(set([l.report_datetime.date() for l in self.plot_logs] or [self.plot.modified.date()]))
        self.plot_log_dates.sort()
        self.plot_log_status = [p.log_status for p in self.plot_logs]

    def update_households(self):
        self.households = Household.objects.filter(plot=self.plot)
        self.household_structures = HouseholdStructure.objects.filter(household__plot=self.plot).order_by('survey__survey_slug')
        self.household_identifiers = [h.household_identifier for h in self.households]
        self.household_count = self.households.count()

    def update_members(self):
        self.household_members = HouseholdMember.objects.filter(household_structure__household__plot=self.plot)
        for survey in Survey.objects.all():
            setattr(
                self, '{}_{}'.format('member_count', survey.survey_abbrev.lower()),
                self.household_members.filter(household_structure__survey__survey_slug=survey.survey_slug).count()
                )
            setattr(
                self, '{}_{}'.format('members_eligible', survey.survey_abbrev.lower()),
                self.household_members.filter(household_structure__survey__survey_slug=survey.survey_slug, eligible_member=True).count()
                )
            setattr(
                self, '{}_{}'.format('members_eligible_for_survey', survey.survey_abbrev.lower()),
                self.household_members.filter(household_structure__survey__survey_slug=survey.survey_slug, eligible_subject=True).count()
                )
