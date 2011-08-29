from django.conf import settings
from django.db import models
from bhp_identifier.classes import Identifier


class ReceiveManager(models.Manager):

    def get_identifier(self, **kwargs):
        site_code = kwargs.get('site_code', settings.SITE_CODE)
        return Identifier(settings.SITE_CODE).create()

    def create_from_requisition(self, requisition_identifier):
        pass

