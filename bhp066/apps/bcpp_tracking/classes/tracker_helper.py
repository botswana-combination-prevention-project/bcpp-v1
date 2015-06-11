import socket

from datetime import datetime

from django.conf import settings

from apps.bcpp_subject.models import PimaVl
from ..models import Tracker, SiteTracker

class TrackerHelper(object):
    """Calculates and updates tracked value.
    """


    def update_site_tracker(self):
        pass


    def update_producer_tracker(self, using, value_type, name):
        """Updates the tracked value on the producer."""

        try:
            tracker = Tracker.objects.get(is_active=True, name=name, value_type)
            tracker.tracked_value = self.tracker_value_at_site(using)
            tracker.update_date = datetime.today()
            tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
        except Tracker.DoesNotExist:
            # Create the tracker if it does not exist.
            Tracker.objects.create(is_active=True,
                                   name=name,
                                   value_type=value_type,
                                   app_name='',
                                   model='',
                                   tracked_value=self.tracked_value_at_site(using),
                                   start_date=datetime.today(),
                                   end_date=datetime.today())
        site = settings.CURRENT_COMMUNITY
        try:
            site_tracker = SiteTracker.objects.get(site_name=site)
            site_tracker.tracked_value = self.site_tracked_value(value_type, site)
            site_tracker.update_date = datetime.today()
            site_tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
        except SiteTracker.DoesNotExist:
            # Create the site tracker if it does not exist.
            Tracker.objects.create(is_active=True,
                                   tracker=tracker,
                                   name=name,
                                   value_type=value_type,
                                   app_name='',
                                   site_name=site,
                                   model='',
                                   tracked_value=self.tracked_value_at_site(using),
                                   start_date=datetime.today(),
                                   end_date=datetime.today())

    def update_central_tracker(self, using, value_type, name):
        """Undates the tracked value on the central site."""

        if settings.DEVICE_ID == 99:
            try:
                tracker = Tracker.objects.get(is_active=True, name=name, value_type)
                tracker.tracked_value = self.tracked_value(value_type)
                tracker.update_date = datetime.today()
                tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
            except Tracker.DoesNotExist:
                Tracker.objects.create(is_active=True,
                                   name=name,
                                   value_type=value_type,
                                   app_name='',
                                   model='',
                                   tracked_value=self.tracked_value(value_type),
                                   start_date=datetime.today(),
                                   end_date=datetime.today())
            tracked_sites = settings.REGISTERED_SITES
            for site in tracked_sites:
                try:
                    site_tracker = SiteTracker.objects.get(site_name=site)
                    site_tracker.tracked_value = self.site_tracked_value(value_type, site)
                    site_tracker.update_date = datetime.today()
                    site_tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
                except SiteTracker.DoesNotExist:
                    Tracker.objects.create(is_active=True,
                                   tracker=tracker,
                                   name=name,
                                   value_type=value_type,
                                   app_name='',
                                   site_name=site,
                                   model='',
                                   tracked_value=self.tracked_value(value_type),
                                   start_date=datetime.today(),
                                   end_date=datetime.today())

    def tracked_value(self, value_type):
        """Gets the tracked value."""

        tracked_value = PimaVl.objects.filter(value_type=value_type)
        return tracked_value

    def site_tracked_value(self, value_type, site):
        """Gets the value of the tracked value for the site."""

        site_tracked_value = PimaVl.objects.filter(
            value_type=value_type,
            subject_visit__household_member__household_structure__household__plot__community=site)
        site_tracked_value.count()
        return site_tracked_value

    def tracked_value_at_site(self, using):
        """Queries the tracked value from the site server."""

        site = settings.CURRENT_COMMUNITY
        tracker = Tracker.objects.get(site_name=site, using=using)
        return tracker.tracked_value

    def producer_online(self):
        pass

    def registered_sites(self):
        return settings.REGISTERED_SITES

