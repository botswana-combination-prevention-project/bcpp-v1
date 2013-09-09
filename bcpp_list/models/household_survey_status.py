from bhp_base_model.models import BaseListModel


class HouseholdSurveyStatus(BaseListModel):
    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Household Survey Status"
        verbose_name_plural = "Household Survey Status"
