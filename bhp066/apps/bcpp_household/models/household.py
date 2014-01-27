from django.db import models
from django.utils.translation import ugettext as _
from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.core.crypto_fields.fields import (EncryptedTextField, EncryptedDecimalField)
from ..managers import HouseholdManager
from ..classes import HouseholdIdentifier
from .plot import Plot

from ..choices import ENUMERATION_STATUS

class Household(BaseDispatchSyncUuidModel):

    plot = models.ForeignKey(Plot, null=True)  # TODO: field should not be nullable.

    household_identifier = models.CharField(
        verbose_name='Household Identifier',
        max_length=25,
        unique=True,
        help_text=_("Household identifier"),
        null=True,
        editable=False,
        )

    household_sequence = models.IntegerField(
        editable=False,
        null=True,
        help_text='is 1 for first household in plot, 2 for second, 3, etc. Embedded in household identifier.'
        )

    hh_int = models.IntegerField(
        null=True,
        editable=False,
        help_text='not used'
        )

    hh_seed = models.IntegerField(
        null=True,
        editable=False,
        help_text='not used'
        )

    report_datetime = models.DateTimeField(
        verbose_name='Report Date/Time',
        null=True,
        )

    gps_degrees_s = EncryptedDecimalField(
        verbose_name='GPS Degrees-South',
        max_digits=10,
        null=True,
        decimal_places=0,
        editable=False,
        help_text='comes from plot',
        )

    gps_minutes_s = EncryptedDecimalField(
        verbose_name='GPS Minutes-South',
        max_digits=10,
        null=True,
        decimal_places=4,
        editable=False,
        help_text='comes from plot',
        )

    gps_degrees_e = EncryptedDecimalField(
        verbose_name='GPS Degrees-East',
        null=True,
        max_digits=10,
        decimal_places=0,
        editable=False,
        help_text='comes from plot',
        )

    gps_minutes_e = EncryptedDecimalField(
        verbose_name='GPS Minutes-East',
        max_digits=10,
        null=True,
        decimal_places=4,
        editable=False,
        help_text='comes from plot',
        )

    gps_lon = models.FloatField(
        verbose_name='longitude',
        null=True,
        editable=False,
        help_text='comes from plot',
        )

    gps_lat = models.FloatField(
        verbose_name='latitude',
        null=True,
        editable=False,
        help_text='comes from plot',
        )

    gps_target_lon = models.FloatField(
        verbose_name='target waypoint longitude',
        null=True,
        editable=False,
        help_text='comes from plot',
        )

    gps_target_lat = models.FloatField(
        verbose_name='target waypoint latitude',
        null=True,
        editable=False,
        help_text='comes from plot',
        )

    target_radius = models.FloatField(default=.025, help_text='km', editable=False)

    community = models.CharField(
        max_length=25,
        help_text='If the community is incorrect, please contact the DMC immediately.',
        null=True,
        editable=False,
        )

    allowed_to_enumerate = models.CharField(
        max_length=25,
        default='no',
        null=False,
        verbose_name='Does the Household memeber and Head of Household allow you to enumerate them?',
        choices=ENUMERATION_STATUS,
        editable=True,
        )

    #Indicates that a household has been replaced if its part of twenty percent.
    #For five percent indicates that a household has been used for replacement.
    replacement = models.BooleanField(default=False, editable=False)

    comment = EncryptedTextField(
        max_length=250,
        help_text=_("You may provide a comment here or leave BLANK."),
        blank=True,
        null=True,
        )

    uploaded_map = models.CharField(
        verbose_name="filename of uploaded map",
        max_length=25,
        null=True,
        blank=True,
        )

    action = models.CharField(
        max_length=25,
        null=True,
        default='unconfirmed',
        editable=False)

    enrolled = models.BooleanField(default=False, editable=False, help_text='Set to true if one member is consented')

    complete = models.BooleanField(default=False, editable=False, help_text='Set to true if one member is consented')

    enumeration_attempts = models.IntegerField(
        default=0,
        editable=False,
        help_text='Number of attempts to enumerate a plot to determine it\'s status.'
        )

    objects = HouseholdManager()

    history = AuditTrail()

    @property
    def mapper_name(self):
        return self.community

    def __unicode__(self):
        return self.household_identifier

    def natural_key(self):
        return (self.household_identifier,)
    natural_key.dependencies = ['bcpp_household.plot', ]

    def post_save_update_identifier(self, instance, created):
        """Updates the identifier field if this is a new instance."""
        if created:
            instance.community = instance.plot.community
            household_identifier = HouseholdIdentifier(plot_identifier=instance.plot.plot_identifier)
            instance.household_identifier = household_identifier.get_identifier()
            instance.save()

    def post_save_create_household_structure(self, instance, created):
        """Creates, for each defined survey, a household structure(s) for this household."""
        if created:
            HouseholdStructure = models.get_model('bcpp_household', 'HouseholdStructure')
            Survey = models.get_model('bcpp_survey', 'Survey')  # checked for on pre-save
            for survey in Survey.objects.all():  # create a household_structure for each survey defined
                if not HouseholdStructure.objects.filter(household__pk=instance.pk, survey=survey):
                    HouseholdStructure.objects.create(household=instance, survey=survey)

    def post_save_plot_allowed_to_enumerate(self, instance, created):
        """Updates the allowed_to_enumerate field on the plot model."""
        plot = Plot.objects.get(plot_identifier=instance.plot.plot_identifier)
        if instance.allowed_to_enumerate == 'no':
            plot.allowed_to_enumerate = 'no'
            plot.save()
        else:
            plot.allowed_to_enumerate = 'yes'
            plot.save()

    def get_subject_identifier(self):
        return self.household_identifier

    def gps(self):
        return "S{0} {1} E{2} {3}".format(self.gps_degrees_s, self.gps_minutes_s, self.gps_degrees_e, self.gps_minutes_e)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot__plot_identifier')

    def structure(self):
        #url = reverse('admin:{0}__{1}__changelist'.format('bcpp_household', 'householdstructure'))
        return """<a href="{url}" />structure</a>"""  # .format(url=url)
    structure.allow_tags = True

    def member_count(self):
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        return HouseholdMember.objects.filter(household_structure__household__pk=self.pk).count()

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-household_identifier', ]
