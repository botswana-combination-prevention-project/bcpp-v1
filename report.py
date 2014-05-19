from django.db.models import Max, Min
import collections
from apps.bcpp_household.constants import NO_HOUSEHOLD_INFORMANT, REFUSED_ENUMERATION
from django.db.models.loading import get_model
from apps.bcpp_household.helpers import ReplacementHelper
replacement_values = {}
accessment_forms_to_fill = 0
household_refusal_forms_to_fill = 0
replaceble_households = 0
replaced_households = 0
replaced_plots = 0
replaceble_plots = 0
plt = Plot.objects.all()
replacement_helper = ReplacementHelper()
first_survey_start_datetime = Survey.objects.all().aggregate(datetime_start=Min('datetime_start')).get('datetime_start')
survey = Survey.objects.get(datetime_start=first_survey_start_datetime)
for plot in plt:
    replacement_helper.plot = plot
    if replacement_helper.replaceable_plot and not plot.replaced_by:
        replaceble_plots += 1
    if plot.replaced_by:
        replaced_plots += 1
for household_structure in get_model('bcpp_household', 'HouseholdStructure').objects.filter(survey=survey):
    household_status = None
    household_log = get_model('bcpp_household', 'HouseholdLog').objects.filter(household_structure=household_structure)
    replacement_helper.household_structure = household_structure
    if replacement_helper.replaceable and not household_structure.household.replaced_by:
        replaceble_households += 1
    if household_structure.household.replaced_by:
        replaced_households += 1
    try:
        report_datetime = get_model('bcpp_household', 'HouseholdLogEntry').objects.filter(household_log=household_log).aggregate(Max('report_datetime')).get('report_datetime__max')
        lastest_household_log_entry = get_model('bcpp_household', 'HouseholdLogEntry').objects.get(household_log__household_structure=household_structure, report_datetime=report_datetime)
        household_status = lastest_household_log_entry.household_status
    except get_model('bcpp_household', 'HouseholdLogEntry').DoesNotExist:
        household_status = None
    if household_structure.failed_enumeration_attempts == 3:
        if not get_model('bcpp_household', 'HouseholdAssessment').objects.filter(household_structure=household_structure) and household_status == NO_HOUSEHOLD_INFORMANT:
            accessment_forms_to_fill += 1
    elif household_status == REFUSED_ENUMERATION:
        household_refusal_forms_to_fill += 1
replacement_values['1. Total replaced households'] = replaced_households
replacement_values['2. Total replaced plots'] = replaced_plots
replacement_values['3. Total number of replaceble households'] = replaceble_households
replacement_values['4. Total household accessment pending'] = accessment_forms_to_fill
replacement_values['5. Total Household refusals'] = household_refusal_forms_to_fill
replacement_values = collections.OrderedDict(sorted(replacement_values.items()))

print "******************"
print "* 75 percent data *"
print "******************"
import csv
plots_75_list = open('Otse_75pct.csv', 'r')
lines_75 = plots_75_list.readlines()
lines_75.pop(0)
plot_identifiers_75 = []
new_added_plots_75 = []
removed_plots_75 = []
for line in lines_75:
    line = line.split(',')
    plot_identifier = line[-4][1:-1]
    plot_identifiers_75.append(plot_identifier)
current_db_plots_75 = Plot.objects.filter(selected=None)
current_db_plot_identifiers_75 = []
for plot in current_db_plots_75:
    current_db_plot_identifiers_75.append(plot.plot_identifier)
if len(set(current_db_plot_identifiers_75)) > len(set(plot_identifiers_75)):
    new_added_plots_75 = set(current_db_plot_identifiers_75) - set(plot_identifiers_75)
if len(set(current_db_plot_identifiers_75)) < len(set(plot_identifiers_75)):
    removed_plots_75 = set(plot_identifiers_75) - set(current_db_plot_identifiers_75)
print "plot list still the same: ", len(set(current_db_plot_identifiers_75 + plot_identifiers_75)) == len(current_db_plot_identifiers_75) == len(plot_identifiers_75)
print "Total Plot sent to CDC: ", len(plot_identifiers_75)
print "Total current plots that shows to have been sent to CDC: ", len(current_db_plot_identifiers_75)
print "Total added plots: ", len(new_added_plots_75)
print "Total removed plots: ", len(removed_plots_75)
print "*******************"
print "* 20 percent data *"
print "*******************"
plots_20_list = open('Otse_20pct.csv', 'r')
lines_20 = plots_20_list.readlines()
lines_20.pop(0)
plot_identifiers_20 = []
new_added_plots_20 = []
removed_plots_20 = []
for line in lines_20:
    line = line.split(',')
    plot_identifier = line[-4][1:-1]
    plot_identifiers_20.append(plot_identifier)
current_db_plots_20 = Plot.objects.filter(selected=1)
current_db_plot_identifiers_20 = []
for plot in current_db_plots_20:
    current_db_plot_identifiers_20.append(plot.plot_identifier)
if len(set(current_db_plot_identifiers_20)) > len(set(plot_identifiers_20)):
    new_added_plots20 = set(current_db_plot_identifiers_20) - set(plot_identifiers_20)
if len(set(current_db_plot_identifiers_20)) < len(set(plot_identifiers_20)):
    removed_plots_20 = set(plot_identifiers_20) - set(current_db_plot_identifiers_20)
print "plot list still the same: ", len(set(current_db_plot_identifiers_20 + plot_identifiers_20)) == len(current_db_plot_identifiers_20) == len(plot_identifiers_20)
print "Total Plots for BHS 20 percent: ", len(plot_identifiers_20)
print "Total current Plots for BHS 20 percent in the db: ", len(current_db_plot_identifiers_20)
print "Total added plots: ", len(new_added_plots_20)
print "Total removed plots: ", len(removed_plots_20)
print "******************"
print "* 5 percent data *"
print "******************"
plots_5_list = open('Otse_backup.csv', 'r')
lines_5 = plots_5_list.readlines()
lines_5.pop(0)
plot_identifiers_5 = []
new_added_plots_5 = []
removed_plots_5 = []
for line in lines_5:
    line = line.split(',')
    plot_identifier = line[-4][1:-1]
    plot_identifiers_5.append(plot_identifier)
current_db_plots_5 = Plot.objects.filter(selected=2)
current_db_plot_identifiers_5 = []
for plot in current_db_plots_5:
    current_db_plot_identifiers_5.append(plot.plot_identifier)
if len(set(current_db_plot_identifiers_5)) > len(set(plot_identifiers_5)):
    new_added_plots5 = set(current_db_plot_identifiers_5) - set(plot_identifiers_5)
if len(set(current_db_plot_identifiers_5)) < len(set(plot_identifiers_5)):
    removed_plots_5 = set(plot_identifiers_5) - set(current_db_plot_identifiers_5)
print "plot list still the same: ", len(set(current_db_plot_identifiers_5 + plot_identifiers_5)) == len(current_db_plot_identifiers_5) == len(plot_identifiers_5)
print "Total Plots for BHS 20 percent: ", len(plot_identifiers_5)
print "Total current Plots for BHS 20 percent in the db: ", len(current_db_plot_identifiers_5)
print "Total added plots: ", len(new_added_plots_5)
print "Total removed plots: ", len(removed_plots_5)
