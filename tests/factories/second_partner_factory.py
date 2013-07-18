import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SecondPartner


class SecondPartnerFactory(BaseUuidModelFactory):
    FACTORY_FOR = SecondPartner

    report_datetime = datetime.today()
    rel_type = (('Longterm partner', 'Longterm partner (>2 years) or spouse'), ('Boyfriend/Girlfriend', 'Boyfriend/Girlfriend'), ('Casual', 'Casual (known) partner'), ('One time partner', 'One time partner (previously unknown)'), ('Commercial sex worker', 'Commercial sex worker'), ('Other, specify', 'Other, specify'))[0][0]
    rel_type_other = factory.Sequence(lambda n: 'rel_type_other{0}'.format(n))
    partner_residency = (('In this community', 'In this community'), ('On farm/cattle post', 'On farm/cattle post'), ('Outside this community', 'Outside this community'), ("Don't want to answer", "Don't want to answer"))[0][0]
    partner_age = 2
    partner_gender = (('M', 'Male'), ('F', 'Female'))[0][0]
    last_sex_contact = 2
    last_sex_contact_other = factory.Sequence(lambda n: 'last_sex_contact_other{0}'.format(n))
    first_sex_contact = 2
    first_sex_contact_other = factory.Sequence(lambda n: 'first_sex_contact_other{0}'.format(n))
    regular_sex = 2
    having_sex_reg = (('All of the time', 'All of the time'), ('Sometimes', 'Sometimes'), ('Never', 'Never'))[0][0]
    alcohol_before_sex = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    partner_status = (('POS', 'Positive'), ('NEG', 'Negative'), ('UNKNOWN', 'Unknown'))[0][0]
