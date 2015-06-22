from django.db import models

from edc.base.model.models import BaseModel


class Tracker(BaseModel):

    update_date = models.DateTimeField(
         verbose_name='Start Date/Time',
         null=True
        )

    is_active = models.BooleanField(
        default=True,
        help_text=("Is the tracker active."))

    name = models.CharField(
        max_length=100,
        help_text=("The name of the server, e.g central.")
        )

    value_type = models.CharField(
        max_length=100,
        help_text=("Type of the value being tracked, e.g mobile setup value or household setup.")
        )

    app_name = models.CharField(
        max_length=100,
        help_text=("app where the value being tracked is.")
        )

    model = models.CharField(
        max_length=150,
        help_text=("model being tracked.")
        )

    tracked_value = models.IntegerField(
        default=0,
        editable=True,
        help_text=("updated after consuming transactions.")
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

    def __unicode__(self):
        return "{}_{}".format(self.name, self.value_type)

    class Meta:
        app_label = 'bcpp_tracking'


class SiteTracker(BaseModel):

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

    def __unicode__(self):
        return "{}_{}".format(self.model, self.tracker.value_type)

    class Meta:
        app_label = 'bcpp_tracking'
        unique_together = (('site_name', 'tracker'),)
