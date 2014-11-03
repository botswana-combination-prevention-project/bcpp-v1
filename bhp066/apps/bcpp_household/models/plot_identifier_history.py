from edc.core.identifier.models import BaseIdentifierModel


class PlotIdentifierHistory(BaseIdentifierModel):
    """A system model to track allocated plot identifiers."""

    def ignore_for_dispatch(self):
        return True

    class Meta:
        app_label = "bcpp_household"
