from django.db import models
#from bhp_common.models import MyBasicListModel, MyBasicUuidModel
#from bhp_content_type_map.models import ContentTypeMap
from bhp_common.choices import YES_NO
from bhp_visit.models import BaseWindowPeriodItem
from lab_panel.models import Panel
from lab_clinic_api.models import Panel as LabClinicApiPanel
from bhp_entry.choices import ENTRY_CATEGORY, ENTRY_WINDOW, ENTRY_STATUS


class BaseLabEntry(BaseWindowPeriodItem):

    # TODO: this needs to be dropped
    panel = models.ForeignKey(Panel)

    # TODO: this needs to be filled in then renamed as panel
    lab_clinic_api_panel = models.ForeignKey(LabClinicApiPanel,
        null=True,
        help_text='This is to replace panel above...')

    entry_order = models.IntegerField()

    required = models.CharField(
        max_length=10,
        choices=YES_NO,
        default='YES')

    entry_category = models.CharField(
        max_length=25,
        choices=ENTRY_CATEGORY,
        default='CLINIC',
        )

    entry_window_calculation = models.CharField(
        max_length=25,
        choices=ENTRY_WINDOW,
        default='VISIT',
        help_text='Base the entry window period on the visit window period or specify a form specific window period',
        )

    default_entry_status = models.CharField(
        max_length=25,
        choices=ENTRY_STATUS,
        default='NEW',
        )

    class Meta:
        abstract = True
