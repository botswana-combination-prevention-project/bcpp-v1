from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.bcpp_survey.models import Survey

from ..classes import HouseholdIdentifier

from .household import Household
from .household_refusal import HouseholdRefusal
from .household_refusal import HouseholdRefusalHistory
from .household_log import HouseholdLogEntry, HouseholdLog
from .household_assessment import HouseholdAssessment
from .household_structure import HouseholdStructure
from .plot import Plot
from .plot_log import PlotLog, PlotLogEntry

from ..constants import (ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT,
                         REFUSED_ENUMERATION, INACCESSIBLE)


@receiver(post_save, weak=False, dispatch_uid="household_on_post_save")
def household_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Creates a household_structure for each survey for this household AND
    updates the identifier field if this is a new instance.."""
    if not raw:
        if isinstance(instance, Household):
            using = kwargs.get('using')
            if created:
                instance.community = instance.plot.community
                instance.household_identifier = HouseholdIdentifier(plot_identifier=instance.plot.plot_identifier).get_identifier()
                instance.save(using=using, update_fields=['household_identifier', 'community'])
            for survey in Survey.objects.using(using).all():
                try:
                    HouseholdStructure.objects.using(using).get(household__pk=instance.pk, survey=survey)
                except HouseholdStructure.DoesNotExist:
                    HouseholdStructure.objects.using(using).create(household=instance, survey=survey)


@receiver(post_save, weak=False, dispatch_uid="household_structure_on_post_save")
def household_structure_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, HouseholdStructure):
            if created:
                try:
                    HouseholdLog.objects.get(household_structure__pk=instance.pk)
                except HouseholdLog.DoesNotExist:
                    HouseholdLog.objects.create(household_structure=instance)
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
                instance.household.enrolled_datetime = instance.enrolled_datetime if instance.enrolled else None
                instance.household.save(using=using, update_fields=['enrolled', 'enrolled_datetime'])
                # update plot if enrolled
                instance.household.plot.bhs = instance.enrolled or False  # uses NullBoolean
                instance.household.plot.enrolled_datetime = instance.enrolled_datetime
                instance.household.plot.save(using=using, update_fields=['bhs', 'enrolled_datetime'])


@receiver(post_save, weak=False, dispatch_uid="plot_on_post_save")
def plot_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Creates / deletes households on after Plot."""
    if not raw:
        if isinstance(instance, Plot):
            original_household_count = instance.household_count
            instance.household_count = instance.create_or_delete_households(instance, using)
            if original_household_count != instance.household_count:
                instance.save(using=using, update_fields=['household_count'])


@receiver(post_save, weak=False, dispatch_uid="household_refusal_on_post_save")
def household_refusal_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates household_structure refused enumeration after Household Refusal is updated."""
    if not raw:
        if isinstance(instance, HouseholdRefusal):
            instance.household_structure.refused_enumeration = True
            instance.household_structure.save(using=using, update_fields=['refused_enumeration'])


@receiver(post_delete, weak=False, dispatch_uid="household_refusal_on_delete")
def household_refusal_on_delete(sender, instance, using, **kwargs):
    if isinstance(instance, HouseholdRefusal):
        # update the history model
        options = {'household_structure': instance.household_structure,
                   'report_datetime': instance.report_datetime,
                   'reason': instance.reason,
                   'reason_other': instance.reason_other}
        HouseholdRefusalHistory.objects.using(using).create(**options)
        instance.household_structure.refused_enumeration = False
        instance.household_structure.save(using=using, update_fields=['refused_enumeration'])


# @receiver(post_save, weak=False, dispatch_uid="plot_log_on_post_save")
# def plot_log_on_post_save(sender, instance, raw, created, using, **kwargs):
#     """Updates Plot's status from the Plot Log."""
#     if not raw:
#         if isinstance(instance, PlotLogEntry):
#             if instance.log_status == INACCESSIBLE:
#                 plot = Plot.objects.using(using).get(pk=instance.plot_log.plot.pk)
#                 plot.status = INACCESSIBLE
#                 plot.save(using=using, updated_fields=['status'])


@receiver(post_save, weak=False, dispatch_uid="plot_log_entry_on_post_save")
def plot_log_entry_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates Plot with the number of attempts and calculates if the
    plot.status is INACCESSIBLE."""
    if not raw:
        if isinstance(instance, PlotLogEntry):
            instance.plot_log.plot.access_attempts = PlotLogEntry.objects.using(using).filter(plot_log__plot=instance.plot_log.plot).count()
            update_fields = ['access_attempts']
            if instance.plot_log.plot.access_attempts >= 3:
                status_list = PlotLogEntry.objects.using(using).values_list('log_status').filter(
                    plot_log__plot=instance.plot_log.plot).order_by('report_datetime')
                status_list = [x[0] for x in status_list]
                if len([status for status in status_list if status == INACCESSIBLE]) >= 3:
                    instance.plot_log.plot.status = INACCESSIBLE
                    update_fields.append('status')
            instance.plot_log.plot.save(using=using, update_fields=update_fields)


@receiver(post_delete, weak=False, dispatch_uid="household_assessment_on_delete")
def household_assessment_on_delete(sender, instance, using, **kwargs):
    if isinstance(instance, HouseholdAssessment):
        household_structure = HouseholdStructure.objects.using(using).get(pk=instance.household_structure.pk)
        household_structure.no_informant = False
        household_structure.save(using=using, update_fields=['no_informant'])


@receiver(post_save, weak=False, dispatch_uid='household_log_entry_on_post_save')
def household_log_entry_on_post_save(sender, instance, raw, created, using, **kwargs):
    """HouseholdRefusal should be deleted if household_status.refused = False,
    updates failed enumeration attempts and no_elgible_members."""
    if not raw:
        if isinstance(instance, HouseholdLogEntry):
            household_structure = HouseholdStructure.objects.using(using).get(pk=instance.household_log.household_structure.pk)
            if not instance.household_status == REFUSED_ENUMERATION:
                HouseholdRefusal.objects.using(using).filter(household_structure=household_structure).delete()
            # update enumeration attempts
            if not household_structure.enumerated and instance.household_status in [ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT, REFUSED_ENUMERATION]:
                household_structure.failed_enumeration_attempts = HouseholdLogEntry.objects.using(using).filter(household_log__household_structure=household_structure).count()
            household_structure.save(using=using, update_fields=['failed_enumeration_attempts'])


# @receiver(pre_save, weak=False, dispatch_uid="plot_on_pre_save")
# def plot_on_pre_save(sender, instance, raw, **kwargs):
#     """Checks that the survey exists."""
#     if not raw:
#         if isinstance(instance, (Plot)):
#             instance.check_for_survey_on_pre_save(**kwargs)


