import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import HivResultDocumentation


class HivResultDocumentationFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HivResultDocumentation

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    result_date = date.today()
    result_recorded = (('HIV-Negative', 'HIV Negative (Non-reactive)'), ('HIV-Positive', 'HIV Positive (Reactive)'), ('Indeterminate', 'Indeterminate'), ('No result recorded', 'No result recorded'))[0][0]
    result_doc_type = (('Tebelopele', 'Tebelopele'), ('Lab result form', 'Lab result form'), ('ART Prescription', 'ART Prescription'), ('PMTCT Prescription', 'PMTCT Prescription'), ('Record of CD4 count', 'Record of CD4 count'), ('OTHER', 'Other OPD card or ANC card documentation'))[0][0]
