from edc_base.model.models import BaseListModel


class HeartDisease (BaseListModel):
    pass

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Heart Disease"
        verbose_name_plural = "Heart Disease"
