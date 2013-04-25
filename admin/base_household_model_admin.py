from bhp_export_data.actions import export_as_csv_action
from bhp_base_model.classes import BaseModelAdmin


class BaseHouseholdModelAdmin(BaseModelAdmin):

    actions = [export_as_csv_action("Export as csv",
        fields=[],
        exclude=['id', ],
        )]
