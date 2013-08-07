from django.db import models
from bhp_base_model.models import BaseModel


class ModelHelpText(BaseModel):

    help_text = models.TextField(max_length=500)
    additional_comment = models.TextField(max_length=500)
    trans_assistance = models.TextField(max_length=500)
    status = models.CharField(
        max_length=35,
        choices=(('active', 'Active'), ('inactive', 'Inactive')),
        default='Active')
    app_label = models.CharField(max_length=50)
    module_name = models.CharField(max_length=50, editable=False)
    field_name = models.CharField(max_length=50)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.module_name = self.module_name.lower()
        super(ModelHelpText, self).save(*args, **kwargs)

    class Meta:
        app_label = "bhp_data_manager"
