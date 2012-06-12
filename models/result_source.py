from bhp_base_model.classes import BaseListModel


class ResultSource(BaseListModel):
    pass

    class Meta:
        app_label = 'lab_result' 
        db_table = 'bhp_lab_core_resultsource'



