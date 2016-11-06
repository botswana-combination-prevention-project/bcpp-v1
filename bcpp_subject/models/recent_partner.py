from simple_history.models import HistoricalRecords

from .detailed_sexual_history import DetailedSexualHistory


class RecentPartner (DetailedSexualHistory):

    history = HistoricalRecords()

    class Meta(DetailedSexualHistory.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Most Recent Partner"
        verbose_name_plural = "CS003: Most Recent Partner"
