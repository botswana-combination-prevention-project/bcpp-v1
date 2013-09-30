import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ..models import HtcRecentPartner
from htc_subject_visit_factory import HtcSubjectVisitFactory


class HtcRecentPartnerFactory(BaseUuidModelFactory):
    FACTORY_FOR = HtcRecentPartner

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    partner_tested = (('Yes', u'Yes'), ('No', u'No'))[0][0]
    parter_status = (('positive', 'HIV Positive'), ('negative', 'HIV Negative'), ('not_sure', 'I am not sure'), ('declined', 'Decline to answer'))[0][0]
    partner_residency = (('Yes', u'Yes'), ('No', u'No'))[0][0]
    recent_partner_rel = (('spouse', 'Spouse (husband/wife)'), ('cohabiting', 'Cohabitating partner'), ('boy_girl_friend', 'Boyfriend/Girlfriend'), ('casual', 'Casual (known) sex partner'), ('partner_unknown', 'One time partner (previously unknown)'), ('sex_worker', 'Commercial sex worker'), ('OTHER', 'Other, specify'), ('declined', 'Decline to answer'))[0][0]
