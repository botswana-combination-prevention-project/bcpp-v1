import collections
import datetime
from django.db.models import Count
from edc.device.dispatch.models import DispatchContainerRegister

from bhp066.apps.bcpp_household.constants import (
    CONFIRMED, UNCONFIRMED, INACCESSIBLE, NON_RESIDENTIAL,
    RESIDENTIAL_NOT_HABITABLE, RESIDENTIAL_HABITABLE)
from bhp066.apps.bcpp_household.models import Plot, PlotLogEntry, HouseholdStructure

from .base_operational_report import BaseOperationalReport


class OperationalPlots(BaseOperationalReport):

    def report_data(self):

        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        plt = Plot.objects.all()
        dispatched_identifiers = [container.container_identifier for container in DispatchContainerRegister.objects.filter(is_dispatched=True)]
        total_dispatched = Plot.objects.filter(community__icontains=self.community,
                                               modified__gte=self.date_from, modified__lte=self.date_to,
                                               user_modified__icontains=self.ra_username,
                                               plot_identifier__in=dispatched_identifiers)
        self.data_dict['1. Total No. of plots'] = plt.filter(community__icontains=self.community,
                                               modified__gte=self.date_from, modified__lte=self.date_to,
                                               user_modified__icontains=self.ra_username).count()
        self.data_dict['2. Total plots dispatched'] = len(total_dispatched)
        #data_dict['1. Plots reached'] = reached
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
        self.data_dict['3. Plots accessible'] = accessible_plots
        in_accessible_plots = plt.filter(community__icontains=self.community,
                                      modified__gte=self.date_from, modified__lte=self.date_to,
                                      user_modified__icontains=self.ra_username,
                                      status=INACCESSIBLE).count()
        self.data_dict['4. Plots in-accessible'] = in_accessible_plots
        self.data_dict['5. Plots in-accessible once'] = not_accessible_plots1
        self.data_dict['6. Plots in-accessible twice'] = not_accessible_plots2
        self.data_dict['7. Plots in-accessible thrice'] = not_accessible_plots3
        confirmed = plt.filter(action=CONFIRMED, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.data_dict['8. Plots confirmed'] = confirmed
        un_confirmed = plt.filter(action=UNCONFIRMED, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.data_dict['9. Plots not confirmed'] = un_confirmed
        plots_enmerated_structures = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=True)
        plots_enumerated = plots_enmerated_structures.values('household__plot__plot_identifier').annotate(dcount=Count('household__plot__plot_identifier'))
        self.data_dict['91. Enumerated plots'] = len(plots_enumerated)
        res_habitable = plt.filter(status=RESIDENTIAL_HABITABLE, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.data_dict['92. Residential habitable plots'] = res_habitable
        res_not_habitable = plt.filter(status=RESIDENTIAL_NOT_HABITABLE, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.data_dict['93. Residential not habitable plots'] = res_not_habitable
        non_residential = plt.filter(status=NON_RESIDENTIAL, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.data_dict['94. Not residential plots'] = non_residential
        enrolled_plots = plt.filter(bhs=True, community__icontains=self.community,
                                        modified__gte=self.date_from, modified__lte=self.date_to,
                                        user_modified__icontains=self.ra_username).count()
        self.data_dict['95. Enrolled plots'] = enrolled_plots
#         not_reached = (plt.filter(action=UNCONFIRMED, community__icontains=self.community,
#                                                 modified__gte=self.date_from, modified__lte=self.date_to,
#                                                 user_modified__icontains=self.ra_username).count())
#         self.data_dict['12. Plots not reached'] = not_reached
        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values