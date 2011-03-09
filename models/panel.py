from django.db import models
from bhp_common.models import MyBasicModel


class Panel(MyBasicModel):
    name = models.CharField("Panel Name", max_length=25)
    comment = models.CharField("Comment", max_length=250, blank=True)

    def __unicode__(self):
        return self.name


