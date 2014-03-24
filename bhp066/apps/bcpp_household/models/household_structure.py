from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import get_model

from edc.audit.audit_trail import AuditTrail

from apps.bcpp_survey.models import Survey

from ..managers import HouseholdStructureManager

from .household import Household
from .plot import Plot
from .base_replacement import BaseReplacement


class HouseholdStructure(BaseReplacement):

    """ Each year/survey a new household_structure is created for the household """

    household = models.ForeignKey(Household)

    survey = models.ForeignKey(Survey)

    progress = models.CharField(
        verbose_name='Progress',
        max_length=25,
        default='Not Started',
        null=True,
        editable=False)

    note = models.CharField("Note", max_length=250, blank=True)

    enrolled = models.NullBooleanField(default=None, editable=False, help_text='enrolled by the subject consent of a household_member')

    enrolled_household_member = models.CharField(max_length=36, null=True, editable=False, help_text='pk of consenting household_member that triggered the enroll')

    enrolled_datetime = models.DateTimeField(null=True, editable=False, help_text='datetime household_structure enrolled')

    objects = HouseholdStructureManager()

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.household)

    def save(self, *args, **kwargs):
        if self.enrolled and not self.household.enrolled:
            self.household.enrolled = True
            self.household.save()
        super(HouseholdStructure, self).save(*args, **kwargs)

    def natural_key(self):
        return self.household.natural_key() + self.survey.natural_key()
    natural_key.dependencies = ['bcpp_household.household', 'bcpp_survey.survey']

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household__plot__plot_identifier')

    def replacement_container(self, using=None):
        return self.household

    def get_subject_identifier(self):
        return self.household.plot.plot_identifier

    @property
    def member_count(self):
        """Returns the number of household members in this household for all surveys."""
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        return HouseholdMember.objects.filter(household_structure__pk=self.pk).count()

    @property
    def enrolled_member_count(self):
        """Returns the number of consented (or enrolled) household members in this household for all surveys."""
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        return HouseholdMember.objects.filter(household_structure__pk=self.pk, is_consented=True).count()

    def create_household_log_on_post_save(self, **kwargs):
        HouseholdLog = models.get_model('bcpp_household', 'HouseholdLog')
        if not HouseholdLog.objects.filter(household_structure__pk=self.pk):
            HouseholdLog.objects.create(household_structure=self)

    def plot(self):
        url = reverse('admin:{app_label}_{model_name}_changelist'.format(app_label='bcpp_household', model_name='plot'))
        return """<a href="{url}?q={q}" />plot</a>""".format(url=url, q=self.household.plot.plot_identifier)
    plot.allow_tags = True

    def house(self):
        url = reverse('admin:{app_label}_{model_name}_changelist'.format(app_label='bcpp_household', model_name='household'))
        return """<a href="{url}?q={q}" />household</a>""".format(url=url, q=self.household.household_identifier)
    house.allow_tags = True

    def members(self):
        url = reverse('admin:{app_label}_{model_name}_changelist'.format(app_label='bcpp_household_member', model_name='householdmember'))
        return """<a href="{url}?q={q}'" />members</a>""".format(url=url, q=self.pk)
    members.allow_tags = True

    def logs(self):
        url = reverse('admin:{app_label}_{model_name}_changelist'.format(app_label='bcpp_household', model_name='householdlog'))
        return """<a href="{url}?q={q}'" />log</a>""".format(url=url, q=self.pk)
    logs.allow_tags = True

    def dashboard(self):
        url = reverse('household_dashboard_url', kwargs={'dashboard_type': 'household', 'dashboard_model': 'household_structure', 'dashboard_id': self.pk})
        return """<a href="{url}" />composition</a>""".format(url=url)
    dashboard.allow_tags = True

    class Meta:
        app_label = 'bcpp_household'
        #unique_together = (('household', 'survey'), )
