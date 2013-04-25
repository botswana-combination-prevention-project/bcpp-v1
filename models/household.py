import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from audit_trail.audit import AuditTrail
from bhp_common.choices import YES_NO
from bhp_device.classes import Device
from bhp_identifier.exceptions import IdentifierError
from bhp_crypto.fields import EncryptedCharField, EncryptedTextField, EncryptedDecimalField
# from bcpp_household.choices import BCPP_WARDS 
from bcpp_household.choices import BCPP_VILLAGES
from bcpp_list.models import BcppWards
from bcpp_household.managers import HouseholdManager
from bcpp_household.classes import Identifier
from gps_device import GpsDevice
from bhp_dispatch.models import BaseDispatchSyncUuidModel


class Household(BaseDispatchSyncUuidModel):

    """ To find duplicates for cso and gps in SQL::

            # duplicate cso_number
            select cso_number, count(*)
            from bcpp_household where cso_number is not null
            group by cso_number
            having count(*) > 1;

            #duplicate gps
            select gps_point_1, gps_point_11, gps_point_2, gps_point_21, count(*)
            from bcpp_household
            group by gps_point_1, gps_point_11, gps_point_2, gps_point_21
            having count(*) > 1;
    """

    household_identifier = models.CharField(
        verbose_name=_('Household Identifier'),
        max_length=25,
        unique=True,
        help_text=_("Household identifier"),
        editable=False,
        db_index=True,
        )

    device_id = models.CharField(
        max_length=2,
        null=True,
        editable=False,
        )

    hh_int = models.IntegerField(
        editable=False
        )

    hh_seed = models.IntegerField(
        editable=False,
        default=0,
        )

    gps_device = models.ForeignKey(GpsDevice,
        help_text=_("select your GPS device"),
        )

    gps_waypoint = models.CharField(
        verbose_name=_('Waypoint'),
        max_length=25,
        help_text=_("the waypoint number is taken from the GPS reading"),
        )

    gps_datetime = models.DateTimeField(
        verbose_name=_('GPS Date/Time'),
        help_text=_("Date format YYYY-MM-DD, Time format is 24hr time HH:MM"),
        )

    gps_point_1 = EncryptedDecimalField(
        verbose_name='GPS S',
        max_digits=10,
        decimal_places=4,
        default=24,
        db_index=True,
        )

    gps_point_11 = EncryptedDecimalField(
        verbose_name='Longitude',
        max_digits=10,
        decimal_places=4,
        db_index=True,
        )

    gps_point_2 = EncryptedDecimalField(
        verbose_name='GPS E',
        max_digits=10,
        decimal_places=4,
        default=26,
        db_index=True,
        )

    gps_point_21 = EncryptedDecimalField(
        verbose_name='Latitude',
        max_digits=10,
        decimal_places=4,
        db_index=True,
        )

    cso_number = EncryptedCharField(
        verbose_name="CSO Number",
        blank=True,
        null=True,
        #unique=True,
        db_index=True,
        help_text=_("provide the CSO number or leave BLANK."),
        )
    
    village = EncryptedCharField(
        verbose_name=_("Village"),
        choices=BCPP_VILLAGES,
        db_index=True,
        )
    
    ward_section = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        )

    ward = models.ManyToManyField(BcppWards,
        verbose_name="Ward",
#         verbose_name=_("Ward"),
#         choices=BCPP_WARDS,
        db_index=True,
        )
    # this is a flag for follow-up / missing data
    was_surveyed_previously = models.CharField(
        verbose_name=_("Was this household surveyed previously?"),
        max_length=10,
        choices=YES_NO,
        default='No',
        help_text="For example, you know BHP was here before but the household is not in the system."
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

    target = models.IntegerField(default=0)

    objects = HouseholdManager()
    history = AuditTrail()

    @property
    def producer_dispatched_to(self):
        container = self.dispatch_container_lookup()
        if container:
            producer_name = container.producer.name
            return producer_name.split('-')[0]
        return 'Not Dispatched'

    def natural_key(self):
        return (self.household_identifier,)
    natural_key.dependencies = ['bcpp_household.gpsdevice', ]

    def save(self, *args, **kwargs):
        if not self.id:
            if self.old_household_identifier:
                self.household_identifier = self.old_household_identifier
                if not re.search('\d+', self.household_identifier):
                    raise IdentifierError('Expected household_identifier format to include an integer. Format H999999-99. Did you try to use an "old" paper identifier of the incorrect format? Got {0}'.format(self.household_identifier))
            else:
                device = Device()
                identifier = Identifier()
                self.household_identifier = identifier.get_identifier()
                self.device_id = device.device_id
            if not self.household_identifier:
                raise IdentifierError('Expected a value for household_identifier. Got None')
            self.hh_int = re.search('\d+', self.household_identifier).group(0)
        super(Household, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.household_identifier

    def get_subject_identifier(self):
        return self.household_identifier

    def gps(self):
        return "S0{0} {1} E0{2} {3}".format(self.gps_point_1,
                                        self.gps_point_11,
                                        self.gps_point_2,
                                        self.gps_point_21
                                        )

    def gps_lat(self):
        x = self.gps_point_2
        y = self.gps_point_21
        if x and y:
            x = float(x)
            y = float(y)
        return round((x) + (y / 60), 5)

    def gps_lon(self):
        x = self.gps_point_1
        y = self.gps_point_11
        if x and y:
            x = float(x)
            y = float(y)
            return -1 * round((x) + (y / 60), 5)
        return None

    #We can't call a method from a template so wrap the method within a property
    lat = property(gps_lat)
    lon = property(gps_lon)

    def get_absolute_url(self):
        return "/bcpp_household/household/{0}/".format(self.id)

    def calendar_datetime(self):
        return self.created

    def calendar_label(self):
        return self.__unicode__()

    def is_dispatch_container_model(self):
        return True

    def dispatched_as_container_identifier_attr(self):
        """Return the field attrname of the identifier used for dispatch."""
        return 'household_identifier'

    def dispatch_container_lookup(self):
        dispatch_container = models.get_model('bhp_dispatch','DispatchContainerRegister')
        if dispatch_container.objects.filter(container_identifier=self.household_identifier, is_dispatched=True).exists():
            return dispatch_container.objects.get(container_identifier=self.household_identifier, is_dispatched=True)
        return None

    def include_for_dispatch(self):
        return True
    
    def is_server(self):
        if Device().get_device_id() == '99':
            return True
        return False
    
    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-household_identifier', ]
