from datetime import datetime

from ...models import Circumcision

from ..factories import BaseScheduledModelFactory


class CircumcisionFactory(BaseScheduledModelFactory):
    FACTORY_FOR = Circumcision

    report_datetime = datetime.today()
    circumcised = (('Yes', u'Yes'), ('No', u'No'), ('not_sure', u'I am not sure'), ('not_answering', u"Don't want to answer"))[0][0]
