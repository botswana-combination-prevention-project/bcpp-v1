import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Cancer


class CancerFactory(BaseUuidModelFactory):
    FACTORY_FOR = Cancer

    report_datetime = datetime.today()
    date_cancer = date.today()
    dx_cancer = (("Kaposi's sarcoma (KS)", <django.utils.functional.__proxy__ object at 0x103afa8d0>), ('Cervical cancer', <django.utils.functional.__proxy__ object at 0x103afa950>), ('Breast cancer', <django.utils.functional.__proxy__ object at 0x103afa9d0>), ("Non-Hodgkin's lymphoma (NHL)", <django.utils.functional.__proxy__ object at 0x103afaa50>), ('Colorectal cancer', <django.utils.functional.__proxy__ object at 0x103afaad0>), ('Prostate cancer', <django.utils.functional.__proxy__ object at 0x103afab50>), ('Cancer of mouth, throat, voice box (larynx)', <django.utils.functional.__proxy__ object at 0x103afabd0>), ('Cancer of oesophagus', <django.utils.functional.__proxy__ object at 0x103afac50>), ('Other', <django.utils.functional.__proxy__ object at 0x103afacd0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103afad50>))[0][0]
