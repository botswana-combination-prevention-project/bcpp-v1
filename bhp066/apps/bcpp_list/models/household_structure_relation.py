from edc_base.model.models import BaseListModel


class HouseholdStructureRelation(BaseListModel):

    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Household Structure Relation"
        ordering = ["name"]
