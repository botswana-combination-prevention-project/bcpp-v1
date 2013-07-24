from django.db import models
from bhp_base_model.models import BaseModel


class Community(BaseModel):

    name = models.CharField("Name", max_length=25)
    is_current = models.BooleanField(default=False)

    objects = models.Manager()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'bcpp_household'
