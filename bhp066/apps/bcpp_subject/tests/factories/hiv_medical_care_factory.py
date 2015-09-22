import factory

from datetime import date, datetime

from ...models import HivMedicalCare


class HivMedicalCareFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivMedicalCare

    report_datetime = datetime.today()
    first_hiv_care_pos = date.today()
    last_hiv_care_pos = date.today()
    lowest_cd4 = (('0-49', u'0-49'), ('50-99', u'50-99'), ('100-199', u'100-199'), ('200-349', u'200-349'), ('350-499', u'350-499'), ('500 or more', u'500 or more'), ('not_sure', u'I am not sure'), ('not_answering', u"Don't want to answer"))[0][0]
