from bhp_base_model.models import BaseListModel


class ElectricalAppliances (BaseListModel):
    pass

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Electrical Appliances"
        verbose_name_plural = "Electrical Appliances"
