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
