from lab_import.models import BaseImportHistory


class DmisImportHistory(BaseImportHistory):

    class Meta:
        app_label = 'lab_import_dmis'
