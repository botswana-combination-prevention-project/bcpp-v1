from datetime import date, datetime
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

from edc.core.crypto_fields.fields import EncryptedTextField
from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from edc.base.model.validators import datetime_not_future
from edc.choices.common import YES_NO, PIMA, PIMA_SETTING_VL
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future

from edc_quota.client.models import QuotaMixin


from edc.subject.consent.models import BaseConsentedUuidModel

from apps.bcpp.choices import EASY_OF_USE
from apps.bcpp_household.models import Plot

from .subject_off_study_mixin import SubjectOffStudyMixin
from ..managers import PimaVlManager
from .subject_visit import SubjectVisit


class PimaVl (QuotaMixin, SubjectOffStudyMixin, BaseConsentedUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.now,  # By passing datetime.now without the parentheses, you are passing the actual function, which will be called each time a record is added ref: http://stackoverflow.com/questions/2771676/django-default-datetime-now-problem
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

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

    objects = PimaVlManager()

    def pre_order(self):
        if self.pre_order_instance:
            url = reverse('admin:bcpp_lab_preorder')
            return '<a href="{0}?q={1}">pre_orders</a>'.format(url, self.subject_visit.subject_identifier)
        else:
            return None
    pre_order.allow_tags = True

    def pre_order_instance(self):
        from apps.bcpp_lab.models import PreOrder
        return PreOrder.objects.filter(subject_visit=self.subject_visit)

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
