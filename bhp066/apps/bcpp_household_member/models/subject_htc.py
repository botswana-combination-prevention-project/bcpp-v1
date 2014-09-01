from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.device.device.classes import Device
from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO, YES_NO_NA
from edc.core.bhp_variables.models import StudySite
from edc.core.bhp_string.classes import StringHelper
from edc.constants import NOT_APPLICABLE

from apps.bcpp_household_member.constants import HTC, HTC_ELIGIBLE, REFUSED_HTC
from apps.bcpp_household_member.exceptions import MemberStatusError
from apps.bcpp.choices import HIV_RESULT

from apps.bcpp_household.exceptions import AlreadyReplaced

from .base_member_status_model import BaseMemberStatusModel


HIV_RESULT = list(HIV_RESULT)
HIV_RESULT.append((NOT_APPLICABLE, 'Not applicable'))
HIV_RESULT = tuple(HIV_RESULT)


class SubjectHtc(BaseMemberStatusModel):

    tracking_identifier = models.CharField(
        verbose_name=_("HTC tracking identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text='After saving, re-open this form and transcribe this tracking identifier in to the paper form.')

    offered = models.CharField(
        verbose_name=_("Was the subject offered HTC"),
        max_length=10,
        choices=YES_NO)

    accepted = models.CharField(
        verbose_name=_("Did the subject accept HTC"),
        max_length=25,
        choices=YES_NO)

    refusal_reason = models.CharField(
        verbose_name=_("If the subject did not accept HTC, please explain"),
        max_length=50,
        null=True,
        blank=True,
        help_text='Required if subject did not accepted HTC')

    referred = models.CharField(
        verbose_name=_("Was the subject referred"),
        max_length=10,
        choices=YES_NO,
        help_text='Required if subject accepted HTC')

    referral_clinic = models.CharField(
        verbose_name=_("If referred, which clinic"),
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
        if not self.id:
            self.tracking_identifier = self.prepare_tracking_identifier()
        self.registered_subject = self.household_member.registered_subject
        super(SubjectHtc, self).save(*args, **kwargs)

    def prepare_tracking_identifier(self):
        device = Device()
        device_id = device.device_id
        string = StringHelper()
        length = 5
        template = 'HTC{device_id}{random_string}'
        opts = {'device_id': device_id, 'random_string': string.get_safe_random_string(length=length)}
        tracking_identifier = template.format(**opts)
        # look for a duplicate
        if self.__class__.objects.filter(tracking_identifier=tracking_identifier):
            n = 1
            while self.__class__.objects.filter(tracking_identifier=tracking_identifier):
                tracking_identifier = template.format(**opts)
                n += 1
                if n == len(string.safe_allowed_chars) ** length:
                    raise TypeError('Unable prepare a unique htc tracking identifier, '
                                    'all are taken. Increase the length of the random string')
        return tracking_identifier
#         device = Device()
#         site_code = None
#         if 'SITE_CODE' in dir(settings):
#             site_code = settings.SITE_CODE
#         if not site_code:
#             site_code = StudySite.objects.all()[0].site_code
#         return 'HTC{0}{1}{2}'.format(site_code, device.device_id, datetime.today().strftime('%Y%m%d%H%M'))

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Htc"
        verbose_name_plural = "Subject Htc"
        unique_together = ('registered_subject', 'survey',)
