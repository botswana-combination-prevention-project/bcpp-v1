from django.db import models
from bhp_base_model.models import BaseUuidModel


class BaseLockModel(BaseUuidModel):

    """ Track who is updating from dmis to django-lis.

    The lock data is on the django-lis and managed by clients via :class:DmisLock.

    ..seealso:: :class:DmisLock."""

    lock_name = models.CharField(max_length=50, unique=True)
    objects = models.Manager()

    def __unicode__(self):
        return self.lock_name

    class Meta:
        abstract = True
