from edc_base.model.models import BaseListModel


class ReferredTo (BaseListModel):
    pass

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Referred To"
        verbose_name_plural = "Referred To"
