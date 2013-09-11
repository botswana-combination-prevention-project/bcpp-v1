import re
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.conf import settings
from audit_trail.audit import AuditTrail
from bhp_dispatch.models import BaseDispatchSyncUuidModel
from django.utils.translation import ugettext as _
from bhp_crypto.fields import (EncryptedCharField, EncryptedTextField, EncryptedDecimalField)
from bhp_device.classes import Device
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError
from bhp_identifier.exceptions import IdentifierError
from bcpp_household.managers import PlotManager
from bcpp_household.classes import PlotIdentifier
from bcpp_household.choices import PLOT_STATUS, SECTIONS, SUB_SECTIONS, BCPP_VILLAGES


def is_valid_community(self, value):
        """Validates the community string against a list of site_mappers map_areas."""
        if value.lower() not in [l.lower() for l in site_mappers.get_as_list()]:
            raise ValidationError(u'{0} is not a valid community name.'.format(value))


class Plot(BaseDispatchSyncUuidModel):

    plot_identifier = models.CharField(
        verbose_name='Plot Identifier',
        max_length=25,
        unique=True,
        help_text=_("Plot identifier"),
        editable=False,
        db_index=True,
        )

    eligible_members = models.IntegerField(
        verbose_name="Number of Eligible member",
        blank=True,
        null=True,
        help_text=("Provide the number of people who live in the household who are eligible."),)

    description = EncryptedTextField(
        verbose_name="House household description",
        max_length=250,
        help_text=("You may provide a comment here about the house description, e.g color of the house."),
        blank=True,
        null=True,
        )

    cso_number = EncryptedCharField(
        verbose_name="CSO Number",
        blank=True,
        null=True,
        db_index=True,
        help_text=("provide the CSO number or leave BLANK."),
        )

    num_household = models.IntegerField(
        verbose_name="Number of Households in a plot.",
        blank=True,
        null=True,
        help_text=("Provide the number of Households in a plot.."),)

    comment = EncryptedTextField(
        max_length=250,
        help_text=("You may provide a comment here or leave BLANK."),
        blank=True,
        null=True,
        )

    availability_datetime = models.DateTimeField(
        verbose_name='General Date/Time when most of the household members will be available',
        null=True,
        )

    gps_degrees_s = EncryptedDecimalField(
        verbose_name='GPS Degrees-South',
        max_digits=10,
        null=True,
        decimal_places=0,
        )

    gps_minutes_s = EncryptedDecimalField(
        verbose_name='GPS Minutes-South',
        max_digits=10,
        null=True,
        decimal_places=4,
        )

    gps_degrees_e = EncryptedDecimalField(
        verbose_name='GPS Degrees-East',
        null=True,
        max_digits=10,
        decimal_places=0,
        )

    gps_minutes_e = EncryptedDecimalField(
        verbose_name='GPS Minutes-East',
        max_digits=10,
        null=True,
        decimal_places=4,
        )

    gps_lon = models.FloatField(
        verbose_name='longitude',
        null=True,
        editable=False,
        )

    gps_lat = models.FloatField(
        verbose_name='latitude',
        null=True,
        editable=False,
        )

    gps_target_lon = models.FloatField(
        verbose_name='target waypoint longitude',
        null=True,
        editable=False,
        )

    gps_target_lat = models.FloatField(
        verbose_name='target waypoint latitude',
        null=True,
        editable=False,
        )

    target_radius = models.FloatField(default=.025, help_text='km', editable=False)

    device_id = models.CharField(
        max_length=2,
        null=True,
        editable=False,
        )

    action = models.CharField(
        max_length=25,
        null=True,
        default='unconfirmed',
        editable=False)

    uploaded_map = models.CharField(
        verbose_name="filename of uploaded map",
        max_length=25,
        null=True,
        blank=True,
        )

    community = models.CharField(
        max_length=25,
        help_text='If the community is incorrect, please contact the DMC immediately.',
        validators=[is_valid_community, ],
        )

    section = models.CharField(
        max_length=25,
        null=True,
        verbose_name='Section',
        choices=SECTIONS,
        )

    sub_section = models.CharField(
        max_length=25,
        null=True,
        verbose_name='Sub-section',
        choices=SUB_SECTIONS,
        help_text=u'',
        )

    status = models.CharField(
        verbose_name='Plot status',
        max_length=15,
        null=True,
        choices=PLOT_STATUS,
        )

    objects = PlotManager()
    history = AuditTrail()

    def __unicode__(self):
        return self.plot_identifier

    def natural_key(self):
        return (self.plot_identifier,)

    def save(self, *args, **kwargs):
        # if user added/updated gps_degrees_[es] and gps_minutes_[es], update gps_lat, gps_lon
        if not self.community:
            raise ValidationError('Attribute \'community\' may not be None for model {0}'.format(self))
        mapper_cls = site_mappers.get_registry(self.community)
        mapper = mapper_cls()
        if not self.id:
#             device = Device()
#             self.device_id = device.device_id
            plot_identifier = PlotIdentifier(community=mapper.get_map_code())
            self.plot_identifier = plot_identifier.get_identifier()
            if not self.plot_identifier:
                raise IdentifierError('Expected a value for plot_identifier. Got None')
#             self.hh_int = re.search('\d+', self.plot_identifier).group(0)
        if self.gps_degrees_e and self.gps_degrees_s and self.gps_minutes_e and self.gps_minutes_s:
            self.gps_lat = mapper.get_gps_lat(self.gps_degrees_s, self.gps_minutes_s)
            self.gps_lon = mapper.get_gps_lon(self.gps_degrees_e, self.gps_minu.tes_e)
            mapper.verify_gps_location(self.gps_lat, self.gps_lon, MapperError)
            mapper.verify_gps_to_target(self.gps_lat, self.gps_lon, self.gps_target_lat, self.gps_target_lon, self.target_radius, MapperError)
        self.action = self.get_action()
        super(Plot, self).save(*args, **kwargs)

    def get_next_household_sequence(self):
        """Returns the next sequence number for the next household identifier to use in this plot.

        Default is 1"""
        Household = models.get_model('bcpp_household', 'Household')
        sequence = 1
        for household in Household.objects.filter(plot=self):
            sequence += 1
            if sequence >= 10:
                raise IdentifierError('Maximum number of Households for on plot is 9.')
        return sequence

    def post_save_create_household(self, created):
        """Creates one household for this plot but only if none exist."""
        Household = models.get_model('bcpp_household', 'Household')
        if Household.objects.filter(gps_target_lat=self.gps_target_lat, gps_target_lon=self.gps_target_lon).count() == 0:
            Household.objects.create(**{'plot': self,
                                        'gps_target_lat': self.gps_target_lat,
                                        'gps_target_lon': self.gps_target_lon,
                                        'gps_lat': self.gps_lat,
                                        'gps_lon': self.gps_lon,
                                        'gps_degrees_e': self.gps_degrees_e,
                                        'gps_degrees_s': self.gps_degrees_s,
                                        'gps_minutes_e': self.gps_minutes_e,
                                        'gps_minutes_s': self.gps_minutes_s,
                                        })
        else:
            # update all HH with new gps data
            for household in Household.objects.filter(plot=self):
                household.gps_target_lat = self.gps_target_lat
                household.gps_target_lon = self.gps_target_lon
                household.gps_lat = self.gps_lat
                household.gps_lon = self.gps_lon
                household.gps_degrees_e = self.gps_degrees_e
                household.gps_degrees_s = self.gps_degrees_s
                household.gps_minutes_e = self.gps_minutes_e
                household.gps_minutes_s = self.gps_minutes_s
                household.save()

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

    def gps(self):
        return "S{0} {1} E{2} {3}".format(self.gps_degrees_s, self.gps_minutes_s, self.gps_degrees_e, self.gps_minutes_e)

    def is_dispatch_container_model(self):
        return True

    def dispatched_as_container_identifier_attr(self):
        return 'plot_identifier'

    def dispatch_container_lookup(self):
        dispatch_container = models.get_model('bhp_dispatch', 'DispatchContainerRegister')
        if dispatch_container.objects.filter(container_identifier=self.plot_identifier, is_dispatched=True).exists():
            return dispatch_container.objects.get(container_identifier=self.plot_identifier, is_dispatched=True)
        return None

    def check_for_survey_on_pre_save(self, **kwargs):
        Survey = models.get_model('bcpp_survey', 'Survey')
        if Survey.objects.all().count() == 0:
            raise ImproperlyConfigured('Model Survey is empty. Please define at least one survey before creating a Plot.')

    def community_number(self):
        """Sets the community number to use for the plot identifier."""
        community_number = None
        for commun in BCPP_VILLAGES:
            if commun[1] == (settings.CURRENT_COMMUNITY).title():
                community_number = commun[0]
                return community_number
        return community_number

    def include_for_dispatch(self):
        return True

    def is_server(self):
        if Device().get_device_id() == '99':
            return True
        return False

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-plot_identifier', ]
        unique_together = (('gps_target_lat', 'gps_target_lon'), )
