from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.core.exceptions import ValidationError
from django.dispatch import receiver

from .household import Household
from .household_refusal import HouseholdRefusal
from .household_refusal import HouseholdRefusalHistory
from .household_log import HouseholdLogEntry
from .household_assessment import HouseholdAssessment
from .household_structure import HouseholdStructure
from .plot import Plot
from .plot_log import PlotLogEntry

from ..constants import ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT, REFUSED_ENUMERATION


@receiver(pre_save, weak=False, dispatch_uid="check_for_survey_on_pre_save")
def check_for_survey_on_pre_save(sender, instance, raw, **kwargs):
    if not raw:
        if isinstance(instance, (Plot)):
            instance.check_for_survey_on_pre_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="post_save_on_household")
def post_save_on_household(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, Household):
            using = kwargs.get('using')
            instance.post_save_update_identifier(instance, created, using)
            instance.post_save_create_household_structure(instance, created, using)


@receiver(pre_delete, weak=False, dispatch_uid="household_structure_on_pre_delete")
def household_structure_on_pre_delete(sender, instance, using, **kwargs):
    """Raises an exception if instance.eligible_members is not 0."""
    if isinstance(instance, HouseholdStructure):
        if not instance.eligible_members:
            raise ValidationError('Cannot delete HouseholdStructure instance if eligible members equals {}'.format(instance.eligible_members))


@receiver(post_save, weak=False, dispatch_uid="household_structure_on_post_save")
def household_structure_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, HouseholdStructure):
            instance.create_household_log_on_post_save(**kwargs)
            if not created:
                if instance.enumerated and instance.no_informant:
                    #  TODO: why is this being deleted?
                    try:
                        # TODO: be aware that deleting HouseholdAssessment will
                        #       recall this post-save signal.
                        HouseholdAssessment.objects.using(using).get(
                            household_structure=instance).delete(using=using)
                    except HouseholdAssessment.DoesNotExist:
                        pass
                # update household if enrolled
                instance.household.enrolled = instance.enrolled or False  # uses NullBoolean
                instance.household.enrolled_datetime = instance.enrolled_datetime
                instance.household.save(using=using)
                # update plot if enrolled
                instance.household.plot.bhs = instance.enrolled or False  # uses NullBoolean
                instance.household.plot.enrolled_datetime = instance.enrolled_datetime
                instance.household.plot.save(using=using)


@receiver(post_save, weak=False, dispatch_uid="create_household_on_post_save")
def create_household_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, Plot):
            original_household_count = instance.household_count
            instance.household_count = instance.create_or_delete_households(instance, using)
            if original_household_count != instance.household_count:
                instance.save()


@receiver(post_save, weak=False, dispatch_uid="plot_access_attempts_on_post_save")
def plot_access_attempts_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, PlotLogEntry):
            plot = instance.plot_log.plot
            attempts = PlotLogEntry.objects.using(using).filter(plot_log__plot=plot).count()
            if attempts <= 3:
                plot.access_attempts = attempts
                plot.save(using=using)
            else:
                raise TypeError('Have more than 3 log entries for {0}'.format(instance.plot_log.plot))


@receiver(post_delete, weak=False, dispatch_uid="household_refusal_on_delete")
def household_refusal_on_delete(sender, instance, using, **kwargs):
    if isinstance(instance, HouseholdRefusal):
        # update the history model
        options = {'household_structure': instance.household_structure,
                   'report_datetime': instance.report_datetime,
                   'reason': instance.reason,
                   'reason_other': instance.reason_other}
        HouseholdRefusalHistory.objects.using(using).create(**options)
        household_structure = instance.household_structure
        household_structure.refused_enumeration = False
        household_structure.save(using=using)


@receiver(post_delete, weak=False, dispatch_uid="household_assessment_on_delete")
def household_assessment_on_delete(sender, instance, using, **kwargs):
    if isinstance(instance, HouseholdAssessment):
        instance.household_structure.no_informant = False
        instance.household_structure.save(using=using)


@receiver(post_save, weak=False, dispatch_uid='household_enumeration_on_past_save')
def household_enumeration_on_past_save(sender, instance, raw, created, using, **kwargs):
    """HouseholdRefusal should be deleted if household_status.refused = False, updates failed enumeration attempts and no_elgible_members."""
    if not raw:
        if isinstance(instance, HouseholdLogEntry):
            household_structure = instance.household_log.household_structure
            if not instance.household_status == REFUSED_ENUMERATION:
                HouseholdRefusal.objects.using(using).filter(household_structure=household_structure).delete()
            # update enumeration attempts
            if not household_structure.enumerated and instance.household_status in [ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT, REFUSED_ENUMERATION]:
                household_structure.failed_enumeration_attempts = HouseholdLogEntry.objects.filter(household_log__household_structure=household_structure).count()
            household_structure.save(using=using)
