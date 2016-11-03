from datetime import datetime
from django.db import models

from django.core.urlresolvers import reverse

from django.core.validators import MinValueValidator, RegexValidator

from edc.data_manager.models import TimePointStatusMixin
from edc.device.dispatch.models.base_dispatch_sync_uuid_model import BaseDispatchSyncUuidModel
from edc_sync.models import SyncModelMixin
from edc_base.model.models import BaseUuidModel
from edc_base.audit_trail import AuditTrail
from edc_base.encrypted_fields import EncryptedTextField
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_consent.models import RequiresConsentMixin
from edc_constants.choices import YES_NO, PIMA
from edc_quota.client.models import QuotaMixin, QuotaManager

from bhp066.apps.bcpp.choices import EASY_OF_USE, QUANTIFIER
from bhp066.apps.bcpp_household.models import Plot

from ..managers import PimaVlManager

from .subject_visit import SubjectVisit
from .subject_off_study_mixin import SubjectOffStudyMixin
from .subject_consent import SubjectConsent

PIMA_SETTING_VL = (
    ('mobile setting', 'Mobile Setting'),
    ('household setting', 'Household Setting'),
)


class PimaVl (QuotaMixin, SubjectOffStudyMixin, RequiresConsentMixin, TimePointStatusMixin,
              BaseDispatchSyncUuidModel, SyncModelMixin, BaseUuidModel):

    CONSENT_MODEL = SubjectConsent

    subject_visit = models.ForeignKey(SubjectVisit, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.now,  # ref: http://stackoverflow.com/questions/2771676/django-default-datetime-now-problem
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    poc_vl_type = models.CharField(
        verbose_name="Type mobile or household setting",
        choices=PIMA_SETTING_VL,
        max_length=150,
        default=PIMA_SETTING_VL[0][0],
    )

    poc_vl_today = models.CharField(
        verbose_name="Was a POC viral load done today?",
        choices=YES_NO,
        max_length=3,
        help_text="",
    )

    poc_vl_today_other = models.CharField(
        verbose_name="If no POC viral load today, please explain why",
        max_length=50,
        choices=PIMA,
        null=True,
        blank=True,
    )

    poc_today_vl_other_other = OtherCharField()

    pima_id = models.CharField(
        verbose_name="POC viral load machine ID?",
        max_length=9,
        validators=[RegexValidator(regex='\d+', message='POC viral load ID must be a two digit number.')],
        null=True,
        blank=True,
        help_text="type this id directly from the machine as labeled")

# removed
#     poc_vl_datetime = models.DateTimeField(
#         verbose_name="POC viral load Date and time",
#         validators=[datetime_not_future],
#         null=True,
#         blank=True,
#     )

    vl_value_quatifier = models.CharField(
        verbose_name="Select a quantifier for the value of the result",
        choices=QUANTIFIER,
        max_length=20,
    )

    # vl_value_quatifier_other = OtherCharField()

    poc_vl_value = models.DecimalField(
        verbose_name="POC viral load count",
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="",
    )

    time_of_test = models.DateTimeField(
        verbose_name="Test Date and time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    time_of_result = models.DateTimeField(
        verbose_name="Result Date and time",
        validators=[datetime_not_future],
        help_text="Time it takes to obtain viral load result.",
        null=True,
        blank=True,
    )

    easy_of_use = models.CharField(
        verbose_name="Ease of use by field operator?",
        max_length=200,
        choices=EASY_OF_USE,
    )

    stability = EncryptedTextField(
        verbose_name="Stability",
        max_length=250,
        null=True,
        blank=True,
        help_text="Comment")

    objects = PimaVlManager()

    history = AuditTrail()

    quota = QuotaManager()

    def pre_order(self):
        url = reverse('admin:bcpp_lab_preorder_changelist')
        return '<a href="{0}?q={1}">pre_orders</a>'.format(url, self.subject_visit.subject_identifier)
    pre_order.allow_tags = True

    def bypass_for_edit_dispatched_as_item(self, using=None, update_fields=None):
        return True

    def natural_key(self):
        return self.subject_visit.natural_key()

    def get_visit(self):
        return self.subject_visit

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    def get_report_datetime(self):
        return self.created

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'subject_visit__household_member__household_structure__household__plot__plot_identifier')

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "POC VL"
        verbose_name_plural = "POC VL"
