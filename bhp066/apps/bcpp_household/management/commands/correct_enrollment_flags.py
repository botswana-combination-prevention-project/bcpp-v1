from optparse import make_option

from django.conf import settings
from django.db.models import get_model
from django.core.management.base import BaseCommand, CommandError

from edc.map.classes import site_mappers


class Command(BaseCommand):
    """ Corrects all bhs related enrollment flags in household, household_structure and plot
    """
    args = ('--site_code')

    help = 'Corrects all bhs related enrollment flags in household, household_structure and plot for site_code x.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--site_code',
            dest='site_code',
            action='store_true',
            default=False,
            help=('Enter site_code')),
        )

    def handle(self, *args, **options):
        if len(args) == 1:
            pass
        else:
            raise CommandError('Command expecting One arguments, being --site_code <site_code>')
        print options
        if options['site_code']:
            self.correct_enrollment_flags(args[0])
        else:
            raise CommandError('Command expecting One arguments, being --site_code <site_code>')

    def correct_enrollment_flags(self, site_code):
        community = None
        SubjectConsent = get_model('bcpp_subject', 'SubjectConsent')
        HouseholdStructure = get_model('bcpp_household', 'HouseholdStructure')
        Household = get_model('bcpp_household', 'Household')
        Plot = get_model('bcpp_household', 'Plot')
        household_structure = []
        households = []
        plots = []
        print "======================================="
        print ".....Correcting for SITE_CODE={}".format(site_code)
        for key, value in site_mappers.registry.iteritems():
            if value.map_code == site_code:
                print ".....SITE_CODE={} represents {}".format(site_code, key.upper())
                community = key
        if not community:
            print ".....Could not find a corresponding community for SITE_CODE={}".format(site_code)
            print ".....Quitting Now"
            return
        consents = SubjectConsent.objects.filter(community=community)
        print ".....Found {} consents for community {}".format(consents.count(), community.upper())
        for consent in consents:
            if consent.household_member.household_structure.id not in household_structure:
                household_structure.append(consent.household_member.household_structure.id)
        not_enrolled_structures = HouseholdStructure.objects.filter(
            id__in=household_structure,
            household__replaced_by__isnull=True).exclude(enrolled=True)
        print "..... {}/{} household structures for community {} are not enrolled".format(
            not_enrolled_structures.count(),
            len(household_structure),
            community.upper())
        if not_enrolled_structures.count() > 0:
            print ".....Starting the correction for HouseholdStructure, setting enrolled=True"
        else:
            print ".....Nothing to correct for HouseholdStructure, moving on."
        count = 0
        for st in not_enrolled_structures:
            st.enrolled = True
            st.save()
            count += 1
            print "{}/{} {}".format(count, len(not_enrolled_structures), st)
        for consent in consents:
            if consent.household_member.household_structure.household.id not in households:
                households.append(consent.household_member.household_structure.household.id)
        not_enrolled_household = Household.objects.filter(
            id__in=households, replaced_by__isnull=True).exclude(enrolled=True)
        print "..... {}/{} households for community {} are not enrolled".format(not_enrolled_household.count(),
                                                                                len(households),
                                                                                community.upper())
        if not_enrolled_household.count() > 0:
            print ".....Starting the correction for Households, setting enrolled=True"
        else:
            print ".....Nothing to correct for Household, moving on."
        count = 0
        for hd in not_enrolled_household:
            hd.enrolled = True
            hd.save()
            count += 1
            print "{}/{} {}".format(count, len(not_enrolled_household), hd)
        for consent in consents:
            if consent.household_member.household_structure.household.plot.id not in plots:
                plots.append(consent.household_member.household_structure.household.plot.id)
        not_enrolled_plot = Plot.objects.filter(id__in=plots, replaced_by__isnull=True).exclude(bhs=True)
        print "..... {}/{} plots for community {} are not enrolled".format(not_enrolled_plot.count(),
                                                                           len(plots),
                                                                           community.upper())
        if not_enrolled_plot.count() > 0:
            print ".....Starting the correction for plots, setting bhs=True"
        else:
            print ".....Nothing to correct for Plots, moving on."
        count = 0
        settings.VERIFY_GPS = False
        for pt in not_enrolled_plot:
            pt.bhs = True
            pt.save()
            count += 1
            print "{}/{} {}".format(count, len(not_enrolled_plot), pt)
        settings.VERIFY_GPS = True
        print ".....Finished applying corrections. The END."