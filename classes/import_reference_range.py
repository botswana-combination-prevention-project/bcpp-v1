from django.conf import settings
from lab_test_code.models import TestCodeReferenceList, TestCodeReferenceListItem
from lab_clinic_reference.models import ReferenceRangeList, ReferenceRangeListItem


class ImportReferenceRange(object):

    def __init__(self, db):
        self.db = db

    def import_list(self):

        for test_code_reference_list in TestCodeReferenceList.objects.using(self.db).filter(name=settings.REFERENCE_RANGE_LIST):
            reference_range_list, created = ReferenceRangeList.objects.get_or_create(name=settings.REFERENCE_RANGE_LIST)
            for field in reference_range_list._meta.fields:
                if field.name in [field.name for field in test_code_reference_list._meta.fields if field.name != 'id']:
                    setattr(reference_range_list, field.name, getattr(test_code_reference_list, field.name))
            reference_range_list.save()

            for test_code_reference_list_item in TestCodeReferenceListItem.objects.using(self.db).filter(test_code_reference_list=test_code_reference_list):
                reference_range_list_item, created = ReferenceRangeListItem.objects.get_or_create(reference_range_list=reference_range_list)
                for field in reference_range_list_item._meta.fields:
                    if field.name in [field.name for field in test_code_reference_list_item._meta.fields if field.name != 'id']:
                        setattr(reference_range_list_item, field.name, getattr(test_code_reference_list_item, field.name))
                reference_range_list.save()
