from edc.device.dispatch.models import DispatchContainerRegister

from ..constants import RESIDENTIAL_HABITABLE, NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE, FIVE_PERCENT
from ..models import HouseholdStructure, Plot


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

    def get_replaceable_items_for_view(self):
        pass

    @property
    def household_structure(self):
        return self._household_structure

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
#         if self.plot.status == RESIDENTIAL_HABITABLE and (self.household_structure.failed_enumeration and not self.household_structure.eligible_members):
#             replaceable = True
        return replaceable

    @property
    def replaceable_plot(self):
        """Returns True if a plot meets the criteria to be replaced by a plot."""
        replaceable = False
        if self.plot.replaces and self.plot.status in [NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE]:
            replaceable = True
        return replaceable

    def replaceable_households(self, survey):
        """Returns a list of households that meet the criteria to be replaced by a plot."""
        replaceable_households = []
        for household_structure in HouseholdStructure.objects.filter(survey=survey):
            self.household_structure = household_structure
            if self.replaceable_household:
                replaceable_households.append(household_structure.household)
        return replaceable_households

    def replaceable_plots(self):
        """Returns a list of plots that meet the criteria to be replaced by a plot."""
        replaceable_plots = []
        for plot in Plot.objects.filter(selected=FIVE_PERCENT):
            self.plot = plot
            if self.replaceable_plot:
                replaceable_plots.append(self.plot)
        return replaceable_plots

    def replaced_by(self, household_structure):
        """Returns the plot instance that was used to replace the household_structure or None."""
        try:
            return Plot.objects.get(replaces=household_structure.household.household_identifier)
        except Plot.DoesNotExist:
            return None

    def replacement_reason(self, replacement_item):
        """check the reason why a plot or household is being replaced."""
        reason = None
        if self.is_absent(replacement_item):
            reason = 'all members are absent'
        elif self.household_structure.refused_enumeration:
            reason = 'HOH refusal'
        elif self.no_eligible_rep(replacement_item):
            reason = 'no eligible members'
        return reason
