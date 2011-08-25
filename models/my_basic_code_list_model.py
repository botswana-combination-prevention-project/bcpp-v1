from django.db import models
from bhp_common.models import MyBasicListModel

       
class MyBasicCodeListModel(MyBasicListModel):

    """Basic Code List Model."""

    code = models.CharField(max_length=25, unique=True)
                
    def __unicode__(self):
        return "%s: %s" % (self.code, self.name)

    class Meta:
        abstract = True
