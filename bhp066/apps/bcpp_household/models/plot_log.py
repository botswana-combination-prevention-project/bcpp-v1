from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.db import models
from django.db.models import Min
from django.db.models.loading import get_model

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.core.crypto_fields.fields import EncryptedTextField

from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from apps.bcpp_survey.models import Survey
from apps.bcpp_survey.validators import date_in_survey

from .plot import Plot
from ..choices import PLOT_LOG_STATUS, INACCESSIBILITY_REASONS

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

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[datetime_not_before_study_start, datetime_not_future, date_in_survey])

    log_status = models.CharField(
        verbose_name='What is the status of this plot?',
        max_length=25,
        choices=PLOT_LOG_STATUS)

    reason = models.CharField(
        verbose_name=_('If inaccessible, please indicate the reason.'),
        max_length=25,
        blank=True,
        null=True,
        choices=INACCESSIBILITY_REASONS)

    reason_other = models.CharField(
        verbose_name=_('If Other, specify'),
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

    def natural_key(self):
        return (self.report_datetime, ) + self.plot_log.natural_key()

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot_log__plot__plot_identifier')

    def allow_enrollment(self, plot_log_entry, exception_cls=None, using=None):
        """Stops enrollments."""
        exception_cls = exception_cls or ValidationError
        using = using or 'default'
        allow_edit = []
        households = None
        first_survey_start_datetime = Survey.objects.using(using).all().aggregate(datetime_start=Min('datetime_start')).get('datetime_start')
        survey = Survey.objects.using(using).get(datetime_start=first_survey_start_datetime)
        if self.plot_log.plot.household_count >= 1:
            households = get_model('bcpp_household', 'Household').objects.filter(plot=self.plot_log.plot)
            for household in households:
                allow_edit.append(get_model('bcpp_household', 'HouseholdStructure').objects.get(survey=survey, household=household).enrolled)
        if not (len(set(allow_edit)) == 1):
            raise exception_cls("adding logs or modifying logs is not allowed anymore where there is no at least one enrolled individual")

    def __unicode__(self):
        return unicode(self.plot_log) + '(' + unicode(self.report_datetime) + ')'

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('plot_log', 'report_datetime')
