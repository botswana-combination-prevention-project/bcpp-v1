from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from bhp_common.models import MyBasicModel

class Netbook(MyBasicModel):

    name = models.CharField(
        verbose_name = _("Netbook Name"), 
        unique=True,        
        max_length=10)

    date_purchased = models.DateField(
        verbose_name = _("Date Purchased"), 
        )

    make = models.CharField(
        verbose_name = _("Make"), 
        max_length=25)

    model = models.CharField(
        verbose_name = _("Model"), 
        max_length=25)

    serial_number = models.CharField(
        verbose_name = _("Serial Number"), 
        unique=True,
        max_length=25)

    class Meta:
        ordering = ["name"]
       
    def get_absolute_url(self):
        return "/bhp_netbook/netbook/%s/" % self.id   
    
    def __unicode__(self):
        return "%s" % (self.name)

class NetbookUser(MyBasicModel):
  
    netbook = models.ForeignKey(Netbook)    
    
    user = models.ForeignKey(User)
    
    start_date = models.DateField("Date assigned", 
        help_text=_("Format is YYYY-MM-DD"),
        )
    end_date = models.DateField("Date revoked", 
        null=True, 
        blank=True, 
        help_text = _("Leave blank if in use. Format is YYYY-MM-DD"),
        )

    def __unicode__(self):
        return "%s %s" % (self.user, self.netbook)

