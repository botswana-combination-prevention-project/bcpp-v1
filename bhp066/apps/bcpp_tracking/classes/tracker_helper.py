import socket

from datetime import datetime

from django.conf import settings
from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured

from edc.device.sync.utils import getproducerbyaddr
from edc.device.device.classes import Device
from edc.device.sync.models import Producer

from ..models import Tracker, SiteTracker
from .mail import Reciever, Mail


class TrackerHelper(object):
    """Calculates and updates tracked value.
    """

    def __init__(self, plot=None, household_structure=None):
        """Sets value_type, and tracker server name."""

        self.value_type = settings.PIMA_VL_TYPE_SETTING
        self.name = settings.TRACKER_SERVER_NAME

    def update_site_tracker(self):
        """Update the tracker and site tracker at the site."""

        online_sites = self.online_producers
        if Device().is_central_server:
            for site in self.registered_sites:
                # Update tracker
                using = site + ".bhp.org.bw"
                if using in online_sites:
                    try:
                        tracker = Tracker.objects.get(is_active=True, name=self.name, value_type=self.value_type)
                        tracker.tracked_value = self.site_tracked_value(site)
                        tracker.update_date = datetime.today()
                        tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
                    except Tracker.DoesNotExist:
                        # Create the tracker if it does not exist.
                        Tracker.objects.create(is_active=True,
                                               name=self.name,
                                               value_type=self.value_type,
                                               app_name='',
                                               model='',
                                               tracked_value=self.site_tracked_value(site),
                                               start_date=datetime.today(),
                                               end_date=datetime.today(),
                                               using=using)
                    #Update site tracker
                    try:
                        site_tracker = SiteTracker.objects.get(site_name=site)
                        site_tracker.tracked_value = self.site_tracked_value(site)
                        site_tracker.update_date = datetime.today()
                        site_tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
                    except SiteTracker.DoesNotExist:
                        # Create the site tracker if it does not exist.
                        SiteTracker.objects.create(is_active=True,
                                               tracker=tracker,
                                               name=self.name,
                                               value_type=self.value_type,
                                               app_name='bcpp_subject',
                                               site_name=site,
                                               model='PimaVl',
                                               tracked_value=self.site_tracked_value(site),
                                               start_date=datetime.today(),
                                               end_date=datetime.today(),
                                               using=using)

    def update_producer_tracker(self):
        """Updates the tracked value on the producer.

        Attributes:
        using: The using value for the database in the producer.
        value_type: The type of value being tracked, e.g mobile setup or household setup for poc vl.
        name: The name of the central site
        """

        site = settings.CURRENT_COMMUNITY
        online_sites = self.online_producers
        if Device().is_community_server:
            for using in online_sites:
                if not using in settings.MIDDLE_MAN_LIST:
                    # Update tracker
                    try:
                        tracker = Tracker.objects.get(is_active=True, name=self.name, value_type=self.value_type)
                        tracker.tracked_value = self.site_tracked_value(site)
                        tracker.update_date = datetime.today()
                        tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
                    except Tracker.DoesNotExist:
                        # Create the tracker if it does not exist.
                        Tracker.objects.create(is_active=True,
                                               name=self.name,
                                               value_type=self.value_type,
                                               app_name='',
                                               model='',
                                               tracked_value=self.site_tracked_value(site),
                                               start_date=datetime.today(),
                                               end_date=datetime.today(),
                                               using=using)
                    #Update site tracker
                    try:
                        site_tracker = SiteTracker.objects.get(site_name=site)
                        site_tracker.tracked_value = self.site_tracked_value(site)
                        site_tracker.update_date = datetime.today()
                        site_tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
                    except SiteTracker.DoesNotExist:
                        # Create the site tracker if it does not exist.
                        SiteTracker.objects.create(is_active=True,
                                               tracker=tracker,
                                               name=self.name,
                                               value_type=self.value_type,
                                               app_name='bcpp_subject',
                                               site_name=site,
                                               model='PimaVl',
                                               tracked_value=self.site_tracked_value(site),
                                               start_date=datetime.today(),
                                               end_date=datetime.today(),
                                               using=using)

    def update_central_tracker(self, using='default'):
        """Undates the tracked value on the central site."""

        if Device().is_central_server:
            try:
                tracker = Tracker.objects.get(is_active=True, name=self.name, value_type=self.value_type)
                tracker.tracked_value = self.tracked_value
                tracker.update_date = datetime.today()
                tracker.save(update_fields=['tracked_value', 'update_date'])
            except Tracker.DoesNotExist:
                Tracker.objects.create(is_active=True,
                                   name=self.name,
                                   value_type=self.value_type,
                                   app_name='bcpp_subject',
                                   model='PimaVl',
                                   tracked_value=self.tracked_value,
                                   start_date=datetime.today(),
                                   end_date=datetime.today())
            for site in self.registered_sites:
                try:
                    site_tracker = SiteTracker.objects.get(site_name=site)
                    site_tracker.tracked_value = self.site_tracked_value(site)
                    site_tracker.update_date = datetime.today()
                    site_tracker.save(update_fields=['tracked_value', 'update_date'])
                except SiteTracker.DoesNotExist:
                    SiteTracker.objects.create(is_active=True,
                                   tracker=tracker,
                                   name=self.name,
                                   value_type=self.value_type,
                                   app_name='bcpp_subject',
                                   site_name=site,
                                   model='PimaVl',
                                   tracked_value=self.tracked_value,
                                   start_date=datetime.today(),
                                   end_date=datetime.today())

    @property
    def tracked_value(self):
        """Gets the tracked value."""
        try:
            return Tracker.objects.get(value_type=self.value_type, name=self.name, is_active=True)
        except Tracker.DoesNotExist:
            raise ImproperlyConfigured("Cannot retrieve tracker model instance, make sure it exists.")

    @property
    def required_pimavl(self):
        """ Return the number of required pimavl """
        return self.tracked_value.value_limit - self.tracked_value.tracked_value

    def site_tracked_value(self, site, using='default'):
        """Gets the value of the tracked value for the site."""
        PimaVl = get_model('bcpp_subject', 'pimavl')
        site_tracked_value = PimaVl.objects.filter(
            value_type=self.value_type,
            subject_visit__household_member__household_structure__household__plot__community=site,
            using=using)
        site_tracked_value.count()
        return site_tracked_value

    def producer_online(self, producer):
        hostname, _, _ = getproducerbyaddr(producer)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        try:
            s.connect((hostname, 3306))
            connected = True
        except socket.error:
            pass
        s.close()
        return connected

    @property
    def online_producers(self):
        producers = Producer.objects.all()
        online_producers = []
        for producer in producers:
            if self.producer_online(producer):
                online_producers.append(producer.name)
        return online_producers

    @property
    def registered_sites(self):
        return settings.REGISTERED_SITES

    def update_trackers(self):
        """Update all trackers."""

        self.update_site_tracker()
        self.update_producer_tracker()
        self.update_central_tracker()

    def tracked_values(self):
        tracked_dict = {}
        tracker = self.tracked_value
        color_scheme = ['F2FFA1', 'FFE787', 'FF9A42', 'FF4B1F']
        if tracker.tracked_value == 400:
            req_color = color_scheme[3]
        elif tracker.tracked_value >= 390:
            req_color = color_scheme[2]
        elif tracker.tracked_value >= 350:
            req_color = color_scheme[1]
        else:
            req_color = color_scheme[0]
        tracked_dict['tracked_value'] = tracker.tracked_value
        tracked_dict['value_type'] = TrackerHelper().value_type
        tracked_dict['req_pimavl'] = TrackerHelper().required_pimavl
        tracked_dict['color_status'] = req_color
        return tracked_dict

    def send_email_notification(self):
        if Device().is_central_server:
            if self.tracked_value.tracked_value >= 300:
                mail = Mail(receiver=Reciever())
                mail.send_mail()
