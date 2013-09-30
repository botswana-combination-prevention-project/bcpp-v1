from edc.core.identifier.models import BaseIdentifierModel


class HouseholdIdentifierHistory(BaseIdentifierModel):

    def ignore_for_dispatch(self):
        return True

    class Meta:
        app_label = "bcpp_household"
