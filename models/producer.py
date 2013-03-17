from django.db import models
from bhp_base_model.models import BaseUuidModel


class Producer(BaseUuidModel):

    name = models.CharField(
        max_length=50,
        help_text='Usually hostname-database_name. e.g mpp83-bhp041_survey',
        unique=True,
        )

    settings_key = models.CharField(
        max_length=50,
        help_text='Key in settings.DATABASES, usually hostname of producer',
        unique=True,
        )

    url = models.CharField(
        max_length=64,
        )

    is_active = models.BooleanField(
        default=True
        )

    sync_datetime = models.DateTimeField(
        null=True
        )

    sync_status = models.CharField(
        max_length=250,
        default='-',
        null=True)
    json_limit = models.IntegerField(
        default=0)
    json_total_count = models.IntegerField(
        default=0
        )

    comment = models.TextField(
        max_length=50,
        null=True,
        blank=True)
    objects = models.Manager()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'bhp_sync'
        ordering = ['name']
        unique_together = (('settings_key', 'is_active'), )
