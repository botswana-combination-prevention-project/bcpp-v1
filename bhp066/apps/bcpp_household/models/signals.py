from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .household import Household
from .household_log import HouseholdLogEntry
from .plot import Plot
from .plot_log import PlotLogEntry
from .household_structure import HouseholdStructure
from apps.bcpp_household_member.models import HouseholdMember


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
            instance.fetch_and_count_members_on_post_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="create_household_on_post_save")
def create_household_on_post_save(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False) and created:
        if isinstance(instance, Plot):
            instance.create_or_delete_households(instance)


@receiver(post_save, weak=False, dispatch_uid="plot_visit_attempts_on_post_save")
def plot_visit_attempts_on_post_save(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, PlotLogEntry):
            plot = instance.plot_log.plot
            attempts = PlotLogEntry.objects.filter(plot_log__plot=plot).count()
            if attempts <= 3:
                plot.access_attempts = attempts
                plot.save()
            else:
                raise TypeError('Have more than 3 log entries for {0}'.format(instance.plot_log.plot))


@receiver(post_save, weak=False, dispatch_uid='household_visit_attempts_on_post_save')
def household_visit_attempts_on_post_save(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdLogEntry):
            household = instance.household_log.household_structure.household
            household_structure = instance.household_log.household_structure
            household_members = HouseholdMember.objects.filter(household_structure=household_structure)
            if not household_members and instance.household_status == 'no_household_informant':
                enumeration_attempts = HouseholdLogEntry.objects.filter(household_log__household_structure__household=household).count()
                household.enumeration_attempts = enumeration_attempts
                household.save()
