from edc_base.model.models import HistoricalRecords
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_offstudy.model_mixins import OffStudyMixin


class SubjectOffStudy(OffStudyMixin, BaseUuidModel):

    """A model completed by the user that completed when the subject is taken off-study."""

    history = HistoricalRecords()

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Subject Off Study"
        verbose_name_plural = "Subject Off Study"
