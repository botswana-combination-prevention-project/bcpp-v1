import re
from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bhp_dispatch.models import BaseDispatchSyncUuidModel
from bhp_common.choices import YES_NO
from bhp_device.classes import Device
from bhp_identifier.exceptions import IdentifierError
from bhp_crypto.fields import (EncryptedCharField, EncryptedTextField, EncryptedDecimalField)
from bcpp_household.managers import HouseholdManager
from bcpp_household.classes import Identifier
from bcpp_household.choices import HOUSEHOLD_STATUS


class Household(BaseDispatchSyncUuidModel):

    household_identifier = models.CharField(
        verbose_name='Household Identifier',
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

    report_datetime = models.DateTimeField(
        verbose_name='Report Date/Time',
        null=True,
        )

    status = models.CharField(
        verbose_name='Household status',
        max_length=15,
        null=True,
        choices=HOUSEHOLD_STATUS,
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

    cso_number = EncryptedCharField(
        verbose_name="CSO Number",
        blank=True,
        null=True,
        db_index=True,
        help_text=_("provide the CSO number or leave BLANK."),
        )

    community = models.CharField(
        max_length=25)

    section = models.CharField(
        max_length=25,
        )

    sub_section = models.CharField(
        max_length=25,
        )

#     was_surveyed_previously = models.CharField(
#         verbose_name="Was this household surveyed previously?",
#         max_length=10,
#         choices=YES_NO,
#         default='No',
#         help_text="For example, you know BHP was here before but the household is not in the system."
#         )

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
            device = Device()
            identifier = Identifier()
            self.household_identifier = identifier.get_identifier()
            self.device_id = device.device_id
            if not self.household_identifier:
                raise IdentifierError('Expected a value for household_identifier. Got None')
            self.hh_int = re.search('\d+', self.household_identifier).group(0)
        self.gps_lat = self.get_gps_lat()
        self.gps_lon = self.get_gps_lon()
        self.action = self.get_action()
        super(Household, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.household_identifier

    def get_action(self):
        if not self.gps_lon and not self.gps_lat:
            retval = 'unconfirmed'
        elif self.status == 'occupied':
            retval = 'valid'
        elif self.status == 'vacant' or self.status == 'invalid':
            retval = 'invalid'
        else:
            retval = 'unconfirmed'
        return retval

    def get_subject_identifier(self):
        return self.household_identifier

    def gps(self):
        return "S{0} {1} E{2} {3}".format(self.gps_degrees_s, self.gps_minutes_s, self.gps_degrees_e, self.gps_minutes_e)

    def get_gps_lat(self):
        x = self.gps_degrees_s
        y = self.gps_minutes_s
        if x and y:
            x = float(x)
            y = float(y)
            return round((x) + (y / 60), 5)
        return None

    def get_gps_lon(self):
        x = self.gps_degrees_e
        y = self.gps_minutes_e
        if x and y:
            x = float(x)
            y = float(y)
            return -1 * round((x) + (y / 60), 5)
        return None

    def is_dispatch_container_model(self):
        return True

    def dispatched_as_container_identifier_attr(self):
        return 'household_identifier'

    def dispatch_container_lookup(self):
        dispatch_container = models.get_model('bhp_dispatch', 'DispatchContainerRegister')
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
