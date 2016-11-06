from edc_base.model.models import ListModelMixin


class ResidentMostLikely (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Resident Most Likely Status"
        verbose_name_plural = "Resident Most Likely Status"
