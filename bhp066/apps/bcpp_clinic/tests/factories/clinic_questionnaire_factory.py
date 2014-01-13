import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import ClinicQuestionnaire


class ClinicQuestionnaireFactory(BaseUuidModelFactory):
    FACTORY_FOR = ClinicQuestionnaire

    report_datetime = datetime.today()
    on_arv = (('Yes', 'Yes'), ('No', 'No'), ('DWTA', 'Don\'t want to answer'))[0][0]
    cd4_count = factory.Sequence(lambda n: 'cd4_count{0}'.format(n))
