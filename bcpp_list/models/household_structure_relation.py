from bhp_base_model.models import BaseListModel


class HouseholdStructureRelation(BaseListModel):

    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Household Structure Relation"
        ordering = ["name"]
