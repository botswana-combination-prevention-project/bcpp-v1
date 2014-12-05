import os
import csv

from django.core.management.base import BaseCommand, CommandError

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_subject.models.subject_consent import SubjectConsent


class Command(BaseCommand):

    args = 'community'
    help = 'Export subject_identifier, community, ... as a csv file in your home folder'

    def handle(self, *args, **options):
        try:
            community = args[0]
        except IndexError:
            raise CommandError('Expected at least one parameter for community')
        n = 0
        filename = os.path.expanduser('~/subject_identifier_{}.csv')
        with open(filename.format(community), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['subject_identifier', 'community', 'subject_identifier_aka', 'dm_reference'])
            for hm in HouseholdMember.objects.filter(
                    household_structure__survey__survey_slug='bcpp-year-1',
                    registered_subject__subject_identifier__startswith='066',
                    household_structure__household__plot__community=community,
                    ).order_by('registered_subject__subject_identifier'):
                n += 1
                try:
                    # hm.registered_subject attributes should equal subject_consent
                    SubjectConsent.objects.get(
                        household_member=hm,
                        subject_identifier=hm.registered_subject.subject_identifier,
                        subject_identifier_aka=hm.registered_subject.subject_identifier_aka,
                        )
                except SubjectConsent.DoesNotExist:
                    raise CommandError('Inconsistent identifiers between SubjectConsent and '
                                       'RegisteredSubject. Got {}.'.format(hm.registered_subject))
                writer.writerow(
                    [hm.registered_subject.subject_identifier,
                     hm.household_structure.household.plot.community,
                     hm.registered_subject.subject_identifier_aka,
                     hm.registered_subject.dm_reference]
                    )
        print 'Exported {} identifiers to {}'.format(n, filename)
