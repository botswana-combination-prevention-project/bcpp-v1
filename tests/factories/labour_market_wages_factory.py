import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import LabourMarketWages


class LabourMarketWagesFactory(BaseUuidModelFactory):
    FACTORY_FOR = LabourMarketWages

    report_datetime = datetime.today()
    employed = (('government sector', u'Yes, In the government sector'), ('private sector', u'Yes, in the private sector'), ('self-employed working on my own', u'Yes, self-employed working on my own'), ('self-employed with own employees', u'Yes, self-employed with own employees'), ('not working', u'No, not working'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    occupation_other = factory.Sequence(lambda n: 'occupation_other{0}'.format(n))
    household_income = (('None', u'None'), ('1-200 pula', u'1-200 pula'), ('200-499 pula', u'200-499 pula'), ('500-999 pula', u'500-999 pula'), ('1000-4999 pula', u'1000-4999 pula'), ('5000-10,000 pula', u'5000-10,000 pula'), ('10,0000-20,000 pula', u'10,0000-20,000 pula'), ('More than 20,000 pula', u'More than 20,000 pula'), ('I am not sure', u'I am not sure'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    other_occupation = (('Studying', u'Studying'), ('Doing housework', u'Doing housework'), ('Looking for work', u'Looking for work'), ('Doing nothing (not looking for paid work)', u'Doing nothing (not looking for paid work)'), ('Retired/old age', u'Retired/old age'), ('Pregnant or recently pregnant', u'Pregnant or recently pregnant'), ('Sick or injured', u'Sick or injured'), ('OTHER', u'Other, specify:'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    other_occupation_other = factory.Sequence(lambda n: 'other_occupation_other{0}'.format(n))
    govt_grant = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48f50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48fd0>), ('REF', <django.utils.functional.__proxy__ object at 0x101d52090>))[0][0]
    weeks_out = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48f50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48fd0>), ('REF', <django.utils.functional.__proxy__ object at 0x101d52090>))[0][0]
