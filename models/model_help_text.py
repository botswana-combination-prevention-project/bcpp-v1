from django.db import models
from bhp_base_model.models import BaseModel
from bhp_common.utils import convert_from_camel


class ModelHelpText(BaseModel):

    help_text = models.TextField(max_length=500)
    additional_comment = models.TextField(max_length=500)
    trans_assistance = models.TextField(max_length=500)
    status = models.CharField(
        max_length=35,
        choices=(('active', 'Active'), ('inactive', 'Inactive')),
        default='Active')
    app_label = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50, editable=False)
    object_name = models.CharField(max_length=50)
    field_name = models.CharField(max_length=50)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.model_name = convert_from_camel(self.object_name)
        super(ModelHelpText, self).save(*args, **kwargs)

    class Meta:
        app_label = "bhp_data_manager"
