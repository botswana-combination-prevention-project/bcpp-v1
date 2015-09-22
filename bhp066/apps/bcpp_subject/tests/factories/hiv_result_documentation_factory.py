import factory

from datetime import date, datetime

from ...models import HivResultDocumentation


class HivResultDocumentationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivResultDocumentation

    report_datetime = datetime.today()
    result_date = date.today()
    result_recorded = (('POS', u'HIV Positive (Reactive)'), ('NEG', u'HIV Negative (Non-reactive)'), ('IND', u'Indeterminate'), ('No result recorded', u'No result recorded'))[0][0]
    result_doc_type = (('Tebelopele', u'Tebelopele'), ('Lab result form', u'Lab result form'), ('ART Prescription', u'ART Prescription'), ('PMTCT Prescription', u'PMTCT Prescription'), ('Record of CD4 count', u'Record of CD4 count'), ('OTHER', u'Other OPD card or ANC card documentation'))[0][0]
