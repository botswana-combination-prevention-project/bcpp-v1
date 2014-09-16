import socket

from datetime import datetime

from django.db.models import Min, Max

from edc.device.sync.exceptions import PendingTransactionError
from edc.device.sync.models import OutgoingTransaction
from edc.device.device.classes import Device

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_survey.models import Survey

from ..constants import (RESIDENTIAL_HABITABLE, NON_RESIDENTIAL,
                         RESIDENTIAL_NOT_HABITABLE, FIVE_PERCENT, RARELY_OCCUPIED,
                         ELIGIBLE_REPRESENTATIVE_ABSENT, VISIT_ATTEMPTS)
from ..models import Plot, HouseholdStructure, ReplacementHistory, HouseholdLogEntry, HouseholdAssessment


class ReplacementHelper(object):
    """Check replaceable household and plots, then replace them.

    Attributes involved:
        plot.status
        household.replaced_by
        household_structure.enumerated
        household_structure.refused_enumeration
        household_structure.no_informant
        household_structure.failed_enumeration_attempts
    """

    def __init__(self, plot=None, household_structure=None):
        self.household_structure = household_structure
        try:
            self.household = household_structure.household
        except AttributeError:
            self.household = None
        try:
            self.plot = household_structure.household.plot
        except AttributeError:
            self.plot = plot

    def __repr__(self):
        return 'ReplacementHelper()'

    def __str__(self):
        return '()'

    def outgoing_transactions(self, producer):
        """Checks if a producer has OutgoingTransactions."""
        if OutgoingTransaction.objects.using(producer).filter(
                is_ignored=False, is_consumed_server=False):
            raise PendingTransactionError
        return False

    def delete_server_transactions_on_producer(self, destination):
        if Device.is_server():
            try:
                OutgoingTransaction.objects.using(destination).filter(
                    is_ignored=False, is_consumed_server=False, hostname_created=socket.gethostname()).delete()
            except OutgoingTransaction.DoesNotExist:
                pass

    @property
    def survey(self):
        """Returns the first survey."""
        first_survey_start_datetime = Survey.objects.all().aggregate(
            datetime_start=Min('datetime_start')).get('datetime_start')
        return Survey.objects.get(datetime_start=first_survey_start_datetime)

    @property
    def replaceable_household(self):
        """Returns True if a household meets the criteria to be replaced by a plot."""
        replaceable = False
        try:
            if self.household_structure.household.plot.status == RESIDENTIAL_HABITABLE:
                if ((self.household_structure.refused_enumeration or
                        self.all_eligible_members_refused) and
                        not self.household_structure.household.replaced_by):
                    replaceable = True
                elif ((self.eligible_representative_absent or
                      self.all_eligible_members_absent) and
                      not self.household_structure.household.replaced_by):
                    replaceable = True
                elif (self.household_structure.failed_enumeration and
                      self.household_structure.no_informant and
                      not self.household_structure.household.replaced_by):
                    replaceable = True
                elif self.vdc_form_status == RARELY_OCCUPIED:
                    replaceable = False
                elif self.household_structure.enumerated and not self.household_structure.eligible_members:
                    replaceable = False
                elif self.household_structure.enrolled:
                    replaceable = False
        except AttributeError as attribute_error:
            if 'has no attribute \'household\'' in str(attribute_error):
                pass
        return replaceable

    @property
    def replaceable_plot(self):
        """Returns True if a plot meets the criteria to be replaced by another plot."""
        replaceable = False
        if (not self.plot.replaced_by and self.plot.replaces and
                self.plot.status in [NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE]):
            replaceable = True
        elif not self.plot.replaces and self.plot.status in [NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE]:
            replaceable = False
        return replaceable

    def replaceable_households(self, producer_name):
        """Returns a list of households that meet the criteria to be replaced by a plot."""
        replaceable_households = []
        for self.household_structure in HouseholdStructure.objects.filter(survey=self.survey).order_by('household__household_identifier'):
            if producer_name == self.household_structure.household.plot.dispatched_to:
                if self.replaceable_household:
                    if not self.household_structure.household.replaced_by:
                        replaceable_households.append(self.household_structure.household)
        return replaceable_households

    def replaceable_plots(self, producer_name):
        """Returns a list of plots that meet the criteria to be replaced by a plot."""
        replaceable_plots = []
        for self.plot in Plot.objects.filter(selected=FIVE_PERCENT).order_by('plot_identifier'):
            if producer_name == self.plot.dispatched_to:
                if self.replaceable_plot:
                    replaceable_plots.append(self.plot)
        return replaceable_plots

    def replaced_by(self, household_structure):
        """Returns the plot instance that was used to replace the household_structure or None."""
        try:
            return Plot.objects.get(replaces=household_structure.household.household_identifier)
        except Plot.DoesNotExist:
            return None

    @property
    def available_plots(self):
        return Plot.objects.filter(
            selected=FIVE_PERCENT, replaced_by=None, replaces=None)

    def replace_household(self, destination):
        """Replaces a household with a plot.

        This takes a list of replaceable households and plots that
        are to replace those households. The replacement history model
        is updated to specify when the household was replaced and what
        it was replaced with."""
        new_bhs_plots = []
        if not destination:
            raise TypeError('Expected a valid producer. Got None.')
        if not self.outgoing_transactions(destination):
            available_plots = self.available_plots
            for index, household in enumerate(self.replaceable_households(destination)):
                try:
                    household.replaced_by = available_plots[index].plot_identifier
                    available_plots[index].replaces = household.household_identifier
                    household.save(update_fields=['replaced_by'], using='default')
                    available_plots[index].save(update_fields=['replaces'], using='default')
                    household.save(update_fields=['replaced_by'], using=destination)
                    household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey)
                    # Creates a history of replacement
                    ReplacementHistory.objects.create(
                        replacing_item=available_plots[index].plot_identifier,
                        replaced_item=household.household_identifier,
                        replacement_datetime=datetime.now(),
                        replacement_reason=self.household_replacement_reason(household_structure))
                    new_bhs_plots.append(available_plots[index])
                    # delete transactions created when saving to remote
                    self.delete_server_transactions_on_producer(destination)
                except IndexError:
                    break
        return new_bhs_plots

    def replace_plot(self, destination):
        """Replaces a plot with a plot.

        This takes a list of replaceable plots and replaces each with a plot.
        The replacement history model is also update to keep track of what replace what."""
        new_bhs_plots = []
        if not destination:
            raise TypeError('Expected a valid producer. Got None.')
        if not self.outgoing_transactions(destination):
            # replaceable_plot is a plot that is eligible for replacement.
            # new_bhs_plot is a plot that is available to replace replaceable_plot.
            available_plots = self.available_plots
            for index, replaceable_plot in enumerate(self.replaceable_plots(destination)):
                try:
                    replaceable_plot.replaced_by = available_plots[index].plot_identifier
                    replaceable_plot.htc = True  # If a plot is replaced it goes to CDC
                    replaceable_plot.save(update_fields=['replaced_by'], using='default')
                    replaceable_plot.save(update_fields=['replaced_by'], using=destination)
                    available_plots[index].replaces = replaceable_plot.plot_identifier
                    available_plots[index].save(update_fields=['replaces'], using='default')
                    # Creates a history of replacement
                    ReplacementHistory.objects.create(
                        replacing_item=available_plots[index].plot_identifier,
                        replaced_item=replaceable_plot.plot_identifier,
                        replacement_datetime=datetime.now(),
                        replacement_reason='plot for plot replacement')
                    new_bhs_plots.append(available_plots[index])
                    # delete transactions created when saving to remote
                    self.delete_server_transactions_on_producer(destination)
                except IndexError:
                    break
        return new_bhs_plots

    def household_replacement_reason(self):
        """check the reason why a plot or household is being replaced."""
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

    @property
    def all_eligible_members_refused(self):
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

    @property
    def vdc_form_status(self):
        if self.household_structure.no_informant:
            try:
                return HouseholdAssessment.objects.get(
                    household_structure=self.household_structure).vdc_househould_status
            except HouseholdAssessment.DoesNotExist:
                pass
        return None
