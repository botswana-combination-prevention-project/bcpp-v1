from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO, YES_NO_NA

from apps.bcpp_household_member.constants import HTC, HTC_ELIGIBLE, REFUSED_HTC
from apps.bcpp_household_member.exceptions import MemberStatusError
from apps.bcpp.choices import HIV_RESULT

from apps.bcpp_household.exceptions import AlreadyReplaced

from .base_member_status_model import BaseMemberStatusModel


HIV_RESULT = list(HIV_RESULT)
HIV_RESULT.append(('N/A', 'Not applicable'))
HIV_RESULT = tuple(HIV_RESULT)


class SubjectHtc(BaseMemberStatusModel):

    offered = models.CharField(
        verbose_name="Was the subject offered HTC",
        max_length=10,
        choices=YES_NO)

    accepted = models.CharField(
        verbose_name="Did the subject accept HTC",
        max_length=25,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        )

    refusal_reason = models.CharField(
        verbose_name="If the subject did not accept HTC, please explain",
        max_length=50,
        null=True,
        blank=True,
        help_text='Required if subject did not accepted HTC')

    hiv_result = models.CharField(
        verbose_name="What was the result of todays\'s HIV test",
        max_length=10,
        choices=HIV_RESULT,
        help_text='Required if subject accepted HTC')

    referred = models.CharField(
        verbose_name="Was the subject referred",
        max_length=10,
        choices=YES_NO_NA,
        help_text='Required if subject accepted HTC')

    referral_clinic = models.CharField(
        verbose_name="If referred, which clinic",
        max_length=25,
        blank=True,
        null=True,
        help_text='Required if subject was referred')

    comment = models.TextField(max_length=250, null=True, blank=True)

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.household_member.household_structure.household.replaced_by:
            raise AlreadyReplaced('Model {0}-{1} has its container replaced.'.format(self._meta.object_name, self.pk))
        if self.household_member.member_status not in [HTC, HTC_ELIGIBLE, REFUSED_HTC]:
            raise MemberStatusError('Expected member status to be on of {0}. Got {1}'.format([HTC, HTC_ELIGIBLE, REFUSED_HTC], self.household_member.member_status))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        self.household_member.htc = True
        self.household_member.save()
        super(SubjectHtc, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Htc"
        verbose_name_plural = "Subject Htc"
        unique_together = ('registered_subject', 'survey',)
