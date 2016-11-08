from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from edc_base.model.fields import OtherCharField
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.model.validators import datetime_not_future

from bcpp_household.models import Plot


from ..choices import GRANT_TYPE
from ..managers import GrantManager

from .crf_model_mixin import CrfModelMixin
from .labour_market_wages import LabourMarketWages


class Grant(CrfModelMixin):

    """Inline for labour_market_wages."""

    labour_market_wages = models.ForeignKey(LabourMarketWages)

    report_datetime = models.DateTimeField(
        verbose_name="Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=timezone.now)

    grant_number = models.IntegerField(
        verbose_name="How many of each type of grant do you receive?",
        null=True,
        blank=True,
    )
    grant_type = models.CharField(
        verbose_name="Grant name",
        choices=GRANT_TYPE,
        max_length=50,
        null=True,
        blank=True,
    )
    other_grant = OtherCharField()

    objects = GrantManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.report_datetime = self.labour_market_wages.report_datetime
        super(Grant, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.labour_market_wages.subject_visit)

    def get_visit(self):
        return self.labour_market_wages.subject_visit

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_labourmarketwages_change', args=(self.id,))

    def get_report_datetime(self):
        return self.report_datetime

    def get_versioned_field_names(self, version_number):
        """Returns a list of field names under version control by version number.

        Users should override at the model class to return a list of field names for a given version_number."""
        return []

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
                'labour_market_wages__subject_visit__household_member_'
                '_household_structure__household__plot__plot_identifier')

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Grant"
        verbose_name_plural = "Grants"
