from edc.export.actions import export_as_csv_action
from edc.base.modeladmin.admin import BaseModelAdmin


class BaseHouseholdModelAdmin(BaseModelAdmin):

    actions = [export_as_csv_action(
        "Export as csv", fields=[], exclude=['id', ]
    )]
