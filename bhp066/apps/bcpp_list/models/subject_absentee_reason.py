from edc_base.model.models import BaseListModel


class SubjectAbsenteeReason(BaseListModel):

    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Subject Absentee Reason"
        verbose_name_plural = "Subject Absentee Reason"
