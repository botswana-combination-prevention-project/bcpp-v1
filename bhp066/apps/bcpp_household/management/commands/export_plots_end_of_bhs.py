import csv

from django.db.models import Min, Max
from django.core.management.base import BaseCommand, CommandError

from apps.bcpp_survey.models import Survey

from apps.bcpp_household.choices import NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE, ELIGIBLE_REPRESENTATIVE_PRESENT, RESIDENTIAL_HABITABLE
from apps.bcpp_household.models import Plot, Household, HouseholdStructure, HouseholdLogEntry


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse>'
    help = 'Creates a  two csv files of plot lists, 25 percent and 75 percent. List that goes to CDC.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        cdc_plots = []
        first_survey_start_datetime = Survey.objects.all().aggregate(datetime_start=Min('datetime_start')).get('datetime_start')
        survey = Survey.objects.get(datetime_start=first_survey_start_datetime)
        enrolled = []
        household_reason = []
        erolled_plot = 0
        not_enrolled = 0
        confirmed = 0
        unconfirmed = 0
        plots = Plot.objects.filter(community=community_name, selected__isnull=False)
        cdc_plots.append(['plot_identifier', 'action', 'status', 'household_count', 'gps_target_lat', 'gps_target_lon', 'enrolled', 'comment'])
        for plot in plots:
            if plot.status in ['inaccessible', None]:
                cdc_plots.append([plot.plot_identifier, plot.action, plot.status, plot.household_count, plot.gps_target_lat, plot.gps_target_lon, 'No', plot.status])
                unconfirmed += 1
                not_enrolled += 1
            elif plot.status in [NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE]:
                cdc_plots.append([plot.plot_identifier, plot.action, plot.status, plot.household_count, plot.gps_target_lat, plot.gps_target_lon, 'No', plot.status])
                if plot.action == 'unconfirmed':
                    unconfirmed += 1
                elif plot.action == 'confirmed':
                    confirmed += 1
                not_enrolled += 1
            if plot.household_count > 0 and plot.action == 'confirmed' and plot.status == RESIDENTIAL_HABITABLE:
                confirmed += 1
                households = Household.objects.filter(plot=plot)
                household_structures = HouseholdStructure.objects.filter(household__in=households, survey=survey)
                household_reason = []
                enrolled = []
                for household_structure in household_structures:
                    enrolled.append(household_structure.enrolled)
                    try:
                        report_datetime = HouseholdLogEntry.objects.filter(household_log__household_structure=household_structure).aggregate(Max('report_datetime')).get('report_datetime__max')
                        lastest_household_log_entry = HouseholdLogEntry.objects.get(household_log__household_structure=household_structure, report_datetime=report_datetime)
                        if lastest_household_log_entry.household_status == ELIGIBLE_REPRESENTATIVE_PRESENT:
                            if household_structure.all_eligible_members_refused:
                                household_reason.append("all members refused")
                            elif household_structure.all_eligible_members_absent:
                                household_reason.append("all members absent")
                            else:
                                household_reason.append("all members refused")
                        else:
                            household_reason.append(lastest_household_log_entry.household_status)
                    except HouseholdLogEntry.DoesNotExist:
                        household_reason.append('not visited')
                enrolled = list(set(enrolled))
                if True in enrolled:
                    erolled_plot += 1
#                     if not plot.htc:
#                         plot.htc = True
#                         plot.save()
                    cdc_plots.append([plot.plot_identifier, plot.action, plot.status, plot.household_count, plot.gps_target_lat, plot.gps_target_lon, 'Yes', ''])
                elif not enrolled[0]:
                    cdc_plots.append([plot.plot_identifier, plot.action, plot.status, plot.household_count, plot.gps_target_lat, plot.gps_target_lon, 'No', '; '.join(household_reason)])
                    not_enrolled += 1
                else:
                    raise TypeError()
        for plot_values in cdc_plots:
            if not plot_values[0] == 'plot_identifier' and plot_values[6] == 'No':
                plot_instance = Plot.objects.get(plot_identifier=plot_values[0])
#                 plot_instance.htc = True
#                 plot_instance.save()
        filename_25_pct = str(community_name) + '_25_pct.csv'
        filename_75_pct = str(community_name) + '_75_pct.csv'
        cdc_file = open(filename_25_pct, 'wb')
        writer = csv.writer(cdc_file, delimiter=',')
        writer.writerows(cdc_plots)
        plots_75_pct = Plot.objects.filter(community=community_name, selected__isnull=True)
        cdc_plots_75_pct = []
        cdc_plots_75_pct.append(['Plot identifier', 'Plot confirmation status', 'Plot status', 'Original latitude coordinate', 'Original longitude coordinate'])
        for plot in plots_75_pct:
            cdc_plots_75_pct.append([plot.plot_identifier, plot.action, plot.status, plot.gps_target_lat, plot.gps_target_lon])
        cdc_file_75_pct = open(filename_75_pct, 'wb')
        writer_75_pct = csv.writer(cdc_file_75_pct, delimiter=',')
        writer_75_pct.writerows(cdc_plots_75_pct)
        # Report of the statistics
        print "Total plots in the Database: ", Plot.objects.filter(community=community_name).count()
        print "Total number of plots in the 75 percent: ", plots_75_pct.count()
        print "Total number of plots in the 25 percent: ", plots.count()
        print "Total number of confirmed plots in the 25 percent:", confirmed
        print "Total number of unconfirmed plots in the 25 percent:", unconfirmed
        print "total number of enrolled plots in the 25 percent: ", erolled_plot
        print "Total number of plots not enrolled in the 25 percent: ", not_enrolled
