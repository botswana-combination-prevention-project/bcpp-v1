from edc_base.model.models import ListModelMixin


class FamilyPlanning (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Family Planning"
        verbose_name_plural = "Family Planning"
