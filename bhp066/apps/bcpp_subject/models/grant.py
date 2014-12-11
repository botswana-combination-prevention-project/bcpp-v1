from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.base.model.fields import OtherCharField
from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future

from apps.bcpp_household.models import Plot

from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..managers import GrantManager
from ..choices import GRANT_TYPE

from .labour_market_wages import LabourMarketWages


class Grant(BaseDispatchSyncUuidModel):

    """Inline for labour_market_wages."""

    labour_market_wages = models.ForeignKey(LabourMarketWages)

    report_datetime = models.DateTimeField(
        verbose_name="Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today())

    grant_number = models.IntegerField(
        verbose_name=_("How many of each type of grant do you receive?"),
        max_length=2,
        null=True,
        blank=True,
        )
    grant_type = models.CharField(
        verbose_name=_("Grant name"),
        choices=GRANT_TYPE,
        max_length=50,
        null=True,
        blank=True,
        )
    other_grant = OtherCharField()

    history = AuditTrail()

    objects = GrantManager()

    def save(self, *args, **kwargs):
        self.report_datetime = self.labour_market_wages.report_datetime
        super(Grant, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.labour_market_wages.subject_visit)

    @property
    def inline_parent(self):
        """Used??"""
        return self.labour_market_wages

    def get_visit(self):
        return self.labour_market_wages.subject_visit

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_labourmarketwages_change', args=(self.id,))

    def get_report_datetime(self):
        return self.report_datetime

    def get_subject_identifier(self):
        return self.labour_market_wages.subject_visit.get_subject_identifier()

    def natural_key(self):
        return (self.report_datetime, ) + self.labour_market_wages.natural_key()  # 1st natural key might be wrong
    natural_key.dependencies = ['bcpp_subject.labourmarketwages', ]

    def is_dispatched_item_within_container(self, using=None):
        return (('bcpp_household', 'plot'),
                'labour_market_wages__subject_visit__household_member__household_structure__household__plot')

    def dispatch_container_lookup(self, using=None):
        return (Plot,
                'labour_market_wages__subject_visit__household_member__household_structure__household__plot__plot_identifier')

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Grant"
        verbose_name_plural = "Grants"
