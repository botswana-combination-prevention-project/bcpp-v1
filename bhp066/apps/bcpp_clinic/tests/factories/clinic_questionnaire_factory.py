import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from .clinic_visit_factory import ClinicVisitFactory
from ...models import Questionnaire


class QuestionnaireFactory(BaseUuidModelFactory):
    FACTORY_FOR = Questionnaire

    clinic_visit = factory.SubFactory(ClinicVisitFactory)
    report_datetime = datetime.today()
    on_arv = (('Yes', 'Yes'), ('No', 'No'), ('DWTA', 'Don\'t want to answer'))[0][0]
    cd4_count = 500
