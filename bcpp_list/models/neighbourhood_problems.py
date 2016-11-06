from edc_base.model.models import ListModelMixin


class NeighbourhoodProblems (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Neighbourhood Problems"
        verbose_name_plural = "Neighbourhood Problems"
