from edc_core.bhp_export_data.actions import export_as_csv_action
from edc_core.bhp_base_admin.admin import BaseModelAdmin


class BaseHouseholdModelAdmin(BaseModelAdmin):

    actions = [export_as_csv_action("Export as csv",
        fields=[],
        exclude=['id', ],
        )]
