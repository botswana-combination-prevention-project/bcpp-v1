from edc_base.model.models import ListModelMixin


class HouseholdSurveySource (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Household Survey Source"
        verbose_name_plural = "Household Survey Source"
