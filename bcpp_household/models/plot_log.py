from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from simple_history.models import HistoricalRecords as AuditTrail

from edc_base.model.models import BaseUuidModel
from edc_base.model.validators.date import datetime_not_future
from edc_sync.model_mixins import SyncModelMixin

from bcpp_survey.validators import date_in_survey

from ..choices import PLOT_LOG_STATUS, INACCESSIBILITY_REASONS
from ..managers import PlotLogManager, PlotLogEntryManager

from .plot import Plot


class PlotLog(SyncModelMixin, BaseUuidModel):
    """A system model to track an RA\'s attempts to confirm a Plot (related)."""

    # TODO: Dispatch
    plot = models.OneToOneField(Plot)

    history = AuditTrail()

    objects = PlotLogManager()

    def __str__(self):
        return str(self.plot)

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


class PlotLogEntry(SyncModelMixin, BaseUuidModel):
    """A model completed by the user to track an RA\'s attempts to confirm a Plot."""
    plot_log = models.ForeignKey(PlotLog)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[datetime_not_future, date_in_survey])

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

    def __str__(self):
        return '{} ({})'.format(self.plot_log, self.report_datetime.strftime('%Y-%m-%d'))

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('plot_log', 'report_datetime')
