from lab_import.models import BaseImportHistory


class ImportHistoryModel(BaseImportHistory):

    class Meta:
        app_label = 'lab_clinic_api'
