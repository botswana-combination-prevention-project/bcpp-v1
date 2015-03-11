import collections
import datetime
from django.db.models import Count
from django.contrib.auth.models import User
from edc.core.bhp_birt_reports.classes import OperationalReportUtilities
from edc.device.dispatch.models import DispatchContainerRegister

from apps.bcpp_household.constants import (CONFIRMED, UNCONFIRMED, INACCESSIBLE, NON_RESIDENTIAL,
                                           RESIDENTIAL_NOT_HABITABLE, RESIDENTIAL_HABITABLE)
from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_household.models import Plot, PlotLogEntry, HouseholdStructure


class OperationalSpecimen():

    def __init__(self, request):
        self.plot_info = {}
        self.utilities = OperationalReportUtilities()
        self.date_from = self.utilities.date_format_utility(request.GET.get('date_from', ''), '1960-01-01')
        self.date_to = self.utilities.date_format_utility(request.GET.get('date_to', ''), '2099-12-31')
        self.ra_username = request.GET.get('ra', '')
        self.community = request.GET.get('community', '')
        self.previous_ra = self.ra_username
        self.previous_community = self.community
        self.communities = None
        self.ra_usernames = None

#     def operational_plots(self):
#         pass

    def return_communities(self):
        return self.communities

    def return_ra_usernames(self):
        return self.ra_usernames

    def return_plot_data(self):

        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        plt = Plot.objects.all()
        dispatched_identifiers = [container.plot_identifier for container in DispatchContainerRegister.objects.filter(is_dispatched=True)]
        total_dispatched = Plot.objects.filter(community__icontains=self.community,
                                               modified__gte=self.date_from, modified__lte=self.date_to,
                                               user_modified__icontains=self.ra_username,
                                               plot_identifier__in=dispatched_identifiers)
        self.plot_info['1. Total No. of plots'] = plt.filter(community__icontains=self.community,
                                               modified__gte=self.date_from, modified__lte=self.date_to,
                                               user_modified__icontains=self.ra_username).count()
        self.plot_info['2. Total plots dispatched'] = len(total_dispatched)
        #plot_info['1. Plots reached'] = reached
        inaccessible_log_entry = PlotLogEntry.objects.filter(plot_log__plot__community__icontains=self.community,
                                      plot_log__plot__status=INACCESSIBLE,
                                      modified__gte=self.date_from, modified__lte=self.date_to,
                                      user_modified__icontains=self.ra_username,
                                      log_status=INACCESSIBLE)
        annotated_log_enry = inaccessible_log_entry.values('plot_log__plot__plot_identifier').annotate(dcount=Count('plot_log__plot__plot_identifier'))
        not_accessible_plots1 = 0
        not_accessible_plots2 = 0
        not_accessible_plots3 = 0
        for group in annotated_log_enry:
            if group.get('dcount') == 1:
                not_accessible_plots1 += 1
            if group.get('dcount') == 2:
                not_accessible_plots2 += 1
            if group.get('dcount') == 3:
                not_accessible_plots3 += 1
        accessible_plots = plt.filter(community__icontains=self.community,
                                      modified__gte=self.date_from, modified__lte=self.date_to,
                                      user_modified__icontains=self.ra_username).exclude(status=INACCESSIBLE).count()
        self.plot_info['3. Plots accessible'] = accessible_plots
        in_accessible_plots = plt.filter(community__icontains=self.community,
                                      modified__gte=self.date_from, modified__lte=self.date_to,
                                      user_modified__icontains=self.ra_username,
                                      status=INACCESSIBLE).count()
        self.plot_info['4. Plots in-accessible'] = in_accessible_plots
        self.plot_info['5. Plots in-accessible once'] = not_accessible_plots1
        self.plot_info['6. Plots in-accessible twice'] = not_accessible_plots2
        self.plot_info['7. Plots in-accessible thrice'] = not_accessible_plots3
        confirmed = plt.filter(action=CONFIRMED, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.plot_info['8. Plots confirmed'] = confirmed
        un_confirmed = plt.filter(action=UNCONFIRMED, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.plot_info['9. Plots not confirmed'] = un_confirmed
        plots_enmerated_structures = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=True)
        plots_enumerated = plots_enmerated_structures.values('household__plot__plot_identifier').annotate(dcount=Count('household__plot__plot_identifier'))
        self.plot_info['91. Enumerated plots'] = len(plots_enumerated)
        res_habitable = plt.filter(status=RESIDENTIAL_HABITABLE, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.plot_info['92. Residential habitable plots'] = res_habitable
        res_not_habitable = plt.filter(status=RESIDENTIAL_NOT_HABITABLE, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.plot_info['93. Residential not habitable plots'] = res_not_habitable
        non_residential = plt.filter(status=NON_RESIDENTIAL, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.plot_info['94. Not residential plots'] = non_residential
        enrolled_plots = plt.filter(bhs=True, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.plot_info['95. Enrolled plots'] = enrolled_plots
#         not_reached = (plt.filter(action=UNCONFIRMED, community__icontains=self.community,
#                                                 modified__gte=self.date_from, modified__lte=self.date_to,
#                                                 user_modified__icontains=self.ra_username).count())
#         self.plot_info['12. Plots not reached'] = not_reached
        values = collections.OrderedDict(sorted(self.plot_info.items()))
        communities = []
        if (self.previous_community.find('----') == -1) and (not self.previous_community == ''):  # Passing filtered results
            # communities = [community[0].lower() for community in  COMMUNITIES]
            for community in  COMMUNITIES:
                if community[0].lower() != self.previous_community:
                    communities.append(community[0])
            communities.insert(0, self.previous_community)
            communities.insert(1, '---------')
        else:
            communities = [community[0].lower() for community in  COMMUNITIES]
            communities.insert(0, '---------')
        self.communities = communities
        ra_usernames = []
        if (self.previous_ra.find('----') == -1) and (not self.previous_ra == ''):
            for ra_name in [user.username for user in User.objects.filter(groups__name='field_research_assistant')]:
                if ra_name != self.previous_ra:
                    ra_usernames.append(ra_name)
            ra_usernames.insert(0, self.previous_ra)
            ra_usernames.insert(1, '---------')
        else:
            ra_usernames = [user.username for user in User.objects.filter(groups__name='field_research_assistant')]
            ra_usernames.insert(0, '---------')
        self.ra_usernames = ra_usernames
        return values