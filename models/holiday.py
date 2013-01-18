from django.db import models
from django.core.urlresolvers import reverse
from bhp_sync.models import BaseSyncUuidModel
from configuration import Configuration


class Holiday(BaseSyncUuidModel):

    configuration = models.ForeignKey(Configuration)
    holiday_name = models.CharField(
        max_length=25,
        default='holiday')
    holiday_date = models.DateField(
        unique=True)

    objects = models.Manager()

    def __unicode__(self):
        return "%s on %s" % (self.holiday_name, self.holiday_date)

    def get_absolute_url(self):
        return reverse('admin:bhp_appointment_holiday_change', args=(self.id,))

    class Meta:
        ordering = ['holiday_date', ]
        app_label = 'bhp_appointment'
