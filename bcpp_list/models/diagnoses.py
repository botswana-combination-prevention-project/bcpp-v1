from bhp_base_model.models import BaseListModel


class Diagnoses (BaseListModel):
    pass

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Diagnoses"
        verbose_name_plural = "Diagnoses"
