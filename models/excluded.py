from django.db import models
from bhp_sync.models import BaseSyncUuidModel


class Excluded (BaseSyncUuidModel):

    app_label = models.CharField(
        max_length=50,
        )
    object_name = models.CharField(
        max_length=50,
        )
    model_pk = models.CharField(
        max_length=36,
        unique=True
        )
    excluded = models.TextField()

    objects = models.Manager()

    class Meta:
        app_label = 'bhp_supplemental_fields'
