import factory

from datetime import datetime

from ...models import HivHealthCareCosts


class HivHealthCareCostsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivHealthCareCosts

    report_datetime = datetime.today()
    hiv_medical_care = (('Yes', u'Yes'), ('No', u'No'), ('Refuse', u'Refused to answer'))[0][0]
    place_care_received = (('Government dispensary', u'Government dispensary'), ('Government health center', u'Government health center'), ('Government hospital', u'Government hospital'), ('Christian/mission health center', u'Christian/mission health center'), ('Islamic health center', u'Islamic health center'), ('Private health center for all illnesses', u'Private health center for all illnesses'), ('Private health center for HIV/AIDS', u'Private health center for HIV/AIDS'), ('Mobile services', u'Mobile services'), ('Plantation health center', u'Plantation health center'), ('NGO clinic', u'NGO clinic'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    care_regularity = (('0 times', u'0 times'), ('1 time', u'1 time'), ('2 times', u'2 times'), ('3 times', u'3 times'), ('4 times', u'4 times'), ('5 times', u'5 times'), ('6-10 times', u'6-10 times'), ('More than 10 times', u'More than 10 times'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    doctor_visits = (('always', u'All of the time (always)'), ('almost always', u'Most of the time (almost always)'), ('sometimes', u'Some of the time (sometimes)'), ('rarely', u'Almost none of the time (rarely)'), ('never', u'None of the time (never)'), ("Don't want to answer", u"Don't want to answer"))[0][0]
