from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .household import Household
from .household_refusal import HouseholdRefusal
from .household_refusal import HouseholdRefusalHistory
from .household_log import HouseholdLogEntry
from .household_structure import HouseholdStructure
from .plot import Plot
from .plot_log import PlotLogEntry

from ..constants import ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT, REFUSED_ENUMERATION


@receiver(pre_save, weak=False, dispatch_uid="check_for_survey_on_pre_save")
def check_for_survey_on_pre_save(sender, instance, **kwargs):
    if isinstance(instance, (Plot)):
        instance.check_for_survey_on_pre_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="post_save_on_household")
def post_save_on_household(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, Household):
            instance.post_save_update_identifier(instance, created)
            instance.post_save_create_household_structure(instance, created)
#             instance.post_save_plot_allowed_to_enumerate(instance, created)


@receiver(post_save, weak=False, dispatch_uid="household_structure_on_post_save")
def household_structure_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdStructure):
            instance.create_household_log_on_post_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="create_household_on_post_save")
def create_household_on_post_save(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False) and created:
        if isinstance(instance, Plot):
            instance.create_or_delete_households(instance)


@receiver(post_save, weak=False, dispatch_uid="plot_access_attempts_on_post_save")
def plot_access_attempts_on_post_save(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, PlotLogEntry):
            plot = instance.plot_log.plot
            attempts = PlotLogEntry.objects.filter(plot_log__plot=plot).count()
            if attempts <= 3:
                plot.access_attempts = attempts
                plot.save()
            else:
                raise TypeError('Have more than 3 log entries for {0}'.format(instance.plot_log.plot))


@receiver(post_delete, weak=False, dispatch_uid="household_refusal_on_delete")
def household_refusal_on_delete(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdRefusal):
            # update the history model
            options = {'household_member': instance.household_member,
                       'survey': instance.survey,
                       'refusal_date': instance.refusal_date,
                       'reason': instance.reason,
                       'reason_other': instance.reason_other}
            HouseholdRefusalHistory.objects.create(**options)
            household_member = instance.household_member
            household_member.refused_enumeration = False
            household_member.save()


@receiver(post_save, weak=False, dispatch_uid='household_enumeration_on_past_save')
def household_enumeration_on_past_save(sender, instance, created, **kwargs):
    """HouseholdRefusal should be deleted if household_status.refused = False, updates failed enumeration attempts and no_elgible_members."""
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdLogEntry):
            household_structure = instance.household_log.household_structure
            if not instance.household_status == REFUSED_ENUMERATION:
                HouseholdRefusal.objects.filter(household_structure=household_structure).delete()
            # update enumeration attempts
            if not household_structure.enumerated and instance.household_status in [ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT, REFUSED_ENUMERATION]:
                household_structure.failed_enumeration_attempts = HouseholdLogEntry.objects.filter(household_log__household_structure=household_structure).count()
            household_structure.save()
