import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Education


class EducationFactory(BaseUuidModelFactory):
    FACTORY_FOR = Education

    report_datetime = datetime.today()
    education = (('None', u'None'), ('Non formal', u'Non formal'), ('Primary', u'Primary'), ('Junior Secondary', u'Junior Secondary'), ('Senior Secondary', u'Senior Secondary'), ('Higher than senior secondary (university, diploma, etc.)', u'Higher than senior secondary (university, diploma, etc.)'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    working = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48e50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48ed0>))[0][0]
    job_type = (('piece job', u'Occassional or Casual employment (piece job)'), ('seasonal', u'Seasonal employment'), ('full-time', u'Formal wage employment (full-time)'), ('part-time', u'Formal wage employment (part-time)'), ('agric', u'Self-employed in agriculture'), ('self full-time', u'Self-employed making money, full time'), ('self part-time', u'Self-employed making money, part time'), ('OTHER', u'Other'))[0][0]
    job_description = (('farmer', u'Farmer (own land)'), ('farm work', u'Farm work on employers land'), ('domestic', u'Domestic worker'), ('bar/hotel', u'Work in bar/ hotel/ guest house'), ('fishing', u'Fishing'), ('mining', u'Mining'), ('shop', u'Working in shop'), ('selling', u'Informal selling'), ('sexworker', u'Commercial sex work'), ('transport', u'Transport (trucker/ taxi driver)'), ('factory', u'Factory worker'), ('guard', u'Guard (security company)'), ('police', u'Police/ Soldier'), ('office', u'Clerical and office work'), ('govt worker', u'Government worker'), ('teacher', u'Teacher'), ('hcw', u'Health care worker'), ('Other', u'Other professional'), ('OTHER', u'Other'))[0][0]
    monthly_income = (('None', u'None'), ('1-199 pula', u'1-199 pula'), ('200-499 pula', u'200-499 pula'), ('500-999 pula', u'500-999 pula'), ('1000-4999 pula', u'1000-4999 pula'), ('5000-10,000 pula', u'5000-10,000 pula'), ('More than 10,000 pula', u'More than 10,000 pula'), ("Don't want to answer", u"Don't want to answer"))[0][0]
