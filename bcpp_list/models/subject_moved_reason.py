from edc_base.model.models import ListModelMixin


class SubjectMovedReason(ListModelMixin):

    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Subject Moved Reason"
        verbose_name_plural = "Subject Moved Reason"
        ordering = ['name']
