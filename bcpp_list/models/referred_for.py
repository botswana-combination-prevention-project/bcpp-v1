from edc_base.model.models import BaseListModel


class ReferredFor (BaseListModel):
    pass

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Referred For"
        verbose_name_plural = "Referred For"
