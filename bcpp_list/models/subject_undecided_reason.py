from edc_base.model.models import ListModelMixin


class SubjectUndecidedReason(ListModelMixin):

    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Subject Undecided Reason"
        verbose_name_plural = "Subject Undecided Reason"
