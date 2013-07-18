import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivResultDocumentation


class HivResultDocumentationFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivResultDocumentation

    report_datetime = datetime.today()
    result_date = date.today()
    result_recorded = (('POS', 'HIV Positive (Reactive)'), ('NEG', 'HIV Negative (Non-reactive)'), ('IND', 'Indeterminate'), ('No result recorded', 'No result recorded'))[0][0]
    result_doc_type = (('Tebelopele', 'Tebelopele'), ('Lab result form', 'Lab result form'), ('ART Prescription', 'ART Prescription'), ('PMTCT Prescription', 'PMTCT Prescription'), ('Record of CD4 count', 'Record of CD4 count'), ('OTHER', 'Other OPD card or ANC card documentation'))[0][0]
