from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured
from audit_trail.audit import AuditTrail
from bhp_dispatch.models import BaseDispatchSyncUuidModel
from bhp_device.classes import Device
from bhp_identifier.exceptions import IdentifierError
from bhp_crypto.fields import (EncryptedTextField, EncryptedDecimalField)
from bcpp_household.managers import HouseholdManager
from bcpp_household.classes import HouseholdIdentifier
from bcpp_household.choices import HOUSEHOLD_STATUS
from plot import Plot


class Household(BaseDispatchSyncUuidModel):

    plot = models.ForeignKey(Plot, null=True)

    household_identifier = models.CharField(
        verbose_name='Household Identifier',
        max_length=25,
        unique=True,
        help_text=_("Household identifier"),
        editable=False,
        db_index=True,
        )

    household_sequence = models.IntegerField(
        editable=False,
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

    status = models.CharField(
        verbose_name='Household status',
        max_length=17,
        null=True,
        choices=HOUSEHOLD_STATUS,
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
        editable=False,
        )

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

    is_randomised = models.BooleanField(
            verbose_name='Is_randomised',
            editable=False)

    action = models.CharField(
        max_length=25,
        null=True,
        default='unconfirmed',
        editable=False)

    objects = HouseholdManager()
    history = AuditTrail()

    @property
    def mapper_name(self):
        return self.community

    def natural_key(self):
        return (self.household_identifier,)
    natural_key.dependencies = ['bcpp_household.plot', ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.community = self.plot.community
            device = Device()
            self.household_sequence = self.plot.get_next_household_sequence()
            household_identifier = HouseholdIdentifier(plot_identifier=self.plot.plot_identifier,
                                                       household_sequence=self.household_sequence)
            self.household_identifier = household_identifier.get_identifier()
            self.device_id = device.device_id
            if not self.household_identifier:
                raise IdentifierError('Expected a value for household_identifier. Got None')
        self.action = self.get_action()
        super(Household, self).save(*args, **kwargs)

    def check_for_survey_on_pre_save(self, **kwargs):
        Survey = models.get_model('bcpp_survey', 'Survey')
        if Survey.objects.all().count() == 0:
            raise ImproperlyConfigured('Model Survey is empty. Please define at least one survey before creating a Household.')

    def create_household_structure_on_post_save(self, **kwargs):
        """Creates, for each defined survey, a household structure(s) for this household."""
        HouseholdStructure = models.get_model('bcpp_household', 'HouseholdStructure')
        Survey = models.get_model('bcpp_survey', 'Survey')  # checked for on pre-save
        for survey in Survey.objects.all():  # create a household_structure for each survey defined
            if not HouseholdStructure.objects.filter(household=self, survey=survey):
                HouseholdStructure.objects.create(household=self, survey=survey)

    def __unicode__(self):
        return self.household_identifier

    def get_action(self):
        if not self.gps_lon and not self.gps_lat:
            retval = 'unconfirmed'
        elif self.status == 'occupied':
            retval = 'confirmed'
        elif self.status == 'vacant' or self.status == 'invalid':
            retval = 'confirmed'
        else:
            retval = 'unconfirmed'
        return retval

    def get_subject_identifier(self):
        return self.household_identifier

    def gps(self):
        return "S{0} {1} E{2} {3}".format(self.gps_degrees_s, self.gps_minutes_s, self.gps_degrees_e, self.gps_minutes_e)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot__plot_identifier')

#     def is_dispatched_as_container(self, using=None):
#         return False

    def structure(self):
        #url = reverse('admin:{0}__{1}__changelist'.format('bcpp_household', 'householdstructure'))
        return """<a href="{url}" />structure</a>"""#.format(url=url)
    structure.allow_tags = True

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-household_identifier', ]
