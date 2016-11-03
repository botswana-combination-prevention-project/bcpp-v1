from edc_base.model.models import BaseListModel


class Diagnoses (BaseListModel):
    pass

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Diagnoses"
        verbose_name_plural = "Diagnoses"
