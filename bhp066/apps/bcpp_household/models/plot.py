from database_storage import DatabaseStorage

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models, IntegrityError
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.choices import TIME_OF_WEEK, TIME_OF_DAY
from edc.core.crypto_fields.fields import (EncryptedCharField, EncryptedTextField, EncryptedDecimalField)
from edc.core.identifier.exceptions import IdentifierError
from edc.device.device.classes import Device
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.map.classes import site_mappers
from edc.map.exceptions import MapperError

from apps.bcpp.choices import COMMUNITIES

from ..choices import PLOT_STATUS, SECTIONS, SUB_SECTIONS, BCPP_VILLAGES, SELECTED, ENUMERATION_STATUS
from ..classes import PlotIdentifier
from ..managers import PlotManager

from .household_identifier_history import HouseholdIdentifierHistory


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
        verbose_name="Approximate number of age eligible members",
        blank=True,
        null=True,
        help_text=("Provide an approximation of the number of people who live in this residence who are age eligible."),)

    description = EncryptedTextField(
        verbose_name="Description of plot/residence",
        max_length=250,
        blank=True,
        null=True,
        )

    comment = EncryptedTextField(
        verbose_name="Comment",
        max_length=250,
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

    household_count = models.IntegerField(
        verbose_name="Number of Households on this plot.",
        default=0,
        null=True,
        validators=[MaxValueValidator(9)],
        help_text=("Provide the number of households in this plot."))

    time_of_week = models.CharField(
        verbose_name='Time of week when most of the eligible members will be available',
        max_length=25,
        choices=TIME_OF_WEEK,
        blank=True,
        null=True,
        )

    time_of_day = models.CharField(
        verbose_name='Time of day when most of the eligible members will be available',
        max_length=25,
        choices=TIME_OF_DAY,
        blank=True,
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
    # TODO: need to be encrypted!!!!!
    gps_lon = EncryptedDecimalField(
        verbose_name='longitude',
        max_digits=10,
        null=True,
        decimal_places=6,
        )

    # TODO: need to be encrypted!!!!!
    gps_lat = EncryptedDecimalField(
        verbose_name='latitude',
        max_digits=10,
        null=True,
        decimal_places=6,
        )

    # TODO: need to be encrypted!!!!!
    gps_target_lon = EncryptedDecimalField(
        verbose_name='target waypoint longitude',
        max_digits=10,
        null=True,
        decimal_places=6,
        )

    # TODO: need to be encrypted!!!!!
    gps_target_lat = EncryptedDecimalField(
        verbose_name='target waypoint latitude',
        max_digits=10,
        null=True,
        decimal_places=6,
        )

    status = models.CharField(
        verbose_name='Plot status',
        max_length=35,
        null=True,
        choices=PLOT_STATUS,
        help_text='If Inaccessible, update status and comment but not GPS, household count, time_of_week, etc.'
        )

    target_radius = models.FloatField(default=.025, help_text='km', editable=False)

    distance_from_target = models.FloatField(null=True, editable=True, help_text='distance in meters')

    #20 percent plots is reperesented by 1 and 5 percent of by 2, the rest of the plots which is 75 percent selected value is None
    selected = models.CharField(
        max_length=25,
        null=True,
        verbose_name='selected',
        choices=SELECTED,
        editable=False,
        )

#     allowed_to_enumerate = models.CharField(
#         max_length=25,
#         null=True,
#         verbose_name='Does the Household memeber and Head of Household allow you to enumerate them?',
#         choices=ENUMERATION_STATUS,
#         editable=False,
#         )

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

    access_attempts = models.IntegerField(
        default=0,
        editable=False,
        help_text='Number of attempts to access a plot to determine it\'s status.'
        )

    # Google map static images for this plots with different zoom levels. uploaded_map_16, uploaded_map_17, uploaded_map_18 zoom level 16, 17, 18 respectively
    uploaded_map_16 = models.CharField(verbose_name="Map image at zoom level 16", max_length=25, null=True, blank=True, editable=False)

    uploaded_map_17 = models.CharField(verbose_name="Map image at zoom level 17", max_length=25, null=True, blank=True, editable=False)

    uploaded_map_18 = models.CharField(verbose_name="Map image at zoom level 18", max_length=25, null=True, blank=True, editable=False)

    community = models.CharField(
        max_length=25,
        help_text='If the community is incorrect, please contact the DMC immediately.',
        choices=COMMUNITIES,
        validators=[is_valid_community, ],
        editable=False,
        )

    section = models.CharField(
        max_length=25,
        null=True,
        verbose_name='Section',
        choices=SECTIONS,
        editable=False,
        )

    sub_section = models.CharField(
        max_length=25,
        null=True,
        verbose_name='Sub-section',
        choices=SUB_SECTIONS,
        help_text=u'',
        editable=False,
        )

    bhs = models.NullBooleanField(editable=False)

    objects = PlotManager()

    history = AuditTrail()

    def __unicode__(self):
        return self.plot_identifier

    def natural_key(self):
        return (self.plot_identifier,)

    def save(self, *args, **kwargs):
        # if user added/updated gps_degrees_[es] and gps_minutes_[es], update gps_lat, gps_lon
        if not self.community:
            # plot data is imported and not entered, so community must be provided on import
            raise ValidationError('Attribute \'community\' may not be None for model {0}'.format(self))
        if self.household_count > 9:
            raise ValidationError('Number of households cannot exceed 9. Perhaps catch this in the forms.py')
        # if self.community does not get valid mapper, will raise an error that should be caught in forms.py
        mapper_cls = site_mappers.get_registry(self.community)
        mapper = mapper_cls()
        if not self.plot_identifier:
            plot_identifier = PlotIdentifier(community=mapper.get_map_code())
            self.plot_identifier = plot_identifier.get_identifier()
            if not self.plot_identifier:
                raise IdentifierError('Expected a value for plot_identifier. Got None')
        if self.status == 'inaccessible':
            # reset any editable fields that the user changed
            for field in  [fld for fld in self.__class__._meta.fields if fld.editable == False and fld.null == True and field.name not in ['status', 'comment']]:
                setattr(self, field.name, None)
        else:
            if (self.gps_degrees_e and self.gps_degrees_s and self.gps_minutes_e and self.gps_minutes_s):
                self.gps_lat = mapper.get_gps_lat(self.gps_degrees_s, self.gps_minutes_s)
                self.gps_lon = mapper.get_gps_lon(self.gps_degrees_e, self.gps_minutes_e)
                mapper.verify_gps_location(self.gps_lat, self.gps_lon, MapperError)
                mapper.verify_gps_to_target(self.gps_lat, self.gps_lon, self.gps_target_lat, self.gps_target_lon, self.target_radius, MapperError)
                self.distance_from_target = mapper.gps_distance_between_points(self.gps_lat, self.gps_lon, self.gps_target_lat, self.gps_target_lon, self.target_radius) * 1000
            self.action = self.get_action()
            if self.id:
                self.household_count = self.create_or_delete_households(self)
            if ((self.household_count == 0 and self.status in  ['occupied', 'occupied_no_residents', 'occupied_refused_enumeration']) or
                    (self.household_count > 0 and not self.status in  ['occupied', 'occupied_no_residents', 'occupied_refused_enumeration'])):
                raise ValidationError('Invalid number of households for plot that is {0}. Got {1}. Perhaps catch this in the form clean method.'.format(self.status, self.household_count))
        super(Plot, self).save(*args, **kwargs)

    @property
    def identifier_segment(self):
        return self.plot_identifier[:-3]

    def create_household(self, instance):
        Household = models.get_model('bcpp_household', 'Household')
        Household.objects.create(**{
           'plot': instance,
            'gps_target_lat': instance.gps_target_lat,
            'gps_target_lon': instance.gps_target_lon,
            'gps_lat': instance.gps_lat,
            'gps_lon': instance.gps_lon,
            'gps_degrees_e': instance.gps_degrees_e,
            'gps_degrees_s': instance.gps_degrees_s,
            'gps_minutes_e': instance.gps_minutes_e,
            'gps_minutes_s': instance.gps_minutes_s,
            })

    def delete_unused_households(self, instance):
        """Deletes households and HouseholdStructure if member_count==0 and no log entry."""
        Household = models.get_model('bcpp_household', 'Household')
        HouseholdStructure = models.get_model('bcpp_household', 'HouseholdStructure')
        HouseholdLog = models.get_model('bcpp_household', 'HouseholdLog')
        HouseholdLogEntry = models.get_model('bcpp_household', 'HouseholdLogEntry')
        for household_structure in HouseholdStructure.objects.filter(household__plot__pk=instance.pk, member_count=0).order_by('-created'):
            if Household.objects.filter().count() > instance.household_count:
                try:
                    if not HouseholdLogEntry.objects.filter(household_log__household_structure=household_structure):
                        HouseholdLog.objects.filter(household_structure=household_structure).delete()
                        household_pk = unicode(household_structure.household.pk)
                        household_structure.delete()
                        for household in Household.objects.filter(pk=household_pk):
                            HouseholdIdentifierHistory.objects.filter(identifier=household.household_identifier).delete
                            household.delete()
                except IntegrityError:
                    pass

    def create_or_delete_households(self, instance):
        """Creates or deletes households to try to equal the number of households reported on the plot instance.

        This gets called by a signal on add and on the save method on change.

            * If number is greater than actual household instances, households are created.
            * If number is less than actual household instances, households are deleted as long as
              there are no household members and the household log does not have entries."""
        Household = models.get_model('bcpp_household', 'Household')
        # check that tuple has not changed and has "occupied"
        if instance.status:
            if instance.status not in [item[0] for item in PLOT_STATUS]:
                raise AttributeError('{0} not found in choices tuple PLOT_STATUS. {1}'.format(instance.status, PLOT_STATUS))
        if instance.status in  ['occupied', 'occupied_no_residents', 'occupied_refused_enumeration'] and not Household.objects.filter(plot__pk=instance.pk).count() == instance.household_count:
            while Household.objects.filter(plot__pk=instance.pk).count() < instance.household_count:
                instance.create_household(instance)
            number_of_households = Household.objects.filter(plot__pk=instance.pk).count()
            if number_of_households > instance.household_count:
                instance.delete_unused_households(instance)
        else:
            instance.delete_unused_households(instance)
        return Household.objects.filter(plot__pk=instance.pk).count()

    def get_action(self):
        retval = 'unconfirmed'
        if self.gps_lon and self.gps_lat:
            retval = 'confirmed'
        return retval

    def gps(self):
        return "S{0} {1} E{2} {3}".format(self.gps_degrees_s, self.gps_minutes_s, self.gps_degrees_e, self.gps_minutes_e)

    @property
    def producer_dispatched_to(self):
        container = self.dispatch_container_lookup()
        if container:
            producer_name = container.producer.name
            return producer_name.split('-')[0]
        return 'Not Dispatched'

    def is_server(self):
        if Device().get_device_id() == '99':
            return True
        return False

    def is_dispatch_container_model(self):
        return True

    def dispatched_as_container_identifier_attr(self):
        return 'plot_identifier'

    def dispatch_container_lookup(self):
        dispatch_container = models.get_model('dispatch', 'DispatchContainerRegister')
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
            if commun[1] == (site_mappers.get_current_mapper().map_area).title():
                community_number = commun[0]
                return community_number
        return community_number

    def include_for_dispatch(self):
        return True

    def get_contained_households(self):
        from apps.bcpp_household.models import Household
        households = Household.objects.filter(plot__plot_identifier=self.plot_identifier)
        return households

    def bypass_for_edit_dispatched_as_item(self):
        return True

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-plot_identifier', ]
        unique_together = (('gps_target_lat', 'gps_target_lon'),)
