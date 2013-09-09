from django.db import models
from base_code_list import BaseCodeList


class DxCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    def __unicode__(self):
        return '%s: %s' % (self.code, self.short_name)

    class Meta:
        app_label = "bhp_code_lists"
