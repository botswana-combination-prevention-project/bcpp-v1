from django.db import models
from bhp_common.models import MyBasicModel


class Test(MyBasicModel):
    test_code = models.CharField("Univeral Test ID", max_length=10, unique=True)
    test_name = models.CharField("UTestID Description", max_length=25)
    comment = models.CharField("Comment", max_length=250, blank=True)
    panel = models.ForeignKey(Panel)

    def __unicode__(self):
        return "%s: %s" % (self.test_code,self.test_name)
