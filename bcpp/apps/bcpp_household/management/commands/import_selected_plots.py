import os

from django.core.management.base import BaseCommand, CommandError

from bhp066.apps.bcpp_household.models import Plot


def create_plots(plot_list, community_name, selected=None):
    """D"""
    number_of_plots = 0
    htc = False
    selection_percentage = None
    if not selected:
        htc = True
        selection_percentage = "75%"
    elif selected == 1:
        selection_percentage = "20%"
    elif selected == 2:
        selection_percentage = "5%"
    for plot in plot_list:
        plot = plot.split(',')
        idnt = plot[0]
        idnt = idnt.replace('\"', '')
        gps_target_lat = float(plot[1])
        gps_target_lon = float(plot[2])
        if Plot.objects.filter(plot_identifier=idnt):
            print "Plot {0} already created".format(idnt)
        else:
            plot_in_75 = Plot(plot_identifier=idnt, gps_target_lat=gps_target_lat,
                              gps_target_lon=gps_target_lon, community=community_name,
                              htc=htc, selected=selected)
            plot_in_75.save()
        number_of_plots += 1
        print "plots created {0} out of {1} of the {2}".format(number_of_plots, len(plot_list), selection_percentage)


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse>, file path e.g /Users/ckgathi/source/bhp066_project/bhp066/'
    help = 'Creates plots from csv files containing plot lists of the 5 percent, 20 percent and 75 percent.'

    def handle(self, *args, **options):
        if not args or len(args) < 2:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        file_path = str(args[1]) + str(community_name)
        file_75_list = file_path + '_75pct.csv'
        file_20_list = file_path + '_20pct.csv'
        file_5_list = file_path + '_backup.csv'
        if not (os.path.exists(file_75_list) and os.path.exists(file_20_list) and os.path.exists(file_5_list)):
            raise IOError("Files do not exist in the path: {0}.", format(args[1]))
        else:
            # read a list of 75% plots from file
            plots_75 = open(file_75_list, 'r')
            plots_75_list = plots_75.readlines()
            plots_75_list.pop(0)
            # read a list of 20% plots from file
            plots_20 = open(file_20_list, 'r')
            plots_20_list = plots_20.readlines()
            plots_20_list.pop(0)

            # read a list of 5% plots from file
            plots_5 = open(file_5_list, 'r')
            plots_5_list = plots_5.readlines()
            plots_5_list.pop(0)

            # Create plots
            create_plots(plots_75_list, community_name)
            create_plots(plots_20_list, community_name, 1)
            create_plots(plots_5_list, community_name, 2)
            print "Success!!!"
