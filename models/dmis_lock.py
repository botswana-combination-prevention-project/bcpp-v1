from django.db import models
from base_model import BaseModel


class DmisLock(BaseModel):

    """ Track who is updating from dmis to django-lis.

    The lock data is on the django-lis and managed by clients via :class:DmisLock.

    ..seealso:: :class:DmisLock."""

    lock_name = models.CharField(max_length=25, null=True)

    objects = models.Manager()

    def __unicode__(self):
        return self.lock_name

    class Meta:
        app_label = 'lab_import_dmis'
