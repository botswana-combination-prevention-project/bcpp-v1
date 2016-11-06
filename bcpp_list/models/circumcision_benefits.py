from edc_base.model.models import ListModelMixin


class CircumcisionBenefits (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Circumcision Benefits"
        verbose_name_plural = "Circumcision Benefits"
