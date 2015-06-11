import socket

from datetime import datetime

from django.conf import settings

from apps.bcpp_subject.models import PimaVl
from ..models import Tracker, SiteTracker


class TrackerHelper(object):
    """Calculates and updates tracked value.
    """

    def update_site_tracker(self):
        """Update the tracker and site tracker at the site."""

        for site in self.registered_sites:
            # Update tracker
            using = site + ".bhp.org.bw"
            try:
                tracker = Tracker.objects.get(is_active=True, name=name, value_type)
                tracker.tracked_value = self.site_tracked_value(value_type, site)
                tracker.update_date = datetime.today()
                tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
            except Tracker.DoesNotExist:
                # Create the tracker if it does not exist.
                Tracker.objects.create(is_active=True,
                                       name=name,
                                       value_type=value_type,
                                       app_name='',
                                       model='',
                                       tracked_value=self.site_tracked_value(value_type, site),
                                       start_date=datetime.today(),
                                       end_date=datetime.today(),
                                       using=using)
            #Update site tracker
            try:
                site_tracker = SiteTracker.objects.get(site_name=site)
                site_tracker.tracked_value = self.site_tracked_value(value_type, site)
                site_tracker.update_date = datetime.today()
                site_tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
            except SiteTracker.DoesNotExist:
                # Create the site tracker if it does not exist.
                SiteTracker.objects.create(is_active=True,
                                       tracker=tracker,
                                       name=name,
                                       value_type=value_type,
                                       app_name='bcpp_subject',
                                       site_name=site,
                                       model='PimaVl',
                                       tracked_value=self.site_tracked_value(value_type, site),
                                       start_date=datetime.today(),
                                       end_date=datetime.today(),
                                       using=using)

    def update_producer_tracker(self, using, value_type, name):
        """Updates the tracked value on the producer.

        Attributes:
        using: The using value for the database in the producer.
        value_type: The type of value being tracked, e.g mobile setup or household setup for poc vl.
        name: The name of the central site
        """

        site = settings.CURRENT_COMMUNITY
        # Update tracker
        try:
            tracker = Tracker.objects.get(is_active=True, name=name, value_type)
            tracker.tracked_value = self.site_tracked_value(value_type, site)
            tracker.update_date = datetime.today()
            tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
        except Tracker.DoesNotExist:
            # Create the tracker if it does not exist.
            Tracker.objects.create(is_active=True,
                                   name=name,
                                   value_type=value_type,
                                   app_name='',
                                   model='',
                                   tracked_value=self.site_tracked_value(value_type, site),
                                   start_date=datetime.today(),
                                   end_date=datetime.today(),
                                   using=using)
        #Update site tracker
        try:
            site_tracker = SiteTracker.objects.get(site_name=site)
            site_tracker.tracked_value = self.site_tracked_value(value_type, site)
            site_tracker.update_date = datetime.today()
            site_tracker.save(update_fields=['tracked_value', 'update_date'], using=using)
        except SiteTracker.DoesNotExist:
            # Create the site tracker if it does not exist.
            SiteTracker.objects.create(is_active=True,
                                   tracker=tracker,
                                   name=name,
                                   value_type=value_type,
                                   app_name='bcpp_subject',
                                   site_name=site,
                                   model='PimaVl',
                                   tracked_value=self.site_tracked_value(value_type, site),
                                   start_date=datetime.today(),
                                   end_date=datetime.today(),
                                   using=using)

    def update_central_tracker(self, using, value_type, name):
        """Undates the tracked value on the central site."""

        try:
            tracker = Tracker.objects.get(is_active=True, name=name, value_type)
            tracker.tracked_value = self.tracked_value(value_type)
            tracker.update_date = datetime.today()
            tracker.save(update_fields=['tracked_value', 'update_date'])
        except Tracker.DoesNotExist:
            Tracker.objects.create(is_active=True,
                               name=name,
                               value_type=value_type,
                               app_name='bcpp_subject',
                               model='PimaVl',
                               tracked_value=self.tracked_value(value_type),
                               start_date=datetime.today(),
                               end_date=datetime.today())
        for site in self.registered_sites:
            try:
                site_tracker = SiteTracker.objects.get(site_name=site)
                site_tracker.tracked_value = self.site_tracked_value(value_type, site)
                site_tracker.update_date = datetime.today()
                site_tracker.save(update_fields=['tracked_value', 'update_date'])
            except SiteTracker.DoesNotExist:
                SiteTracker.objects.create(is_active=True,
                               tracker=tracker,
                               name=name,
                               value_type=value_type,
                               app_name='bcpp_subject',
                               site_name=site,
                               model='PimaVl',
                               tracked_value=self.tracked_value(value_type),
                               start_date=datetime.today(),
                               end_date=datetime.today())

    def tracked_value(self, value_type):
        """Gets the tracked value."""

        tracked_value = PimaVl.objects.filter(value_type=value_type)
        return tracked_value

    def site_tracked_value(self, using='default', value_type, site):
        """Gets the value of the tracked value for the site."""

        site_tracked_value = PimaVl.objects.filter(
            value_type=value_type,
            subject_visit__household_member__household_structure__household__plot__community=site,
            using=using)
        site_tracked_value.count()
        return site_tracked_value

    def producer_online(self):
        pass

    @property
    def registered_sites(self):
        return settings.REGISTERED_SITES

