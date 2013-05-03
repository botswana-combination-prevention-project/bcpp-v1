from datetime import date
from django.db import models
from bhp_base_model.models import BaseModel
from bhp_crypto.fields import EncryptedTextField


class Comment(BaseModel):

    subject = models.CharField(max_length=50)
    comment_date = models.DateField(default=date.today())
    comment = EncryptedTextField(max_length=500)
    rt = models.IntegerField(default=0, verbose_name='RT Ref.')
    status = models.CharField(
        max_length=35,
        choices=(('Open', 'Open'), ('Stalled', 'Stalled'), ('Resolved', 'Resolved')),
        default='Open')
    objects = models.Manager()

    class Meta:
        app_label = "bhp_data_manager"
