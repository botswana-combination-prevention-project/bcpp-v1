from edc_base.model.models import ListModelMixin


class ElectricalAppliances (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Electrical Appliances"
        verbose_name_plural = "Electrical Appliances"
