from edc_base.model.models import ListModelMixin


class ReferredTo (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Referred To"
        verbose_name_plural = "Referred To"
