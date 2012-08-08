from django.db import models
from lab_result.models.base_result import BaseResult
from order import Order


class Result(BaseResult):

    order = models.ForeignKey(Order)

    objects = models.Manager()

    class Meta:
        app_label = 'lab_clinic_api'
        #ordering =['result_identifier']
