from datetime import date
from django.db import models
from bhp_base_model.models import BaseModel


class DataNote(BaseModel):
    """ Tracks notes on missing or required data.

    Note can be displayed on the dashboard"""
    subject = models.CharField(max_length=50)
    comment_date = models.DateField(default=date.today())
    comment = models.TextField(max_length=500)
    display_on_dashboard = models.BooleanField(default=True)
    rt = models.IntegerField(default=0, verbose_name='RT Ref.')
    status = models.CharField(
        max_length=35,
        choices=(('Open', 'Open'), ('Stalled', 'Stalled'), ('Resolved', 'Resolved')),
        default='Open')
    objects = models.Manager()

    class Meta:
        app_label = "bhp_data_manager"
