from datetime import date, datetime, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator
from django.db import models, IntegrityError, transaction, DatabaseError
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.choices import TIME_OF_WEEK, TIME_OF_DAY
from edc.core.crypto_fields.fields import (
    EncryptedCharField, EncryptedTextField, EncryptedDecimalField)
from edc.core.identifier.exceptions import IdentifierError
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.map.classes import site_mappers
from edc.map.exceptions import MapperError

from ..choices import (PLOT_STATUS, SELECTED, INACCESSIBLE, ACCESSIBLE)
from ..classes import PlotIdentifier
from ..constants import CONFIRMED, UNCONFIRMED, RESIDENTIAL_NOT_HABITABLE, NON_RESIDENTIAL
from ..managers import PlotManager
from ..exceptions import AlreadyReplaced

from .household_identifier_history import HouseholdIdentifierHistory


def is_valid_community(self, value):
        """Validates the community string against a list of site_mappers map_areas."""
        if value.lower() not in [l.lower() for l in site_mappers.get_as_list()]:
            raise ValidationError(u'{0} is not a valid community name.'.format(value))


class Plot(BaseDispatchSyncUuidModel):
    """A model completed by the user (and initially by the system) to represent a Plot
    in the community."""
    plot_identifier = models.CharField(
        verbose_name='Plot Identifier',
        max_length=25,
        unique=True,
        help_text=_("Plot identifier"),
        editable=False,
        db_index=True)

    eligible_members = models.IntegerField(
        verbose_name="Approximate number of age eligible members",
        blank=True,
        null=True,
        help_text=(("Provide an approximation of the number of people "
                    "who live in this residence who are age eligible.")))

    description = EncryptedTextField(
        verbose_name="Description of plot/residence",
        max_length=250,
        blank=True,
        null=True)

    comment = EncryptedTextField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        null=True)

    cso_number = EncryptedCharField(
        verbose_name="CSO Number",
        blank=True,
        null=True,
        db_index=True,
        help_text=("provide the CSO number or leave BLANK."))

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
        null=True)

    time_of_day = models.CharField(
        verbose_name='Time of day when most of the eligible members will be available',
        max_length=25,
        choices=TIME_OF_DAY,
        blank=True,
        null=True)

    gps_degrees_s = EncryptedDecimalField(
        verbose_name='GPS Degrees-South',
        max_digits=10,
        null=True,
        decimal_places=0)

    gps_minutes_s = EncryptedDecimalField(
        verbose_name='GPS Minutes-South',
        max_digits=10,
        null=True,
        decimal_places=4)

    gps_degrees_e = EncryptedDecimalField(
        verbose_name='GPS Degrees-East',
        null=True,
        max_digits=10,
        decimal_places=0)

    gps_minutes_e = EncryptedDecimalField(
        verbose_name='GPS Minutes-East',
        max_digits=10,
        null=True,
        decimal_places=4)

    gps_lon = EncryptedDecimalField(
        verbose_name='longitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    gps_lat = EncryptedDecimalField(
        verbose_name='latitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    gps_target_lon = EncryptedDecimalField(
        verbose_name='target waypoint longitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    gps_target_lat = EncryptedDecimalField(
        verbose_name='target waypoint latitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    status = models.CharField(
        verbose_name='Plot status',
        max_length=35,
        null=True,
        choices=PLOT_STATUS)

    target_radius = models.FloatField(
        default=.025,
        help_text='km',
        editable=False)

    distance_from_target = models.FloatField(
        null=True,
        editable=True,
        help_text='distance in meters')

    # 20 percent plots is reperesented by 1 and 5 percent of by 2, the rest of
    # the plots which is 75 percent selected value is None
    selected = models.CharField(
        max_length=25,
        null=True,
        verbose_name='selected',
        choices=SELECTED,
        editable=False)

    device_id = models.CharField(
        max_length=2,
        null=True,
        editable=False)

    action = models.CharField(
        max_length=25,
        null=True,
        default=UNCONFIRMED,
        editable=False)

    access_attempts = models.IntegerField(
        default=0,
        editable=False,
        help_text='Number of attempts to access a plot to determine it\'s status.')

    # Google map static images for this plots with different zoom levels.
    # uploaded_map_16, uploaded_map_17, uploaded_map_18 zoom level 16, 17, 18 respectively
    uploaded_map_16 = models.CharField(
        verbose_name="Map image at zoom level 16",
        max_length=25,
        null=True,
        blank=True,
        editable=False)

    uploaded_map_17 = models.CharField(
        verbose_name="Map image at zoom level 17",
        max_length=25,
        null=True,
        blank=True,
        editable=False)

    uploaded_map_18 = models.CharField(
        verbose_name="Map image at zoom level 18",
        max_length=25,
        null=True,
        blank=True,
        editable=False)

    community = models.CharField(
        max_length=25,
        help_text='If the community is incorrect, please contact the DMC immediately.',
        validators=[is_valid_community, ],
        editable=False)

    section = models.CharField(
        max_length=25,
        null=True,
        verbose_name='Section',
        editable=False)

    sub_section = models.CharField(
        max_length=25,
        null=True,
        verbose_name='Sub-section',
        help_text=u'',
        editable=False)

    bhs = models.NullBooleanField(
        default=None,
        editable=False,
        help_text=('True indicates that plot is enrolled into BHS. '
                   'Updated by bcpp_subject.subject_consent post_save'))

    enrolled_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text=('datetime that plot is enrolled into BHS. '
                   'Updated by bcpp_subject.subject_consent post_save'))

    htc = models.NullBooleanField(
        default=False,
        editable=False)

    replaces = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        editable=False,
        help_text=("plot or household identifier that this plot replaces."))

    replaced_by = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        editable=False,
        help_text=u'The identifier of the plot that this plot was replaced by')

    replaceable = models.NullBooleanField(
        verbose_name='Replaceable?',
        default=None,
        editable=False,
        help_text='Updated by replacement helper')

    objects = PlotManager()

    history = AuditTrail()

    def __unicode__(self):
        if site_mappers.get_current_mapper()().clinic_plot_identifier == self.plot_identifier:
            return 'BCPP-CLINIC'
        else:
            return self.plot_identifier

    def natural_key(self):
        return (self.plot_identifier, )

    def save(self, *args, **kwargs):
        using = kwargs.get('using')
        update_fields = kwargs.get('update_fields')
        if not self.plot_identifier == site_mappers.get_current_mapper()().clinic_plot_identifier:
            self.allow_enrollment(using, update_fields=update_fields)
        if self.replaced_by and update_fields != ['replaced_by', 'htc']:
            raise AlreadyReplaced('Plot {0} is no longer part of BHS. It has been replaced '
                                  'by plot {1}.'.format(self.plot_identifier, self.replaced_by))
        if not self.community:
            # plot data is imported and not entered, so community must be provided on import
            raise ValidationError('Attribute \'community\' may not be None for model {0}'.format(self))
        if self.household_count > settings.MAX_HOUSEHOLDS_PER_PLOT:
            raise ValidationError('Number of households cannot exceed {}. '
                                  'Perhaps catch this in the forms.py. See '
                                  'settings.MAX_HOUSEHOLDS_PER_PLOT'.format(settings.MAX_HOUSEHOLDS_PER_PLOT))
        # unless overridden, if self.community != to mapper.map_area, raise
        self.verify_plot_community_with_current_mapper(self.community)
        # if self.community does not get valid mapper, will raise an error that should be caught in forms.pyx
        mapper_cls = site_mappers.registry.get(self.community)
        mapper = mapper_cls()
        if not self.plot_identifier:
            self.plot_identifier = PlotIdentifier(mapper.map_code, using).get_identifier()
            if not self.plot_identifier:
                raise IdentifierError('Expected a value for plot_identifier. Got None')
        # if user added/updated gps_degrees_[es] and gps_minutes_[es], update gps_lat, gps_lon
        if (self.gps_degrees_e and self.gps_degrees_s and self.gps_minutes_e and self.gps_minutes_s):
            self.gps_lat = mapper.get_gps_lat(self.gps_degrees_s, self.gps_minutes_s)
            self.gps_lon = mapper.get_gps_lon(self.gps_degrees_e, self.gps_minutes_e)
            mapper.verify_gps_location(self.gps_lat, self.gps_lon, MapperError)
            mapper.verify_gps_to_target(self.gps_lat, self.gps_lon, self.gps_target_lat,
                                        self.gps_target_lon, self.target_radius, MapperError,
                                        self.increase_radius_instance)
            self.distance_from_target = mapper.gps_distance_between_points(
                self.gps_lat, self.gps_lon, self.gps_target_lat, self.gps_target_lon) * 1000
        self.action = self.get_action()
        try:
            update_fields = update_fields + ['action', 'distance_from_target', 'plot_identifier', 'user_modified']
            kwargs.update({'update_fields': update_fields})
        except TypeError:
            pass
        super(Plot, self).save(*args, **kwargs)

    def get_identifier(self):
        return self.plot_identifier

    @property
    def identifier_segment(self):
        return self.plot_identifier[:-3]
    
    @property
    def increase_radius_instance(self):
        IncreasePlotRadius = models.get_model('bcpp_household', 'IncreasePlotRadius')
        try:
            return IncreasePlotRadius.objects.get(plot=self)
        except IncreasePlotRadius.DoesNotExist:
            return None

    def create_household(self, count, instance=None, using=None):
        instance = instance or self
        using = using or 'default'
        if instance.pk:
            for i in range(0, count):
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
                    'gps_minutes_s': instance.gps_minutes_s})

    def allow_enrollment(self, using, exception_cls=None, plot_instance=None, update_fields=None):
        """Raises an exception if an attempt is made to edit a plot after
        the BHS_FULL_ENROLLMENT_DATE or if the plot has been allocated to HTC."""
        plot_instance = plot_instance or self
        using = using or 'default'
        update_fields = update_fields or []
        exception_cls = exception_cls or ValidationError
        if using == 'default':  # do not check on remote systems
            mapper_instance = site_mappers.get_current_mapper()()
            if plot_instance.id:
                if plot_instance.htc and 'htc' not in update_fields:
                    raise exception_cls('Modifications not allowed, this plot has been assigned to the HTC campaign.')
            if not mapper_instance.map_code == '00' and not plot_instance.bhs and date.today() > mapper_instance.current_survey_dates.full_enrollment_date:
                raise exception_cls('BHS enrollment for {0} ended on {1}. This plot, and the '
                                    'data related to it, may not be modified. '
                                    'See site_mappers'.format(
                                        self.community, mapper_instance.current_survey_dates.full_enrollment_date))
        return True

    def safe_delete_households(self, existing_no, instance=None, using=None):
        """ Deletes households and HouseholdStructure if member_count==0 and no log entry.
            If there is a household log entry, this DOES NOT delete the household
        """
        Household = models.get_model('bcpp_household', 'Household')
        HouseholdStructure = models.get_model('bcpp_household', 'HouseholdStructure')
        HouseholdLog = models.get_model('bcpp_household', 'HouseholdLog')
        HouseholdLogEntry = models.get_model('bcpp_household', 'HouseholdLogEntry')
        instance = instance or self
        using = using or 'default'

        def household_valid_to_delete(instance):
            """ Checks whether there is a plot log entry for each log. If it does not exists the
            household can be deleted. """
            allowed_to_delete = []
            for hh in Household.objects.using(using).filter(plot=instance):
                if HouseholdLogEntry.objects.filter(household_log__household_structure__household=hh).exists()\
                    or hh in allowed_to_delete:
                    continue
                allowed_to_delete.append(hh)
            return allowed_to_delete

        def delete_confirmed_household(instance, existing_no):
            """ Deletes required number of households. """
            def validate_number_to_delete(instance, existing_no):
                if existing_no in [0, 1] or instance.household_count == existing_no or instance.household_count >\
                    existing_no or instance.household_count == 0:
                    return False
                else:
                    if household_valid_to_delete(instance):
                        del_valid = existing_no - instance.household_count
                        if len(household_valid_to_delete(instance)) < del_valid:
                            return len(household_valid_to_delete(instance))
                        else:
                            return del_valid
                    return False

            def delete_households_for_non_residential(instance, existing_no):
                household_to_delete = household_valid_to_delete(instance)
                try:
                    if len(household_to_delete) == existing_no and existing_no > 0:
                        hh = HouseholdStructure.objects.filter(household__in=household_to_delete)
                        hl = HouseholdLog.objects.filter(household_structure__in=hh)
                        hl.delete()  # delete household_logs
                        hh.delete()  # delete household_structure
                        for hh in household_to_delete:
                            with transaction.atomic():
                                Household.objects.get(id=hh.id).delete()  # delete household
                        return True
                    else:
                        return False
                except IntegrityError:
                    return False
                except  DatabaseError:
                    return False

            def delete_household(instance, existing_no):
                try:
                    delete_no = validate_number_to_delete(instance, existing_no)\
                                                if validate_number_to_delete(instance, existing_no) else 0
                    if not delete_no == 0:
                        deletes = household_valid_to_delete(instance)[:delete_no]
                        hh = HouseholdStructure.objects.filter(household__in=deletes)
                        hl = HouseholdLog.objects.filter(household_structure__in=hh)
                        hl.delete()  # delete household_logs
                        hh.delete()  # delete household_structure
                        for hh in deletes:
                            with transaction.atomic():
                                Household.objects.get(id=hh.id).delete()  # delete household
                        return True
                    else:
                        return False
                except IntegrityError:
                    return False
                except  DatabaseError:
                    return False
            if instance.status in [RESIDENTIAL_NOT_HABITABLE, NON_RESIDENTIAL]:
                return delete_households_for_non_residential(instance, existing_no)
            else:
                return delete_household(instance, existing_no)
        return delete_confirmed_household(instance, existing_no)

    def create_or_delete_households(self, instance=None, using=None):
        """Creates or deletes households to try to equal the number of households reported on the plot instance.

        This gets called by a household post_save signal and on the plot save method on change.

            * If number is greater than actual household instances, households are created.
            * If number is less than actual household instances, households are deleted as long as
              there are no household members and the household log does not have entries.
            * bcpp_clinic is a special case to allow for a plot to represent the BCPP Clinic."""
        instance = instance or self
        using = using or 'default'
        Household = models.get_model('bcpp_household', 'Household')
        # check that tuple has not changed and has "residential_habitable"
        if instance.status:
            if instance.status not in [item[0] for item in list(PLOT_STATUS) + [('bcpp_clinic', 'BCPP Clinic')]]:
                raise AttributeError('{0} not found in choices tuple PLOT_STATUS. {1}'.format(instance.status,
                                                                                              PLOT_STATUS))
        existing_household_count = Household.objects.using(using).filter(plot__pk=instance.pk).count()
        instance.create_household(instance.household_count - existing_household_count, using=using)
        instance.safe_delete_households(existing_household_count, using=using)
        with transaction.atomic():
            return Household.objects.using(using).filter(plot__pk=instance.pk).count()

    def get_action(self):
        retval = UNCONFIRMED
        if self.gps_lon and self.gps_lat:
            retval = CONFIRMED
        return retval

    @property
    def validate_plot_accessible(self):
        if self.plot_log_entry and (self.plot_inaccessible == False) and self.plot_log_entry.log_status == ACCESSIBLE:
            return True
        return False

    def gps(self):
        return "S{0} {1} E{2} {3}".format(self.gps_degrees_s, self.gps_minutes_s,
                                          self.gps_degrees_e, self.gps_minutes_e)

    def is_dispatch_container_model(self):
        return True

    def dispatched_as_container_identifier_attr(self):
        return 'plot_identifier'

    def dispatch_container_lookup(self):
        return (self.__class__, 'plot_identifier')

    def include_for_dispatch(self):
        return True

    def bypass_for_edit_dispatched_as_item(self, using=None, update_fields=None):
        """Bypasses dispatched check if update_fields is set by the replacement_helper."""
        if update_fields:
            if 'replaces' in update_fields or 'htc' in update_fields or 'replaced_by' in update_fields:
                return True
        return False

    def get_contained_households(self):
        from apps.bcpp_household.models import Household
        households = Household.objects.filter(plot__plot_identifier=self.plot_identifier)
        return households

    @property
    def log_form_label(self):
        # TODO: where is this used?
        using = 'default'
        PlotLog = models.get_model('bcpp_household', 'PlotLog')
        PlotLogEntry = models.get_model('bcpp_household', 'PlotLogEntry')
        form_label = []
        try:
            plot_log = PlotLog.objects.using(using).get(plot=self)
            for plot_log_entry in PlotLogEntry.objects.using(
                    using).filter(plot_log=plot_log).order_by('report_datetime'):
                try:
                    form_label.append((plot_log_entry.log_status.lower() + '-' +
                                       plot_log_entry.report_datetime.strftime('%Y-%m-%d'), plot_log_entry.id))
                except AttributeError:  # log_status is None ??
                    form_label.append((plot_log_entry.report_datetime.strftime('%Y-%m-%d'), plot_log_entry.id))
        except PlotLog.DoesNotExist:
            pass
        if self.access_attempts < 3 and self.action != CONFIRMED:
            form_label.append(('add new entry', 'add new entry'))
        if not form_label and self.action != CONFIRMED:
            form_label.append(('add new entry', 'add new entry'))
        return form_label

    @property
    def log_entry_form_urls(self):
        # TODO: where is this used?
        # TODO: this does not belong on the plot model!
        """Returns a url or urls to the plotlogentry(s) if an instance(s) exists."""
        using = 'default'
        PlotLog = models.get_model('bcpp_household', 'PlotLog')
        PlotLogEntry = models.get_model('bcpp_household', 'PlotLogEntry')
        entry_urls = {}
        try:
            plot_log = PlotLog.objects.using(using).get(plot=self)
            for entry in PlotLogEntry.objects.using(using).filter(plot_log=plot_log).order_by('report_datetime'):
                entry_urls[entry.pk] = self._get_form_url('plotlogentry', entry.pk)
            add_url_2 = self._get_form_url('plotlogentry', model_pk=None, add_url=True)
            entry_urls['add new entry'] = add_url_2
        except PlotLog.DoesNotExist:
            pass
        return entry_urls

    def _get_form_url(self, model, model_pk=None, add_url=None):
        url = ''
        pk = None
        app_label = 'bcpp_household'
        if add_url:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model))
            return url
        if not model_pk:  # This is a like a SubjectAbsentee
            model_class = models.get_model(app_label, model)
            try:
                pk = model_class.objects.get(plot=self).pk
            except model_class.DoesNotExist:
                pk = None
        else:
            pk = model_pk
        if pk:
            url = reverse('admin:{0}_{1}_change'.format(app_label, model), args=(pk, ))
        else:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model))
        return url

    @property
    def location(self):
        if self.plot_identifier.endswith('0000-00'):
            return 'clinic'
        else:
            return 'household'

    @property
    def plot_inaccessible(self):
        """Returns True if the plot is inaccessible as defined by its status and number of attempts."""
        PlotLogEntry = models.get_model('bcpp_household', 'plotlogentry')
        return PlotLogEntry.objects.filter(plot_log__plot__id=self.id, log_status=INACCESSIBLE).count() >= 3

    @property
    def target_radius_in_meters(self):
        return self.target_radius * 1000

    @property
    def increase_plot_radius(self):
        """Returns an instance of IncreasePlotRadius if the user should be
        allowed to change the target_radius otherwise returns None.

        Plot must be inaccessible and the last reason (of 3) be either "dogs"
        or "locked gate" """
        PlotLogEntry = models.get_model('bcpp_household', 'PlotLogEntry')
        IncreasePlotRadius = models.get_model('bcpp_household', 'IncreasePlotRadius')
        created = False
        increase_plot_radius = None
        try:
            increase_plot_radius = IncreasePlotRadius.objects.get(plot=self)
        except IncreasePlotRadius.DoesNotExist:
            if self.plot_inaccessible:
                plot_log_entries = PlotLogEntry.objects.filter(
                    plot_log__plot__id=self.id).order_by('report_datetime')
                if plot_log_entries[2].reason in ['dogs', 'locked_gate']:
                    increase_plot_radius = IncreasePlotRadius.objects.create(plot=self)
                    created = True
        except IndexError:
            pass
        return increase_plot_radius, created

    def verify_plot_community_with_current_mapper(self, community, exception_cls=None):
        """Returns True if the plot.community = the current mapper.map_area.

        This check can be disabled using the settings attribute VERIFY_PLOT_COMMUNITY_WITH_CURRENT_MAPPER.
        """
        verify_plot_community_with_current_mapper = True  # default
        exception_cls = exception_cls or ValidationError
        try:
            verify_plot_community_with_current_mapper = settings.VERIFY_PLOT_COMMUNITY_WITH_CURRENT_MAPPER
        except AttributeError:
            pass
        if verify_plot_community_with_current_mapper:
            if community != site_mappers.current_mapper.map_area:
                raise exception_cls(
                    'Plot community does not correspond with the current mapper '
                    'community of \'{}\'. Got \'{}\'. '
                    'See settings.VERIFY_PLOT_COMMUNITY_WITH_CURRENT_MAPPER'.format(
                        site_mappers.current_mapper.map_area, community))

    @property
    def plot_log(self):
        """Returns an instance of the plot log."""
        PlotLog = models.get_model('bcpp_household', 'plotlog')
        try:
            instance = PlotLog.objects.get(plot__id=self.id)
        except PlotLog.DoesNotExist:
            instance = None
        return instance

    @property
    def plot_log_entry(self):
        PlotLogEntry = models.get_model('bcpp_household', 'plotlogentry')
        try:
            return  PlotLogEntry.objects.filter(
                                plot_log__plot__id=self.id).latest('report_datetime')
        except PlotLogEntry.DoesNotExist:
            print "PlotLogEntry.DoesNotExist"

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-plot_identifier', ]
        unique_together = (('gps_target_lat', 'gps_target_lon'),)
