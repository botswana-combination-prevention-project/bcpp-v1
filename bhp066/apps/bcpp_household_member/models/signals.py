from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .household_member import HouseholdMember
from .enrolment_checklist import EnrolmentChecklist
from .subject_absentee_entry import SubjectAbsenteeEntry
from .subject_undecided_entry import SubjectUndecidedEntry
from .base_member_status_model import BaseMemberStatusModel
from .base_registered_household_member_model import BaseRegisteredHouseholdMemberModel


@receiver(pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
def household_member_on_pre_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdMember):
            instance.update_hiv_history_on_pre_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="enrolment_checklist_on_post_save")
def enrolment_checklist_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, EnrolmentChecklist):
            if not instance.is_eligible:
                instance.delete()


@receiver(post_save, weak=False, dispatch_uid="household_member_on_post_save")
def household_member_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdMember):
            instance.update_registered_subject_on_post_save(**kwargs)  # update HM must not override consent values, if consent exists
            instance.update_household_member_count_on_post_save(sender, using)
            if instance.member_status == 'ABSENT':
                # TODO: probably do not need to call this now??
                instance.subject_absentee
            if instance.member_status == 'UNDECIDED':
                # TODO: probably do not need to call this now??
                instance.subject_undecided


@receiver(post_save, weak=False, dispatch_uid='base_household_member_consent_on_post_save')
def base_household_member_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if isinstance(instance, (BaseMemberStatusModel)):
        instance.post_save_update_hm_status()  # HM values must either be changed or match that provided on the consent
    if isinstance(instance, BaseRegisteredHouseholdMemberModel):
        instance.confirm_registered_subject_pk_on_post_save()


@receiver(post_save, weak=False, dispatch_uid='visit_attempts_on_post_save')
def visit_attempts_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, SubjectAbsenteeEntry) or isinstance(instance, SubjectUndecidedEntry):
            if isinstance(instance, SubjectAbsenteeEntry) and instance.subject_absentee:
                household_member = instance.subject_absentee.household_member
            elif isinstance(instance, SubjectUndecidedEntry) and instance.subject_undecided:
                household_member = instance.subject_undecided.household_member
            if household_member.visit_attempts <= 3:
                household_member.visit_attempts = SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member=household_member).count() + \
                                                  SubjectUndecidedEntry.objects.filter(subject_undecided__household_member=household_member).count()
                household_member.save()