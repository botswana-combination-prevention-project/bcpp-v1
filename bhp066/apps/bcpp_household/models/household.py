from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.core.crypto_fields.fields import (EncryptedTextField, EncryptedDecimalField)
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..managers import HouseholdManager

from .plot import Plot
from ..exceptions import AlreadyReplaced


class Household(BaseDispatchSyncUuidModel):

    plot = models.ForeignKey(Plot, null=True)

    household_identifier = models.CharField(
        verbose_name='Household Identifier',
        max_length=25,
        unique=True,
        help_text=_("Household identifier"),
        null=True,
        editable=False)

    household_sequence = models.IntegerField(
        editable=False,
        null=True,
        help_text='is 1 for first household in plot, 2 for second, 3, etc. Embedded in household identifier.')

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
        verbose_name='Identifier',
        help_text=u'The identifier of the plot that this household is replaced by',
        editable=False)

    comment = EncryptedTextField(
        max_length=250,
        help_text=_("You may provide a comment here or leave BLANK."),
        blank=True,
        null=True)

    uploaded_map = models.CharField(
        verbose_name="filename of uploaded map",
        max_length=25,
        null=True,
        blank=True)

    action = models.CharField(
        max_length=25,
        null=True,
        default='unconfirmed',
        editable=False)

    # updated by subject_consent save method
    enrolled = models.BooleanField(
        default=False,
        editable=False,
        help_text='Set to true if one member is consented. Updated by Household_structure post_save.')

    enrolled_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text='datetime that household is enrolled. Updated by Household_structure post_save.')

    objects = HouseholdManager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        using = kwargs.get('using')
        try:
            # if household is replaced abort the save
            if self.__class__.objects.using(using).get(id=self.id).replaced_by:
                raise AlreadyReplaced('Household {0} has been replaced '
                                      'by plot {1}.'.format(self.household_identifier, self.replaced_by))
        except self.__class__.DoesNotExist:
            pass
        return super(Household, self).save(*args, **kwargs)

    @property
    def mapper_name(self):
        return self.community

    def __unicode__(self):
        return self.household_identifier

    def natural_key(self):
        return (self.household_identifier,)
    natural_key.dependencies = ['bcpp_household.household', ]

    def get_subject_identifier(self):
        return self.household_identifier

    def gps(self):
        return "S{0} {1} E{2} {3}".format(self.gps_degrees_s, self.gps_minutes_s, self.gps_degrees_e, self.gps_minutes_e)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot__plot_identifier')

    def structure(self):
        return """<a href="{url}" />structure</a>"""  # .format(url=url)
    structure.allow_tags = True

    def member_count(self):
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        return HouseholdMember.objects.filter(household_structure__household__pk=self.pk).count()

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-household_identifier', ]
