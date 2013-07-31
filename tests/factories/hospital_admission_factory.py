import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HospitalAdmission


class HospitalAdmissionFactory(BaseUuidModelFactory):
    FACTORY_FOR = HospitalAdmission

    report_datetime = datetime.today()
    reason_hospitalized = (('HIV-related care', u'HIV-related care, including TB and other opportunistic infections'), ('Pregnancy', u'Pregnancy-related care, including delivery'), ('Injuries', u'Injuries or accidents'), ('Chronic disease', u'Chronic disease related care, including high blood pressure, diabetes, cancer, mental illness'), ('Other', u'Other'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    facility_hospitalized = factory.Sequence(lambda n: 'facility_hospitalized{0}'.format(n))
    nights_hospitalized = 2
    healthcare_expense = 2.5
    travel_hours = (('Under 0.5 hour', u'Under 0.5 hour'), ('0.5 to under 1 hour', u'0.5 to under 1 hour'), ('1 to under 2 hours', u'1 to under 2 hours'), ('2 to under 3 hours', u'2 to under 3 hours'), ('More than 3 hours', u'More than 3 hours'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    hospitalization_costs = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48f50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48fd0>), ('REF', <django.utils.functional.__proxy__ object at 0x101d52090>))[0][0]
