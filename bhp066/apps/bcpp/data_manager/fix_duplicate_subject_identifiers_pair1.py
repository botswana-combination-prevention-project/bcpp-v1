
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_subject.models import SubjectConsent


def fix_duplicate_subject_identifiers_pair1(run=False):
    """ Duplicate Subject Identifiers Between First 2 Community Pairs

    Overview
        On 24 June 2014 it was discovered that 22 subjects surveyed in Otse were allocated
        identifiers already in use from the previous BHS surveys conducted in Ranaka (12 subjects)
        and Digawana (10 subjects).

    ... see incident report for details."""

    # 40 identifiers to be replaced.
    # {duplicate: replacement}
#     new_identifiers = [
#         ('066-14120007-5', '066-1120007-5'),
#         ('066-14120008-6', '066-1120008-6'),
#         ('066-14120009-0', '066-1120009-0'),
#         ('066-14120010-1', '066-1120010-1'),
#         ('066-14160011-4', '066-1160011-4'),
#         ('066-14170008-5', '066-1170008-5'),
#         ('066-14170009-6', '066-1170009-6'),
#         ('066-14170010-0', '066-1170010-0'),
#         ('066-14170011-1', '066-1170011-1'),
#         ('066-14170012-2', '066-1170012-2'),
#         ('066-14180006-0', '066-1180006-0'),
#         ('066-14830011-6', '066-1130011-6'),
#         ('066-14830012-0', '066-1130012-0'),
#         ('066-14830013-1', '066-1130013-1'),
#         ('066-14830014-2', '066-1130014-2'),
#         ('066-14860014-0', '066-1160014-0'),
#         ('066-14860015-1', '066-1160015-1'),
#         ('066-14860016-2', '066-1160016-2'),
#         ('066-14860017-3', '066-1160017-3'),
#         ('066-14860018-4', '066-1160018-4'),
#         ('066-14860019-5', '066-1160019-5'),
#         ('066-14860020-6', '066-1160020-6'),
#         ('066-14860021-0', '066-1160021-0'),
#         ('066-14860022-1', '066-1160022-1'),
#         ('066-14860023-2', '066-1160023-2'),
#         ('066-14890013-4', '066-1190013-4'),
#         ('066-14890014-5', '066-1190014-5'),
#         ('066-14210017-2', '066-1210017-2'),
#         ('066-14210018-3', '066-1210018-3'),
#         ('066-14210019-4', '066-1210019-4'),
#         ('066-14210020-5', '066-1210020-5'),
#         ('066-14210021-6', '066-1210021-6'),
#         ('066-14210022-0', '066-1210022-0'),
#         ('066-14210023-1', '066-1210023-1'),
#         ('066-14210024-2', '066-1210024-2'),
#         ('066-14210025-3', '066-1210025-3'),
#         ('066-14210026-4', '066-1210026-4'),
#         ('066-14230012-5', '066-1230012-5'),
#         ('066-14300009-2', '066-1200009-2'),
#         ('066-14300010-3', '066-1200010-3')]

    # convert to dictionary
    # duplicates = {item[0]: item[1] for item in new_identifiers}

    new_identifiers = [
        ('066-14120007-5', '066-1120007-5', '066-11120007-5'),
        ('066-14120008-6', '066-1120008-6', '066-11120008-6'),
        ('066-14120009-0', '066-1120009-0', '066-11120009-0'),
        ('066-14120010-1', '066-1120010-1', '066-11120010-1'),
        ('066-14160011-4', '066-1160011-4', '066-11160011-4'),
        ('066-14170008-5', '066-1170008-5', '066-11170008-5'),
        ('066-14170009-6', '066-1170009-6', '066-11170009-6'),
        ('066-14170010-0', '066-1170010-0', '066-11170010-0'),
        ('066-14170011-1', '066-1170011-1', '066-11170011-1'),
        ('066-14170012-2', '066-1170012-2', '066-11170012-2'),
        ('066-14180006-0', '066-1180006-0', '066-11180006-0'),
        ('066-14830011-6', '066-1130011-6', '066-11830011-6'),
        ('066-14830012-0', '066-1130012-0', '066-11830012-0'),
        ('066-14830013-1', '066-1130013-1', '066-11830013-1'),
        ('066-14830014-2', '066-1130014-2', '066-11830014-2'),
        ('066-14860014-0', '066-1160014-0', '066-11860014-0'),
        ('066-14860015-1', '066-1160015-1', '066-11860015-1'),
        ('066-14860016-2', '066-1160016-2', '066-11860016-2'),
        ('066-14860017-3', '066-1160017-3', '066-11860017-3'),
        ('066-14860018-4', '066-1160018-4', '066-11860018-4'),
        ('066-14860019-5', '066-1160019-5', '066-11860019-5'),
        ('066-14860020-6', '066-1160020-6', '066-11860020-6'),
        ('066-14860021-0', '066-1160021-0', '066-11860021-0'),
        ('066-14860022-1', '066-1160022-1', '066-11860022-1'),
        ('066-14860023-2', '066-1160023-2', '066-11860023-2'),
        ('066-14890013-4', '066-1190013-4', '066-11890013-4'),
        ('066-14890014-5', '066-1190014-5', '066-11890014-5'),
        ('066-14210017-2', '066-1210017-2', '066-12210017-2'),
        ('066-14210018-3', '066-1210018-3', '066-12210018-3'),
        ('066-14210019-4', '066-1210019-4', '066-12210019-4'),
        ('066-14210020-5', '066-1210020-5', '066-12210020-5'),
        ('066-14210021-6', '066-1210021-6', '066-12210021-6'),
        ('066-14210022-0', '066-1210022-0', '066-12210022-0'),
        ('066-14210023-1', '066-1210023-1', '066-12210023-1'),
        ('066-14210024-2', '066-1210024-2', '066-12210024-2'),
        ('066-14210025-3', '066-1210025-3', '066-12210025-3'),
        ('066-14210026-4', '066-1210026-4', '066-12210026-4'),
        ('066-14230012-5', '066-1230012-5', '066-12230012-5'),
        ('066-14300009-2', '066-1200009-2', '066-12300009-2'),
        ('066-14300010-3', '066-1200010-3', '066-12300010-3'),
        ]

    # convert to dictionary
    duplicates = {item[1]: (item[2], item[0]) for item in new_identifiers}

    # fix 40 instances in RegisteredSubject
    n = 0
    for registered_subject in RegisteredSubject.objects.all():
        if registered_subject.subject_identifier in duplicates.keys():
            n += 1
            registered_subject.subject_identifier_aka = duplicates[registered_subject.subject_identifier][1]
            registered_subject.subject_identifier = duplicates[registered_subject.subject_identifier][0]
            print '{} has replaced {}'.format(registered_subject.subject_identifier, registered_subject.subject_identifier_aka)
            if run:
                registered_subject.save_base(raw=True, update_fields=['subject_identifier', 'subject_identifier_aka'])

    # fix 40 instances in SubjectConsent
    m = 0
    for subject_consent in SubjectConsent.objects.all():
        if subject_consent.subject_identifier in duplicates.keys():
            m += 1
            subject_consent.subject_identifier_aka = duplicates[subject_consent.subject_identifier][1]
            subject_consent.subject_identifier = duplicates[subject_consent.subject_identifier][0]
            print '{} has replaced {}'.format(subject_consent.subject_identifier, subject_consent.subject_identifier_aka)
            if run:
                subject_consent.save_base(raw=True, update_fields=['subject_identifier', 'subject_identifier_aka'])

    print 'Done. Replaced {} subject_identifiers in RegisteredSubject and {} in SubjectConsent.'.format(n, m)


#     # fix 40 instances in RegisteredSubject
#     n = 0
#     for registered_subject in RegisteredSubject.objects.all():
#         if registered_subject.subject_identifier in duplicates.keys():
#             n += 1
#             registered_subject.subject_identifier_aka = registered_subject.subject_identifier
#             registered_subject.subject_identifier = duplicates[registered_subject.subject_identifier]
#             print '{} has replaced {}'.format(registered_subject.subject_identifier, registered_subject.subject_identifier_aka)
#             if run:
#                 registered_subject.save_base(raw=True, update_fields='subject_identifier', 'subject_identifier_aka')
# 
#     # fix 40 instances in SubjectConsent
#     m = 0
#     for subject_consent in SubjectConsent.objects.all():
#         if subject_consent.subject_identifier in duplicates.keys():
#             m += 1
#             subject_consent.subject_identifier_aka = subject_consent.subject_identifier
#             subject_consent.subject_identifier = duplicates[subject_consent.subject_identifier]
#             print '{} has replaced {}'.format(subject_consent.subject_identifier, subject_consent.subject_identifier_aka)
#             if run:
#                 subject_consent.save_base(raw=True, update_fields='subject_identifier', 'subject_identifier_aka')
# 
#     print 'Done. Replaced {} subject_identifiers in RegisteredSubject and {} in SubjectConsent.'.format(n, m)
