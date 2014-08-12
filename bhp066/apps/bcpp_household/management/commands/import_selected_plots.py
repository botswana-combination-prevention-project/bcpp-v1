import os

from django.core.management.base import BaseCommand, CommandError

from apps.bcpp_household.models import Plot


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse>, file path e.g /Users/ckgathi/source/bhp066_project/bhp066/'
    help = 'Creates plots from csv files containing plot lists of the 5 percent, 20 percent and 75 percent.'

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
#             lines_75 = lines_75[0].split('\n')
            lines_75.pop(0)
            num_75_pct = 0
            num_20_pct = 0
            for plot in lines_75:
                plot = plot.split(',')
                idnt = plot[0]
                idnt = idnt.replace('\"', '')
                gps_target_lat = float(plot[1])
                gps_target_lon = float(plot[2])
                if Plot.objects.filter(plot_identifier=idnt):
                    print "Plot {0} already created".format(idnt)
                else:
                    plot_in_75 = Plot(plot_identifier=idnt, gps_target_lat=gps_target_lat, gps_target_lon=gps_target_lon, community=community_name, htc=True)
                    plot_in_75.save()
                num_75_pct += 1
                print "plots created {0} out of {1} in the 75%".format(num_75_pct, len(lines_75))
            plots_20_list = open(file_20_list, 'r')
            lines_20 = plots_20_list.readlines()
#             lines_20 = lines_20[0].split('\r')
            total_plots_20 = len(lines_20)
            lines_20.pop(0)
            print lines_20
            num_20_pct = 0
            for plot in lines_20:
                plot = plot.split(',')
                idnt = plot[0]
                idnt = idnt.replace('\"', '')
                gps_target_lat = float(plot[1])
                gps_target_lon = float(plot[2])
                if Plot.objects.filter(plot_identifier=idnt):
                    print "Plot {0} already created".format(idnt)
                else:
                    lines_20 = Plot(plot_identifier=idnt, gps_target_lat=gps_target_lat, gps_target_lon=gps_target_lon, selected=1, community=community_name)
                    lines_20.save()
                num_20_pct += 1
                print "plots created {0} out of {1} in the 20%".format(num_20_pct, total_plots_20)
            # The 5 percent plot list
            plots_5_list = open(file_5_list, 'r')
            lines_5 = plots_5_list.readlines()
#             lines_5 = lines_5[0].split('\r')
            lines_5.pop(0)
            num_5_pct = 0
            total_lines_5 = len(lines_5)
            for plot in lines_5:
                plot = plot.split(',')
                idnt = plot[0]
                idnt = idnt.replace('\"', '')
                gps_target_lat = float(plot[1])
                gps_target_lon = float(plot[2])
                if Plot.objects.filter(plot_identifier=idnt):
                    print "Plot {0} already created".format(idnt)
                else:
                    lines_5 = Plot(plot_identifier=idnt, gps_target_lat=gps_target_lat, gps_target_lon=gps_target_lon, selected=2, community=community_name)
                    lines_5.save()
                num_5_pct += 1
                print "plots created {0} out of {1} in the 5%".format(num_5_pct, total_lines_5)
            print "Success!!!"
