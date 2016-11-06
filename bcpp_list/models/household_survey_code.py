from edc_base.model.models import ListModelMixin


class HouseholdSurveyCode (ListModelMixin):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Household Survey Code"
        verbose_name_plural = "Household Survey Code"
