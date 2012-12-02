from lab_clinic_api.models import TestCode, TestCodeGroup, Panel, AliquotType


class ConvertLisAttr(object):

    def test_code(self, lis_test_code):
        """ Converts a test_code instance from lab_test_code to an instance from lab_clinic_api.

        If lab_clinic_api instance does not exist it will be created."""

        test_code, created = TestCode.objects.get_or_create(code=lis_test_code.code)
        for fld in test_code._meta.fields:
            if fld.name in [fl.name for fl in lis_test_code._meta.fields if fl.name not in ['id', 'code', 'test_code_group']]:
                setattr(test_code, fld.name, getattr(lis_test_code, fld.name))
            if fld.name == 'test_code_group':
                test_code_group, x = TestCodeGroup.objects.get_or_create(code=lis_test_code.test_code_group.code, name=lis_test_code.test_code_group.name)
                setattr(test_code, fld.name, test_code_group)
        test_code.save()
        return test_code, created

    def panel(self, lis_panel):
        panel, created = Panel.objects.get_or_create(name=lis_panel.name)
        for field in panel._meta.fields:
            if field.name in [fld.name for fld in lis_panel._meta.fields if fld.name not in ['id', 'test_code']]:
                setattr(panel, field.name, getattr(lis_panel, field.name))
        for field in panel._meta.many_to_many:
            if issubclass(field.rel.to, TestCode):
                getattr(panel, field.name).clear()
                for lis_code in getattr(lis_panel, field.name).all():
                    test_code, x = self.test_code(lis_code)
                    getattr(panel, field.name).add(test_code)
            if issubclass(field.rel.to, AliquotType):
                getattr(panel, field.name).clear()
                for lis_code in getattr(lis_panel, field.name).all():
                    aliquot_type, x = self.aliquot_type(lis_code)
                    getattr(panel, field.name).add(aliquot_type)
        panel.save()
        return panel, created
