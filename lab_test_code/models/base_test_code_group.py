from django.db import models
from lab_base_model.models import BaseLabModel


class BaseTestCodeGroup(BaseLabModel):

    code = models.CharField(max_length=15, null=True)

    name = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        )

    objects = models.Manager()

    def __unicode__(self):
        return self.code

#    def natural_key(self):
#        return (self.code, )

    class Meta:
        abstract = True
