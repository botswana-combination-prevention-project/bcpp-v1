from edc.core.identifier.models import BaseIdentifierModel
from edc_sync.model_mixins import SyncModelMixin
from edc_base.model.models import BaseUuidModel


class OrderIdentifierHistory(BaseIdentifierModel, SyncModelMixin, BaseUuidModel):

    def ignore_for_dispatch(self):
        return True

    class Meta:
        app_label = "bcpp_lab"
