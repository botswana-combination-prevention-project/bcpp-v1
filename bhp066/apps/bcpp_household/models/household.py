from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.device.sync.models import BaseSyncUuidModel
from edc_base.encrypted_fields import EncryptedTextField, EncryptedDecimalField
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.map.classes import site_mappers

from ..exceptions import AlreadyReplaced
from ..managers import HouseholdManager

from .plot import Plot


class Household(BaseDispatchSyncUuidModel, BaseSyncUuidModel):
    """A system model that represents the household asset. See also HouseholdStructure."""

    plot = models.ForeignKey(Plot, null=True)

    household_identifier = models.CharField(
        verbose_name='Household Identifier',
        max_length=25,
        unique=True,
        help_text="Household identifier",
        null=True,
        editable=False)

    household_sequence = models.IntegerField(
        editable=False,
        null=True,
        help_text=('is 1 for first household in plot, 2 for second, 3, etc. '
                   'Embedded in household identifier.'))

    hh_int = models.IntegerField(
        null=True,
        editable=False,
        help_text='not used')

    hh_seed = models.IntegerField(
        null=True,
        editable=False,
        help_text='not used')

    report_datetime = models.DateTimeField(
        verbose_name='Report Date/Time',
        null=True)

    gps_degrees_s = EncryptedDecimalField(
        verbose_name='GPS Degrees-South',
        max_digits=10,
        null=True,
        decimal_places=0,
        editable=False,
        help_text='comes from plot')

    gps_minutes_s = EncryptedDecimalField(
        verbose_name='GPS Minutes-South',
        max_digits=10,
        null=True,
        decimal_places=4,
        editable=False,
        help_text='comes from plot')

    gps_degrees_e = EncryptedDecimalField(
        verbose_name='GPS Degrees-East',
        null=True,
        max_digits=10,
        decimal_places=0,
        editable=False,
        help_text='comes from plot')

    gps_minutes_e = EncryptedDecimalField(
        verbose_name='GPS Minutes-East',
        max_digits=10,
        null=True,
        decimal_places=4,
        editable=False,
        help_text='comes from plot')

    gps_lon = models.FloatField(
        verbose_name='longitude',
        null=True,
        editable=False,
        help_text='comes from plot')

    gps_lat = models.FloatField(
        verbose_name='latitude',
        null=True,
        editable=False,
        help_text='comes from plot')

    gps_target_lon = models.FloatField(
        verbose_name='target waypoint longitude',
        null=True,
        editable=False,
        help_text='comes from plot')

    gps_target_lat = models.FloatField(
        verbose_name='target waypoint latitude',
        null=True,
        editable=False,
        help_text='comes from plot')

    target_radius = models.FloatField(default=.025, help_text='km', editable=False)

    community = models.CharField(
        max_length=25,
        help_text='If the community is incorrect, please contact the DMC immediately.',
        null=True,
        editable=False)

    replaced_by = models.CharField(
        max_length=25,
        null=True,
        help_text=u'The identifier of the plot that this household is replaced by',
        editable=False)

    replaceable = models.NullBooleanField(
        verbose_name='Replaceable?',
        default=None,
        editable=False,
        help_text='Updated by replacement helper')

    comment = EncryptedTextField(
        max_length=250,
        help_text="You may provide a comment here or leave BLANK.",
        blank=True,
        null=True)

    uploaded_map = models.CharField(
        verbose_name="filename of uploaded map",
        max_length=25,
        null=True,
        blank=True)

    # not used!!
    action = models.CharField(
        max_length=25,
        null=True,
        default='unconfirmed',
        editable=False)

    # updated by subject_consent save method
    enrolled = models.BooleanField(
        default=False,
        editable=False,
        help_text=('Set to true if one member is consented. '
                   'Updated by Household_structure post_save.'))

    enrolled_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text=('datetime that household is enrolled. '
                   'Updated by Household_structure post_save.'))

    history = AuditTrail()

    objects = HouseholdManager()

    def save(self, *args, **kwargs):
        using = kwargs.get('using')
        try:
            if self.__class__.objects.using(using).get(id=self.id).replaced_by:
                raise AlreadyReplaced('Household {0} has been replaced '
                                      'by plot {1}.'.format(self.household_identifier,
                                                            self.replaced_by))
        except self.__class__.DoesNotExist:
            pass
        self.allow_enrollment(using)
        return super(Household, self).save(*args, **kwargs)

    def get_identifier(self):
        return self.household_identifier

    def allow_enrollment(self, using, exception_cls=None, instance=None):
        """Raises an exception if the plot is not enrolled and
        BHS_FULL_ENROLLMENT_DATE is past."""
        instance = instance or self
        return self.plot.allow_enrollment(using, exception_cls,
                                          plot_instance=instance.plot)

    @property
    def mapper_name(self):
        return self.community

    def __unicode__(self):
        if site_mappers.get_mapper(site_mappers.current_community)().clinic_plot_identifier[0:6] == self.household_identifier[0:6]:
            return self.plot.description
        return self.household_identifier

    def natural_key(self):
        return (self.household_identifier,)
    natural_key.dependencies = ['bcpp_household.household', ]

    def get_subject_identifier(self):
        return self.household_identifier

    def gps(self):
        return "S{0} {1} E{2} {3}".format(
            self.gps_degrees_s, self.gps_minutes_s, self.gps_degrees_e, self.gps_minutes_e)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot__plot_identifier')

    def bypass_for_edit_dispatched_as_item(self, using=None, update_fields=None):
        """Bypasses dispatched check if update_fields is set by the replacement_helper."""
        try:
            if 'replaced_by' in update_fields:
                return True
        except TypeError as type_error:
            if '\'NoneType\' is not iterable' in str(type_error):
                pass
        return False

    def structure(self):
        return """<a href="{url}" />structure</a>"""  # .format(url=url)
    structure.allow_tags = True

    def member_count(self):
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        return HouseholdMember.objects.filter(household_structure__household__pk=self.pk).count()

    def deserialize_prep(self, **kwargs):
        # Household being deleted by an IncommingTransaction, we go ahead and delete it.
        # An extra household created by mistake.
        if kwargs.get('action', None) and kwargs.get('action', None) == 'D':
            self.delete()

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-household_identifier', ]
