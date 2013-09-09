from django.db import models
from django.core.urlresolvers import reverse
from bhp_sync.models import BaseSyncUuidModel
from bhp_appointment.managers import ConfigurationManager


class Configuration(BaseSyncUuidModel):
    """Only allows a single record."""
    allowed_iso_weekdays = models.IntegerField(
        default=12345,
        help_text='List ISO weekdays to which appointments may be scheduled. For example, 12345 where 1 is Monday.',
        )

    use_same_weekday = models.BooleanField(
        max_length=3,
        default=True,
        help_text='If Ticked, adjust the appointment date to have appointments always land on the same weekday.',
        )

    default_appt_type = models.CharField(
        max_length=10,
        default='clinic',
        choices=(('clinic', 'In clinic'), ('telephone', 'By telephone')),
        help_text=''
        )

    objects = ConfigurationManager()

    def natural_key(self):
        return (self.allowed_iso_weekdays, )

    def save(self, *args, **kwargs):
        if not self.id and self.__class__.objects.all().count() == 1:
            raise ValueError('Configuration model may only have one record and you are trying to add a second. Edit the first record instead.')
        else:
            super(Configuration, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'admin:bhp_appointment_configuration_change',
            args=(self.id,)
            )

    def __unicode__(self):
        return "{0}".format(self.allowed_iso_weekdays)

    class Meta:
        app_label = 'bhp_appointment'
