from edc.core.identifier.models import BaseIdentifierModel
from edc.device.sync.models import BaseSyncUuidModel


class OrderIdentifierHistory(BaseIdentifierModel, BaseSyncUuidModel):

    def ignore_for_dispatch(self):
        return True

    class Meta:
        app_label = "bcpp_lab"
