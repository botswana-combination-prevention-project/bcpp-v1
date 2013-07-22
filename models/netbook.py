from django.db import models
from django.utils.translation import ugettext as _
from bhp_base_model.models import BaseModel


class Netbook(BaseModel):

    name = models.CharField(
        verbose_name = _("Netbook Name"), 
        unique = True,        
        max_length = 10,
        )

    is_active = models.BooleanField(
        default=False
        )

    db_name = models.CharField(
        verbose_name = _("Database Name"), 
        blank = True,
        null = True,
        max_length = 10,
        )

    is_alive = models.BooleanField(
        default=False
        )
        
    last_seen = models.DateField(
        null=True)   

    date_purchased = models.DateField(
        verbose_name = _("Date Purchased"), 
        )

    make = models.CharField(
        verbose_name = _("Make"), 
        max_length = 25)

    model = models.CharField(
        verbose_name = _("Model"), 
        max_length = 25)

    serial_number = models.CharField(
        verbose_name = _("Serial Number"), 
        unique = True,
        max_length = 25)
        
    ip_address = models.IPAddressField(
        null = True,
        blank = True,
        )        
    
    objects = models.Manager()

    def get_absolute_url(self):
        return "/bhp_netbook/netbook/%s/" % self.id   
    
    def __unicode__(self):
        return "%s" % (self.name)
        
    class Meta:
        ordering = ['name'] 
        app_label = 'bhp_netbook'
