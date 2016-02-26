from optparse import make_option

from django.conf import settings
from django.db.models import get_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """ Corrects all bhs related enrollment flags in household, household_structure and plot
    """
    args = ('--site_code')

    help = 'Corrects all bhs related enrollment flags in household, household_structure and plot for site_code x.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--community',
            dest='community',
            action='store_true',
            default=False,
            help=('Enter community')),
    )

    def handle(self, *args, **options):
        if len(args) == 1:
            pass
        else:
            raise CommandError('Command expecting One arguments, being --community <community>')
        print options
        if options['community']:
            self.correct_enrollment_flags(args[0])
        else:
            raise CommandError('Command expecting One arguments, being --site_code <site_code>')

    def correct_enrollment_flags(self, community):
        SubjectConsent = get_model('bcpp_subject', 'SubjectConsent')
        HouseholdStructure = get_model('bcpp_household', 'HouseholdStructure')
        Household = get_model('bcpp_household', 'Household')
        Plot = get_model('bcpp_household', 'Plot')
        household_structure = []
        households = []
        plots = []
        consents = SubjectConsent.objects.filter(community=community)
        print ".....Found {} consents for community {}".format(consents.count(), community.upper())
        for consent in consents:
            if consent.household_member.household_structure.id not in household_structure:
                household_structure.append(consent.household_member.household_structure.id)
            if consent.household_member.household_structure.household.id not in households:
                households.append(consent.household_member.household_structure.household.id)
            if consent.household_member.household_structure.household.plot.id not in plots:
                plots.append(consent.household_member.household_structure.household.plot.id)
        not_enrolled_plot = Plot.objects.filter(id__in=plots, replaced_by__isnull=True).exclude(bhs=True)
        print "..... {}/{} plots for community {} are not enrolled".format(not_enrolled_plot.count(),
                                                                           len(plots),
                                                                           community.upper())
        not_enrolled_household = Household.objects.filter(
            id__in=households, replaced_by__isnull=True).exclude(enrolled=True)
        not_enrolled_structures = HouseholdStructure.objects.filter(
            id__in=household_structure,
            household__replaced_by__isnull=True).exclude(enrolled=True)
        print "..... {}/{} household structures for community {} are not enrolled".format(
            not_enrolled_structures.count(),
            len(household_structure),
            community.upper())
        print "..... {}/{} households for community {} are not enrolled".format(not_enrolled_household.count(),
                                                                                len(households),
                                                                                community.upper())
        count = 0
        for st in not_enrolled_structures:
            st.enrolled = True
            st.save()
            count += 1
            print "{}/{} {}".format(count, len(not_enrolled_structures), st)
        count = 0
        for hd in not_enrolled_household:
            hd.enrolled = True
            hd.save()
            count += 1
            print "{}/{} {}".format(count, len(not_enrolled_household), hd)
        count = 0
        settings.VERIFY_GPS = False
        for pt in not_enrolled_plot:
            pt.bhs = True
            pt.save()
            count += 1
            print "{}/{} {}".format(count, len(not_enrolled_plot), pt)
        settings.VERIFY_GPS = True
        print ".....Finished applying corrections. The END."
