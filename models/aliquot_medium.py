from bhp_base_model.classes import BaseListModel


class AliquotMedium(BaseListModel):

    def __unicode__(self):
        return "%s" % ( self.name.upper())
    class Meta:
        ordering = ["name"]
        app_label = 'lab_aliquot_list'
        db_table = 'bhp_lab_core_aliquotmedium' 
