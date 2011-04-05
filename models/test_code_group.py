from django.db import models
from bhp_common.models import MyBasicModel, MyBasicListModel


class TestCodeGroup(MyBasicListModel):

    class Meta:
        app_label = 'bhp_lab'  
