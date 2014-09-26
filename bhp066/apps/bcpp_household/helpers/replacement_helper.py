import socket

from datetime import datetime

from django.db.models import Min, Max
from django.db import transaction

from edc.device.sync.helpers import TransactionHelper
from edc.device.sync.utils import load_producer_db_settings

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_survey.models import Survey

from ..constants import (RESIDENTIAL_HABITABLE, NON_RESIDENTIAL,
                         RESIDENTIAL_NOT_HABITABLE, FIVE_PERCENT,
                         ELIGIBLE_REPRESENTATIVE_ABSENT, VISIT_ATTEMPTS)
from ..models import Plot, Household, HouseholdStructure, ReplacementHistory, HouseholdLogEntry


class ReplacementHelper(object):
    """Check replaceable household and plots, then replace them.

    Attributes involved:

        plot.replaced_by: plot identifier of the new replacement plot
        plot.replaces: plot or household identifier of the old plot
            or household being replaced.
        plot.htc
        household.replaced_by: plot identifier of the new replacement plot

        plot.status  # user
        plot.plot_identifier  # save
        plot.dispatched_to  # dispatch
        household.household_identifier  # save
        household_structure.enumerated  # post_save
        household_structure.refused_enumeration  # post_save
        household_structure.no_informant  # post_save
        household_structure.failed_enumeration   # post_save
        household_structure.failed_enumeration_attempts   # post_save
        household_structure.household
        household_structure.eligible_members   # post_save
        household_structure.visit_attempts
    """

    def __init__(self, plot=None, household_structure=None):
        """Sets household_structure, household and plot.

        The household_structure takes precedent."""
        self._household_structure = None
        self._plot = None
        self.household_structure = household_structure
        if not household_structure:
            self.plot = plot

    def __repr__(self):
        return 'ReplacementHelper({})'.format(self.household_structure or self.plot)

    def __str__(self):
        return '()'

    @property
    def household_structure(self):
        return self._household_structure

    @household_structure.setter
    def household_structure(self, household_structure):
        """Sets the household structure, househol and plot otherwise
        sets all to None."""
        self._household_structure = household_structure
        try:
            self.household = household_structure.household
            self.plot = household_structure.household.plot
        except AttributeError:
            self.household = None
            self.plot = None

    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, plot):
        """Sets the plot attr but raises an exception if an attempt
        is made to change the plot attr set by the household structure setter."""
        try:
            if plot != self.household_structure.household.plot:
                raise TypeError('Plot cannot be changed explicitly if household_structure is already set.')
            self._plot = plot
        except AttributeError:
            self._plot = plot

    @property
    def survey(self):
        """Returns the first survey."""
        first_survey_start_datetime = Survey.objects.all().aggregate(
            datetime_start=Min('datetime_start')).get('datetime_start')
        return Survey.objects.get(datetime_start=first_survey_start_datetime)

    @property
    def replaceable_household(self):
        """Returns True if a household meets the criteria to be replaced by a plot.

        * Plot where the household resides must be RESIDENTIAL_HABITABLE.
        * household_structure.refused_enumeration is set in the post_save signal
          when the houswehold_refusal is submitted"""
        replaceable = False
        if self.household.replaced_by or self.household.enrolled:
            return False
        try:
            if self.plot.status == RESIDENTIAL_HABITABLE:
                if self.household_structure.refused_enumeration:
                    replaceable = True
                elif self.all_eligible_members_refused:
                    replaceable = True
                elif self.eligible_representative_absent:
                    replaceable = True
                elif self.all_eligible_members_absent:
                    replaceable = True
                elif (self.household_structure.failed_enumeration and
                      self.household_structure.no_informant):
                    replaceable = True
        except AttributeError as attribute_error:
            if 'has no attribute \'household\'' in str(attribute_error):
                pass
        return replaceable

    @property
    def replaceable_plot(self):
        """Returns True if the plot meets the criteria to be replaced by another plot."""
        # TODO: a plot, that is added as a replacement, itself can be replaced if not yet enrolled
        # and residential habitable
        replaceable = False
        if (not self.plot.replaced_by and self.plot.replaces and
                self.plot.status in [NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE]):
            replaceable = True
        return replaceable

    def replaceable_households(self, producer_name):
        """Returns a list of households that meet the criteria to be replaced by a plot."""
        replaceable_households = []
        for self.household_structure in HouseholdStructure.objects.filter(
                survey=self.survey,
                household__replaced_by__isnull=True):
            if producer_name == self.plot.dispatched_to:
                if self.replaceable_household:
                    replaceable_households.append(self.household)
        # reset instance attributes
        self.household_structure = None
        return replaceable_households

    def replaceable_plots(self, producer_name=None):
        """Returns a list of existing BHS plots that meet the criteria
        to be replaced by a new plot from the pool of 5 percent.

        A plot is replaceable if it is from the 5 percent, has been
        allocated to BHS for confirmation and potential enrollment
        (replaces__isnull=False, bhs=False) and meets other criteria
        (self.replaceable_plot=True).

        plot.dispatched_to is a property method which should indicate
        that the plot is currently dispatched"""
        replaceable_plots = []
        for self.plot in Plot.objects.filter(selected=FIVE_PERCENT,
                                             replaces__isnull=False,
                                             bhs__isnull=True).order_by('plot_identifier'):
            if not producer_name and self.replaceable_plot:
                replaceable_plots.append(self.plot)
            elif self.plot.dispatched_to == producer_name and self.replaceable_plot:
                replaceable_plots.append(self.plot)
        self.plot = None
        return replaceable_plots

    def replace_household(self, producer_name):
        """Replaces a household with a plot.

        This takes a list of replaceable households and plots that
        are to replace those households. The replacement history model
        is updated to specify when the household was replaced and what
        it was replaced with."""
        new_bhs_plots = []
        if not producer_name:
            raise TypeError('Expected a valid producer. Got None.')
        load_producer_db_settings()
        if not TransactionHelper().outgoing_transactions(socket.gethostname(),
                                                         producer_name,
                                                         raise_exception=True):
            available_plots = self.available_plots
            for household in self.replaceable_households(producer_name):
                try:
                    # confirm household exists on remote
                    Household.objects.using(producer_name).get(
                        household_identifier=household.household_identifier)
                    plot = available_plots.pop()
                    with transaction.atomic():
                        household.replaced_by = plot.plot_identifier
                        plot.replaces = household.household_identifier
                        household.save(update_fields=['replaced_by'], using='default')
                        plot.save(update_fields=['replaces'], using='default')
                        ReplacementHistory.objects.using('default').create(
                            replacing_item=plot.plot_identifier,
                            replaced_item=household.household_identifier,
                            replacement_datetime=datetime.now(),
                            replacement_reason=self.household_replacement_reason())
                        household.save(update_fields=['replaced_by'], using=producer_name)
                        new_bhs_plots.append(plot)
                        TransactionHelper().outgoing_transactions(socket.gethostname(),
                                                                  producer_name).delete()
                except Household.DoesNotExist:  # does not exist on producer
                    pass
                except IndexError as index_error:
                    if 'pop from empty list' in str(index_error):
                        break
                    raise
        return new_bhs_plots

    @property
    def available_plots(self):
        """Returns a list of plot instances that are available to be used
        as replacement plots."""
        available_plots = []
        for plot in Plot.objects.filter(selected=FIVE_PERCENT, replaces=None):
            try:
                ReplacementHistory.objects.using('default').get(
                    replacing_item=plot.plot_identifier)
            except ReplacementHistory.DoesNotExist:
                available_plots.append(plot)
        return available_plots

    def replace_plot(self, producer_name):
        """Replaces a plot with a plot.

        This takes a list of replaceable plots and replaces each with a plot.
        The replacement history model is also update to keep track of what replace what."""
        new_bhs_plots = []
        if not producer_name:
            raise TypeError('Expected a valid producer. Got None.')
        load_producer_db_settings()
        if not TransactionHelper().outgoing_transactions(socket.gethostname(),
                                                         producer_name,
                                                         raise_exception=True):
            available_plots = self.available_plots
            for replaceable_plot in self.replaceable_plots(producer_name):
                try:
                    available_plot = available_plots.pop()
                    Plot.objects.using(producer_name).get(
                        plot_identifier=available_plot.plot_identifier)
                    with transaction.atomic():
                        replaceable_plot.replaced_by = available_plot.plot_identifier
                        replaceable_plot.htc = True  # If a plot is replaced it goes to CDC
                        replaceable_plot.save(update_fields=['replaced_by', 'htc'], using='default')
                        replaceable_plot.save(update_fields=['replaced_by', 'htc'], using=producer_name)
                        available_plot.replaces = replaceable_plot.plot_identifier
                        available_plot.save(update_fields=['replaces'], using='default')
                        ReplacementHistory.objects.create(
                            replacing_item=available_plot.plot_identifier,
                            replaced_item=replaceable_plot.plot_identifier,
                            replacement_datetime=datetime.now(),
                            replacement_reason='plot for plot replacement')
                        new_bhs_plots.append(available_plot)
                        TransactionHelper().outgoing_transactions(socket.gethostname(),
                                                                  producer_name).delete()
                except Plot.DoesNotExist:
                    pass
                except IndexError as index_error:
                    if 'pop from empty list' in str(index_error):
                        break
                    raise
        return new_bhs_plots

    @property
    def all_eligible_members_refused(self):
        """Returns True if all eligible members refuse participation in BHS."""
        if self.household_structure.enumerated:
            refused_members_count = HouseholdMember.objects.filter(
                household_structure=self.household_structure,
                eligible_member=True,
                refused=True).count()
            if refused_members_count:
                eligible_member_count = HouseholdMember.objects.filter(
                    household_structure=self.household_structure,
                    eligible_member=True).count()
                return eligible_member_count == refused_members_count
        return False

    @property
    def all_eligible_members_absent(self):
        """Returns True if all eligible members are absent
        after 3 attempts."""
        if self.household_structure.enumerated:
            absent_member_count = HouseholdMember.objects.filter(
                household_structure=self.household_structure,
                eligible_member=True,
                absent=True,
                visit_attempts__gte=VISIT_ATTEMPTS).count()
            if absent_member_count:
                eligible_member_count = HouseholdMember.objects.filter(
                    household_structure=self.household_structure,
                    eligible_member=True).count()
                return eligible_member_count == absent_member_count
        return False

    @property
    def eligible_representative_absent(self):
        """Returns True if no household age eligible representative is available after
        (x) attempts (e.g., VISIT_ATTEMPTS=3) to complete the HouseholdAssessment.

        Information comes from the last HouseholdLog entry for a household that has
        not been enumerated and has been visited at least 3 times"""
        eligible_representative_absent = False
        if (not self.household_structure.enumerated
                and self.household_structure.failed_enumeration_attempts >= VISIT_ATTEMPTS):
            try:
                report_datetime = HouseholdLogEntry.objects.filter(
                    household_log__household_structure=self.household_structure
                    ).aggregate(Max('report_datetime')).get('report_datetime__max')
                HouseholdLogEntry.objects.get(
                    household_log__household_structure=self.household_structure,
                    report_datetime=report_datetime,
                    household_status=ELIGIBLE_REPRESENTATIVE_ABSENT)
                eligible_representative_absent = True
            except HouseholdLogEntry.DoesNotExist:
                pass
        return eligible_representative_absent

    def household_replacement_reason(self):
        """Returns the reason why a plot or household is being replaced."""
        reason = None
        if self.all_eligible_members_absent:
            reason = 'all members are absent'
        elif self.household_structure.refused_enumeration:
            reason = 'HOH refusal'
        elif self.all_eligible_members_refused:
            reason = 'all eligible members refused'
        elif self.eligible_representative_absent:
            reason = 'no eligible representative'
        elif self.household_structure.failed_enumeration and self.household_structure.no_informant:
            reason = 'no informant'
        return reason
