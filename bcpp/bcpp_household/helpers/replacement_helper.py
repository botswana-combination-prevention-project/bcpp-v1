import socket

from datetime import datetime

from django.db.models import Min, Max
from django.db import transaction, OperationalError
from django.db.utils import ConnectionDoesNotExist

from edc.device.dispatch.models.dispatch_item_register import DispatchItemRegister
from edc.device.sync.helpers import TransactionHelper
from edc.device.sync.models import Producer
from edc.device.sync.utils import load_producer_db_settings
from edc.device.sync.exceptions import PendingTransactionError

from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_survey.models import Survey

from ..constants import (RESIDENTIAL_HABITABLE, NON_RESIDENTIAL,
                         RESIDENTIAL_NOT_HABITABLE, FIVE_PERCENT,
                         ELIGIBLE_REPRESENTATIVE_ABSENT, VISIT_ATTEMPTS)
from ..exceptions import ReplacementError
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
        self._replacement_reason = None
        self.recently_replaced = {'households': [], 'plots': []}
        self.household_structure = household_structure
        if not household_structure:
            self.plot = plot

    def __repr__(self):
        return 'ReplacementHelper(plot={0.plot!r}, household_structure={0.household_structure!r})'.format(self)

    def __str__(self):
        return '({!r})'.format(self.household_structure or self.plot)

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
        # self._replacement_reason = None

    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, plot):
        """Sets the plot attr but raises an exception if an attempt
        is made to change the plot attr set by the household structure setter."""
        try:
            if plot != self.household_structure.household.plot:
                raise TypeError('Plot cannot be changed explicitly if household_structure is '
                                'already set. Got {} != {}'.format(plot, self.household_structure.household.plot))
            self._plot = plot
        except AttributeError:
            self._plot = plot
        # self._replacement_reason = None

    @property
    def survey(self):
        """Returns the first survey."""
        first_survey_start_datetime = Survey.objects.using('default').all().aggregate(
            datetime_start=Min('datetime_start')).get('datetime_start')
        return Survey.objects.using('default').get(datetime_start=first_survey_start_datetime)

    @property
    def household_replacement_reason(self):
        replacement_reason = None
        if self.plot.status == RESIDENTIAL_HABITABLE:
            if self.household_structure.refused_enumeration:
                replacement_reason = 'household refused_enumeration'
            elif self.all_eligible_members_refused:
                replacement_reason = 'household all_eligible_members_refused'
            elif self.eligible_representative_absent:
                replacement_reason = 'household eligible_representative_absent'
            elif self.all_eligible_members_absent:
                replacement_reason = 'household all_eligible_members_absent'
            elif (self.household_structure.failed_enumeration and
                  self.household_structure.no_informant):
                replacement_reason = 'household failed_enumeration no_informant'
        return replacement_reason

    @property
    def plot_replacement_reason(self):
        return 'replaced. NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE 5% plot'

    def replaceable_ressidential_habitables(self):
        """Replaceable residential habitable households."""
        replaceable = False
        if self.plot.status == RESIDENTIAL_HABITABLE:
            if self.household_structure.refused_enumeration:
                replaceable = True
                # self.replacement_reason = 'household refused_enumeration'
            elif self.all_eligible_members_refused:
                replaceable = True
                # self.replacement_reason = 'household all_eligible_members_refused'
            elif self.eligible_representative_absent:
                replaceable = True
                # self.replacement_reason = 'household eligible_representative_absent'
            elif self.all_eligible_members_absent:
                replaceable = True
                self.replacement_reason = 'household all_eligible_members_absent'
            elif (self.household_structure.failed_enumeration and
                  self.household_structure.no_informant):
                replaceable = True
                # self.replacement_reason = 'household failed_enumeration no_informant'
        return replaceable

    @property
    def replaceable_household(self):
        """Returns True if a household meets the criteria to be replaced by a plot.

        * Plot where the household resides must be RESIDENTIAL_HABITABLE.
        * household_structure.refused_enumeration is set in the post_save signal
          when the houswehold_refusal is submitted"""
        replaceable = False
        # self.replacement_reason = None
        if self.household.replaced_by or self.household.enrolled:
            return False
        if self.household_replacement_reason:
            replaceable = True
        try:
            replaceable = self.replaceable_ressidential_habitables()
        except AttributeError as attribute_error:
            if 'has no attribute \'household\'' in str(attribute_error):
                pass
        return replaceable

    @property
    def replaceable_plot(self):
        """Returns True if the plot, from the 5% pool, meets the criteria to be replaced by another plot.

        Also, a plot, that is added as a replacement, itself can be replaced if not yet enrolled
        and residential habitable."""
        replaceable = False
        if not self.plot.replaced_by and not self.plot.bhs and self.plot.selected == FIVE_PERCENT:
            if self.plot.status in [NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE] and self.plot.replaces:
                replaceable = True
        return replaceable

    def replaceable_households(self, using_producer=None):
        """Returns a generator that yields a tuple of (household, dispatch_item_register)
        of households dispatched to a given \'producer_name\'
        that meet the criteria to be replaced by a plot.

        Args:
          * producer_name: name of a valid producer (Default: None).
        """
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot')
        if using_producer:
            options.update(producer__settings_key=using_producer)
        for dispatch_item_register in DispatchItemRegister.objects.using('default').filter(**options):
            for self.household_structure in HouseholdStructure.objects.using('default').filter(
                    survey__survey_name=self.survey.survey_name,
                    household__replaced_by__isnull=True,
                    household__plot__pk=dispatch_item_register.item_pk):
                if self.replaceable_household:
                    household_structure = self.household_structure
                    self.household_structure = None
                    yield household_structure.household, dispatch_item_register
                self.household_structure = None

    def dispatched_plot_ids(self, using_producer):
        return DispatchItemRegister.objects.values('item_identifier').filter(
            producer__settings_key=using_producer, is_dispatched=True)

    def replaceable_plots(self, using_producer=None):
        """Returns a generator that yields a tuple of (plot, dispatch_item_register)
        of existing BHS plots that meet the criteria to be replaced by a new plot
        from the pool of 5 percent.

        Args:
          * producer_name: name of a valid producer (Default: None).

        A plot is replaceable if it is from the 5 percent, has been
        allocated to BHS for confirmation and potential enrollment
        (replaces__isnull=False, bhs=False) and meets other criteria
        (self.replaceable_plot=True)."""
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot')
        if using_producer:
            options.update(producer__settings_key=using_producer)
        for dispatch_item_register in DispatchItemRegister.objects.using('default').filter(**options):
            try:
                self.plot = Plot.objects.using('default').get(
                    selected=FIVE_PERCENT,
                    bhs__isnull=True,
                    pk=dispatch_item_register.item_identifier)
                if self.replaceable_plot:
                    plot = self.plot
                    self.plot = None
                    yield plot, dispatch_item_register
                self.plot = None
            except Plot.DoesNotExist:
                pass

    @property
    def available_plots(self):
        """Returns a generator that holds plot instances that are available to be used
        as replacement plots."""
        for plot in Plot.objects.using('default').filter(
                selected=FIVE_PERCENT, replaces=None).order_by('plot_identifier'):
            try:
                ReplacementHistory.objects.using('default').get(
                    replacing_item=plot.plot_identifier)
            except ReplacementHistory.DoesNotExist:
                if not plot.dispatched_to and not plot.section == 'E':
                    yield plot

    def replace_household(self, using_producer):
        """Returns a list of plots used to replace households for a
        given \'producer_name\'.

        Args:
            * producer_name

        This takes a list of replaceable households and plots that
        are to replace those households. The replacement history model
        is updated to specify when the household was replaced and what
        it was replaced with."""
        new_bhs_plots = []
        try:
            using_producer = Producer.objects.get(settings_key=using_producer).settings_key
            load_producer_db_settings()
            if (not TransactionHelper().outgoing_transactions(
                    socket.gethostname(), using_producer, raise_exception=True)) and (
                        not TransactionHelper().has_incoming_for_producer(using_producer, 'default')):
                    available_plots = self.available_plots
                    for replaceable_household, _ in self.replaceable_households(using_producer):
                        try:
                            Household.objects.using(using_producer).get(
                                household_identifier=replaceable_household.household_identifier)
                            plot = available_plots.next()
                            self.household_structure = HouseholdStructure.objects.get(
                                household=replaceable_household, survey=self.survey)
                            replaceable_household.replaced_by = plot.plot_identifier
                            plot.replaces = replaceable_household.household_identifier
                            with transaction.atomic():
                                replaceable_household.save(update_fields=['replaced_by'], using='default')
                                plot.save(update_fields=['replaces'], using='default')
                                with transaction.atomic(using_producer):
                                    replaceable_household.save(update_fields=['replaced_by'], using=using_producer)
                                    TransactionHelper().outgoing_transactions(
                                        hostname=socket.gethostname(), using=using_producer).delete()
                                ReplacementHistory.objects.using('default').create(
                                    replacing_item=plot.plot_identifier,
                                    replaced_item=replaceable_household.household_identifier,
                                    replacement_datetime=datetime.now(),
                                    replacement_reason=self.household_replacement_reason)
                            new_bhs_plots.append(plot)
                            self.recently_replaced['households'].append(replaceable_household)
                        except Household.DoesNotExist:
                            pass  # household is not dispatched to this producer!
                        except StopIteration:
                            break  # ran out of available plots
                        except ConnectionDoesNotExist as connection_does_not_exist:
                            raise ReplacementError('Unable to connect to producer with settings key \'{}\'. '
                                                   'Got {}'.format(using_producer, str(connection_does_not_exist)))
                        except OperationalError as operational_error:
                            raise ReplacementError('Unable to connect to producer with settings key \'{}\'. '
                                                   'Got {}'.format(using_producer, str(operational_error)))
            else:
                raise PendingTransactionError('Pending incoming transactions. Consume transactions first')
        except Producer.DoesNotExist as does_not_exist:
            raise ReplacementError('Unable to find to producer with settings key \'{}\'. '
                                   'Got {}'.format(using_producer, str(does_not_exist)))
        return new_bhs_plots

    def replace_plot(self, using_producer):
        """Replaces a plot with a plot.

        This takes a list of replaceable plots and replaces each with a plot.
        The replacement history model is also update to keep track of what replace what."""
        new_bhs_plots = []
        try:
            using_producer = Producer.objects.get(settings_key=using_producer).settings_key
            load_producer_db_settings()
            if (not TransactionHelper().outgoing_transactions(
                    socket.gethostname(), using_producer, raise_exception=True)) and (
                        not TransactionHelper().has_incoming_for_producer(using_producer, 'default')):
                    available_plots = self.available_plots
                    for replaceable_plot, _ in self.replaceable_plots(using_producer):
                        try:
                            Plot.objects.using(using_producer).get(
                                plot_identifier=replaceable_plot.plot_identifier)
                            available_plot = available_plots.next()
                            self.plot = replaceable_plot
                            replaceable_plot.replaced_by = available_plot.plot_identifier
                            replaceable_plot.htc = True  # If a plot is replaced it goes to CDC
                            available_plot.replaces = replaceable_plot.plot_identifier
                            with transaction.atomic():
                                replaceable_plot.save(update_fields=['replaced_by', 'htc'], using='default')
                                available_plot.save(update_fields=['replaces'], using='default')
                                with transaction.atomic(using=using_producer):
                                    replaceable_plot.save(update_fields=['replaced_by', 'htc'], using=using_producer)
                                    TransactionHelper().outgoing_transactions(
                                        hostname=socket.gethostname(), using=using_producer).delete()
                                ReplacementHistory.objects.using('default').create(
                                    replacing_item=available_plot.plot_identifier,
                                    replaced_item=replaceable_plot.plot_identifier,
                                    replacement_datetime=datetime.now(),
                                    replacement_reason=self.plot_replacement_reason)
                            new_bhs_plots.append(available_plot)
                            self.recently_replaced['plots'].append(replaceable_plot)
                        except Plot.DoesNotExist:
                            pass  # replaceable_plot is not dispatched to this producer!
                        except StopIteration:
                            break  # ran out of available plots
                        except ConnectionDoesNotExist as connection_does_not_exist:
                            raise ReplacementError('Unable to connect to producer with settings key \'{}\'. '
                                                   'Got {}'.format(using_producer, str(connection_does_not_exist)))
                        except OperationalError as operational_error:
                            raise ReplacementError('Unable to connect to producer with settings key \'{}\'. '
                                                   'Got {}'.format(using_producer, str(operational_error)))
            else:
                raise PendingTransactionError('Pending incoming transactions. Consume transactions first')
        except Producer.DoesNotExist as does_not_exist:
            raise ReplacementError('Unable to find to producer with settings key \'{}\'. '
                                   'Got {}'.format(using_producer, str(does_not_exist)))
        return new_bhs_plots

    @property
    def all_eligible_members_refused(self):
        """Returns True if all eligible members refuse participation in BHS."""
        if self.household_structure.enumerated:
            refused_members_count = HouseholdMember.objects.using('default').filter(
                household_structure=self.household_structure,
                eligible_member=True,
                refused=True).count()
            if refused_members_count:
                eligible_member_count = HouseholdMember.objects.using('default').filter(
                    household_structure=self.household_structure,
                    eligible_member=True).count()
                return eligible_member_count == refused_members_count
        return False

    @property
    def all_eligible_members_absent(self):
        """Returns True if all eligible members are absent
        after 3 attempts."""
        eligible_members = HouseholdMember.objects.using('default').filter(
            household_structure=self.household_structure,
            eligible_member=True)
        # If eligible members are consented the household is not replaceable
        if eligible_members:
            for member in eligible_members:
                if member.is_consented:
                    return False
        if self.household_structure.enumerated:
            absent_member_count = HouseholdMember.objects.using('default').filter(
                household_structure=self.household_structure,
                eligible_member=True,
                absent=True,
                visit_attempts__gte=VISIT_ATTEMPTS).count()
            if absent_member_count:
                eligible_member_count = eligible_members.count()
                return eligible_member_count == absent_member_count
        return False

    @property
    def eligible_representative_absent(self):
        """Returns True if no household age eligible representative is available after
        (x) attempts (e.g., VISIT_ATTEMPTS=3) to complete the HouseholdAssessment.

        Information comes from the last HouseholdLog entry for a household that has
        not been enumerated and has been visited at least 3 times"""
        eligible_representative_absent = False
        if (not self.household_structure.enumerated and
                self.household_structure.failed_enumeration_attempts >= VISIT_ATTEMPTS):
            try:
                report_datetime = HouseholdLogEntry.objects.using('default').filter(
                    household_log__household_structure=self.household_structure).aggregate(
                        Max('report_datetime')).get('report_datetime__max')
                HouseholdLogEntry.objects.using('default').get(
                    household_log__household_structure=self.household_structure,
                    report_datetime=report_datetime,
                    household_status=ELIGIBLE_REPRESENTATIVE_ABSENT)
                eligible_representative_absent = True
            except HouseholdLogEntry.DoesNotExist:
                pass
        return eligible_representative_absent

    @property
    def isreplaceable_household(self):
        """Returns True if a household meets the criteria to be replaced by a plot."""
        replaceable = False
        try:
            if self.plot.status == RESIDENTIAL_HABITABLE:
                if self.household_structure.refused_enumeration:
                    replaceable = True
                    # self.replacement_reason = 'household refused_enumeration'
                elif self.all_eligible_members_refused:
                    replaceable = True
                    # self.replacement_reason = 'household all_eligible_members_refused'
                elif self.eligible_representative_absent:
                    replaceable = True
                    # self.replacement_reason = 'household eligible_representative_absent'
                elif self.all_eligible_members_absent:
                    replaceable = True
                    self.replacement_reason = 'household all_eligible_members_absent'
                elif (self.household_structure.failed_enumeration and
                      self.household_structure.no_informant):
                    replaceable = True
        except AttributeError as attribute_error:
            if 'has no attribute \'household\'' in str(attribute_error):
                pass
        return replaceable

    @property
    def isreplaceable_plot(self):
        """Returns True if the plot, from the 5% pool, meets the criteria to be replaced by another plot."""
        replaceable = False
        if self.plot.selected == FIVE_PERCENT:
            if self.plot.status in [NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE] and self.plot.replaces:
                replaceable = True
        return replaceable
