from datetime import date
from django.db import models
from bhp_base_model.classes import BaseModel


class Comment(BaseModel):

    subject = models.CharField(max_length=50)

    comment_date = models.DateField(default=date.today())

    comment = models.TextField(max_length=500)

    objects = models.Manager()

    class Meta:
        app_label = "bhp_data_manager"
