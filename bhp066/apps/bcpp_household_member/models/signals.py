from django.db.models import get_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from ..constants import ABSENT, UNDECIDED

from .household_member import HouseholdMember
from .enrolment_checklist import EnrolmentChecklist
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
            if instance.member_status == ABSENT:
                SubjectAbsentee = get_model('bcpp_household_member', 'SubjectAbsentee')
                if not SubjectAbsentee.objects.filter(household_member=instance).exists():
                    SubjectAbsentee.objects.create(household_member=instance, subject_absentee_status=ABSENT)
            elif instance.member_status == UNDECIDED:
                SubjectUndecided = get_model('bcpp_household_member', 'SubjectUndecided')
                if not SubjectUndecided.objects.filter(household_member=instance).exists():
                    SubjectUndecided.objects.create(household_member=instance, subject_absentee_status=UNDECIDED)
            else:
                pass



@receiver(post_save, weak=False, dispatch_uid='base_household_member_consent_on_post_save')
def base_household_member_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if isinstance(instance, BaseRegisteredHouseholdMemberModel):
        instance.confirm_registered_subject_pk_on_post_save()
