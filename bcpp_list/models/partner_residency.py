from edc_base.model.models import ListModelMixin


class PartnerResidency (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Partner Residency"
        verbose_name_plural = "Partner Residency"
