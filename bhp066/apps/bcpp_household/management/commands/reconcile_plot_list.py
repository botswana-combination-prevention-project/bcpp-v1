import os

from django.core.management.base import BaseCommand, CommandError

from apps.bcpp_household.constants import CONFIRMED, UNCONFIRMED
from apps.bcpp_household.models import Plot


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community_name e.g otse>, <file_path e.g /home/django/>'
    help = 'Prints a report that shows reconciliation statistics of plot lists belonging to 75%, 20%, 5%.'

    def handle(self, *args, **options):
        if not args or len(args) < 2:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        file_path = str(args[1]) + str(community_name.title())
        file_75_list = file_path + '_75pct.csv'
        file_20_list = file_path + '_20pct.csv'
        file_5_list = file_path + '_backup.csv'
        if not (os.path.exists(file_75_list) and os.path.exists(file_20_list) and os.path.exists(file_5_list)):
            raise IOError("Files do not exist in the path: {0}.", format(args[1]))
        else:
            plots_75_list = open(file_75_list, 'r')
            lines_75 = plots_75_list.readlines()
            lines_75.pop(0)
            plot_identifiers_75 = []
            action_confirmed_75 = 0
            action_unconfirmed_75 = 0
            new_added_plots_75 = []
            removed_plots_75 = []
            for line in lines_75:
                line = line.split(',')
                plot_identifier = line[-4][1:-1]
                plot_identifiers_75.append(plot_identifier)
            current_db_plots_75 = Plot.objects.filter(selected=None, community=community_name)
            current_db_plot_identifiers_75 = []
            for plot in current_db_plots_75:
                current_db_plot_identifiers_75.append(plot.plot_identifier)
            if len(set(current_db_plot_identifiers_75)) > len(set(plot_identifiers_75)):
                new_added_plots_75 = set(current_db_plot_identifiers_75) - set(plot_identifiers_75)
            if len(set(current_db_plot_identifiers_75)) < len(set(plot_identifiers_75)):
                removed_plots_75 = set(plot_identifiers_75) - set(current_db_plot_identifiers_75)
            plots = Plot.objects.filter(plot_identifier__in=current_db_plot_identifiers_75)
            for plot in plots:
                if plot.action == CONFIRMED:
                    action_confirmed_75 += 1
                elif plot.action == UNCONFIRMED:
                    action_unconfirmed_75 += 1
            # The 20 percent plot list
            plots_20_list = open(file_20_list, 'r')
            lines_20 = plots_20_list.readlines()
            lines_20.pop(0)
            action_confirmed_20 = 0
            action_unconfirmed_20 = 0
            plot_identifiers_20 = []
            new_added_plots_20 = []
            removed_plots_20 = []
            for line in lines_20:
                line = line.split(',')
                plot_identifier = line[-4][1:-1]
                plot_identifiers_20.append(plot_identifier)
            current_db_plots_20 = Plot.objects.filter(selected=1, community=community_name)
            current_db_plot_identifiers_20 = []
            for plot in current_db_plots_20:
                current_db_plot_identifiers_20.append(plot.plot_identifier)
            if len(set(current_db_plot_identifiers_20)) > len(set(plot_identifiers_20)):
                new_added_plots_20 = set(current_db_plot_identifiers_20) - set(plot_identifiers_20)
            if len(set(current_db_plot_identifiers_20)) < len(set(plot_identifiers_20)):
                removed_plots_20 = set(plot_identifiers_20) - set(current_db_plot_identifiers_20)
            plots = Plot.objects.filter(plot_identifier__in=current_db_plot_identifiers_20)
            for plot in plots:
                if plot.action == CONFIRMED:
                    action_confirmed_20 += 1
                elif plot.action == UNCONFIRMED:
                    action_unconfirmed_20 += 1
            # The 5 percent plot list
            plots_5_list = open(file_5_list, 'r')
            lines_5 = plots_5_list.readlines()
            lines_5.pop(0)
            action_confirmed_5 = 0
            action_unconfirmed_5 = 0
            plot_identifiers_5 = []
            new_added_plots_5 = []
            removed_plots_5 = []
            for line in lines_5:
                line = line.split(',')
                plot_identifier = line[-4][1:-1]
                plot_identifiers_5.append(plot_identifier)
            current_db_plots_5 = Plot.objects.filter(selected=2, community=community_name)
            current_db_plot_identifiers_5 = []
            for plot in current_db_plots_5:
                current_db_plot_identifiers_5.append(plot.plot_identifier)
            if len(set(current_db_plot_identifiers_5)) > len(set(plot_identifiers_5)):
                new_added_plots_5 = set(current_db_plot_identifiers_5) - set(plot_identifiers_5)
            if len(set(current_db_plot_identifiers_5)) < len(set(plot_identifiers_5)):
                removed_plots_5 = set(plot_identifiers_5) - set(current_db_plot_identifiers_5)
            plots = Plot.objects.filter(plot_identifier__in=current_db_plot_identifiers_5)
            for plot in plots:
                if plot.action == CONFIRMED:
                    action_confirmed_5 += 1
                elif plot.action == UNCONFIRMED:
                    action_unconfirmed_5 += 1
            print "*******************"
            print "* 75 percent data *"
            print "*******************"
            print "plot list in the 75 percent still the same: ", len(
                set(current_db_plot_identifiers_75 + plot_identifiers_75)
                ) == len(current_db_plot_identifiers_75) == len(plot_identifiers_75)
            print "Total number of plots initially loaded as 75 percent: ", len(plot_identifiers_75)
            print "Total current number of plots in the 75 percent: ", len(current_db_plot_identifiers_75)
            print "Total number of added to plots 75 percent: ", len(new_added_plots_75)
            print "Total number of plots removed from the 75 percent: ", len(removed_plots_75)
            print "Total confirmed plots in the 75 percent: ", action_confirmed_75
            print "Total unconfirmed plots in the 75 percent: ", action_unconfirmed_75
            print "*******************"
            print "* 20 percent data *"
            print "*******************"
            print "plot list in the 20 percent still the same: ", len(
                set(current_db_plot_identifiers_20 + plot_identifiers_20)
                ) == len(current_db_plot_identifiers_20) == len(plot_identifiers_20)
            print "Total number of plots initially loaded as 20 percent: ", len(plot_identifiers_20)
            print "Total current number of plots in the 20 percent in the db: ", len(current_db_plot_identifiers_20)
            print "Total number of added to plots 20 percent: ", len(new_added_plots_20)
            print "Total number of plots removed from the 20 percent: ", len(removed_plots_20)
            print "Total confirmed plots in the 20 percent: ", action_confirmed_20
            print "Total unconfirmed plots in the 20 percent: ", action_unconfirmed_20
            print "******************"
            print "* 5 percent data *"
            print "******************"
            print "Is the plot list in the 5 percent still the same: ", len(
                set(current_db_plot_identifiers_5 + plot_identifiers_5)
                ) == len(current_db_plot_identifiers_5) == len(plot_identifiers_5)
            print "Total number of added to plots 5 percent: ", len(new_added_plots_5)
            print "Total number of plots removed from the 5 percent: ", len(removed_plots_5)
            print "Total confirmed plots in the 5 percent: ", action_confirmed_5
            print "Total unconfirmed plots in the 5 perecnt: ", action_unconfirmed_5
