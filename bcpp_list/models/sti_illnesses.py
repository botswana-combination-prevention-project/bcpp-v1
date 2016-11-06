from edc_base.model.models import ListModelMixin


class StiIllnesses (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "HIV-related illness"
        verbose_name_plural = "HIV-related illness"
