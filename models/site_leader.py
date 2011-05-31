from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from bhp_common.validators import datetime_not_future, datetime_is_future
from bhp_common.choices import YES_NO
from bhp_common.models import MyBasicUuidModel
from bhp_common.fields import NameField, InitialsField

class SiteLeader (MyBasicUuidModel):

    first_name = NameField(
        verbose_name = _("First name")
        )
        
    last_name = NameField(
        verbose_name = _("Last name")
    )
    
    initials = InitialsField()

    def __unicode__(self):
        return '%s, %s' % (self.last_name, self.first_name)
           
    def get_absolute_url(self):
        return "/bhp_lab_registration/siteleader/%s/" % self.id   

    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ['last_name', 'first_name']
        #abstract = True


        

