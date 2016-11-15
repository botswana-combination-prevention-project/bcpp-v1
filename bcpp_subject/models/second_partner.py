from edc_base.model.models import HistoricalRecords

from .detailed_sexual_history import DetailedSexualHistory


class SecondPartner (DetailedSexualHistory):

    history = HistoricalRecords()

    class Meta(DetailedSexualHistory.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Second Partner"
        verbose_name_plural = "CS003: Second Partner"
