import csv
from django.db.models import Min, Max
from apps.bcpp_household.choices import NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE, ELIGIBLE_REPRESENTATIVE_PRESENT
cdc_plots = []
first_survey_start_datetime = Survey.objects.all().aggregate(datetime_start=Min('datetime_start')).get('datetime_start')
survey = Survey.objects.get(datetime_start=first_survey_start_datetime)
enrolled = []
household_reason = []
lis = 0
plots = Plot.objects.filter(selected__isnull=False)
cdc_plots.append(['Plot identifier', 'Original latitude coordinate', 'Original longitude coordinate', 'Confirmation latitude coordiante', 'confirmation longitude coordiante', 'Reason not enrolled'])
for plot in plots:
    if plot.status in ['inaccesseble', NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE]:
        cdc_plots.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.gps_lat, plot.gps_lon, plot.status])
    if plot.household_count > 0:
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
                    household_reason.append('Refusal/Absentees/Undecided')
                else:
                    household_reason.append(lastest_household_log_entry.household_status)
            except HouseholdLogEntry.DoesNotExist:
                pass
        lis = list(set(enrolled))
        if lis[0] == None and len(lis) == 1:
            cdc_plots.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.gps_lat, plot.gps_lon, household_reason])
cdc_file = open('cdc_plot_list.csv', 'wb')
writer = csv.writer(cdc_file)
writer.writerows(cdc_plots)

