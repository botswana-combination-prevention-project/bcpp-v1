import socket
from django.conf import settings

from apps.bcpp_subject.models import PimaVl
from ..models import Tracker, SiteTracker

class TrackerHelper(object):
    """Calculates and updates tracked value.
    """


    def update_site_tracker(self):
        pass


    def update_producer_tracker(self, using, value_type, name):
        try:
            tracker = Tracker.objects.get(is_active=True, name=name, value_type)
            tracker.tracked_value = self.tracked_value(value_type)
            tracker.save(update_fields=['tracked_value'], using=using)
        except Tracker.DoesNotExist:
            pass
        tracked_sites = settings.REGISTERED_SITES
        site = settings.CURRENT_COMMUNITY
        try:
            site_tracker = SiteTracker.objects.get(site_name=site)
            site_tracker.tracked_value = self.site_tracked_value(value_type, site)
            site_tracker.save(update_fields=['tracked_value'], using=using)
        except SiteTracker.DoesNotExist:
            pass


    def update_central_tracker(self, using, value_type, name):
        try:
            tracker = Tracker.objects.get(is_active=True, name=name, value_type)
            tracker.tracked_value = self.tracked_value(value_type)
            tracker.save(update_fields=['tracked_value'], using=using)
        except Tracker.DoesNotExist:
            pass
        tracked_sites = settings.REGISTERED_SITES
        for site in tracked_sites:
            try:
                site_tracker = SiteTracker.objects.get(site_name=site)
                site_tracker.tracked_value = self.site_tracked_value(value_type, site)
                site_tracker.save(update_fields=['tracked_value'], using=using)
            except SiteTracker.DoesNotExist:
                pass



    def tracked_value(self, value_type):
        tracked_value = PimaVl.objects.filter(value_type=value_type)
        return tracked_value

    def site_tracked_value(self, value_type, site):
        site_tracked_value = PimaVl.objects.filter(
            value_type=value_type,
            subject_visit__household_member__household_structure__household__plot__community=site)
        site_tracked_value.count()
        return site_tracked_value


    def producer_online(self):
        pass

    def registered_sites(self):
        return settings.REGISTERED_SITES

