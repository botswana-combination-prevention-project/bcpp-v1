import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivResultDocumentation


class HivResultDocumentationFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivResultDocumentation

    report_datetime = datetime.today()
    result_date = date.today()
    result_recorded = (('POS', <django.utils.functional.__proxy__ object at 0x103aea910>), ('NEG', <django.utils.functional.__proxy__ object at 0x103aea990>), ('IND', <django.utils.functional.__proxy__ object at 0x103aeaa10>), ('No result recorded', <django.utils.functional.__proxy__ object at 0x103aeaa90>))[0][0]
    result_doc_type = (('Tebelopele', <django.utils.functional.__proxy__ object at 0x103a20850>), ('Lab result form', <django.utils.functional.__proxy__ object at 0x103a208d0>), ('ART Prescription', <django.utils.functional.__proxy__ object at 0x103a20950>), ('PMTCT Prescription', <django.utils.functional.__proxy__ object at 0x103a209d0>), ('Record of CD4 count', <django.utils.functional.__proxy__ object at 0x103a20a50>), ('OTHER', <django.utils.functional.__proxy__ object at 0x103a20ad0>))[0][0]
