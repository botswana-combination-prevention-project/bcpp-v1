import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Education


class EducationFactory(BaseUuidModelFactory):
    FACTORY_FOR = Education

    report_datetime = datetime.today()
    education = (('None', 'None'), ('Non formal', 'Non formal'), ('Primary', 'Primary'), ('Junior Secondary', 'Junior Secondary'), ('Senior Secondary', 'Senior Secondary'), ('Higher than senior secondary (university, diploma, etc.)', 'Higher than senior secondary (university, diploma, etc.)'), ("Don't want to answer", "Don't want to answer"))[0][0]
    working = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    job_type = (('piece job', 'Occassional or Casual employment (piece job)'), ('seasonal', 'Seasonal employment'), ('full-time', 'Formal wage employment (full-time)'), ('part-time', 'Formal wage employment (part-time)'), ('agric', 'Self-employed in agriculture'), ('self full-time', 'Self-employed making money, full time'), ('self part-time', 'Self-employed making money, part time'), ('OTHER', 'Other'))[0][0]
    job_description = (('farmer', 'Farmer (own land)'), ('farm work', 'Farm work on employers land'), ('domestic', 'Domestic worker'), ('bar/hotel', 'Work in bar/ hotel/ guest house'), ('fishing', 'Fishing'), ('mining', 'Mining'), ('shop', 'Working in shop'), ('selling', 'Informal selling'), ('sexworker', 'Commercial sex work'), ('transport', 'Transport (trucker/ taxi driver)'), ('factory', 'Factory worker'), ('guard', 'Guard (security company)'), ('police', 'Police/ Soldier'), ('office', 'Clerical and office work'), ('govt worker', 'Government worker'), ('teacher', 'Teacher'), ('hcw', 'Health care worker'), ('Other', 'Other professional'), ('OTHER', 'Other'))[0][0]
    monthly_income = (('None', 'None'), ('1-199 pula', '1-199 pula'), ('200-499 pula', '200-499 pula'), ('500-999 pula', '500-999 pula'), ('1000-4999 pula', '1000-4999 pula'), ('5000-10,000 pula', '5000-10,000 pula'), ('More than 10,000 pula', 'More than 10,000 pula'), ("Don't want to answer", "Don't want to answer"))[0][0]
