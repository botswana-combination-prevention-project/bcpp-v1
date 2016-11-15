from edc_base.model.models import HistoricalRecords

from .detailed_sexual_history import DetailedSexualHistory


class ThirdPartner (DetailedSexualHistory):

    history = HistoricalRecords()

    class Meta(DetailedSexualHistory.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Third Partner"
        verbose_name_plural = "CS003: Third Partner"
