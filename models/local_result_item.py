from django.db import models
from lab_result_item.models import BaseResultItem
from local_result import LocalResult


class LocalResultItem(BaseResultItem):

    local_result = models.ForeignKey(LocalResult)
    
    class Meta:
        app_label = "lab_clinic_api"
    
