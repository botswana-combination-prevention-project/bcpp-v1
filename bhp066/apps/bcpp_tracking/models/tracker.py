from django.db import models

from edc.base.model.models import BaseModel

from .site_tracker import SiteTracker


class Tracker(BaseModel):

    update_date = models.DateTimeField(
         verbose_name='Start Date/Time',
         null=True
        )

    app_name = models.CharField(
        max_length=100,
        )

    model = models.CharField(
        max_length=150,
        )

    tracked_value = models.IntegerField(
        default=0,
        editable=True,
        help_text=('Updated by a signal on <<<>>>. '
                   'Number of <<><>>>.')
    )

    value_limit = models.IntegerField(
        default=400,
        editable=True,
    )

    start_date = models.DateTimeField(
         verbose_name='Start Date/Time',
         null=True
        )

    end_date = models.DateTimeField(
        verbose_name='End Date/Time',
        null=True
        )

    def save(self, *args, **kwargs):
        using = kwargs.get('using,')
        super(Tracker, self).save(*args, **kwargs)


    class Meta:
        app_label = 'bcpp_tracking'

class SiteTracker(BaseDispatchSyncUuidModel):

    tracker = models.ForeignKey(Tracker)

    update_date = models.DateTimeField(
         verbose_name='Start Date/Time',
         null=True
        )

    app_name = models.CharField(
        max_length=100,
        )

    model = models.CharField(
        max_length=150,
        )

    tracked_value = models.IntegerField(
        default=0,
        editable=True,
        help_text=('Updated by a signal on <<<>>>. '
                   'Number of <<><>>>.')
    )

    site_name = models.CharField(
        max_length=200,
        )

    start_date = models.DateTimeField(
         verbose_name='Start Date/Time',
         null=True
        )

    end_date = models.DateTimeField(
        verbose_name='End Date/Time',
        null=True
        )


    def save(self, *args, **kwargs):
        using = kwargs.get('using,')
        super(SiteTracker, self).save(*args, **kwargs)