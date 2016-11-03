import dateutil.parser

from datetime import timedelta
from django.db import models


class ContactLogManager(models.Manager):
    def get_by_natural_key(self, pk):
        return self.get(pk=pk)


class ContactLogItemManager(models.Manager):
    def get_by_natural_key(self, contact_datetime, pk):
        contact_datetime = dateutil.parser.parse(contact_datetime)
        margin = timedelta(microseconds=999)
        ContactLog = models.get_model('bcpp_household_member', 'ContactLog')
        contact_log = ContactLog.objects.get_by_natural_key(pk)
        return self.get(report_datetime__range=(contact_datetime - margin, contact_datetime + margin),
                        contact_log=contact_log)
        return self.get(pk=pk)
