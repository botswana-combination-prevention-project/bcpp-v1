from django.db.models.signals import post_save
from django.dispatch import receiver
from subject_visit import SubjectVisit
from bhp_consent.models import BaseConsent
from base_member_status_model import BaseMemberStatusModel
from base_registered_household_member_model import BaseRegisteredHouseholdMemberModel


@receiver(post_save, weak=False, dispatch_uid='bcpp_subject_on_post_save')
def bcpp_subject_on_post_save(sender, instance, **kwargs):
    if isinstance(instance, SubjectVisit):
        instance.post_save_update_appt_status()
    if isinstance(instance, (BaseConsent, BaseMemberStatusModel)):
        instance.post_save_update_hsm_status()
    if isinstance(instance, BaseRegisteredHouseholdMemberModel):
        instance.confirm_registered_subject_pk_on_post_save()