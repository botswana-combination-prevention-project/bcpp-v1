from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.core.crypto_fields.fields import EncryptedTextField

from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from apps.bcpp_survey.validators import date_in_survey

from .plot import Plot
from ..choices import PLOT_LOG_STATUS

from ..managers import PlotLogManager, PlotLogEntryManager


class PlotLog(BaseDispatchSyncUuidModel):

    plot = models.OneToOneField(Plot)

    history = AuditTrail()

    objects = PlotLogManager()

    def __unicode__(self):
        return unicode(self.plot)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot__plot_identifier')

    def natural_key(self):
        return self.plot.natural_key()
    natural_key.dependencies = ['bcpp_household.plot', ]

    class Meta:
        app_label = 'bcpp_household'


class PlotLogEntry(BaseDispatchSyncUuidModel):

    plot_log = models.ForeignKey(PlotLog)

    log_status = models.CharField(
        verbose_name='What is the status of this log?',
        max_length=25,
        choices=PLOT_LOG_STATUS,
        blank=True,
        null=True,
        )

    report_datetime = models.DateTimeField("Report date",
        validators=[datetime_not_before_study_start, datetime_not_future, date_in_survey],
        )

    comment = EncryptedTextField(
        null=True,
        blank=True,
        )

    history = AuditTrail()

    objects = PlotLogEntryManager()

    def save(self, *args, **kwargs):
        if self.log_status == 'INACCESSIBLE':
            plt = self.plot_log.plot
            plt.status = 'inaccessible'
            plt.save()
        super(PlotLogEntry, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.report_datetime, ) + self.plot_log.natural_key()

    def bypass_for_edit_dispatched_as_item(self):
        return True

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot_log__plot__plot_identifier')

    def __unicode__(self):
        return unicode(self.plot_log) + '(' + unicode(self.report_datetime) + ')'

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('plot_log', 'report_datetime')
