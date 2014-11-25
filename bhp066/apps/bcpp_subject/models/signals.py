from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from edc.base.model.constants import BASE_MODEL_UPDATE_FIELDS, BASE_UUID_MODEL_UPDATE_FIELDS
from edc.core.bhp_data_manager.models import TimePointStatus
from edc.constants import CLOSED, OPEN, YES, NO, ALIVE, DEAD

from apps.bcpp_household_member.exceptions import MemberStatusError
from apps.bcpp_household_member.models import MemberAppointment

from .subject_consent import SubjectConsent

from ..classes import SubjectReferralHelper

from ..models import SubjectReferral, SubjectVisit, CallLogEntry, CallList


@receiver(post_save, weak=False, dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    """Updates household_structure and household_members to reflect enrollment and
    changed member status.

    Also, update_fields is set when verifying consents using the Admin action
    under edc.subject.consent. The list of fields is passed and trapped
    here to prevent further modifications to  household_structure and
    household_members.

    See also edc.subject.consent.actions.flag_as_verified_against_paper."""
    if not raw:
        if isinstance(instance, (SubjectConsent, )):
            try:
                update_fields = sorted(update_fields)
            except TypeError:
                pass
            if update_fields != sorted((['is_verified', 'is_verified_datetime'] +
                                        BASE_MODEL_UPDATE_FIELDS +
                                        BASE_UUID_MODEL_UPDATE_FIELDS)):
                # instance.post_save_update_registered_subject(using) (called in base)
                instance.household_member.is_consented = True
                instance.household_member.save(using=using, update_fields=['is_consented'])
                # update household_structure if enrolled
                instance.household_member.household_structure.enrolled = True
                instance.household_member.household_structure.enrolled_household_member = instance.pk
                instance.household_member.household_structure.enrolled_datetime = instance.consent_datetime
                instance.household_member.household_structure.save(using=using,
                                                                   update_fields=['enrolled',
                                                                                  'enrolled_household_member',
                                                                                  'enrolled_datetime'])
                # update household if enrolled
                instance.household_member.household_structure.household.enrolled = True
                instance.household_member.household_structure.household.enrolled_datetime = \
                    instance.consent_datetime
                instance.household_member.household_structure.household.save(
                    using=using, update_fields=['enrolled', 'enrolled_datetime'])
                # update plot if enrolled
                instance.household_member.household_structure.household.plot.bhs = True
                instance.household_member.household_structure.household.plot.enrolled_datetime = \
                    instance.consent_datetime
                instance.household_member.household_structure.household.plot.save(
                    using=using, update_fields=['bhs', 'enrolled_datetime'])
                # The PLOT is now enrolled so re-save all household_members in the PLOT
                # to re-calculated member_status (excluding the current
                # instance.household_member)
                if instance.household_member.household_structure.enrolled:
                    household_members = instance.household_member.__class__.objects.filter(
                        household_structure__household__plot=instance.household_member.household_structure.household.plot
                        ).exclude(is_consented=True)  # This includes instance.household_member
                    for household_member in household_members:
                        try:
                            household_member.save(update_fields=['member_status'])
                        except MemberStatusError:
                            pass


@receiver(post_save, weak=False, dispatch_uid='update_subject_referral_on_post_save')
def update_subject_referral_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates the subject referral if a model that is part of the referral data is changed.

    The sender classes are listed in the SubjectReferralHelper."""
    if not raw:
        try:
            if sender in SubjectReferralHelper.models.values():
                subject_referral = SubjectReferral.objects.using(using).get(
                    subject_visit=instance.subject_visit)
                # calling save will run it through export_history manager. This may be noisy
                # but it ensures all modifications get exported
                if not SubjectReferralHelper(subject_referral).missing_data:
                    #Only resave the referral if there is no missing data.
                    subject_referral.save(using=using)
        except SubjectReferral.DoesNotExist:
            pass
        except AttributeError as attribute_error:
            if 'has no attribute \'subject_visit\'' in str(attribute_error):
                # TODO: subject_referral = query for the referral using enrollment checklist, subject consent, etc
                # subject_referral.save(using=using)
                pass
            else:
                raise


@receiver(post_save, weak=False, dispatch_uid='time_point_status_on_post_save')
def time_point_status_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Attempt to save the subject referral to refer participants that
    do not complete data collection (partial participation)."""
    if not raw:
        if isinstance(instance, (TimePointStatus, )):
            if instance.status == CLOSED:
                try:
                    subject_visit = SubjectVisit.objects.get(appointment=instance.appointment)
                    SubjectReferral.objects.using(using).get(
                        subject_visit=subject_visit)
                except SubjectReferral.DoesNotExist:
                    # create a new instance and flag as partial
                    try:
                        SubjectReferral.objects.using(using).create(
                            subject_visit=subject_visit,
                            subject_referred='No',
                            comment='(Partial participation. Auto generated when time point closed.)'
                            )
                    except ValidationError:
                        # TODO: TimePointStatus form should catch this error instead
                        # of hiding it like this
                        pass


@receiver(post_save, weak=False, dispatch_uid='call_log_entry_on_post_save')
def call_log_entry_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates call list after a call log entry ('call_status', 'call_attempts', 'call_outcome').""" 
    if not raw:
        if isinstance(instance, CallLogEntry):
            call_list = CallList.objects.get(
                household_member=instance.call_log.household_member,
                label=instance.call_log.label)
            outcome = []
            member_appointment = None
            try:
                call_log_entry = CallLogEntry.objects.filter(call_log=instance.call_log).order_by('-call_datetime')[0]
                if call_log_entry.appt_date:
                    outcome.append('Appt')
                    try:
                        member_appointment = MemberAppointment.objects.get(
                            household_member=call_log_entry.call_log.household_member,
                            appt_date=call_log_entry.appt_date,
                            )
                    except MemberAppointment.DoesNotExist:
                        member_appointment = MemberAppointment.objects.create(
                            household_member=call_log_entry.call_log.household_member,
                            appt_date=call_log_entry.appt_date,
                            survey=call_log_entry.call_log.survey,
                            label=call_log_entry.call_log.label,
                            time_of_day=call_log_entry.time_of_day,
                            time_of_week=call_log_entry.time_of_week,
                            is_confirmed=True,
                            )
                else:
                    if call_log_entry.survival_status in [ALIVE, DEAD]:
                        outcome.append('Alive' if ALIVE else 'Deceased')
                    if call_log_entry.moved_community == YES:
                        outcome.append('Moved')
                    if call_log_entry.call_again == YES:
                        outcome.append('Call again')
                    elif call_log_entry.call_again == NO:
                        outcome.append('Do not call')
            except IndexError:
                pass
            call_list.call_outcome = '. '.join(outcome)
            call_list.member_appointment = member_appointment
            call_list.call_datetime = CallLogEntry.objects.filter(
                call_log=instance.call_log).order_by('-created')[0].call_datetime
            call_list.call_attempts = CallLogEntry.objects.filter(
                call_log=instance.call_log).count()
            if instance.call_again == YES:
                call_list.call_status = OPEN
            else:
                call_list.call_status = CLOSED
            call_list.save(update_fields=['call_status', 'call_attempts', 'call_outcome', 'member_appointment'])
