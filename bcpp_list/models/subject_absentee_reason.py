from edc_base.model.models import ListModelMixin


class SubjectAbsenteeReason(ListModelMixin):

    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Subject Absentee Reason"
        verbose_name_plural = "Subject Absentee Reason"
