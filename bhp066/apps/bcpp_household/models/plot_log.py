from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.device.sync.models import BaseSyncUuidModel
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_base.encrypted_fields import EncryptedTextField
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from bhp066.apps.bcpp_survey.validators import date_in_survey

from ..choices import PLOT_LOG_STATUS, INACCESSIBILITY_REASONS
from ..managers import PlotLogManager, PlotLogEntryManager

from .plot import Plot


class PlotLog(BaseDispatchSyncUuidModel, BaseSyncUuidModel):
    """A system model to track an RA\'s attempts to confirm a Plot (related)."""
    plot = models.OneToOneField(Plot)

    history = AuditTrail()

    objects = PlotLogManager()

    def __unicode__(self):
        return unicode(self.plot)

    def save(self, *args, **kwargs):
        using = kwargs.get('using,')
        self.allow_enrollment(using)
        super(PlotLog, self).save(*args, **kwargs)

    def allow_enrollment(self, using, exception_cls=None, instance=None):
        """Stops enrollments."""
        instance = instance or self
        return self.plot.allow_enrollment(using, exception_cls, plot_instance=instance.plot)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot__plot_identifier')

    def natural_key(self):
        return self.plot.natural_key()
    natural_key.dependencies = ['bcpp_household.plot', ]

    class Meta:
        app_label = 'bcpp_household'


class PlotLogEntry(BaseDispatchSyncUuidModel, BaseSyncUuidModel):
    """A model completed by the user to track an RA\'s attempts to confirm a Plot."""
    plot_log = models.ForeignKey(PlotLog)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[datetime_not_before_study_start, datetime_not_future, date_in_survey])

    log_status = models.CharField(
        verbose_name='What is the status of this plot?',
        max_length=25,
        choices=PLOT_LOG_STATUS)

    reason = models.CharField(
        verbose_name='If inaccessible, please indicate the reason.',
        max_length=25,
        blank=True,
        null=True,
        choices=INACCESSIBILITY_REASONS)

    reason_other = models.CharField(
        verbose_name='If Other, specify',
        max_length=100,
        blank=True,
        null=True)

    comment = EncryptedTextField(
        verbose_name="Comments",
        max_length=250,
        null=True,
        blank=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
                   'information in this comment'))

    history = AuditTrail()

    objects = PlotLogEntryManager()

    def save(self, *args, **kwargs):
        using = kwargs.get('using,')
        self.allow_enrollment(using)
        super(PlotLogEntry, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.report_datetime, ) + self.plot_log.natural_key()

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot_log__plot__plot_identifier')

    def allow_enrollment(self, using, exception_cls=None, instance=None):
        """Stops enrollments."""
        instance = instance or self
        return self.plot_log.plot.allow_enrollment(
            using, exception_cls, plot_instance=instance.plot_log.plot)

    def __unicode__(self):
        return unicode(self.plot_log) + '(' + unicode(self.report_datetime) + ')'

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('plot_log', 'report_datetime')
