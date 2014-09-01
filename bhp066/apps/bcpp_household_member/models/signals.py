import pprint

from datetime import datetime

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from edc.map.classes.controller import site_mappers

from apps.bcpp_household.models import HouseholdStructure

from .base_registered_household_member_model import BaseRegisteredHouseholdMemberModel
from .enrollment_checklist import EnrollmentChecklist, EnrollmentLoss
from .household_member import HouseholdMember
from .subject_absentee import SubjectAbsentee
from .subject_absentee_entry import SubjectAbsenteeEntry
from .subject_htc import SubjectHtc
from .subject_refusal import SubjectRefusal
from .subject_refusal_history import SubjectRefusalHistory
from .subject_undecided import SubjectUndecided
from .subject_undecided_entry import SubjectUndecidedEntry

from ..constants import BHS_ELIGIBLE, BHS_SCREEN, NOT_ELIGIBLE, REFUSED, ABSENT, UNDECIDED


@receiver(post_delete, weak=False, dispatch_uid="subject_refusal_on_post_delete")
def subject_refusal_on_post_delete(sender, instance, using, **kwargs):
    if isinstance(instance, SubjectRefusal):
        # update the history model
        household_member = HouseholdMember.objects.using(using).get(pk=instance.household_member.pk)
        options = {'household_member': household_member,
                   'survey': instance.survey,
                   'refusal_date': instance.refusal_date,
                   'reason': instance.reason,
                   'reason_other': instance.reason_other}
        SubjectRefusalHistory.objects.using(using).create(**options)
        household_member.refused = False
        household_member.save(using=using)


# @receiver(post_save, weak=False, dispatch_uid="subject_refusal_on_post_save")
# def subject_refusal_on_post_save(sender, instance, raw, created, using, **kwargs):
#     if not raw:
#         if isinstance(instance, SubjectRefusal):
#             household_member = HouseholdMember.objects.get(pk=instance.household_member.pk)
#             household_member.refused = True
#             household_member.member_status = REFUSED
#             household_member.save(using=using)


@receiver(post_delete, weak=False, dispatch_uid="enrollment_checklist_on_post_delete")
def enrollment_checklist_on_post_delete(sender, instance, using, **kwargs):
    """Resets household member values to before the enrollment checklist was entered.

    A number of places check for these values including URLs in templates."""
    if isinstance(instance, EnrollmentChecklist):
        # re-save the member to recalc the member_status
        # If this gets deleted, then the process must be started again from BHS_SCREEN
        # household_member = HouseholdMember.objects.using(using).get(pk=instance.household_member.pk)
        try:
            EnrollmentLoss.objects.using(using).get(household_member=instance.household_member).delete(using=using)
        except EnrollmentLoss.DoesNotExist:
            pass
        instance.household_member.enrollment_checklist_completed = False
        instance.household_member.enrollment_loss_completed = False
        instance.household_member.eligible_subject = False
        # household_member.member_status = BHS_SCREEN
        instance.household_member.save(using=using, update_fields=['enrollment_checklist_completed',
                                                                   'enrollment_loss_completed',
                                                                   'eligible_subject',
                                                                   'member_status'])


@receiver(post_save, weak=False, dispatch_uid="enrollment_checklist_on_post_save")
def enrollment_checklist_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates household_member and removes the Loss form if it exusts."""
    if not raw:
        if isinstance(instance, EnrollmentChecklist):
            instance.household_member.eligible_subject = False
            instance.household_member.enrollment_checklist_completed = True
            instance.household_member.enrollment_loss_completed = False
            if instance.is_eligible:
                instance.household_member.eligible_subject = True
                try:
                    EnrollmentLoss.objects.using(using).get(household_member=instance.household_member).delete(using=using)
                except EnrollmentLoss.DoesNotExist:
                    pass
                instance.household_member.enrollment_loss_completed = False
            else:
                if instance.loss_reason:
                    instance.household_member.member_status = NOT_ELIGIBLE  # to allow edit of enrollment loss only
                    instance.household_member.enrollment_loss_completed = True
                    try:
                        enrollment_loss = EnrollmentLoss.objects.using(using).get(household_member=instance.household_member)
                        enrollment_loss.report_datetime = instance.report_datetime
                        enrollment_loss.reason = ';'.join(instance.loss_reason)
                        enrollment_loss.save(using=using, update_fields=['report_datetime', 'reason'])
                    except EnrollmentLoss.DoesNotExist:
                        EnrollmentLoss.objects.using(using).create(
                            household_member=instance.household_member,
                            report_datetime=instance.report_datetime,
                            reason=';'.join(instance.loss_reason))
            instance.household_member.save(using=using, update_fields=['eligible_subject',
                                                                       'enrollment_checklist_completed',
                                                                       'enrollment_loss_completed',
                                                                       'member_status',
                                                                       'eligible_htc'])


@receiver(pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
def household_member_on_pre_save(sender, instance, raw, using, **kwargs):
    if not raw:
        if isinstance(instance, HouseholdMember):
            instance.update_hiv_history_on_pre_save(using, **kwargs)


@receiver(post_save, weak=False, dispatch_uid="household_member_on_post_save")
def household_member_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates enumerated, eligible_members on household structure."""
    if not raw:
        if isinstance(instance, HouseholdMember):
            household_structure = HouseholdStructure.objects.using(using).get(pk=instance.household_structure.pk)
            # update registered subject
            instance.update_registered_subject_on_post_save(using, **kwargs)
            # create subject absentee if member_status == ABSENT otherwise delete the entries
            if instance.absent or instance.present_today == 'No':
                try:
                    SubjectAbsentee.objects.using(using).get(household_member=instance)
                except SubjectAbsentee.DoesNotExist:
                    SubjectAbsentee.objects.using(using).create(
                        report_datetime=datetime.today(),
                        registered_subject=instance.registered_subject,
                        household_member=instance,
                        survey=household_structure.survey,
                        )
            else:
                SubjectAbsenteeEntry.objects.using(using).filter(subject_absentee__household_member=instance).delete()
            # create subject undecided if member_status == UNDECIDED otherwise delete the entries
            if instance.undecided:
                try:
                    SubjectUndecided.objects.using(using).get(household_member=instance)
                except SubjectUndecided.DoesNotExist:
                    SubjectUndecided.objects.using(using).create(
                        report_datetime=datetime.today(),
                        registered_subject=instance.registered_subject,
                        household_member=instance,
                        survey=household_structure.survey,
                        )
            else:
                SubjectUndecidedEntry.objects.using(using).filter(subject_undecided__household_member=instance).delete()
            # update household structure
            if not household_structure.enumerated:
                household_structure.enumerated = True
            household_structure.eligible_members = False
            if HouseholdMember.objects.using(using).filter(
                    household_structure=household_structure, eligible_member=True):
                household_structure.eligible_members = True
            household_structure.save(using=using, update_fields=['enumerated', 'eligible_members'])


@receiver(post_save, weak=False, dispatch_uid='subject_xxx_on_post_save')
def subject_xxx_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Deletes the Enrollment checklist if it exists and sets the 
    household member booleans accordingly."""
    if not raw:
        if isinstance(instance, (SubjectAbsentee, SubjectUndecided, SubjectRefusal)):
            # delete enrollment checklist
            EnrollmentChecklist.objects.using(using).filter(household_member=instance.household_member).delete()
            instance.household_member.enrollment_checklist_completed = False
            # update household member
            # household_member = HouseholdMember.objects.get(pk=instance.household_member.pk)
            instance.household_member.reported = True  # because one of these forms is saved
            instance.household_member.enrollment_loss_completed = False
            instance.household_member.eligible_htc = False
            instance.household_member.htc = False
            instance.household_member.refused_htc = False
            if isinstance(instance, SubjectAbsentee):
                instance.household_member.undecided = False
                instance.household_member.refused = False
            elif isinstance(instance, SubjectUndecided):
                instance.household_member.absent = False
                instance.household_member.refused = False
            elif isinstance(instance, SubjectRefusal):
                intervention = site_mappers.get_current_mapper().intervention
                # print 'intervention = {}'.format('True' if intervention else 'False')
                # print 'enrolled = {}'.format('True' if instance.household_member.household_structure.enrolled else 'False')
                if intervention and instance.household_member.household_structure.enrolled:
                    instance.household_member.eligible_htc = True
                elif not intervention:
                    instance.household_member.eligible_htc = True
                instance.household_member.refused = True
                instance.household_member.absent = False
                instance.household_member.undecided = False
            instance.household_member.save(using=using, update_fields=['reported',
                                                                       'undecided',
                                                                       'absent',
                                                                       'refused',
                                                                       'enrollment_loss_completed',
                                                                       'enrollment_checklist_completed',
                                                                       'htc',
                                                                       'refused_htc',
                                                                       'eligible_htc'
                                                                       ])


@receiver(post_save, weak=False, dispatch_uid='subject_absentee_entry_on_post_save')
def subject_absentee_entry_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, SubjectAbsenteeEntry):
            if created:
                # household_member = HouseholdMember.objects.using(using).get(pk=instance.subject_absentee.household_member.pk)
                instance.subject_absentee.household_member.visit_attempts += 1
                instance.subject_absentee.household_member.save(using=using, update_fields=['visit_attempts'])


@receiver(post_save, weak=False, dispatch_uid='subject_undecided_entry_on_post_save')
def subject_undecided_entry_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, SubjectUndecidedEntry):
            if created:
                # household_member = HouseholdMember.objects.using(using).get(pk=instance.subject_undecided.household_member.pk)
                instance.subject_undecided.household_member.visit_attempts += 1
                instance.subject_undecided.household_member.save(using=using, update_fields=['visit_attempts'])


@receiver(post_save, weak=False, dispatch_uid='base_household_member_consent_on_post_save')
def base_household_member_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, BaseRegisteredHouseholdMemberModel):
            instance.confirm_registered_subject_pk_on_post_save(using)


@receiver(post_save, weak=False, dispatch_uid='subject_htc_on_post_save')
def subject_htc_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, SubjectHtc):
            if instance.accepted == 'No':
                instance.household_member.htc = False
                instance.household_member.refused_htc = True
            else:
                instance.household_member.htc = True
                instance.household_member.refused_htc = False
            instance.household_member.save(using=using, update_fields=['htc',
                                                                       'refused_htc'])
