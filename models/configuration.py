from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from bhp_common.models import MyBasicUuidModel
from bhp_common.choices import YES_NO
from bhp_appointment.managers import ConfigurationManager


class Configuration(MyBasicUuidModel):

    allowed_iso_weekdays = models.IntegerField(
        default = 12345,
        help_text = 'List ISO weekdays to which appointments may be scheduled. For example, 12345 where 1 is Monday.' ,
        )

    use_same_weekday = models.BooleanField(
        max_length = 3,
        default = True,
        help_text = 'If Ticked, adjust the appointment date to have appointments always land on the same weekday.',
        )
        
    objects = ConfigurationManager()        

    def save(self, *args, **kwargs):
        
        if not self.id and self.__class__.objects.all().count() == 1:
            raise ValidationError, 'Configuration model may only have one record and you are trying to add a second. Edit the first record instead.'
        else:
            super(Configuration, self).save(*args, **kwargs)            

    def get_absolute_url(self):
        return reverse('admin:bhp_appointment_configuration_change', args=(self.id,))

    class Meta:
        app_label = 'bhp_appointment' 
    
