import csv

from django.core.management.base import BaseCommand

from bhp066.apps.bcpp_subject.models import SubjectConsent


ECC_COMMUNITIES = [
    'bokaa',
    'letlhakeng',
    'mmandunyane',
    'mmathethe',
    'metsimotlhabe',
    'molapowabojang',
    'nata',
    'rakops',
    'ramokgonami',
    'ranaka',
    'sebina',
    'sefophe',
    'shakawe',
    'tsetsebjwe',
]


class Command(BaseCommand):

    args = ''
    help = 'Create a list of omang number for all ECC communities'

    def handle(self, *args, **options):
        self.omang_list()

    def omang_list(self):
        """Generate omang list of an ecc community."""
        omang_community_list = []
        all_communities_omang_file = open('all_communities_omang_numbers.csv', 'wb')
        for community in ECC_COMMUNITIES:
            community_omang_file = open(community + '_omang_numbers.csv', 'wb')
            omang_list = []
            print "Attending {0} omang numbers".format(community)
            consents = SubjectConsent.objects.filter(household_member__household_structure__household__plot__community=community)
            cosents_count = consents.count()
            print "There are {0} consents for {1} community".format(cosents_count, community)
            omang_total = 0
            for consent in consents:
                if consent.identity not in omang_list:
                    omang_list.append(consent.identity)
                    omang_community_list.append([consent.identity, community])
                    omang_total += 1
                    print "{0} omang numbers added out of {1} duplicates are ignored".format(omang_total, cosents_count)
                else:
                    print "{0} omang numbers added out of {1} duplicates are ignored".format(omang_total, cosents_count)
            print "Creating csv file for {0} community".format(community)
            community_csv = csv.writer(community_omang_file)
            community_csv.writerows(omang_list)
        print "Creating csv file for all community"
        all_communities = csv.writer(all_communities_omang_file)
        all_communities.writerows(omang_community_list)
