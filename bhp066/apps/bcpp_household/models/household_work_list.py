from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from bhp066.apps.bcpp_survey.models import Survey

from ..choices import HOUSEHOLD_LOG_STATUS
from ..managers import HouseholdWorkListManager

from .household_structure import HouseholdStructure
from .plot import Plot


class HouseholdWorkList(BaseDispatchSyncUuidModel):

    """A system model that links a household to its household members
    for a given survey year and helps track the enrollment status, enumeration
    status, enumeration attempts and other system values. """

    household_structure = models.ForeignKey(HouseholdStructure)

    survey = models.ForeignKey(
        Survey,
        editable=False)

    label = models.CharField(
        max_length=25,
        help_text="label to group, e.g. T1 prep"
    )

    visit_date = models.DateField(
        editable=False)

    status = models.CharField(
        max_length=25,
        choices=(
            ('scheduled', 'Scheduled'),
            ('missed_scheduled', 'Scheduled!!'),
            ('unscheduled', 'Unscheduled'),
            ('incomplete', 'Incomplete'),
            ('done', 'Done'),
        ),
        editable=False
    )

    appt_count = models.IntegerField(
        default=0,
        editable=False,
        help_text='Number of currently scheduled appointments, including missed.'
    )

    enrolled_type = models.CharField(
        choices=(
            ('hic', 'HIC/BHS'),
            ('bhs', 'BHS Only')
        ),
        max_length=3,
        editable=False
    )

    note = models.CharField("Note", max_length=250, blank=True)

    log_date = models.DateField(
        editable=False,
        null=True,
        help_text='From household_log entries')

    log_status = models.CharField(
        verbose_name='Household Status',
        max_length=50,
        choices=HOUSEHOLD_LOG_STATUS,
        null=True,
        blank=False)

    log_attempts = models.IntegerField(default=0)

    members = models.IntegerField(default=0)

    bhs = models.IntegerField(default=0)

    hic = models.IntegerField(default=0)

    objects = HouseholdWorkListManager()

    history = AuditTrail()

    def __unicode__(self):
        return '{}'.format(unicode(self.household_structure))

    def save(self, *args, **kwargs):
        super(HouseholdWorkList, self).save(*args, **kwargs)

    def natural_key(self):
        return self.household.natural_key() + self.survey.natural_key()
    natural_key.dependencies = ['bcpp_household.householdstructure', 'bcpp_survey.survey']

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_structure__household__plot__plot_identifier')

    def get_subject_identifier(self):
        return self.household_structure.household.plot.plot_identifier

    def call_list(self):
        url = reverse('admin:bcpp_subject_calllist_changelist')
        return """<a href="{url}?q={q}" />call list</a>""".format(
            url=url, q=self.household_structure.pk)
    call_list.allow_tags = True

    def plot(self):
        search_term = self.household_structure.household.plot.plot_identifier
        url = reverse('section_search_word_url', kwargs={
            'section_name': 'plot',
            'search_name': 'word',
            'search_term': search_term})
        return """<a href="{url}" />{q}</a>""".format(
            url=url, q=search_term)
    plot.allow_tags = True

    def appt(self):
        url = reverse('admin:bcpp_household_member_memberappointment_changelist')
        return """<a href="{url}?q={q}" />appts</a>""".format(
            url=url, q=self.household_structure.pk)
    appt.allow_tags = True

    def composition(self):
        url = reverse('household_dashboard_url',
                      kwargs={'dashboard_type': 'household',
                              'dashboard_model': 'household_structure',
                              'dashboard_id': self.household_structure.pk})
        return """<a href="{url}" />{identifier}</a>""".format(
            url=url, identifier=self.household_structure.household.household_identifier)
    composition.allow_tags = True

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('household_structure', 'label')
