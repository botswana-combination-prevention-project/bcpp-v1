from bhp_common.models import MyBasicListModel


class ResultSource(MyBasicListModel):
    pass

    class Meta:
        app_label = 'bhp_lab_result' 
        db_table = 'bhp_lab_core_resultsource'



