import os

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_household.models import Plot
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey


class ExportPlotToValidateTest(TestCase):

    def setUp(self):
            try:
                site_lab_profiles.register(BcppSubjectProfile())
            except AlreadyRegisteredLabProfile:
                pass
            BcppAppConfiguration()
            site_lab_tracker.autodiscover()
            BcppSubjectVisitSchedule().build()

            self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration

    def test_export_plot_to_validate(self):
        """Tests the if the exported plots are the right number and the correct ones."""

        community_name = 'lentsweletau'
        # Plot statistics in the database
        db_all_plots = Plot.objects.all()  # Total number of plots in the database
        db_plots = []
        db_plots_75pct = []
        db_plots_25pct = []
        db_plots_20pct = []
        db_plots_5pct = []
        count_db_75 = 0
        count_db_25 = 0
        count_db_20 = 0
        count_db_5 = 0
        # Plot statistics in the csv files
        csv_all_plots = []
        csv_plots_75pct = []
        csv_plots_25pct = []
        csv_plots_20pct = []
        csv_plots_5pct = []

        for plot in db_all_plots:
            if plot.selected == '1':
                db_plots_20pct.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
                db_plots.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
                count_db_20 += 1
            elif plot.selected == '2':
                db_plots_5pct.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
                db_plots.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
                count_db_5 += 1
            elif plot.selected:
                db_plots_25pct.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
                db_plots.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
                count_db_25 += 1
            elif not plot.selected:
                db_plots_75pct.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
                db_plots.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
                count_db_75 += 1

        file_path = '/Users/ckgathi/source/community_plot_list/'

        file_path = file_path + str(community_name.title())
        file_75_list = file_path + '_75pct.csv'
        file_25_list = file_path + '_25pct.csv'
        file_20_list = file_path + '_20pct.csv'
        file_5_list = file_path + '_backup.csv'
        if not (os.path.exists(file_75_list) and os.path.exists(file_25_list) and os.path.exists(file_20_list) and os.path.exists(file_5_list)):
            raise IOError("Files do not exist in the path: {0}.", format(file_path))
        else:
            plots_75_list = open(file_75_list, 'r')
            lines_75 = plots_75_list.readlines()
            lines_75.pop(0)
            line_75 = lines_75.split('|')
            for plot in line_75:
                csv_plots_75pct.append([plot[0], float(plot[1]), float(plot[2]), plot[3][0]])
                csv_all_plots.append([plot[0], float(plot[1]), float(plot[2]), plot[3][0]])

            plots_25_list = open(file_25_list, 'r')
            lines_25 = plots_25_list.readlines()
            lines_25.pop(0)
            line_25 = lines_25.split('|')
            for plot in line_25:
                csv_plots_25pct.append([plot[0], float(plot[1]), float(plot[2]), plot[3][0]])
                csv_all_plots.append([plot[0], float(plot[1]), float(plot[2]), plot[3][0]])

            plots_20_list = open(file_20_list, 'r')
            lines_20 = plots_20_list.readlines()
            lines_20.pop(0)
            line_20 = lines_20.split('|')
            for plot in line_20:
                csv_plots_20pct.append([plot[0], float(plot[1]), float(plot[2]), plot[3][0]])
                csv_all_plots.append([plot[0], float(plot[1]), float(plot[2]), plot[3][0]])

            plots_5_list = open(file_5_list, 'r')
            lines_5 = plots_5_list.readlines()
            lines_5.pop(0)
            line_5 = lines_5.split('|')
            for plot in line_5:
                csv_plots_5pct.append([plot[0], float(plot[1]), float(plot[2]), plot[3][0]])
                csv_all_plots.append([plot[0], float(plot[1]), float(plot[2]), plot[3][0]])
            # Compare plot list in the database and in the csv files of the 75 percent
            self.assertEqual(csv_plots_75pct, db_plots_75pct)
            self.assertEqual(len(csv_plots_75pct), count_db_75)
            # Compare plot list in the database and in the csv files of the 25 percent
            self.assertEqual(csv_plots_25pct, db_plots_25pct)
            self.assertEqual(len(csv_plots_25pct), count_db_25)
            # Compare plot list in the database and in the csv files of the 20 percent
            self.assertEqual(csv_plots_20pct, db_plots_20pct)
            self.assertEqual(len(csv_plots_20pct), count_db_20)
            # Compare plot list in the database and in the csv files of the 5 percent
            self.assertEqual(csv_plots_5pct, db_plots_5pct)
            self.assertEqual(len(csv_plots_5pct), count_db_5)

            self.assertEqual(csv_all_plots, db_plots)
            self.assertEqual(len(csv_all_plots), db_all_plots.count())
