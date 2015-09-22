import factory
from datetime import date, datetime
from ...models import ThirdPartner


class ThirdPartnerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ThirdPartner

    report_datetime = datetime.today()
    rel_type = (('Longterm partner', u'Longterm partner (>2 years) or spouse'), ('Boyfriend/Girlfriend', u'Boyfriend/Girlfriend'), ('Casual', u'Casual (known) partner'), ('One time partner', u'One time partner (previously unknown)'), ('Commercial sex worker', u'Commercial sex worker'), ('Other, specify', u'Other, specify'))[0][0]
    rel_type_other = factory.Sequence(lambda n: 'rel_type_other{0}'.format(n))
    partner_residency = (('In this community', u'In this community'), ('On farm/cattle post', u'On farm/cattle post'), ('Outside this community', u'Outside this community'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    partner_age = 2
    partner_gender = (('M', '<django.utils.functional.__proxy__ object at 0x1021b8590>'), ('F', '<django.utils.functional.__proxy__ object at 0x1021b85d0>'))[0][0]
    last_sex_contact = 2
    last_sex_contact_other = factory.Sequence(lambda n: 'last_sex_contact_other{0}'.format(n))
    first_sex_contact = 2
    first_sex_contact_other = factory.Sequence(lambda n: 'first_sex_contact_other{0}'.format(n))
    regular_sex = 2
    having_sex_reg = (('All of the time', u'All of the time'), ('Sometimes', u'Sometimes'), ('Never', u'Never'))[0][0]
    alcohol_before_sex = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8890>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b88d0>'), ('REF', '<django.utils.functional.__proxy__ object at 0x1021b8910>'))[0][0]
    partner_status = (('POS', '<django.utils.functional.__proxy__ object at 0x1021b8750>'), ('NEG', '<django.utils.functional.__proxy__ object at 0x1021b8790>'), ('UNKNOWN', '<django.utils.functional.__proxy__ object at 0x1021b87d0>'))[0][0]
