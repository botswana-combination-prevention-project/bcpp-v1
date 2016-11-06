from edc_base.model.models import ListModelMixin


class SurveyGroup(ListModelMixin):

    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Survey Group"
        verbose_name_plural = "Survey Group"
