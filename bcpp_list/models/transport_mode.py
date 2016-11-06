from edc_base.model.models import ListModelMixin


class TransportMode (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Transport Mode"
        verbose_name_plural = "Transport Mode"
