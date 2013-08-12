from django.db import models
#import django
from bhp_base_model.models import BaseModel
from bcpp_household.managers import CommunityManager


class Community(BaseModel):

    name = models.CharField("Name", max_length=25)
    is_current = models.BooleanField(default=False)

    objects = CommunityManager()

    def natural_key(self):
        return (self.name, )
    
    def __unicode__(self):
        return self.name
#     def save(self, *args, **kwargs):
#         import sys
#         print sys.path
#         print django.VERSION
#         super(Community, self).save(*args, **kwargs)
    class Meta:
        app_label = 'bcpp_household'
