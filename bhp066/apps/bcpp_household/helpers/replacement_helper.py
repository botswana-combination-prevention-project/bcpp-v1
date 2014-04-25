from datetime import datetime

from django.db.models.loading import get_model
from django.db.models import Min

from edc.device.dispatch.models import DispatchContainerRegister

from apps.bcpp_survey.models import Survey

from ..constants import RESIDENTIAL_HABITABLE, NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE, FIVE_PERCENT


class ReplacementHelper(object):

    def __init__(self):
        self._household_structure = None
        self._plot = None
        self.household = None

    def __repr__(self):
        return 'ReplacementHelper()'

    def __str__(self):
        return '()'

    @property
    def producer(self):
        """Returns the producer where the plot is dispatched to."""
        producer = None
        if DispatchContainerRegister.objects.filter(container_identifier=self.plot.plot_identifier):
            producer = producer.producer
        return producer

    def synchronized(self, producer):
        """Check if a producer has been synchronized."""
        pass

    @property
    def household_structure(self):
        return self._household_structure

    @property
    def survey(self):
        first_survey_start_datetime = Survey.objects.all().aggregate(datetime_start=Min('datetime_start')).get('datetime_start')
        survey = Survey.objects.get(datetime_start=first_survey_start_datetime)
        return survey

    @household_structure.setter
    def household_structure(self, household_structure):
        """Sets the household structure (and household and plot using the household structure)."""
        self._household_structure = household_structure
        self.household = household_structure.household
        self._plot = household_structure.household.plot  # NOTE: accessing _plot instance attribute.

    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, plot):
        """Sets the plot and clears the household and household structure."""
        self._plot = plot
        self._household_structure = None  # NOTE: accessing _household_structure instance attribute.
        self.household = None

    @property
    def replaceable(self):
        """Returns True if a household or a plot meets the criteria to be replaced by plot."""
        if self.household_structure:
            return self.replaceable_household
        else:
            return self.replaceable_plot

    @property
    def replaceable_household(self):
        """Returns True if a household meets the criteria to be replaced by a plot."""
        replaceable = False
        if self.plot.status == RESIDENTIAL_HABITABLE:
            if self.household_structure.refused_enumeration or self.household_structure.all_eligible_members_refused:
                replaceable = True
            elif self.household_structure.eligible_representative_absent or self.household_structure.all_eligible_members_absent:
                replaceable = True
            elif self.household_structure.failed_enumeration and self.household_structure.no_informant:
                replaceable = True
        return replaceable

    @property
    def replaceable_plot(self):
        """Returns True if a plot meets the criteria to be replaced by a plot."""
        replaceable = False
        if self.plot.replaces and self.plot.status in [NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE]:
            replaceable = True
        return replaceable

    def replaceable_households(self, survey, producer_name):
        """Returns a list of households that meet the criteria to be replaced by a plot."""
        replaceable_households = []
        for household_structure in get_model('bcpp_household', 'HouseholdStructure').objects.filter(survey=survey):
            self.household_structure = household_structure
            if producer_name.split('-')[0] == household_structure.household.plot.producer_dispatched_to:
                if self.replaceable_household:
                    if not household_structure.household.replaced_by:
                        replaceable_households.append(household_structure.household)
        return replaceable_households

    def replaceable_plots(self, producer_name):
        """Returns a list of plots that meet the criteria to be replaced by a plot."""
        replaceable_plots = []
        for plot in get_model('bcpp_household', 'Plot').objects.filter(selected=FIVE_PERCENT):
            self.plot = plot
            if producer_name.split('-')[0] == plot.producer_dispatched_to:
                if self.replaceable_plot:
                    replaceable_plots.append(self.plot)
        return replaceable_plots

    def replaced_by(self, household_structure):
        """Returns the plot instance that was used to replace the household_structure or None."""
        try:
            return get_model('bcpp_household', 'Plot').objects.get(replaces=household_structure.household.household_identifier)
        except get_model('bcpp_household', 'Plot').DoesNotExist:
            return None

    def replace_household(self, replaceble_households, destination):
        """"Replaces a household with a plot.

        This takes a list of replaceble households and plots that are to replace those households.
        The replacement history model is udated to specify when the household was replaced and what it was replaced with."""
        plots = get_model('bcpp_household', 'Plot').objects.filter(selected=FIVE_PERCENT, replaced_by=None, replaces=None)
        replacing_plots = []
        for household, plot in zip(replaceble_households, plots):
#             if self.synchronized(destination):
            household.replaced_by = plot.plot_identifier
            plot.replaces = household.household_identifier
            household.save()
            plot.save()
            household.save(using=destination)
            plot.save(using=destination)
            household_structure = get_model('bcpp_household', 'HouseholdStructure').objects.get(household=household, survey=self.survey)
            # Creates a history of replacement
            get_model('bcpp_household', 'ReplacementHistory').objects.create(
                    replacing_item=plot.plot_identifier,
                    replaced_item=household.household_identifier,
                    replacement_datetime=datetime.now(),
                    replacement_reason=self.household_replacement_reason(household_structure))
            replacing_plots.append(plot)
        return replacing_plots

    def replace_plot(self, replaceble_plots, destination):
        """Replaces a plot with a plot.

        This takes a list of replaceble plots and replaces each with a plot.
        The replacement history model is also update to keep track of what replace what."""
        plots = get_model('bcpp_household', 'Plot').objects.filter(selected=FIVE_PERCENT, replaced_by=None, replaces=None)
        replacing_plots = []
        #plot_a  is a plot that is being replaced. plot_b is the plot that replaces plot_a.
        for plot_a, plot_b in zip(replaceble_plots, plots):
#             if self.synchronized(destination):
            plot_a.repalced_by = plot_b.plot_identifier
            plot_b.replaces = plot_a.plot_identifier
            plot_a.save()
            plot_b.save()
            plot_a.save(using=destination)
            plot_b.save(using=destination)
            # Creates a history of replacement
            get_model('bcpp_household', 'ReplacementHistory').objects.create(
                    replacing_item=plot_b.plot_identifier,
                    replaced_item=plot_a.plot_identifier,
                    replacement_datetime=datetime.now(),
                    replacement_reason='Invalid plot replacement')
            replacing_plots.append(plot_b)
        return replacing_plots

    def household_replacement_reason(self, household_structure):
        """check the reason why a plot or household is being replaced."""
        reason = None
        if household_structure.all_eligible_members_absent:
            reason = 'all members are absent'
        elif household_structure.refused_enumeration:
            reason = 'HOH refusal'
        elif household_structure.all_eligible_members_refused:
            reason = 'all eligible members refused'
        elif household_structure.eligible_representative_absent:
            reason = 'no eligible Representative'
        elif household_structure.failed_enumeration and household_structure.no_informant:
            reason = 'No informant'
        return reason
