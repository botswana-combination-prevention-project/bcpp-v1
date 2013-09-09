from bhp_base_model.models import BaseListModel


class SubjectAbsenteeReason(BaseListModel):

    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Subject Absentee Reason"
        verbose_name_plural = "Subject Absentee Reason"
        