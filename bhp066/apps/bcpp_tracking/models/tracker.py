from django.db import models

from edc.base.model.models import BaseModel


class Tracker(BaseModel):

    app_name = models.CharField(
        max_length=100,
        )

    model = models.CharField(
        max_length=150,
        )

    name = models.CharField(
        max_length=200,
        )

    limit = models.IntegerField(
        default=0,
        editable=True,
        help_text=('Updated by a signal on <<<>>>. '
                   'Number of <<><>>>.')
    )

    start_date = models.DateTimeField(
         verbose_name='Start Date/Time',
         null=True
        )

    end_date = models.DateTimeField(
        verbose_name='End Date/Time',
        null=True
        )

    class Meta:
        abstract = True
