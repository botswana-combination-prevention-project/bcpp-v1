from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from apps.bcpp_survey.models import Survey

from ..managers import HouseholdStructureManager

from .household_structure import HouseholdStructure
from .plot import Plot


class HouseholdWorkList(BaseDispatchSyncUuidModel):

    """A system model that links a household to its household members
    for a given survey year and helps track the enrollment status, enumeration
    status, enumeration attempts and other system values. """

    household_structure = models.ForeignKey(HouseholdStructure)

    survey = models.ForeignKey(Survey,
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
        max_length=25,
        editable=False
        )

    note = models.CharField("Note", max_length=250, blank=True)

    log_date = models.DateField(
        editable=False,
        help_text='From household_log entries')

    log_status = models.DateField(
        editable=False,
        help_text='From household_log entries')

    log_attempts = models.IntegerField(default=0)

    objects = HouseholdStructureManager()

    history = AuditTrail()

    def __unicode__(self):
        return '{}'.format(unicode(self.household))

    def save(self, *args, **kwargs):
        super(HouseholdWorkList, self).save(*args, **kwargs)

    def natural_key(self):
        return self.household.natural_key() + self.survey.natural_key()
    natural_key.dependencies = ['bcpp_household.householdstructure', 'bcpp_survey.survey']

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_structure__household__plot__plot_identifier')

    def get_subject_identifier(self):
        return self.household_structure.household.plot.plot_identifier

    @property
    def members(self):
        """Returns the number of household members in this household for all surveys."""
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        return HouseholdMember.objects.filter(household_structure__pk=self.pk).count()

    @property
    def bhs(self):
        """Returns the number of consented (or enrolled) household members
        in this household for all surveys."""
        SubjectConsent = models.get_model('bcpp_subject', 'SubjectConsent')
        return SubjectConsent.objects.filter(
            household_member__household_structure__pk=self.household_structure.pk).count()

    def call_list(self):
        url = reverse('admin:bcpp_subject_calllist_changelist')
        return """<a href="{url}?q={q}" />call list</a>""".format(
            url=url, q=self.household_structure.pk)
    call_list.allow_tags = True

    def appt(self):
        url = reverse('admin:bcpp_househol_member_memberappointment_changelist')
        return """<a href="{url}?q={q}" />call list</a>""".format(
            url=url, q=self.household_structure.pk)
    call_list.allow_tags = True

    def composition(self):
        url = reverse('household_dashboard_url',
                      kwargs={'dashboard_type': 'household',
                              'dashboard_model': 'household_structure',
                              'dashboard_id': self.household_structure.pk})
        return """<a href="{url}" />composition</a>""".format(url=url)
    composition.allow_tags = True

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('household_structure', 'label')
