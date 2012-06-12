from bhp_base_model.classes import BaseListModel


class SpecimenType (BaseListModel):
    pass
    
    class Meta:
        app_label = 'lab_aliquot'
        db_table = 'bhp_lab_core_specimentype'
