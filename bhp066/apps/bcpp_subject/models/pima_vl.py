from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User

from edc.device.device.classes import Device
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from edc.base.model.validators import datetime_not_future
from edc.choices.common import YES_NO, PIMA, PIMA_SETTING_VL
from edc_tracker import TrackerHelper

from .base_scheduled_visit_model import BaseScheduledVisitModel
from ..exceptions import DeniedPermissionPimaVLError

from ..constants import PIMA_VL_TYPE, CENTRAL_SERVER, CLINIC_RESEARCH_ASSISTANT, FIELD_RESEARCH_ASSISTANT_GROUP

from apps.bcpp.choices import EASY_OF_USE


class PimaVl (BaseScheduledVisitModel):

    poc_vl_type = models.CharField(
        verbose_name=_("Type mobile or household setting"),
        choices=PIMA_SETTING_VL,
        max_length=150,
        default=PIMA_SETTING_VL[0][0],
        )

    poc_vl_today = models.CharField(
        verbose_name=_("Was a POC viral load done today?"),
        choices=YES_NO,
        max_length=3,
        help_text="",
        )

    poc_vl_today_other = models.CharField(
        verbose_name=_("If no POC viral load today, please explain why"),
        max_length=50,
        choices=PIMA,
        null=True,
        blank=True,
        )

    poc_today_vl_other_other = OtherCharField()

    pima_id = models.CharField(
        verbose_name=_("POC viral load machine ID?"),
        max_length=9,
        validators=[RegexValidator(regex='\d+', message='POC viral load ID must be a two digit number.')],
        null=True,
        blank=True,
        help_text="type this id directly from the machine as labeled")

    poc_vl_datetime = models.DateTimeField(
        verbose_name=_("POC viral load Date and time"),
        validators=[datetime_not_future],
        null=True,
        blank=True,
        )

    poc_vl_value = models.DecimalField(
        verbose_name=_("POC viral load count"),
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        help_text="",
        )

    time_of_test = models.DateTimeField(
        verbose_name=_("Test Date and time"),
        validators=[datetime_not_future],
        null=True,
        blank=True,
        )

    time_of_result = models.DateTimeField(
        verbose_name=_("Result Date and time"),
        validators=[datetime_not_future],
        help_text="Time it takes to obtain viral load result.",
        null=True,
        blank=True,
        )

    easy_of_use = models.CharField(
        verbose_name=_("Easy of user by field operator?"),
        max_length=200,
        choices=EASY_OF_USE,
        )

    stability = EncryptedTextField(
        verbose_name=_("Stability"),
        max_length=250,
        null=True,
        blank=True,
        help_text="Comment")

    history = AuditTrail()

    def save(self, *args, **kwargs):
        super(PimaVl, self).save(*args, **kwargs)

    def valid_user(self, user):
        """ A list for user contacts."""
        tracker_helper = TrackerHelper()
        tracker_helper.app_label = 'bcpp_subject'
        tracker_helper.model_name = 'PimaVl'
        tracker_helper.master_server_url = 'central'
        tracker_helper.value_type = 'Mobile settings'
        tracker_helper.tracked_model = self.__class__
        #NOTE: un-comment this line
        #tracker_helper.value_limit = 5
        device = Device()
        if device.is_central_server:
            tracker_helper.master_filter_dict.update({'poc_vl_type': PIMA_VL_TYPE})
        else:
            tracker_helper.site_filter_dict.update({'poc_vl_type': PIMA_VL_TYPE})
        tracker_helper.master_server_name = CENTRAL_SERVER
#         tracker_helper.value_type = PIMA_VL_TYPE
        #print 'TRACKED_VALUE='+str(tracker_helper.tracker().tracked_value)
        if tracker_helper.tracker().tracked_value <= tracker_helper.value_limit:
            #if user not in User.objects.filter(groups__name__in=[CLINIC_RESEARCH_ASSISTANT]):
            if not user.groups.filter(name=CLINIC_RESEARCH_ASSISTANT).exists():
                raise DeniedPermissionPimaVLError("Access denied, you don't have permission to save/modified this model.")
        else:
            #if user not in User.objects.filter(groups__name__in=[FIELD_RESEARCH_ASSISTANT_GROUP]):
            if not user.groups.filter(name=FIELD_RESEARCH_ASSISTANT_GROUP).exists():
                raise DeniedPermissionPimaVLError("Access denied, you don't have permission to save/modified this model.")
        return True

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "POC VL"
        verbose_name_plural = "POC VL"
