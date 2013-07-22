import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import RecentPartner


class RecentPartnerFactory(BaseUuidModelFactory):
    FACTORY_FOR = RecentPartner

    report_datetime = datetime.today()
    rel_type = (('Longterm partner', <django.utils.functional.__proxy__ object at 0x103a167d0>), ('Boyfriend/Girlfriend', <django.utils.functional.__proxy__ object at 0x103a16810>), ('Casual', <django.utils.functional.__proxy__ object at 0x103a16850>), ('One time partner', <django.utils.functional.__proxy__ object at 0x103a168d0>), ('Commercial sex worker', <django.utils.functional.__proxy__ object at 0x103a16950>), ('Other, specify', <django.utils.functional.__proxy__ object at 0x103a169d0>))[0][0]
    rel_type_other = factory.Sequence(lambda n: 'rel_type_other{0}'.format(n))
    partner_residency = (('In this community', <django.utils.functional.__proxy__ object at 0x103a16a50>), ('On farm/cattle post', <django.utils.functional.__proxy__ object at 0x103a16ad0>), ('Outside this community', <django.utils.functional.__proxy__ object at 0x103a16b50>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103a16bd0>))[0][0]
    partner_age = 2
    partner_gender = (('M', 'Male'), ('F', 'Female'))[0][0]
    last_sex_contact = 2
    last_sex_contact_other = factory.Sequence(lambda n: 'last_sex_contact_other{0}'.format(n))
    first_sex_contact = 2
    first_sex_contact_other = factory.Sequence(lambda n: 'first_sex_contact_other{0}'.format(n))
    regular_sex = 2
    having_sex_reg = (('All of the time', <django.utils.functional.__proxy__ object at 0x103a16c50>), ('Sometimes', <django.utils.functional.__proxy__ object at 0x103a16cd0>), ('Never', <django.utils.functional.__proxy__ object at 0x103a16d50>))[0][0]
    alcohol_before_sex = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    partner_status = (('POS', 'Positive'), ('NEG', 'Negative'), ('UNKNOWN', 'Unknown'))[0][0]
