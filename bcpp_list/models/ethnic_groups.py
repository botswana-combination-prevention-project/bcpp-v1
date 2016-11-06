from edc_base.model.models import ListModelMixin


class EthnicGroups (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Ethnic Groups"
        verbose_name_plural = "Ethnic Groups"
