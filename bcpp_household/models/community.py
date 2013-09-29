from django.db import models
from edc_core.bhp_base_model.models import BaseModel
from ..managers import CommunityManager


class Community(BaseModel):

    name = models.CharField("Name", max_length=25)
    is_current = models.BooleanField(default=False)

    objects = CommunityManager()

    def natural_key(self):
        return (self.name, )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'bcpp_household'
