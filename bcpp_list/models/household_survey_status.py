from edc_base.model.models import ListModelMixin


class HouseholdSurveyStatus(ListModelMixin):

    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Household Survey Status"
        verbose_name_plural = "Household Survey Status"
