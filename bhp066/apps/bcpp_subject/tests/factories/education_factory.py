import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Education


class EducationFactory(BaseUuidModelFactory):
    FACTORY_FOR = Education

    report_datetime = datetime.today()
    education = (('None', u'None'), ('Non formal', u'Non formal'), ('Primary', u'Primary'), ('Junior Secondary', u'Junior Secondary'), ('Senior Secondary', u'Senior Secondary'), ('Higher than senior secondary (university, diploma, etc.)', u'Higher than senior secondary (university, diploma, etc.)'), ('not_answering', u"Don't want to answer"))[0][0]
    working = (('Yes', u'Yes'), ('No', u'No'))[0][0]
