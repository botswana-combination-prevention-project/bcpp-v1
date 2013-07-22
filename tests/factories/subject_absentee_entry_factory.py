import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SubjectAbsenteeEntry
from bcpp_subject.tests.factories import SubjectAbsenteeFactory


class SubjectAbsenteeEntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectAbsenteeEntry

    report_datetime = datetime.today()
    reason_other = factory.Sequence(lambda n: 'reason_other{0}'.format(n))
    next_appt_datetime = datetime.today()
    next_appt_datetime_source = (('participant', <django.utils.functional.__proxy__ object at 0x103a23a50>), ('household member', <django.utils.functional.__proxy__ object at 0x103a23ad0>), ('hbc', <django.utils.functional.__proxy__ object at 0x103a23b50>), ('other', <django.utils.functional.__proxy__ object at 0x103a23bd0>))[0][0]
    subject_absentee = factory.SubFactory(SubjectAbsenteeFactory)
    reason = (('gone visiting (relatives,holidays,weddings,funerals)', <django.utils.functional.__proxy__ object at 0x103a25110>), ('stays at lands or cattlepost ', <django.utils.functional.__proxy__ object at 0x103a25190>), ('stepped out(shops, errands etc) ', <django.utils.functional.__proxy__ object at 0x103a25210>), ('works in village and comes home daily', <django.utils.functional.__proxy__ object at 0x103a25290>), ('goes to school in village and comes home daily', <django.utils.functional.__proxy__ object at 0x103a25310>), ('works outside village and comes home daily', <django.utils.functional.__proxy__ object at 0x103a25390>), ('goes to school outside village and comes home daily', <django.utils.functional.__proxy__ object at 0x103a25410>), ('works outside village and comes home irregularly ', <django.utils.functional.__proxy__ object at 0x103a25490>), ('goes to school outside village and comes home irregularly ', <django.utils.functional.__proxy__ object at 0x103a25510>), ('works outside village and comes home monthly ', <django.utils.functional.__proxy__ object at 0x103a25590>), ('goes to school outside village and comes home monthly ', <django.utils.functional.__proxy__ object at 0x103a25610>), ('works outside village and comes home on weekends ', <django.utils.functional.__proxy__ object at 0x103a25690>), ('goes to school outside village and comes home on weekends ', <django.utils.functional.__proxy__ object at 0x103a25710>), ('OTHER', <django.utils.functional.__proxy__ object at 0x103a25790>))[0][0]
