import factory
from datetime import date, datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import HtcHivResult

from .htc_subject_visit_factory import HtcSubjectVisitFactory


class HtcHivResultFactory(BaseUuidModelFactory):
    FACTORY_FOR = HtcHivResult

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    todays_result = (('POS', 'Positive'), ('NEG', 'Negative'), ('IND', 'Indeterminate'))[0][0]
    couples_testing = 'No'
    symptoms = (('cough', u'Cough > 2 weeks'), ('fever', u'Fever > 2 weeks'), ('big_lymph', u'Enlarged lymph nodes'), ('cough_blood', u'Coughing up blood'), ('night_sweats', u'Night Sweats'), ('weight_loss', u'Unexplained weight loss'), ('none', u'None of the above symptoms reported'))[0][0]
    family_tb = (('Yes', 'Yes'), ('No', 'No'), ('Dont_know', 'Do not Know'))[0][0]
