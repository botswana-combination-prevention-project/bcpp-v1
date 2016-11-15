from edc_base.model.models import HistoricalRecords

from .crf_model_mixin import CrfModelMixin
from .detailed_sexual_history import DetailedSexualHistory


class MostRecentPartner (DetailedSexualHistory, CrfModelMixin):

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Most Recent Partner"
        verbose_name_plural = "CS003: Most Recent Partner"
