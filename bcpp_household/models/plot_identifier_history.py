from edc_identifier.models import BaseIdentifierModel
from edc_base.model.models.base_uuid_model import BaseUuidModel


class PlotIdentifierHistory(BaseIdentifierModel, BaseUuidModel):
    """A system model to track allocated plot identifiers."""

    def ignore_for_dispatch(self):
        return True

    class Meta:
        app_label = "bcpp_household"
