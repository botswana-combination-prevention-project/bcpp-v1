import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SubjectUndecidedEntry
from bcpp_subject.tests.factories import SubjectUndecidedFactory


class SubjectUndecidedEntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectUndecidedEntry

    report_datetime = datetime.today()
    reason_other = factory.Sequence(lambda n: 'reason_other{0}'.format(n))
    next_appt_datetime = datetime.today()
    next_appt_datetime_source = (('participant', <django.utils.functional.__proxy__ object at 0x103a23a50>), ('household member', <django.utils.functional.__proxy__ object at 0x103a23ad0>), ('hbc', <django.utils.functional.__proxy__ object at 0x103a23b50>), ('other', <django.utils.functional.__proxy__ object at 0x103a23bd0>))[0][0]
    subject_undecided = factory.SubFactory(SubjectUndecidedFactory)
    subject_undecided_reason = (('afraid_to_test', <django.utils.functional.__proxy__ object at 0x103a25810>), ('not ready to test', <django.utils.functional.__proxy__ object at 0x103a25890>), ('wishes to test with partner', <django.utils.functional.__proxy__ object at 0x103a25910>), ('OTHER', <django.utils.functional.__proxy__ object at 0x103a25990>))[0][0]
