from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.core.exceptions import ValidationError

from edc_base.audit_trail import AuditTrail
from edc_sync.models import SyncModelMixin
from edc_base.model.models import BaseUuidModel
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from bhp066.apps.bcpp_survey.models import Survey

from ..exceptions import AlreadyReplaced
from ..managers import HouseholdStructureManager

from .household import Household
from .plot import Plot


class HouseholdStructure(BaseDispatchSyncUuidModel, BaseSyncUuidModel):

    """A system model that links a household to its household members
    for a given survey year and helps track the enrollment status, enumeration
    status, enumeration attempts and other system values. """

    household = models.ForeignKey(Household)

    survey = models.ForeignKey(Survey)

    progress = models.CharField(
        verbose_name='Progress',
        max_length=25,
        default='Not Started',
        null=True,
        editable=False)

    note = models.CharField("Note", max_length=250, blank=True)

    enrolled = models.NullBooleanField(
        default=None,
        editable=False,
        help_text='enrolled by the subject consent of a household_member')

    enrolled_household_member = models.CharField(
        max_length=36,
        null=True,
        editable=False,
        help_text='pk of consenting household_member that triggered the enroll')

    enrolled_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text='datetime household_structure enrolled')

    enumerated = models.BooleanField(
        default=False,
        editable=False,
        help_text='Set to True when first household_member is enumerated')

    enumeration_attempts = models.IntegerField(
        default=0,
        editable=False,
        help_text=('Updated by a signal on HouseholdLogEntry. '
                   'Number of attempts to enumerate a household_structure.'))

    refused_enumeration = models.BooleanField(
        default=False,
        editable=False,
        help_text='Updated by household enumeration refusal save method only')

    failed_enumeration_attempts = models.IntegerField(
        default=0,
        editable=False,
        help_text=('Updated by a signal on HouseholdLogEntry. Number of failed attempts to'
                   'enumerate a household_structure.'))

    failed_enumeration = models.BooleanField(
        default=False,
        editable=False,
        help_text='Updated by household assessment save method only')

    no_informant = models.BooleanField(
        default=False,
        editable=False,
        help_text='Updated by household assessment save method only')

    eligible_members = models.BooleanField(
        default=False,
        editable=False,
        help_text='Updated by household member save method and post_delete')

    objects = HouseholdStructureManager()

    history = AuditTrail()

    def __unicode__(self):
        return '{} {}'.format(unicode(self.household), self.survey.survey_abbrev)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', [])
        if update_fields:
            pass
        else:
            if self.household.replaced_by:
                raise AlreadyReplaced('Household {0} replaced.'.format(self.household.household_identifier))
            # test survey vs created date + survey_slug for the current survey only
            if self.id and Survey.objects.current_survey().survey_slug == self.survey.survey_slug:
                Survey.objects.current_survey(report_datetime=datetime.today(), survey_slug=self.survey.survey_slug)
        super(HouseholdStructure, self).save(*args, **kwargs)

    def natural_key(self):
        return self.household.natural_key() + self.survey.natural_key()
    natural_key.dependencies = ['bcpp_household.household', 'bcpp_survey.survey']

    def allow_enrollment(self, using, exception_cls=None, instance=None):
        """Raises an exception if the household is not enrolled
        and BHS_FULL_ENROLLMENT_DATE is past."""
        instance = instance or self
        return self.household.plot.allow_enrollment(using, exception_cls=exception_cls,
                                                    plot_instance=instance.household.plot)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household__plot__plot_identifier')

    def get_subject_identifier(self):
        return self.household.plot.plot_identifier

    @property
    def member_count(self):
        """Returns the number of household members in this household for all surveys."""
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        return HouseholdMember.objects.filter(household_structure__pk=self.pk).count()

    @property
    def enrolled_member_count(self):
        """Returns the number of consented (or enrolled) household members
        in this household for all surveys."""
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        return HouseholdMember.objects.filter(household_structure__pk=self.pk,
                                              is_consented=True).count()

    @property
    def previous(self):
        """Returns the previous household_structure (ordered by survey) relative to self
        and returns None if there is no previous survey."""
        household_structure = None
        try:
            household_structure = self.__class__.objects.filter(
                household=self.household,
                survey__datetime_start__lt=self.survey.datetime_start).exclude(
                    id=self.id).order_by('-survey__datetime_start')[0]
        except IndexError:
            pass
        return household_structure

    @property
    def first(self):
        """Returns the first household_structure (ordered by survey) using self
        and returns self if self is the first household_structure."""
        household_structure = None
        try:
            household_structure = self.__class__.objects.filter(
                household=self.household,
                survey__datetime_start__lt=self.survey.datetime_start).exclude(
                    id=self.id).order_by('survey__datetime_start')[0]
        except IndexError:
            household_structure = self
        return household_structure

    def check_eligible_representative_filled(self, using=None, exception_cls=None):
        """Raises an exception if the RepresentativeEligibility form has not been completed.

        Without RepresentativeEligibility, a HouseholdMember cannot be added."""
        exception_cls = exception_cls or ValidationError
        using = using or 'default'
        RepresentativeEligibility = models.get_model('bcpp_household', 'RepresentativeEligibility')
        try:
            RepresentativeEligibility.objects.using(using).get(household_structure=self)
        except RepresentativeEligibility.DoesNotExist:
            verbose_name = RepresentativeEligibility._meta.verbose_name
            raise exception_cls('\'{}\' for an eligible '
                                'representative has not been completed.'.format(verbose_name))

    @property
    def has_household_log_entry(self):
        """Confirms there is an househol_log_entry for today."""
        has_household_log_entry = False
        try:
            if self.household_log.todays_household_log_entries:
                has_household_log_entry = True
        except AttributeError:
            pass
        return has_household_log_entry

    def plot(self):
        url = reverse('admin:{app_label}_{model_name}_changelist'.format(
            app_label='bcpp_household', model_name='plot'))
        return """<a href="{url}?q={q}" />plot</a>""".format(
            url=url, q=self.household.plot.plot_identifier)
    plot.allow_tags = True

    def house(self):
        url = reverse('admin:{app_label}_{model_name}_changelist'.format(
            app_label='bcpp_household', model_name='household'))
        return """<a href="{url}?q={q}" />household</a>""".format(
            url=url, q=self.household.household_identifier)
    house.allow_tags = True

    def members(self):
        url = reverse('admin:{app_label}_{model_name}_changelist'.format(
            app_label='bcpp_household_member', model_name='householdmember'))
        return """<a href="{url}?q={q}'" />members</a>""".format(url=url, q=self.pk)
    members.allow_tags = True

    def logs(self):
        url = reverse('admin:{app_label}_{model_name}_changelist'.format(
            app_label='bcpp_household', model_name='householdlog'))
        return """<a href="{url}?q={q}'" />log</a>""".format(url=url, q=self.pk)
    logs.allow_tags = True

    def dashboard(self):
        url = reverse('household_dashboard_url',
                      kwargs={'dashboard_type': 'household',
                              'dashboard_model': 'household_structure',
                              'dashboard_id': self.pk})
        return """<a href="{url}" />composition</a>""".format(url=url)
    dashboard.allow_tags = True

    def deserialize_prep(self, **kwargs):
        # HouseholdStructure being deleted by an IncommingTransaction, we go ahead and delete it.
        # An extra household created by mistake.
        if kwargs.get('action', None) and kwargs.get('action', None) == 'D':
            self.delete()

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('survey', 'household')
