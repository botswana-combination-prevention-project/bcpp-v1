from bhp_base_model.models import BaseListModel


class SubjectMovedReason(BaseListModel):
    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Subject Moved Reason"
        verbose_name_plural = "Subject Moved Reason"
        ordering = ['name']
