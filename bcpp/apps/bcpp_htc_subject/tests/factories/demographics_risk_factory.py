import factory
from datetime import datetime

from ...models import DemographicsRisk

from .htc_subject_visit_factory import HtcSubjectVisitFactory


class DemographicsRiskFactory(factory.DjangoModelFactory):
    FACTORY_FOR = DemographicsRisk

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    education = (('None', u'None'), ('non_formal', u'Non Formal'), ('primary', u'Primary'), ('secondary', u'Secondary '), ('tertiary', u'Tertiary (Higher than secondary, such as vocational college or university)'))[0][0]
    employment = (('full_time', u'Full-time employed'), ('part_time', u'Part-time employed'), ('seasonal', u'Seasonal or intermittent employment'), ('informal', u'Informal self-employment'), ('student', u'Student'), ('retired', u'Retired'), ('not_woking', u'Not working (non-student, not retired)'), ('not_answering', u"Don't want to answer"))[0][0]
    marital_status = 2
    alcohol_intake = (('NEVER', u'Never'), ('monthly', u'Monthly or less'), ('per_month', u'2-4 times per month'), ('per_week', u'2-3 times per week'), ('more_times', u'4 or more times per week'))[0][0]
