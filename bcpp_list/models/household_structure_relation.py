from edc_base.model.models import ListModelMixin


class HouseholdStructureRelation(ListModelMixin):

    class Meta:
        app_label = 'bcpp_list'
        verbose_name = "Household Structure Relation"
        ordering = ["name"]
