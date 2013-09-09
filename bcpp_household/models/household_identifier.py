from bhp_identifier.models import BaseIdentifierModel


class HouseholdIdentifier(BaseIdentifierModel):

    def ignore_for_dispatch(self):
        return True

    class Meta:
        app_label = "bcpp_household"
